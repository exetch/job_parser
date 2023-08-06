from vacancystorage import JSONVacancyStorage
from vacancy_data import fetch_and_save_hh_vacancies, fetch_and_save_sj_vacancies, find_city_ids_hh, find_city_ids_sj


TOWNS_IDS_HH = "towns_hh.json"
TOWNS_IDS_SJ = "towns_sj.json"

def welcome_message():
    print("Святой поисковик вакансий приветствует вас! Пусть благодать вас направит!")

def get_platform_choice():
    while True:
        print("Светило благочестивого труда зовет вас на праведный путь! Сделайте ваш выбор с мудростью и добром в сердце:")
        print("1. Величественный HeadHunter - Избранная платформа праведного труда")
        print("2. Еретический Superjob - Соблазнительный выбор для отступников")
        print("3. Объединить две платформы - Соединить святые силы в труде и поиске")
        choice = input("Прошу, введите номер выбранной платформы: ")

        if choice in ["1", "2", "3"]:
            return choice
        else:
            print("Боже милостивый, прощение просим, но ввод неверный. Избавь нас от заблуждения!")


def get_keyword_and_city():
    keyword = input("Милостиво введите ключевое слово для поиска светлых вакансий: ")
    city = input("Просим вас указать город или города, чтобы осветить путь к вакансиям (разделите их запятой): ")
    return keyword, city.split(',')


def get_filtered_words():
    return input("Укажите святые ключевые слова для благочестивой фильтрации вакансий (разделяйте пробелами): ")


def get_top_n_or_salary_range():
    while True:
        choice = input(
            "Святая дилемма перед вами, правоверные!\n1. Топ N вакансий по зарплате\n2. Вакансии в святом диапазоне зарплаты\nПрошу, введите номер выбранной опции: ")


        if choice == "1":
            n = int(input("Благодарим за вашу веру! Укажите количество вакансий для святочного вывода: "))
            return n
        elif choice == "2":
            min_salary = int(input("Укажите минимальную зарплату своих желаний: "))
            max_salary = int(input("Укажите максимальную зарплату своих желаний: "))
            return min_salary, max_salary
        else:
            print("Прегрешение ввода, омрачивающее наш поиск. Помилуй нас, Господи!")


if __name__ == "__main__":
    storage = JSONVacancyStorage("../vacancies.json")
    welcome_message()

    platform_choice = get_platform_choice()
    if platform_choice == "1":
        hh_keyword, hh_cities = get_keyword_and_city()
        print(hh_keyword)
        print(hh_cities)
        hh_cities_ids = find_city_ids_hh(TOWNS_IDS_HH, hh_cities)
        fetch_and_save_hh_vacancies(storage, hh_keyword, hh_cities_ids)

    elif platform_choice == "2":
        sj_keyword, sj_cities = get_keyword_and_city()
        sj_cities_ids = find_city_ids_sj(TOWNS_IDS_SJ, sj_cities)
        fetch_and_save_sj_vacancies(storage, sj_keyword, sj_cities_ids)

    elif platform_choice == "3":
        keyword, cities = get_keyword_and_city()
        hh_cities_ids = find_city_ids_hh(TOWNS_IDS_HH, cities)
        sj_cities_ids = find_city_ids_sj(TOWNS_IDS_SJ, cities)
        fetch_and_save_hh_vacancies(storage, keyword, hh_cities_ids)
        fetch_and_save_sj_vacancies(storage, keyword, sj_cities_ids)

    filtered_words = get_filtered_words()
    filtered_vacancies = storage.get_vacancies(filtered_words)
    storage.remove_all_vacancies()

    if filtered_vacancies:
        n_or_salary_range_choice = get_top_n_or_salary_range()
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
