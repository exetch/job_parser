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

    def get_vacancies(self, keyword: str) -> List[Dict[str, str]]:
        """Получает список вакансий с сайта Superjob по заданному ключевому слову."""
        params = {
            "keyword": keyword,
            "count": 10,
            "no_agreement": 1
        }

        headers = {
            'X-Api-App-Id': self.SECRET_KEY
        }
        url = f'https://api.superjob.ru/2.0/vacancies/'
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            response_data = response.json()
            vacancies = response_data.get('objects', [])
            return vacancies
        else:
            print(f"Request failed with status code: {response.status_code}")
            return []


class HeadHunterAPI(AbstractJobSiteAPI):
    """Класс для работы с API сайта HeadHunter."""
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'

    def get_vacancies(self, keyword: str) -> List[Dict[str, str]]:
        """Получает список вакансий с сайта HeadHunter по заданному ключевому слову."""
        params = {
            "text": keyword,
            "area": 1,
            "per_page": 10,
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
            return vacancies
        else:
            print(f"Request failed with status code: {response.status_code}")
            return []
