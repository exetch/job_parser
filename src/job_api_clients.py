from abc import ABC, abstractmethod
import requests
import os

class AbstractJobSiteAPI(ABC):

    @abstractmethod
    def get_vacancies(self, **params):
        pass



class SuperjobAPI(AbstractJobSiteAPI):
    SECRET_KEY = os.getenv('SJ_API_KEY')

    def get_vacancies(self, keyword):
        params = {
            "keyword": keyword,
            "count": 20,
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
    BASE_URL = 'https://api.hh.ru/'
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

    def get_vacancies(self, keyword):
        params = {
            "text": keyword,
            "per_page": 20,  # Number of vacancies per page
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

