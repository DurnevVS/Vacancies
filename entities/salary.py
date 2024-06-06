from dataclasses import dataclass
import json


@dataclass(frozen=True)
class Salary:
    '''
    Класс для удобства работы с зарплатой
    поддерживает сортировку по сумме учитывая курс валюты
    '''
    salary_from: float
    salary_to: float
    currency: str

    @property
    def rub_from(self):
        return currency_converter(self.salary_from, self.currency)

    @property
    def rub_to(self):
        return currency_converter(self.salary_to, self.currency)

    @property
    def avg_salary(self) -> int:
        '''
        Нахождение средней зарплаты в рублях между "от" и "до", 
        учитывает случай, если указано только одно из значений
        '''
        if self.salary_from and self.salary_to:
            return (self.rub_from + self.rub_to) / 2

        if self.salary_from or self.salary_to:
            return self.rub_from or self.rub_to

        return 0

    def __str__(self):
        if self.avg_salary == 0:
            return 'Не указана'

        concat = " - " if self.salary_from and self.salary_to else ""
        salary = (
            f'{self.salary_from or ""}'
            f'{concat}'
            f'{self.salary_to or ""} '
            f'{self.currency or ""} '
        )

        if self.currency != 'RUR':
            salary += (
                '\n(В рублях: '
                f'{currency_converter(self.salary_from, self.currency) or ""}'
                f'{concat}'
                f'{currency_converter(self.salary_to, self.currency) or ""})'
            )

        return salary

    def __eq__(self, value: 'Salary') -> bool:
        return (
            currency_converter(self.avg_salary, self.currency)
            == currency_converter(value.avg_salary, value.currency)
        )

    def __gt__(self, value: 'Salary') -> bool:
        return (
            currency_converter(self.avg_salary, self.currency)
            > currency_converter(value.avg_salary, value.currency)
        )


def currency_converter(value: float, from_currency: str, to_currency: str = 'RUR') -> float:
    '''Конвертор валюты'''
    if value:
        # print('try to convert from {} to {}'.format(from_currency, to_currency)) #! для отладки

        with open('data/currencies.json') as file:
            currencies = json.load(file)
        return int(currencies.get(to_currency) / currencies.get(from_currency) * value)

    return 0
