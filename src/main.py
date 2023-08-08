import os
from vacancystorage import JSONVacancyStorage
from userinterface import UserInterface
from utils import find_city_ids_hh, find_city_ids_sj
from job_api_clients import SuperjobAPI, HeadHunterAPI

TOWNS_IDS_HH = "towns_hh.json"
TOWNS_IDS_SJ = "towns_sj.json"
SECRET_KEY = os.getenv("SJ_API_KEY")
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
STORAGE_NAME = "../vacancies.json"

if __name__ == "__main__":
    storage = JSONVacancyStorage(STORAGE_NAME)
    storage.remove_all_vacancies()
    user_interface = UserInterface()

    platform_choice = user_interface.get_platform_choice()
    if platform_choice == "1":
        hh_keyword, hh_cities = user_interface.get_keyword_and_city()
        hh_cities_ids = find_city_ids_hh(TOWNS_IDS_HH, hh_cities)
        api_hh = HeadHunterAPI(USER_AGENT, hh_keyword, hh_cities_ids)
        api_hh.get_vacancies()
        parsed_vacancies_hh = api_hh.parse_vacancies()
        storage.add_vacancies(parsed_vacancies_hh)

    elif platform_choice == "2":
        sj_keyword, sj_cities = user_interface.get_keyword_and_city()
        sj_cities_ids = find_city_ids_sj(TOWNS_IDS_SJ, sj_cities)
        api_sj = SuperjobAPI(SECRET_KEY, sj_keyword, sj_cities_ids)
        api_sj.get_vacancies()
        parsed_sj_vacancies = api_sj.parse_vacancies()
        storage.add_vacancies(parsed_sj_vacancies)

    elif platform_choice == "3":
        keyword, cities = user_interface.get_keyword_and_city()
        hh_cities_ids = find_city_ids_hh(TOWNS_IDS_HH, cities)
        sj_cities_ids = find_city_ids_sj(TOWNS_IDS_SJ, cities)
        api_hh = HeadHunterAPI(USER_AGENT, keyword, hh_cities_ids)
        api_sj = SuperjobAPI(SECRET_KEY, keyword, sj_cities_ids)

        api_hh.get_vacancies()
        api_sj.get_vacancies()

        parsed_vacancies_hh = api_hh.parse_vacancies()
        storage.add_vacancies(parsed_vacancies_hh)

        parsed_sj_vacancies = api_sj.parse_vacancies()
        storage.add_vacancies(parsed_sj_vacancies)

    filtered_words = user_interface.get_filtered_words()
    filtered_vacancies = storage.get_vacancies(filtered_words)

    if filtered_vacancies:
        n_or_salary_range_choice = user_interface.get_top_n_or_salary_range()
        if isinstance(n_or_salary_range_choice, int):
            top_n_vacancies = filtered_vacancies[:n_or_salary_range_choice]
            for v in top_n_vacancies:
                print(v)
        else:
            min_salary, max_salary = n_or_salary_range_choice
            salary_range_vacancies = [
                v for v in filtered_vacancies if
                (v.salary_from is None and v.salary_to <= max_salary) or
                (v.salary_to is None and min_salary <= v.salary_from <= max_salary) or
                (v.salary_from is not None and v.salary_to is not None and
                 v.salary_from >= min_salary and v.salary_to <= max_salary)]
            for v in salary_range_vacancies:
                print(v)
    else:
        print("Помолимся ещё: вакансий по вашему запросу на сегодняшний день не найдено.")
