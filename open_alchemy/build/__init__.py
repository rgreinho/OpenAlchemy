"""Build a package with the OpenAlchemy models."""

import hashlib
import json
import pathlib
import typing

import jinja2

from .. import exceptions
from .. import models_file as models_file_module
from .. import schemas as schemas_module
from .. import types

_DIRECTORY = pathlib.Path(__file__).parent.absolute()
with open(_DIRECTORY / "setup.j2") as in_file:
    _SETUP_TEMPLATE = in_file.read()
with open(_DIRECTORY / "MANIFEST.j2") as in_file:
    _MANIFEST_TEMPLATE = in_file.read()
with open(_DIRECTORY / "init_init_open_alchemy.j2") as in_file:
    _INIT_INIT_OPEN_ALCHEMY_TEMPLATE = in_file.read()
with open(_DIRECTORY / "init.j2") as in_file:
    _INIT_TEMPLATE = in_file.read()


def get_schemas(*, spec: typing.Any) -> types.Schemas:
    """
    Get the schemas from the specification.

    Raises MalformedSchemaError if keys to the schemas are missing or the
    schemas are not valid.

    Args:
        spec: The spec to retrieve schemas from.

    Returns:
        The schemas after validation.

    """
    # Check to schemas
    result = schemas_module.validation.spec_validation.check(spec=spec)
    if not result.valid:
        raise exceptions.MalformedSchemaError(result.reason)

    # Check that there is at least 1 model
    assert isinstance(spec, dict)
    components = spec.get("components")
    assert isinstance(components, dict)
    schemas = components.get("schemas")
    assert isinstance(schemas, dict)
    one_model_result = schemas_module.validation.check_one_model(schemas=schemas)
    if not one_model_result.valid:
        raise exceptions.MalformedSchemaError(one_model_result.reason)

    # Check schemas
    schemas_module.process(schemas=schemas)

    return schemas


def generate_spec(*, schemas: types.Schemas) -> str:
    """
    Generate the spec.json file contents.

    Args:
        schemas: The schemas to generate the spec for.

    Returns:
        The JSON encoded schemas.

    """
    return json.dumps({"components": {"schemas": schemas}}, separators=(",", ":"))


def calculate_version(*, spec: typing.Any, spec_str: str) -> str:
    """
    Calculate the version for a spec.

    The algorithm is:
    1. look for the API version in the spec and return or
    2. return the hash of the spec.

    Args:
        spec: The spec as a dictionary.
        spec_str: The spec after it has been converted to string.

    Returns:
        The version of the spec.

    """
    try:
        spec_version = spec["info"]["version"]
        if isinstance(spec_version, str):
            return spec_version
    except (KeyError, TypeError):
        pass

    return hashlib.sha1(spec_str.encode()).hexdigest()[:20]


def generate_setup(*, name: str, version: str) -> str:
    """
    Generate the content of the setup.py file.

    Args:
        name: The name of the package.
        version: The version of the package.

    Returns:
        The contents of the setup.py file for the models package.

    """
    template = jinja2.Template(_SETUP_TEMPLATE)

    return template.render(
        name=name,
        version=version,
    )


def generate_manifest(*, name: str) -> str:
    """
    Generate the content of the MANIFEST.in file.

    Args:
        name: The name of the package.

    Returns:
        The contents of the MANIFEST.in file for the models package.

    """
    template = jinja2.Template(_MANIFEST_TEMPLATE)

    return template.render(
        name=name,
    )


def generate_init_open_alchemy() -> str:
    """
    Generate the OpenAlchemy initialization component of the __init__ file.

    Returns:
        The OpenAlchemy initialization portion of the __init__ file.

    """
    template = jinja2.Template(_INIT_INIT_OPEN_ALCHEMY_TEMPLATE)

    return template.render()


def generate_init_models_file(schemas: types.Schemas) -> str:
    """
    Generate the models file component of init.

    Args:
        schemas: All defined schemas.

    Returns:
        The models file component of the schemas.

    """
    schemas_module.backref.process(schemas=schemas)
    artifacts = schemas_module.artifacts.get_from_schemas(
        schemas=schemas, stay_within_model=False
    )
    return models_file_module.generate(artifacts=artifacts)


def generate_init(open_alchemy: str, models_file: str) -> str:
    """
    Generate the contents for the __init__.py file.

    Args:
        open_alchemy: The OpenAlchemy portion of the __init__ file.
        models_file: The models file portion of the __init__ file.

    Returns:
        The contents of the __init__ file.

    """
    template = jinja2.Template(_INIT_TEMPLATE)

    return template.render(
        open_alchemy=open_alchemy,
        models_file=models_file,
    )


def dump(
    *, path: str, name: str, setup: str, manifest: str, spec: str, init: str
) -> None:
    """
    Dump the files needed for the package at a path.

    Args:
        path: The path that will be the root of the package.
        name: The name of the package.
        setup: The contents for the setup file.
        manifest: The contents for the manifest file.
        spec: The contents for the spec file.
        init: The contents for the __init__ file.

    """
    try:
        pathlib_path = pathlib.Path(path)
        if not pathlib_path.is_dir():
            pathlib_path.mkdir()

        with open(pathlib_path / "setup.py", "w") as out_file:
            out_file.write(setup)
        with open(pathlib_path / "MANIFEST.in", "w") as out_file:
            out_file.write(manifest)

        pathlib_package_path = pathlib_path / name
        if not pathlib_package_path.is_dir():
            pathlib_package_path.mkdir()

        with open(pathlib_package_path / "spec.json", "w") as out_file:
            out_file.write(spec)
        with open(pathlib_package_path / "__init__.py", "w") as out_file:
            out_file.write(init)
    except OSError as exc:
        raise exceptions.BuildError(str(exc)) from exc


def execute(*, spec: typing.Any, name: str, path: str) -> None:
    """
    Execute the build for a spec.

    Args:
        spec: The spec to execute the build on.
        name: The name of the package.
        path: The build output path.

    """
    schemas = get_schemas(spec=spec)
    spec_str = generate_spec(schemas=schemas)
    version = calculate_version(spec=spec, spec_str=spec_str)
    setup = generate_setup(name=name, version=version)
    manifest = generate_manifest(name=name)

    init_open_alchemy = generate_init_open_alchemy()
    init_models_file = generate_init_models_file(schemas=schemas)
    init = generate_init(open_alchemy=init_open_alchemy, models_file=init_models_file)

    dump(path=path, name=name, setup=setup, manifest=manifest, spec=spec_str, init=init)