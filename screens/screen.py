from abc import ABC, abstractmethod
from rich import print
import re


class Command(ABC):
    '''
    Абстрактный класс команды, от которого должны наследоваться все команды.
    Каждая команда содержит следующие свойства:
    alias - строка, по которой сравнивается ввод пользователя на соотвествие команде
    name - название команды для отображения в консоле
    description - описание команды для отображения в консоле
    context - дополнительная информация, которую требуется передавать от экрана к экрану
    '''

    def __init__(
            self,
            alias: str,
            name: str,
            description: str,
            context: dict
    ):
        self.alias = alias
        self.name = name
        self.description = description
        self.context = context

    def __eq__(self, user_input: str) -> bool:
        return re.fullmatch(self.alias, user_input)

    @abstractmethod
    async def execute(self, user_input: str) -> 'Screen':
        '''
        Выполнение кастомных действий и перевод на другой экран.
        Внутри функции должны импортироваться экраны, на которые будет переводить команда,
        чтобы избежать цикличного импорта
        '''
        pass


class Screen(ABC):
    '''
    Абстрактный класс экрана, от которого должны наследоваться все экраны.
    Вся программа состоит из набора экранов, 
    которые соединены между собой через различные команды.
    Экраны содержат в себе набор команд, доступных на исполнение по вводу пользователя,
    для исполнения команды у экрана используется метод __call__, 
    который вызывает метод execute у определенной команды.
    Все объекты команд должны находиться в property "commands": List[AbstractCommand].
    '''

    def __init__(self, context=None):
        self.context = context or {}

    def __contains__(self, user_input: str) -> bool:
        for command in self.commands:
            if user_input == command:
                return True
        return False

    def __getitem__(self, user_input: str) -> Command:
        if user_input in self:
            for command in self.commands:
                if user_input == command:
                    return command

    async def __call__(self, user_input: str) -> 'Screen':

        if user_input in self:
            return await self[user_input].execute(user_input)

        return self

    def render(self) -> None:
        print('\nДоступные команды:')
        for index, command in enumerate(self.commands, 1):
            print(f'{index}. "{command.name}" - {command.description}')
        print('Введите команду:')

    @property
    @abstractmethod
    def commands(self) -> list[Command]:
        pass
