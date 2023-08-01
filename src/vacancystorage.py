from abc import ABC, abstractmethod
import json
from src.vacancy import Vacancy

class VacancyStorage(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, criteria):
        pass

    @abstractmethod
    def remove_vacancy(self, vacancy_id):
        pass

class JSONVacancyStorage(VacancyStorage):
    def __init__(self, filename):
        self.filename = filename

    def _read_vacancies_from_file(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def _write_vacancies_to_file(self, vacancies):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy):
        vacancies = self._read_vacancies_from_file()
        vacancy_dict = vacancy.to_dict()
        vacancies.append(vacancy_dict)
        self._write_vacancies_to_file(vacancies)

    def get_vacancies(self, criteria):
        vacancies = self._read_vacancies_from_file()
        return [Vacancy(**v) for v in vacancies if criteria in v["title"]]

    def remove_vacancy(self, vacancy_id):
        vacancies = self._read_vacancies_from_file()
        vacancies = [v for v in vacancies if v["vacancy_id"] != vacancy_id]
        self._write_vacancies_to_file(vacancies)