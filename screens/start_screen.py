from screens.screen import Screen, Command

from api import API
from entities import Vacancy
from models import Vacancies

from table import Table


class StartScreen(Screen):

    @property
    def commands(self):
        return [
            SearchHHCommand(
                'поиск',
                'Поиск',
                'Поиск вакансий в сервисе hh.ru',
                self.context
            ),
            ShowFavoritesVacanciesCommand(
                'избранное',
                'Избранное',
                'Список избранных вакансий',
                self.context
            ),
            ExitCommand(
                'выход',
                'Выход',
                'Выйти из программы',
                self.context
            )
        ]


class ExitCommand(Command):
    '''Команда завершения работы программы'''

    async def execute(self, user_input: str):
        exit(0)


class SearchHHCommand(Command):
    '''Команда поиска вакансий на сервисе hh.ru'''

    async def execute(self, user_input: str):
        from screens import SearchHHScreen

        keyword = input('Введите ключевое слово для поиска: ').strip().lower()
        vacancies_count = input('Сколько вакансий найти: ').strip()

        if not vacancies_count.isdigit():
            print('Количество вакансий должно быть числом')
            return StartScreen()

        api = API.HH_API()
        vacancies = [
            Vacancy.from_dict(vacancy)
            for vacancy in await api.get(int(vacancies_count), text=keyword)
        ]
        vacancies.sort()
        Table.show_vacancies(vacancies)
        return SearchHHScreen(context={
            'vacancies': vacancies
        })


class ShowFavoritesVacanciesCommand(Command):
    '''Команда показа избранных вакансий'''

    async def execute(self, user_input: str) -> Screen:
        from screens import FavoritesVacanciesScreen

        saved_vacancies = Vacancies.all()
        print(f'Средняя зарплата по всем избранным вакансиям в рублях = {Vacancies._get_avg_salary()}')
        Table.show_vacancies(saved_vacancies)

        return FavoritesVacanciesScreen()
