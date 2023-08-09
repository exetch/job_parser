from typing import Optional
class Vacancy:
    def __init__(self, vacancy_id: int, title: str, salary_from: Optional[int], salary_to: Optional[int],
                 currency: str, vacancy_type: str, experience: str, requirements: str, responsibility: str,
                 city: str, company_name: str, url: str):
        self.vacancy_id = int(vacancy_id)
        self.title = title
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.vacancy_type = vacancy_type
        self.experience = experience
        self.requirements = requirements
        self.responsibility = responsibility
        self.city = city
        self.company_name = company_name
        self.url = url
        self.salary = self._format_salary()
        self.validate_data()

    def _format_salary(self) -> str:
        if self.salary_from is not None or self.salary_to is not None:
            salary_str = ""
            if self.salary_from is not None:
                salary_str += f"от {self.salary_from}"
            if self.salary_to is not None:
                salary_str += f" до {self.salary_to}"
            return salary_str
        else:
            return "Не указана"

    def validate_data(self):
        if not isinstance(self.vacancy_id, int):
            raise ValueError("ID вакансии должен быть целым числом.")
        if not isinstance(self.title, str):
            raise ValueError("Заголовок должен быть строкой.")
        if not isinstance(self.salary_from, (int, float, type(None))):
            raise ValueError("Начальная зарплата должна быть числом или None.")
        if not isinstance(self.salary_to, (int, float, type(None))):
            raise ValueError("Конечная зарплата должна быть числом или None.")
        if not isinstance(self.currency, str):
            raise ValueError("Валюта должна быть строкой.")
        if not isinstance(self.vacancy_type, str):
            raise ValueError("Тип вакансии должен быть строкой.")
        if not isinstance(self.experience, str):
            raise ValueError("Опыт должен быть строкой.")
        if not isinstance(self.company_name, (str, type(None))):
            raise ValueError("Название компании должно быть строкой или None.")

    def __repr__(self):
        return (
            f"Vacancy(ID={self.vacancy_id}, title='{self.title}', salary='{self.salary}', "
            f"currency='{self.currency}', vacancy_type='{self.vacancy_type}', "
            f"experience='{self.experience}', requirements='{self.requirements}', "
            f"responsibility='{self.responsibility}', city='{self.city}', "
            f"company_name='{self.company_name}', url='{self.url}')"
        )

    def __str__(self):
        return (
            f"ID: {self.vacancy_id}\nTitle: {self.title}\nЗарплата: {self.salary} {self.currency}\n"
            f"Тип: {self.vacancy_type}\nОпыт: {self.experience}\n"
            f"Требования:\n{self.requirements}\nОбязанности:\n{self.responsibility}\n"
            f"Город: {self.city}\nКомпания: {self.company_name}\nURL: {self.url}"
        )

    def __lt__(self, other):
        if self.salary_from is None:
            self_salary_from = 0
        else:
            self_salary_from = self.salary_from

        if other.salary_from is None:
            other_salary_from = 0
        else:
            other_salary_from = other.salary_from

        if self_salary_from != other_salary_from:
            return self_salary_from < other_salary_from
        else:
            if self.salary_to is None:
                self_salary_to = float('inf')
            else:
                self_salary_to = self.salary_to

            if other.salary_to is None:
                other_salary_to = float('inf')
            else:
                other_salary_to = other.salary_to

            return self_salary_to < other_salary_to

    def __eq__(self, other):
        return (self.salary_from, self.salary_to) == (other.salary_from, other.salary_to)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)
