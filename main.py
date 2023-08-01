from src.vacancystorage import JSONVacancyStorage
from src.vacancy_data import fetch_and_save_hh_vacancies, fetch_and_save_sj_vacancies

if __name__ == '__main__':
    storage = JSONVacancyStorage("vacancies.json")

    fetch_and_save_hh_vacancies(storage)
    fetch_and_save_sj_vacancies(storage)
    filtered_vacancies = storage.get_vacancies("разработчик")
    for vacancy in filtered_vacancies:
        print(vacancy)
    print(len(filtered_vacancies))