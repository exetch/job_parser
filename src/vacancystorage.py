from abc import ABC, abstractmethod
import json
from typing import List, Dict, Any, Union
from src.vacancy import Vacancy

class VacancyStorage(ABC):
    @abstractmethod
    def add_vacancies(self, vacancies_list):
        pass

    @abstractmethod
    def get_vacancies(self, filter_words):
        pass

    @abstractmethod
    def remove_vacancy(self, vacancy_id):
        pass

class JSONVacancyStorage(VacancyStorage):
    """
    Класс для хранения вакансий в JSON-файле.
    """

    def __init__(self, filename: str):
        """
        Инициализация объекта JSONVacancyStorage.

        Параметры:
            filename (str): Имя файла для хранения данных в формате JSON.
        """
        self.filename = filename

    def _read_vacancies_from_file(self) -> List[Dict[str, Any]]:
        """
        Метод для чтения вакансий из JSON-файла.

        Возвращает:
            List[Dict[str, Any]]: Список словарей с атрибутами вакансий.
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def _write_vacancies_to_file(self, vacancies: List[Dict[str, Any]]):
        """
        Метод для записи вакансий в JSON-файл.

        Параметры:
            vacancies (List[Dict[str, Any]]): Список словарей с атрибутами вакансий.
        """
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)

    def add_vacancies(self, new_vacancies):
        """
        Добавляет новые вакансии в файл, пропуская дубликаты по vacancy_id.

        Параметры:
            new_vacancies (List[Dict]): Список новых вакансий в формате словарей.

        """
        current_vacancies = self._read_vacancies_from_file()
        current_vacancy_ids = set(v['vacancy_id'] for v in current_vacancies)
        filtered_vacancies = [v for v in new_vacancies if v['vacancy_id'] not in current_vacancy_ids]

        updated_vacancies = current_vacancies + filtered_vacancies

        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(updated_vacancies, file, ensure_ascii=False, indent=4)

    def get_vacancies(self, filter_words: str) -> List[Vacancy]:
        """
        Возвращает список вакансий, отсортированный по убыванию зарплат, которые содержат все слова из filter_words
        в своих атрибутах, имеющих строковые значения.

        Параметры:
            filter_words (str): Строка с ключевыми словами для фильтрации.

        Возвращает:
            List[Vacancy]: Список объектов Vacancy, удовлетворяющих критериям фильтрации.
        """
        vacancies = self._read_vacancies_from_file()
        filter_words_list = filter_words.split()

        def check_words_in_vacancy(vacancy: Dict[str, Any]) -> bool:
            for word in filter_words_list:
                if not any(word.lower() in value.lower() for value in vacancy.values() if isinstance(value, str)):
                    return False
            return True
        return sorted([Vacancy(**v) for v in vacancies if check_words_in_vacancy(v)], reverse=True)

    def remove_vacancy(self, vacancy_id: Union[int, str]):
        """
        Удаляет вакансию из хранилища по указанному ID.

        Параметры:
            vacancy_id (Union[int, str]): ID вакансии, которую нужно удалить.
        """
        vacancies = self._read_vacancies_from_file()
        vacancies = [v for v in vacancies if v["vacancy_id"] != vacancy_id]
        self._write_vacancies_to_file(vacancies)

    def remove_all_vacancies(self):
        """
        Полностью очищает хранилище, удаляя все вакансии из файла vacancies.json.
        """
        empty_vacancies = []
        self._write_vacancies_to_file(empty_vacancies)