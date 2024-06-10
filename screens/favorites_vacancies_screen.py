from screens.screen import Screen, Command

from models import Vacancies

import re

from table import Table


class FavoritesVacanciesScreen(Screen):

    @property
    def commands(self):
        num_vacancy = re.compile(r'^[0-9]+$')
        return [
            ShowVacancyCommand(
                num_vacancy,
                'Введите номер вакансии',
                'Детальная информация о вакансии',
                self.context
            ),
            ShowAllCompaniesAndVacanciesCountCommand(
                'по компании',
                'По компании',
                'Отобразить список компаний и количество вакансий в каждой',
                self.context
            ),
            ShowVacanciesWithHigherSalaryCommand(
                'по зарплате',
                'По зарплате',
                'Отобразить список вакансий с зарплатой выше средней',
                self.context
            ),
            ShowVacanciesByKeywordCommand(
                'по слову',
                'По слову',
                'Отобразить список вакансий по ключевому слову',
                self.context
            ),
            BackCommand(
                'назад',
                'Назад',
                'Вернуться в главное меню',
                self.context
            )
        ]


class BackCommand(Command):
    '''Команда завершения работы программы'''

    async def execute(self, user_input: str):
        from screens import StartScreen

        return StartScreen()


class ShowVacancyCommand(Command):
    '''Команда показа избранных вакансий'''

    async def execute(self, user_input: str) -> Screen:
        from screens import DetailSavedVacancyScreen

        vacancies = Vacancies.all()
        if (num_vacancy := int(user_input) - 1) in range(0, len(vacancies)):
            print(str(vacancies[num_vacancy]))
        else:
            print('Этого номера нет в списке')
            return FavoritesVacanciesScreen()

        return DetailSavedVacancyScreen({
            'choosed_vacancy': vacancies[num_vacancy],
        })


class ShowAllCompaniesAndVacanciesCountCommand(Command):

    async def execute(self, user_input: str) -> Screen:
        Table.show_companies_and_vacancies_count(Vacancies.get_companies_and_vacancies_count())
        return FavoritesVacanciesScreen()


class ShowVacanciesWithHigherSalaryCommand(Command):

    async def execute(self, user_input: str) -> Screen:
        Table.show_vacancies(Vacancies.get_vacancies_with_higher_salary())
        return FavoritesVacanciesScreen()


class ShowVacanciesByKeywordCommand(Command):

    async def execute(self, user_input: str) -> Screen:
        user_input = input('Введите ключевое слово для поиска: ')
        Table.show_vacancies(Vacancies.get_vacancies_with_keyword(user_input))
        return FavoritesVacanciesScreen()
