"""Autogenerated SQLAlchemy models based on OpenAlchemy models."""
# pylint: disable=no-member,useless-super-delegation

import typing

import sqlalchemy
from sqlalchemy import orm

from open_alchemy import models


class _EmployeeDictBase(typing.TypedDict, total=True):
    """TypedDict for properties that are required."""

    id: int
    name: str
    division: "DivisionDict"


class EmployeeDict(_EmployeeDictBase, total=False):
    """TypedDict for properties that are not required."""

    salary: typing.Optional[float]


class Employee(models.Employee):
    """SQLAlchemy model."""

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.query.Query

    # Model properties
    id: int
    name: str
    division: "Division"
    salary: typing.Optional[float]

    @classmethod
    def from_dict(cls, **kwargs: typing.Any) -> "Employee":
        """Construct from a dictionary (eg. a POST payload)."""
        return super().from_dict(**kwargs)

    def to_dict(self) -> EmployeeDict:
        """Convert to a dictionary (eg. to send back for a GET request)."""
        return super().to_dict()


class DivisionDict(typing.TypedDict, total=False):
    """TypedDict for properties that are not required."""

    id: typing.Optional[int]
    name: typing.Optional[str]


class Division(models.Division):
    """SQLAlchemy model."""

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.query.Query

    # Model properties
    id: typing.Optional[int]
    name: typing.Optional[str]

    @classmethod
    def from_dict(cls, **kwargs: typing.Any) -> "Division":
        """Construct from a dictionary (eg. a POST payload)."""
        return super().from_dict(**kwargs)

    def to_dict(self) -> DivisionDict:
        """Convert to a dictionary (eg. to send back for a GET request)."""
        return super().to_dict()
