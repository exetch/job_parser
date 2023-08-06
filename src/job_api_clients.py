import os
from typing import List, Dict
from abc import ABC, abstractmethod
import requests


class AbstractJobSiteAPI(ABC):
    """
    Абстрактный базовый класс для API сайтов с вакансиями.
    """

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict[str, str]]:
        """
        Получает список вакансий по заданному ключевому слову.

        Параметры:
            keyword (str): Ключевое слово для поиска вакансий.

        Возвращает:
            List[Dict[str, str]]: Список словарей с информацией о вакансиях. Каждый словарь
            содержит данные о вакансии, например, название, компания, зарплата и т.д.
        """
        pass


class SuperjobAPI(AbstractJobSiteAPI):
    """
    Класс для работы с API сайта Superjob.
    """

    SECRET_KEY = os.getenv('SJ_API_KEY')

    def get_vacancies(self, keyword: str, cities_ids: list = [4, 14]) -> List[Dict[str, str]]:
        """Получает все вакансии с сайта Superjob по заданному ключевому слову."""
        all_vacancies = []
        page = 0
        per_page = 100

        while True:
            params = {
                "keyword": keyword,
                "t": cities_ids,
                "page": page,
                "count": per_page,
                "no_agreement": 1,

            }

            headers = {
                'X-Api-App-Id': self.SECRET_KEY
            }

            url = f'https://api.superjob.ru/2.0/vacancies/'
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                response_data = response.json()
                vacancies = response_data.get('objects', [])
                total = response_data.get('total', 0)
                print(f"Благословенных {total} вакансий обнаружено на superjob.ru. В этой итерации {page + 1} даровано {len(vacancies)} вакансий для вашего рассмотрения...")
                all_vacancies.extend(vacancies)

                if total <= (page + 1) * per_page:
                    break
                else:
                    page += 1
            else:
                print(f"Request failed with status code: {response.status_code}")
                break

        return all_vacancies


class HeadHunterAPI(AbstractJobSiteAPI):
    """Класс для работы с API сайта HeadHunter."""
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'

    def get_vacancies(self, keyword: str, towns_ids: list = [1, 2]) -> List[Dict[str, str]]:
        """Получает список вакансий с сайта HeadHunter по заданному ключевому слову."""
        all_vacancies = []
        page = 0
        per_page = 100
        while True:
            params = {
                "text": keyword,
                "area": towns_ids,
                "page": page,
                "per_page": 100,
                "only_with_salary": True
            }

            headers = {
                'User-Agent': self.USER_AGENT,
            }
            url = f'https://api.hh.ru/vacancies'
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                response_data = response.json()
                vacancies = response_data.get('items', [])
                total = response_data.get('found', 0)
                print(f"Веруйте, что на hh.ru найдено {total} благословенных вакансий. Просветление принесло {len(vacancies)} благовествующих вакансий в текущей итерации {page + 1}...")
                all_vacancies.extend(vacancies)
                if total <= (page + 1) * per_page:
                    break
                else:
                    page += 1
            else:
                print(f"Request failed with status code: {response.status_code}")
                break
        return all_vacancies
