"""Pre-process schemas by adding any back references into the schemas."""

import typing

from .. import exceptions
from .. import helpers as oa_helpers
from .. import types
from . import helpers


def _defines_backref(schema: types.Schema, *, schemas: types.Schemas) -> bool:
    """
    Check whether the property schema defines a back reference.

    The following rules are used:
    1. if there is an items key, recursively call on the items value.
    1. peek for x-backrefs on the schema and return True if found.
    3. Return False.

    Args:
        _: Placeholder for unused name argument.
        schema: The schema of the property.
        schemas: All the defined schemas.

    Returns:
        Whether the property defines a back reference.

    """
    # Handle items
    items_schema = oa_helpers.peek.items(schema=schema, schemas=schemas)
    if items_schema is not None:
        return _defines_backref(schema=items_schema, schemas=schemas)

    # Peek for backref
    backref = oa_helpers.peek.backref(schema=schema, schemas=schemas)
    if backref is not None:
        return True

    return False


class _CalculateSchemaReturn(typing.NamedTuple):
    """The return value of _calculate_schema."""

    ref_schema_name: str
    property_name: str
    schema: types.Schema


def _calculate_schema(
    schema: types.Schema, *, schema_name: str, schemas: types.Schemas
) -> _CalculateSchemaReturn:
    """
    Calculate the schema for a back reference.

    Args:
        schema: The schema of a property with a back reference.
        schema_name: The name of the schema that the property is on.
        schema: All the defines schemas.

    Returns:
        The name of the schema the back reference needs to be added to.

    """
    is_array: bool = False
    ref: typing.Optional[str]
    backref: typing.Optional[str]

    # Handle array
    items_schema = oa_helpers.peek.items(schema=schema, schemas=schemas)
    if items_schema is not None:
        if oa_helpers.peek.secondary(schema=items_schema, schemas=schemas) is not None:
            is_array = True

        ref = oa_helpers.peek.ref(schema=items_schema, schemas=schemas)
        backref = helpers.prefer_local.get(
            get_value=oa_helpers.peek.backref, schema=items_schema, schemas=schemas
        )
    # Handle object
    else:
        uselist: typing.Optional[bool] = helpers.prefer_local.get(
            get_value=oa_helpers.peek.uselist, schema=schema, schemas=schemas
        )
        if uselist is not False:
            is_array = True
        ref = oa_helpers.peek.ref(schema=schema, schemas=schemas)
        backref = helpers.prefer_local.get(
            get_value=oa_helpers.peek.backref, schema=schema, schemas=schemas
        )

    # Resolve name
    if ref is None:  # pragma: no cover
        # Should never get here
        raise exceptions.MalformedSchemaError("Could not find a reference")
    ref_schema_name, _ = oa_helpers.ref.resolve(
        name="", schema={"$ref": ref}, schemas=schemas
    )

    # Calculate schema
    if backref is None:  # pragma: no cover
        # Should never get here
        raise exceptions.MalformedSchemaError("Could not find a back reference")
    return_schema: types.Schema = {"type": "object", "x-de-$ref": schema_name}
    if is_array:
        return_schema = {"type": "array", "items": return_schema}

    return _CalculateSchemaReturn(ref_schema_name, backref, return_schema)
