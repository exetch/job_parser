from src.job_api_clients import SuperjobAPI, HeadHunterAPI

if __name__ == '__main__':
    api_hh = HeadHunterAPI()

    # Получение вакансий с HeadHunter.ru
    vacancies = api_hh.get_vacancies('python')
    if vacancies:
        for vacancy in vacancies:
            vacancy_id = vacancy.get("id")
            vacancy_title = vacancy.get("name")
            vacancy_url = vacancy.get("alternate_url")
            vacancy_city = vacancy.get("area", {}).get("name", "Unknown City")
            vacancy_salary_info = vacancy.get("salary")
            if vacancy_salary_info:
                salary_from = vacancy_salary_info.get("from")
                salary_to = vacancy_salary_info.get("to")
                currency = vacancy_salary_info.get("currency", "RUR")

                if salary_from and salary_to:
                    vacancy_salary = f"от {salary_from} до {salary_to} {currency}"
                elif salary_from:
                    vacancy_salary = f"от {salary_from} {currency}"
                elif salary_to:
                    vacancy_salary = f"до {salary_to} {currency}"
            else:
                vacancy_salary = "Не указана"
            company_name = vacancy.get("employer", {}).get("name")
            print(f"ID: {vacancy_id}\nTitle: {vacancy_title}\nЗарплата: {vacancy_salary}\nГород: {vacancy_city}\nURL: {vacancy_url}\n")
    else:
        print('No vacancies found.')
    api_sj = SuperjobAPI()

    # Получение вакансий с Superjob.ru
    vacancies = api_sj.get_vacancies('python')


    if vacancies:
        for vacancy in vacancies:
            vacancy_id = vacancy.get("id")
            vacancy_title = vacancy.get("profession")
            vacancy_url = vacancy.get("link")
            vacancy_city = vacancy.get("town", {}).get("title", "Unknown City")
            vacancy_salary = vacancy.get("payment_from") or "Не указана"
            company_name = vacancy.get("client", {}).get("title")
            print(
                f"ID: {vacancy_id}\nTitle: {vacancy_title}\nЗарплата: {vacancy_salary}\nГород: {vacancy_city}\nURL: {vacancy_url}\n")
    else:
        print('No vacancies found.')