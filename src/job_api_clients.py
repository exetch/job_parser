from typing import List, Dict, Union, Tuple
from abc import ABC, abstractmethod
import requests


class AbstractJobSiteAPI(ABC):
    """
    Абстрактный базовый класс для API сайтов с вакансиями.
    """

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def parse_vacancies(self):
        pass


class SuperjobAPI(AbstractJobSiteAPI):
    """
    Класс для работы с API сайта Superjob.
    """

    def __init__(self, secret_key, keyword: str, cities_ids: List[int] = [4, 14]):
        """
        Конструктор класса.

        Параметры:
            secret_key(str): секретный ключ для взаимодействия с API
            keyword (str): Ключевое слово для поиска вакансий.
            cities_ids (List[int]): Список идентификаторов городов для поиска вакансий. По умолчанию равен [4, 14], то есть Москва и Санкт-Петербург.
        """
        self.keyword = keyword
        self.cities_ids = cities_ids
        self.all_vacancies = []
        self.parsed_vacancies = []
        self.secret_key = secret_key

    def get_vacancies(self) -> None:
        """
        Получает вакансии с веб-сайта superjob.ru и сохраняет их в атрибут self.all_vacancies.
        """
        page = 0
        per_page = 100

        while True:
            params = {
                "keyword": self.keyword,
                "t": self.cities_ids,
                "page": page,
                "count": per_page,
                "no_agreement": 1}
            headers = {'X-Api-App-Id': self.secret_key}
            url = f'https://api.superjob.ru/2.0/vacancies/'
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                response_data = response.json()
                vacancies = response_data.get('objects', [])
                total = response_data.get('total', 0)
                print(
                    f"Благословенных {total} вакансий обнаружено на superjob.ru. В {page + 1} итерации "
                    f"даровано {len(vacancies)} вакансий для вашего рассмотрения...")
                self.all_vacancies.extend(vacancies)

                if total <= (page + 1) * per_page:
                    break
                else:
                    page += 1
            else:
                print(f"Request failed with status code: {response.status_code}")
                break

    def parse_vacancies(self) -> List[Dict[str, Union[str, int]]]:
        """
        Парсит вакансии, полученные из метода get_vacancies, и сохраняет их в атрибут self.parsed_vacancies.

        Возвращает:
            List[Dict[str, Union[str, int]]]: Список словарей с деталями обработанных вакансий.
        """

        def get_responsibilities_and_requirements(candidat_text: str) -> Tuple[str, str]:
            """
            Получает текст описания вакансии и анализирует его для извлечения обязанностей и требований.

            Параметры:
                candidat_text (str): Текст описания вакансии.

            Возвращает:
                Tuple[str, str]: Кортеж из двух строк. Первая строка содержит текст обязанностей,
                а вторая строка содержит текст требований. Если обязанности или требования не указаны,
                то вместо них возвращается строка "Не указаны".
            """
            responsibilities = []
            requirements = []
            is_responsibilities_section = False
            is_requirements_section = False
            responsibilities_substrings = ["обязанности", "заниматься", "задач"]
            requirements_substrings = ["требования", "что ждём от вас", "компетенции", "ожидаем", "идеальный кандидат",
                                       "опыт и знания"]
            skip_sections_substrings = ["условия", "пожелания", "преимуществ", "предлагаем", "плюсом", "желательно"]

            if candidat_text:
                candidat_lines = candidat_text.split("\n")

                for line in candidat_lines:
                    lower_line = line.strip().lower()
                    cleaned_line = line.strip("-•*:;. ")
                    if any(substring in lower_line for substring in skip_sections_substrings):
                        is_responsibilities_section = False
                        is_requirements_section = False
                    elif any(substring in lower_line for substring in responsibilities_substrings):
                        is_responsibilities_section = True
                        is_requirements_section = False
                    elif any(substring in lower_line for substring in requirements_substrings):
                        is_responsibilities_section = False
                        is_requirements_section = True
                    else:
                        if is_responsibilities_section and cleaned_line:
                            responsibilities.append(cleaned_line)
                        elif is_requirements_section and cleaned_line:
                            requirements.append(cleaned_line)

            responsibilities_text = ". ".join(responsibilities[:3]) + "..." if responsibilities else "Не указаны"
            requirements_text = ". ".join(requirements[:3]) + "..." if requirements else "Не указаны"

            return responsibilities_text, requirements_text

        self.parsed_vacancies = [{
            "vacancy_id": vacancy.get("id"),
            "vacancy_type": "Закрытая" if vacancy.get("is_closed") else "Открытая",
            "title": vacancy.get("profession"),
            "url": vacancy.get("link"),
            "city": vacancy.get("town", {}).get("title", "Unknown City"),
            "salary_from": vacancy.get("payment_from"),
            "salary_to": vacancy.get("payment_to"),
            "currency": vacancy.get("currency"),
            "company_name": vacancy.get("client", {}).get("title"),
            "experience": vacancy.get("experience", {}).get("title"),
            "requirements": get_responsibilities_and_requirements(vacancy.get("candidat", ""))[1],
            "responsibility": get_responsibilities_and_requirements(vacancy.get("candidat", ""))[0]
        } for vacancy in self.all_vacancies]
        return self.parsed_vacancies


class HeadHunterAPI(AbstractJobSiteAPI):
    """
        Класс для работы с API сайта HeadHunter.
    """

    def __init__(self, user_agent, keyword: str, cities_ids: List[int] = [1, 2]):
        """
        Конструктор класса.

        Параметры:
            user_agent (str): Заголовок User-Agent для запросов к API
            keyword (str): Ключевое слово для поиска вакансий
            cities_ids (List[int]): Список идентификаторов городов для поиска вакансий. По умолчанию равен [1, 2], то есть Москва и Санкт-Петербург.
        """
        self.keyword = keyword
        self.cities_ids = cities_ids
        self.all_vacancies = []
        self.parsed_vacancies = []
        self.user_agent = user_agent

    def get_vacancies(self) -> None:
        """
        Получает вакансии с веб-сайта hh.ru и сохраняет их в атрибут self.all_vacancies.
        """
        page = 0
        per_page = 100
        while True:
            params = {
                "text": self.keyword,
                "area": self.cities_ids,
                "page": page,
                "per_page": 100,
                "only_with_salary": True
            }

            headers = {
                'User-Agent': self.user_agent,
            }
            url = f'https://api.hh.ru/vacancies'
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                response_data = response.json()
                vacancies = response_data.get('items', [])
                total = response_data.get('found', 0)
                print(
                    f"Веруйте, что на hh.ru найдено {total} благословенных вакансий. Просветление "
                    f"принесло {len(vacancies)} благовествующих вакансий в текущей итерации {page + 1}...")
                self.all_vacancies.extend(vacancies)
                if total <= (page + 1) * per_page:
                    break
                else:
                    page += 1
            else:
                print(f"Request failed with status code: {response.status_code}")
                break

    def parse_vacancies(self) -> List[Dict[str, Union[str, int]]]:
        """
        Парсит вакансии, полученные из метода get_vacancies, и сохраняет их в атрибут self.parsed_vacancies.

        Возвращает:
            List[Dict[str, Union[str, int]]]: Список словарей с деталями обработанных вакансий.
        """
        self.parsed_vacancies = [{
            "vacancy_id": vacancy.get("id"),
            "title": vacancy.get("name"),
            "url": vacancy.get("alternate_url"),
            "vacancy_type": vacancy.get("type", {}).get("name"),
            "city": vacancy.get("area", {}).get("name", "Unknown City"),
            "experience": vacancy.get("experience", {}).get("name"),
            "requirements": vacancy.get("snippet", {}).get("requirement"),
            "responsibility": vacancy.get("snippet", {}).get("responsibility"),
            "salary_from": vacancy.get("salary", {}).get("from"),
            "salary_to": vacancy.get("salary", {}).get("to"),
            "currency": vacancy.get("salary", {}).get("currency"),
            "company_name": vacancy.get("employer", {}).get("name")
        } for vacancy in self.all_vacancies]
        return self.parsed_vacancies
