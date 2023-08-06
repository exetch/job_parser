from vacancystorage import JSONVacancyStorage
from vacancy_data import fetch_and_save_hh_vacancies, fetch_and_save_sj_vacancies, find_city_ids_hh, find_city_ids_sj
from userinterface import UserInterface


TOWNS_IDS_HH = "towns_hh.json"
TOWNS_IDS_SJ = "towns_sj.json"

if __name__ == "__main__":
    storage = JSONVacancyStorage("../vacancies.json")
    storage.remove_all_vacancies()
    user_interface = UserInterface()

    platform_choice = user_interface.get_platform_choice()
    if platform_choice == "1":
        hh_keyword, hh_cities = user_interface.get_keyword_and_city()
        hh_cities_ids = find_city_ids_hh(TOWNS_IDS_HH, hh_cities)
        fetch_and_save_hh_vacancies(storage, hh_keyword, hh_cities_ids)

    elif platform_choice == "2":
        sj_keyword, sj_cities = user_interface.get_keyword_and_city()
        sj_cities_ids = find_city_ids_sj(TOWNS_IDS_SJ, sj_cities)
        fetch_and_save_sj_vacancies(storage, sj_keyword, sj_cities_ids)

    elif platform_choice == "3":
        keyword, cities = user_interface.get_keyword_and_city()
        hh_cities_ids = find_city_ids_hh(TOWNS_IDS_HH, cities)
        sj_cities_ids = find_city_ids_sj(TOWNS_IDS_SJ, cities)
        fetch_and_save_hh_vacancies(storage, keyword, hh_cities_ids)
        fetch_and_save_sj_vacancies(storage, keyword, sj_cities_ids)

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
        print("Помолимся ещё: вакансий по вашему запросу на сегодняшний день не найдено. Ждать вакансий — это испытание, посланное нам Господом нашим!")