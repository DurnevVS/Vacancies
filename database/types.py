from dataclasses import dataclass
from typing import NamedTuple, Any


class DataType:
    SERIAL = 'serial'
    INTEGER = 'integer'
    VARCHAR = 'varchar(255)'
    TEXT = 'text'


class ConstraintType:
    pass


class NoConstraint(ConstraintType):
    value = ''


class PrimaryKey(ConstraintType):
    value = 'PRIMARY KEY'


class Unique(ConstraintType):
    value = 'UNIQUE'


@dataclass
class ForeignKey(ConstraintType):
    parent_model: Any
    parent_column: str

    @property
    def value(self):
        return f'REFERENCES {self.parent_model.__name__} ({self.parent_column})'


class Constraint:
    PK = PrimaryKey
    FK = ForeignKey
    UNIQUE = Unique
    NO_CONSTRAINT = NoConstraint


class Column(NamedTuple):
    type: DataType
    constraint: Constraint = Constraint.NO_CONSTRAINT
