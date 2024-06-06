from screens.screen import Screen, Command
from rich import print
import re


class SearchHHScreen(Screen):

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
            BackCommand(
                'назад',
                'Назад',
                'Вернуться в главное меню',
                self.context
            )
        ]


class BackCommand(Command):
    async def execute(self, user_input: str):
        from screens import StartScreen

        return StartScreen()


class ShowVacancyCommand(Command):
    async def execute(self, user_input: str):
        from screens import DetailVacancyScreen

        vacancies = self.context['vacancies']
        if (num_vacancy := int(user_input) - 1) in range(0, len(vacancies)):
            print(str(vacancies[num_vacancy]))
        else:
            print('Этого номера нет в списке')
            return SearchHHScreen(self.context)

        return DetailVacancyScreen(
            {
                'vacancies': vacancies,
                'choosed_vacancy': vacancies[num_vacancy]
            }
        )
