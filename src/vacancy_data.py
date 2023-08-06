import json
from src.job_api_clients import HeadHunterAPI, SuperjobAPI


def fetch_and_save_hh_vacancies(storage, keyword, cities_ids):
    """
    Получает вакансии с сайта hh.ru, фильтрует и сохраняет их в JSON-файл.

    Параметры:
        storage (JSONVacancyStorage): Объект хранилища для сохранения вакансий.

    """
    api_hh = HeadHunterAPI()
    vacancies_hh = api_hh.get_vacancies(keyword, cities_ids)

    if vacancies_hh:
        vacancies_list = []

        for vacancy in vacancies_hh:
            vacancy_id = vacancy.get("id")
            title = vacancy.get("name")
            url = vacancy.get("alternate_url")
            vacancy_type = vacancy.get("type", {}).get("name")
            city = vacancy.get("area", {}).get("name", "Unknown City")
            experience = vacancy.get("experience", {}).get("name")
            requirements = vacancy.get("snippet", {}).get("requirement")
            responsibility = vacancy.get("snippet", {}).get("responsibility")
            salary_from = vacancy.get("salary", {}).get("from")
            salary_to = vacancy.get("salary", {}).get("to")
            currency = vacancy.get("salary", {}).get("currency")
            company_name = vacancy.get("employer", {}).get("name")

            vacancy_dict = {
                "vacancy_id": vacancy_id,
                "title": title,
                "url": url,
                "vacancy_type": vacancy_type,
                "city": city,
                "experience": experience,
                "requirements": requirements,
                "responsibility": responsibility,
                "salary_from": salary_from,
                "salary_to": salary_to,
                "currency": currency,
                "company_name": company_name
            }

            vacancies_list.append(vacancy_dict)

        storage.add_vacancies(vacancies_list)
    else:
        print('No vacancies found.')


def fetch_and_save_sj_vacancies(storage, keyword, cities_ids):
    """
       Получает вакансии с сайта superjob.ru, фильтрует и сохраняет их в JSON-файл.

       Параметры:
           storage (JSONVacancyStorage): Объект хранилища для сохранения вакансий.

       """
    api_sj = SuperjobAPI()
    vacancies_sj = api_sj.get_vacancies(keyword, cities_ids)
    if vacancies_sj:
        vacancies_list = []
        for vacancy in vacancies_sj:
            vacancy_id = vacancy.get("id")
            is_closed = vacancy.get("is_closed")
            if is_closed:
                vacancy_type = "Закрытая"
            else:
                vacancy_type = "Открытая"
            title = vacancy.get("profession")
            url = vacancy.get("link")
            city = vacancy.get("town", {}).get("title", "Unknown City")
            salary_from = vacancy.get("payment_from")
            salary_to = vacancy.get("payment_to")
            currency = vacancy.get("currency")
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
                    cleaned_line = line.strip("-•*:;. ")
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

            responsibilities_text = ". ".join(responsibilities[:3]) + "..." if responsibilities else "Не указаны"
            requirements_text = ". ".join(requirements[:3]) + "..." if requirements else "Не указаны"

            vacancy_dict = {
                "vacancy_id": vacancy_id,
                "title": title,
                "url": url,
                "vacancy_type": vacancy_type,
                "city": city,
                "experience": experience,
                "requirements": requirements_text,
                "responsibility": responsibilities_text,
                "salary_from": salary_from,
                "salary_to": salary_to,
                "currency": currency,
                "company_name": company_name
            }

            vacancies_list.append(vacancy_dict)

        storage.add_vacancies(vacancies_list)
    else:
        print('No vacancies found.')

def find_city_ids_hh(filename, city_names):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    city_ids = []
    normalized_city_names = [city.lower() for city in city_names]

    for region in data:
        for area in region['areas']:
            if area['name'].lower() in normalized_city_names:
                city_ids.append(int(area['id']))

    # Обработка исключений
    for city_name in normalized_city_names:
        if city_name == 'москва':
            city_ids.append(1)
        elif city_name == 'санкт-петербург':
            city_ids.append(2)

    return sorted(city_ids)


def find_city_ids_sj(filename, city_names):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    city_ids = []
    normalized_city_names = [city.lower() for city in city_names]

    for city in data:
        if city['title'].lower() in normalized_city_names:
            city_ids.append(city['id'])

    return sorted(city_ids)