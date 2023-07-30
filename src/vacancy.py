class Vacancy:
    def __init__(self, ID, title, salary, vacancy_type, experience, requirements, responsibility, city, company_name,
                 url):
        self.ID = ID
        self.title = title
        self.salary = salary
        self.vacancy_type = vacancy_type
        self.experience = experience
        self.requirements = requirements
        self.responsibility = responsibility
        self.city = city
        self.company_name = company_name
        self.url = url

    def __repr__(self):
        return (
            f"Vacancy(ID={self.ID}, title='{self.title}', salary='{self.salary}', "
            f"vacancy_type='{self.vacancy_type}', experience='{self.experience}', "
            f"city='{self.city}', company_name='{self.company_name}')"
        )

    def __str__(self):
        return (
            f"ID: {self.ID}\nTitle: {self.title}\nЗарплата: {self.salary}\n"
            f"Тип: {self.vacancy_type}\nОпыт: {self.experience}\n"
            f"Требования:\n{self.requirements}\nОбязанности:\n{self.responsibility}\n"
            f"Город: {self.city}\nКомпания: {self.company_name}\nURL: {self.url}"
        )
