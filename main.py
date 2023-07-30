from src.job_api_clients import SuperjobAPI, HeadHunterAPI
from src.vacancy import Vacancy

if __name__ == '__main__':
    api_hh = HeadHunterAPI()

    # Получение вакансий с HeadHunter.ru
    vacancies = api_hh.get_vacancies('python')
    if vacancies:
        for vacancy in vacancies:
            vacancy_id = vacancy.get("id")
            title = vacancy.get("name")
            url = vacancy.get("alternate_url")
            vacancy_type = vacancy.get("type", {}).get("name")
            city = vacancy.get("area", {}).get("name", "Unknown City")
            salary_info = vacancy.get("salary")
            experience = vacancy.get("experience", {}).get("name")
            requirements = vacancy.get("snippet", {}).get("requirement")
            responsibility = vacancy.get("snippet", {}).get("responsibility")
            if salary_info:
                salary_from = salary_info.get("from")
                salary_to = salary_info.get("to")
                currency = salary_info.get("currency", "RUR")

                if salary_from and salary_to:
                    salary = f"от {salary_from} до {salary_to} {currency}"
                elif salary_from:
                    salary = f"от {salary_from} {currency}"
                elif salary_to:
                    salary = f"до {salary_to} {currency}"
            else:
                salary = "Не указана"
            company_name = vacancy.get("employer", {}).get("name")
            vacancy_obj = Vacancy(vacancy_id, title, salary, vacancy_type, experience,
                                  requirements, responsibility, city, company_name, url)
            print(vacancy_obj)


    else:
        print('No vacancies found.')

    api_sj = SuperjobAPI()

    # Получение вакансий с Superjob.ru
    vacancies = api_sj.get_vacancies('python')
    if vacancies:
        for vacancy in vacancies:
            vacancy_id = vacancy.get("id")
            is_closed = vacancy.get("is_closed")
            if is_closed:
                vacancy_type = "Закрытая"
            else:
                vacancy_type = "Открытая"
            experience = vacancy.get("experience")
            title = vacancy.get("profession")
            url = vacancy.get("link")
            city = vacancy.get("town", {}).get("title", "Unknown City")
            payment_from = vacancy.get("payment_from")
            payment_to = vacancy.get("payment_to")
            if payment_from or payment_to:
                salary_range = f"от {payment_from}" if payment_from else ""
                if payment_to:
                    salary_range += f" до {payment_to}"
            else:
                salary_range = "Не указана"
            company_name = vacancy.get("client", {}).get("title")
            experience = vacancy.get("experience", {}).get("title")
            candidat_text = vacancy.get("candidat", "")
            responsibilities = []
            requirements = []
            is_responsibilities_section = False
            is_requirements_section = False

            if candidat_text:
                candidat_lines = candidat_text.split("\n")
                responsibilities_substrings = ["обязанности", "заниматься", "задач"]
                requirements_substrings = ["требования", "что ждём от вас", "компетенции",
                                           "ожидаем", "идеальный кандидат", "опыт и знания"]
                skip_sections_substrings = ["условия", "пожелания", "преимуществ", "предлагаем", "плюсом", "желательно"]

                for line in candidat_lines:
                    lower_line = line.strip().lower()
                    cleaned_line = line.lstrip("-•* ")
                    if any(substring in lower_line for substring in skip_sections_substrings):
                        is_responsibilities_section = False
                        is_requirements_section = False
                    elif any(substring in lower_line for substring in requirements_substrings):
                        is_responsibilities_section = False
                        is_requirements_section = True
                    elif any(substring in lower_line for substring in responsibilities_substrings):
                        is_responsibilities_section = True
                        is_requirements_section = False
                    else:
                        if is_responsibilities_section and cleaned_line:
                            responsibilities.append(cleaned_line)
                        elif is_requirements_section and cleaned_line:
                            requirements.append(cleaned_line)

            responsibilities_text = "\n".join(responsibilities) if responsibilities else "Не указаны"
            requirements_text = "\n".join(requirements) if requirements else "Не указаны"

            vacancy_obj = Vacancy(vacancy_id, title, salary_range, vacancy_type, experience,
                                  requirements_text, responsibilities_text, city, company_name, url)
            print(vacancy_obj)
    else:
        print('No vacancies found.')
