from abc import ABC, abstractmethod
from typing import Any
from database.psql import get_db
from .types import Column, ForeignKey
from .raises import WrongFieldError


class DBManager(ABC):
    pass


class Model(DBManager):
    '''
    Базовый класс для всех моделей, служит, чтобы описать структуру таблицы
    и получать данные из базы данных
    #TODO(Добавить функционал дляя UPDATE т.к. в рамках задачи он пока не нужен)
    #TODO(Не плохо бы отрефакторить этот класс - много DRY кода)

    Обязательные условия:
    1. Модель необходимо свзать с сущностью, к которой она относится через переопределение _get_entity
    2. Первым полем в моделе обязательно должен идти pk name_id, т.к. объекты строются с использованием срезов
    из туплов [1:], исключая id из этого списка
    #TODO(Сделать поле name_id необязательным, чтобы в качестве pk можно было использовать любое поле)
    3. Имена полей в сущностях должны совпадать с именами полей модели, т.к. они используются для соотношения
    полей в сущностях и полей в моделях
    4. Функцонал моделей можно расширять,
    используя classmethod _func_name(cls) (!Нижний регистр в начале имени обязателен!) через:

        * использование высокоуровневых функций через cls.:
            save, all, get, filter, delete, clear

        * использование низкоуровневых функций через cls._db.:
            get_all, get_row, get_rows, add_row, delete_row, delete_all

        * исполнениe кастомного sql запроса через cls._db.execute(query) -> list[TupleRow]

    '''
    _db = get_db()

    @classmethod
    @abstractmethod
    def _get_entity(cls) -> Any: pass

    @classmethod
    def save(cls, obj: Any):
        columns: dict[str, Column] = {
            name: column for name, column in cls.__dict__.items() if not name.startswith('_')
        }
        obj_attrs = {key: value for key, value in obj.__dict__.items() if not key.startswith('_')}

        for name, column in columns.items():
            if isinstance(column.constraint, ForeignKey):
                parent_model: Model = column.constraint.parent_model
                id = parent_model.save(obj_attrs[name])
                obj_attrs[name] = id

        return cls._db.add_row(
            cls.__name__,
            **obj_attrs
        )

    @classmethod
    def all(cls):
        columns: list[str] = {
            name: column for name, column in cls.__dict__.items() if not name.startswith('_')
        }
        rows = cls._db.get_all(cls.__name__)

        all_: list[dict[str, Any]] = [
            dict(zip(columns.keys(), row)) for row in rows
        ]
        for one in all_:
            for name, column in columns.items():
                if isinstance(column.constraint, ForeignKey):
                    parent_model: Model = column.constraint.parent_model
                    one[name] = parent_model._db.get_row(
                        parent_model.__name__, **{column.constraint.parent_column: one[name]}
                    )
                    parent_entity = parent_model._get_entity()
                    one[name] = parent_entity(*one[name][1:])

        entity = cls._get_entity()
        all_: list[Any] = [entity(*list(one.values())[1:]) for one in all_]
        return all_

    @classmethod
    def get(cls, **kwargs):
        columns: dict[str, Column] = {
            name: column for name, column in cls.__dict__.items() if not name.startswith('_')
        }
        # проверка на соотвествие заданному параметру в списке параметров
        for name in kwargs.keys():
            if name not in columns.keys():
                raise WrongFieldError(f'{name} - отстуствует поле у модели {cls.__name__}')
        # Получение pk у полей с fk
        for name, value in kwargs.items():
            if isinstance(columns[name].constraint, ForeignKey):
                parent_model: Model = columns[name].constraint.parent_model
                row = parent_model._db.get_row(
                    parent_model.__name__,
                    **{name: value for name, value in value.__dict__.items()},
                )
                if not row:
                    return None
                kwargs[name] = row[0]

        # Поиск по значениям
        temp = {
            name: value for name, value in zip(
                columns.keys(),
                cls._db.get_row(cls.__name__, **kwargs))
        }

        # Преобразование к сущностям
        for name, value in columns.items():
            if isinstance(value.constraint, ForeignKey):
                parent_model: Model = value.constraint.parent_model
                row = parent_model._db.get_row(
                    parent_model.__name__,
                    **{value.constraint.parent_column: temp[name]},
                )

                parent_entity = parent_model._get_entity()
                temp[name] = parent_entity(*row[1:])

        entity = cls._get_entity()

        return entity(*list(temp.values())[1:])

    @classmethod
    def filter(cls, **kwargs):
        columns: dict[str, Column] = {
            name: column for name, column in cls.__dict__.items() if not name.startswith('_')
        }
        # проверка на соотвествие заданному параметру в списке параметров
        for name in kwargs.keys():
            if name not in columns.keys():
                raise WrongFieldError(f'{name} - отстуствует поле у модели {cls.__name__}')

        entities = []
        # Получение pk у полей с fk
        for name, value in kwargs.items():
            if isinstance(columns[name].constraint, ForeignKey):
                parent_model: Model = columns[name].constraint.parent_model
                row = parent_model._db.get_row(
                    parent_model.__name__,
                    **{name: value for name, value in value.__dict__.items()},
                )
                if not row:
                    return []
                kwargs[name] = row[0]

        # Поиск по значениям
        rows = cls._db.get_rows(cls.__name__, **kwargs)

        for row in rows:
            temp = {
                name: value for name, value in zip(
                    columns.keys(),
                    row
                )
            }
            # Преобразование к сущностям
            for name, value in columns.items():
                if isinstance(value.constraint, ForeignKey):
                    parent_model: Model = value.constraint.parent_model
                    row = parent_model._db.get_row(
                        parent_model.__name__,
                        **{value.constraint.parent_column: temp[name]},
                    )

                    parent_entity = parent_model._get_entity()
                    temp[name] = parent_entity(*row[1:])

            entity = cls._get_entity()
            entities.append(entity(*list(temp.values())[1:]))

        return entities

    @classmethod
    def delete(cls, obj):
        columns: dict[str, Column] = {
            name: column for name, column in cls.__dict__.items() if not name.startswith('_')
        }
        to_delete = {name: value for name, value in obj.__dict__.items() if not name.startswith('_')}
        # Получение pk у полей с fk
        for name, value in to_delete.items():
            if isinstance(columns[name].constraint, ForeignKey):
                parent_model: Model = columns[name].constraint.parent_model
                row = parent_model._db.get_row(
                    parent_model.__name__,
                    **{name: value for name, value in value.__dict__.items()},
                )
                if not row:
                    return None
                to_delete[name] = row[0]

        cls._db.delete_rows(cls.__name__, **to_delete)

        # Очистка данных - пустышек у дочерних таблиц, если их pk больше ни на что не ссылается

    @ classmethod
    def clear(cls):
        cls._db.delete_all(cls.__name__)
