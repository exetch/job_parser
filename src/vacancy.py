class Vacancy:
    def __init__(self, vacancy_id, title, salary_from, salary_to, currency, vacancy_type, experience, requirements, responsibility, city, company_name,
                 url):
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

        self.validate_data()

        if self.salary_from or self.salary_to:
            self.salary = f"от {salary_from}" if salary_from else ""
            if salary_to:
                self.salary += f" до {salary_to}"
        else:
            self.salary = "Не указана"

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

    def __eq__(self, other):
        return self.salary_from == other.salary_from and self.salary_to == other.salary_to

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.salary_from < other.salary_from

    def __le__(self, other):
        return self.salary_from <= other.salary_from

    def __gt__(self, other):
        return self.salary_from > other.salary_from

    def __ge__(self, other):
        return self.salary_from >= other.salary_from

    def to_dict(self):
        return {
            "vacancy_id": self.vacancy_id,
            "title": self.title,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "currency": self.currency,
            "vacancy_type": self.vacancy_type,
            "experience": self.experience,
            "requirements": self.requirements,
            "responsibility": self.responsibility,
            "city": self.city,
            "company_name": self.company_name,
            "url": self.url
        }