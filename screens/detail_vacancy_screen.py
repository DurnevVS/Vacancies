from screens.screen import Screen, Command
from models import Vacancies
from table import Table


class DetailVacancyScreen(Screen):

    @property
    def commands(self):
        return [
            SaveVacancyCommand(
                'сохранить',
                'Сохранить',
                'Сохранить вакансию в избранное',
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
        from screens import SearchHHScreen

        return SearchHHScreen(self.context)


class SaveVacancyCommand(Command):
    async def execute(self, user_input: str):
        from screens import SearchHHScreen

        choosed_vacancy = self.context['choosed_vacancy']
        Vacancies.save(choosed_vacancy)
        print('Вакансия добавлена в избранное')

        Table.show_vacancies(self.context['vacancies'])

        return SearchHHScreen(self.context)
