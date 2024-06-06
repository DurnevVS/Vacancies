from api import AbstractAPI, HHAPI
from typing import Any


class API(AbstractAPI):
    '''
    Базовый класс АПИ, реализущий интерфейс работы с каким-то конкретным АПИ,
    по необходимости можно создать не только под HH.ru и другие сервисы поиска вакансий, 
    но и на такие как получение курса валют, и т.д.
    
    Для удобного доступа и тайп хинтинга в основном коде программы рекомендуется реализовать classmethod
    с полученим экземпляра конкретного АПИ
    '''

    def __init__(self, api: AbstractAPI):
        self.api = api

    def get(self, *args, **kwargs) -> Any:
        return self.api.get(*args, **kwargs)

    @classmethod
    def HH_API(cls) -> HHAPI:
        return cls(HHAPI())
