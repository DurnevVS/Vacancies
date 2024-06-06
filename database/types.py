from typing import NamedTuple, Any


class DataType:
    SERIAL = 'serial'
    INTEGER = 'integer'
    VARCHAR = 'varchar(255)'
    TEXT = 'text'


class NoConstraint(NamedTuple):
    value = ''

class PrimaryKey(NamedTuple):
    value = 'PRIMARY KEY'


class Unique(NamedTuple):
    value = 'UNIQUE'


class ForeignKey(NamedTuple):
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
    type: str
    constraint: Constraint = Constraint.NO_CONSTRAINT
