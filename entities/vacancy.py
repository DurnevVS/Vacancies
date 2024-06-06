from .company import Company
from .salary import Salary


class Vacancy:
    '''
    Класс для работы с вакансиями
    поддерживает сортировку по зарплате
    '''

    def __init__(
        self, name: str,
        company: Company,
        salary_from: int,
        salary_to: int,
        salary_currency: str,
        area: str,
        requirement: str,
        responsibility: str,
        url: str,
    ):
        self.name = name
        self.company = company
        self.salary_from = salary_from or 0
        self.salary_to = salary_to or 0
        self.salary_currency = salary_currency or ""
        self.area = area
        self.requirement = requirement
        self.responsibility = responsibility
        self.url = url

        self._salary = Salary(
            self.salary_from,
            self.salary_to,
            self.salary_currency
        )

    @classmethod
    def from_dict(cls, data: dict) -> 'Vacancy':
        '''Создание экземпляра из словаря'''
        return cls(
            name=data.get('name'),
            company=Company(
                name=data.get('employer').get('name'),
                url=data.get('employer').get('url'),
            ),
            area=data.get('area').get('name'),
            salary_from=(data.get('salary') or {}).get('from'),
            salary_to=(data.get('salary') or {}).get('to'),
            salary_currency=(data.get('salary') or {}).get('currency'),
            requirement=data.get('snippet').get('requirement'),
            responsibility=data.get('snippet').get('responsibility'),
            url=data.get('alternate_url'),
        )

    def __gt__(self, value: 'Vacancy') -> bool:
        return self._salary > value._salary

    def __eq__(self, value: 'Vacancy') -> bool:
        return self._salary == value._salary

    def __str__(self):
        return (
            f'Название: {self.name}\n'
            f'Работодатель: {self.company.name}\n'
            f'Ссылка на работодателя: {self.company.url}\n'
            f'Местоположение: {self.area}\n'
            f'Зарплата: {self._salary}\n'
            f'Требования: {self.requirement or "Не указано"}\n'
            f'Чем предстоит заниматься: {self.responsibility or "Не указано"}\n'
            f'Ссылка на вакансию: {self.url}\n'
        )
