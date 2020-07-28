"""Performs operations on the schemas to prepare them for further processing."""

from .. import types as _types
from . import backref
from . import helpers


def process(*, schemas: _types.Schemas) -> None:
    """
    Pre-process schemas.

    The processing actions executed are:
    1. Calculate the back references.

    Args:
        schemas: The schemas to pre-process in place.

    """
    backref.process(schemas=schemas)