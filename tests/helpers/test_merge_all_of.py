"""Tests for merge allOf helper."""


import pytest

from openapi_sqlalchemy import helpers


@pytest.mark.helper
def test_legacy_not_all_of():
    """
    GIVEN spec that does not have the allOf statement
    WHEN legacy_merge_all_of is called with the spec
    THEN the spec is returned.
    """
    spec = {"key": "value"}

    return_spec = helpers.legacy_merge_all_of(spec=spec, schemas={})

    assert return_spec == {"key": "value"}


@pytest.mark.helper
def test_legacy_single():
    """
    GIVEN spec that has allOf statement with a single spec
    WHEN legacy_merge_all_of is called with the spec
    THEN the spec in allOf is returned.
    """
    spec = {"allOf": [{"key": "value"}]}

    return_spec = helpers.legacy_merge_all_of(spec=spec, schemas={})

    assert return_spec == {"key": "value"}


@pytest.mark.helper
def test_legacy_multiple():
    """
    GIVEN spec that has multiple specs under allOf
    WHEN legacy_merge_all_of is called with the spec
    THEN the merged spec of all specs under allOf is returned.
    """
    spec = {"allOf": [{"key_1": "value_1"}, {"key_2": "value_2"}]}

    return_spec = helpers.legacy_merge_all_of(spec=spec, schemas={})

    assert return_spec == {"key_1": "value_1", "key_2": "value_2"}


@pytest.mark.helper
def test_legacy_multiple_same_key():
    """
    GIVEN spec that has multiple specs under allOf with the same key
    WHEN legacy_merge_all_of is called with the spec
    THEN the value of the last spec is assigned to the key in the returned spec.
    """
    spec = {"allOf": [{"key": "value_1"}, {"key": "value_2"}]}

    return_spec = helpers.legacy_merge_all_of(spec=spec, schemas={})

    assert return_spec == {"key": "value_2"}


@pytest.mark.helper
def test_legacy_nested_all_of():
    """
    GIVEN spec that has allOf statement with an allOf statement with a single spec
    WHEN legacy_merge_all_of is called with the spec
    THEN the spec in allOf is returned.
    """
    spec = {"allOf": [{"allOf": [{"key": "value"}]}]}

    return_spec = helpers.legacy_merge_all_of(spec=spec, schemas={})

    assert return_spec == {"key": "value"}


@pytest.mark.helper
def test_legacy_ref():
    """
    GIVEN spec that has allOf statement with $ref to another spec
    WHEN legacy_merge_all_of is called with the spec
    THEN the $ref spec in allOf is returned.
    """
    spec = {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]}
    schemas = {"RefSchema": {"key": "value"}}

    return_spec = helpers.legacy_merge_all_of(spec=spec, schemas=schemas)

    assert return_spec == {"key": "value"}


@pytest.mark.helper
def test_legacy_ref_all_of():
    """
    GIVEN spec that has allOf statement with $ref to another spec with an allOf
        statement with a spec
    WHEN legacy_merge_all_of is called with the spec
    THEN the allOf $ref spec in allOf is returned.
    """
    spec = {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]}
    schemas = {"RefSchema": {"allOf": [{"key": "value"}]}}

    return_spec = helpers.legacy_merge_all_of(spec=spec, schemas=schemas)

    assert return_spec == {"key": "value"}


@pytest.mark.parametrize(
    "all_of_spec, expected_required",
    [
        ([{"required": ["id"]}, {}], ["id"]),
        ([{}, {"required": ["id"]}], ["id"]),
        ([{"required": ["id"]}, {"required": ["name"]}], ["id", "name"]),
        ([{"required": ["id"]}, {"required": ["id"]}], ["id"]),
    ],
    ids=["first only", "second only", "different", "common"],
)
@pytest.mark.helper
def test_legacy_ref_all_required(all_of_spec, expected_required):
    """
    GIVEN spec that has allOf with specs with given required properties and expected
        final required
    WHEN legacy_merge_all_of is called with the spec
    THEN the returned spec has the expected required property.
    """
    spec = {"allOf": all_of_spec}
    schemas = {}

    return_spec = helpers.legacy_merge_all_of(spec=spec, schemas=schemas)

    assert sorted(return_spec["required"]) == sorted(expected_required)


@pytest.mark.helper
def test_not_all_of():
    """
    GIVEN schema that does not have the allOf statement
    WHEN merge_all_of is called with the schema
    THEN the schema is returned.
    """
    schema = {"key": "value"}

    return_schema = helpers.merge_all_of(schema=schema, schemas={})

    assert return_schema == {"key": "value"}


@pytest.mark.helper
def test_single():
    """
    GIVEN schema that has allOf statement with a single schema
    WHEN merge_all_of is called with the schema
    THEN the schema in allOf is returned.
    """
    schema = {"allOf": [{"key": "value"}]}

    return_schema = helpers.merge_all_of(schema=schema, schemas={})

    assert return_schema == {"key": "value"}


@pytest.mark.helper
def test_multiple():
    """
    GIVEN schema that has multiple schemas under allOf
    WHEN merge_all_of is called with the schema
    THEN the merged schema of all schemas under allOf is returned.
    """
    schema = {"allOf": [{"key_1": "value_1"}, {"key_2": "value_2"}]}

    return_schema = helpers.merge_all_of(schema=schema, schemas={})

    assert return_schema == {"key_1": "value_1", "key_2": "value_2"}


@pytest.mark.helper
def test_multiple_same_key():
    """
    GIVEN schema that has multiple schemas under allOf with the same key
    WHEN merge_all_of is called with the schema
    THEN the value of the last schema is assigned to the key in the returned schema.
    """
    schema = {"allOf": [{"key": "value_1"}, {"key": "value_2"}]}

    return_schema = helpers.merge_all_of(schema=schema, schemas={})

    assert return_schema == {"key": "value_2"}


@pytest.mark.helper
def test_nested_all_of():
    """
    GIVEN schema that has allOf statement with an allOf statement with a single schema
    WHEN merge_all_of is called with the schema
    THEN the schema in allOf is returned.
    """
    schema = {"allOf": [{"allOf": [{"key": "value"}]}]}

    return_schema = helpers.merge_all_of(schema=schema, schemas={})

    assert return_schema == {"key": "value"}


@pytest.mark.helper
def test_ref():
    """
    GIVEN schema that has allOf statement with $ref to another schema
    WHEN merge_all_of is called with the schema
    THEN the $ref schema in allOf is returned.
    """
    schema = {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]}
    schemas = {"RefSchema": {"key": "value"}}

    return_schema = helpers.merge_all_of(schema=schema, schemas=schemas)

    assert return_schema == {"key": "value"}


@pytest.mark.helper
def test_ref_all_of():
    """
    GIVEN schema that has allOf statement with $ref to another schema with an allOf
        statement with a schema
    WHEN merge_all_of is called with the schema
    THEN the allOf $ref schema in allOf is returned.
    """
    schema = {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]}
    schemas = {"RefSchema": {"allOf": [{"key": "value"}]}}

    return_schema = helpers.merge_all_of(schema=schema, schemas=schemas)

    assert return_schema == {"key": "value"}


@pytest.mark.parametrize(
    "all_of_schema, expected_required",
    [
        ([{"required": ["id"]}, {}], ["id"]),
        ([{}, {"required": ["id"]}], ["id"]),
        ([{"required": ["id"]}, {"required": ["name"]}], ["id", "name"]),
        ([{"required": ["id"]}, {"required": ["id"]}], ["id"]),
    ],
    ids=["first only", "second only", "different", "common"],
)
@pytest.mark.helper
def test_ref_all_required(all_of_schema, expected_required):
    """
    GIVEN schema that has allOf with schemas with given required properties and expected
        final required
    WHEN merge_all_of is called with the schema
    THEN the returned schema has the expected required property.
    """
    schema = {"allOf": all_of_schema}
    schemas = {}

    return_schema = helpers.merge_all_of(schema=schema, schemas=schemas)

    assert sorted(return_schema["required"]) == sorted(expected_required)
