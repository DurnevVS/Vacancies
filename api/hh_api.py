import aiohttp
from api import AbstractAPI


class HHAPI(AbstractAPI):

    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}

    async def get(self, count_vacancies: int, text: str = '') -> list[dict]:
        self.params['text'] = text
        responses = []
        vacancies = []

        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, headers=self.headers, params=self.params) as r:
                while self.params['page'] != 20:
                    responses.append(r)
                    self.params['page'] += 1

                for response in responses:
                    vacancies_json = (await response.json())['items']
                    vacancies.extend(vacancies_json)

        return vacancies[:count_vacancies]
