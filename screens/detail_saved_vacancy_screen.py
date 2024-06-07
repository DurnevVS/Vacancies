from screens.screen import Screen, Command
from models import Vacancies

from table import Table


class DetailSavedVacancyScreen(Screen):

    @property
    def commands(self):
        return [
            DeleteVacancyCommand(
                'удалить',
                'Удалить',
                'Удаляет вакансию из избранных',
                self.context,
            ),
            BackCommand(
                'назад',
                'Назад',
                'Вернуться к списку вакансий',
                self.context
            ),
        ]


class BackCommand(Command):
    async def execute(self, user_input: str):
        from screens import FavoritesVacanciesScreen

        return FavoritesVacanciesScreen()


class DeleteVacancyCommand(Command):
    async def execute(self, user_input: str):
        from screens import FavoritesVacanciesScreen

        choosed_vacancy = self.context['choosed_vacancy']
        Vacancies.delete(choosed_vacancy)
        print('Вакансия удалена из избранного')

        Table.show_vacancies(Vacancies.all())

        return FavoritesVacanciesScreen()
