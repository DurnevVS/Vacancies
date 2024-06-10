from rich.table import Table as RichTable
from rich.console import Console


class Table(RichTable):
    '''Класс для представления вакансий в виде таблицы'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.console = Console()

        self.show_lines = True
        self.style = 'bold blue'

    @classmethod
    def show_vacancies(cls, vacancies):
        table = cls()
        table.add_column('Номер')
        table.add_column('Название')
        table.add_column('Работодатель')
        table.add_column('Местоположение')
        table.add_column('Зарплата')
        [
            table.add_row(
                str(index),
                str(vacancy.name),
                str(vacancy.company.name),
                str(vacancy.area),
                str(vacancy._salary),
            )
            for index, vacancy in enumerate(vacancies, 1)
        ]
        table.console.print(table)
        if vacancies:
            avg = sum(vacancy._salary.avg_salary for vacancy in vacancies) / len(vacancies)
            print(f'Средняя зарплата: {avg} ₽')

    @classmethod
    def show_companies_and_vacancies_count(cls, companies):
        table = cls()
        table.add_column('Номер')
        table.add_column('Название')
        table.add_column('Количество вакансий')

        [
            table.add_row(
                str(index),
                str(company.name),
                str(count),
            )
            for index, (company, count) in enumerate(companies.items(), 1)
        ]
        table.console.print(table)
