import json
from typing import List

def find_city_ids_hh(filename: str, city_names: List[str]) -> List[int]:
    """
    Находит и возвращает идентификаторы городов из файла.

    Параметры:
        filename (str): Имя файла, содержащего данные идентификаторов городов для сайта hh.ru.
        city_names (List[str]): Список названий городов, для которых нужно найти идентификаторы.

    Возвращает:
        List[int]: Отсортированный список идентификаторов городов для сайта hh.ru.
    """
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


def find_city_ids_sj(filename: str, city_names: List[str]) -> List[int]:
    """
    Находит и возвращает идентификаторы городов из файла.

    Параметры:
        filename (str): Имя файла, содержащего данные идентификаторов городов для сайта superjob.ru.
        city_names (List[str]): Список названий городов, для которых нужно найти идентификаторы.

    Возвращает:
        List[int]: Отсортированный список идентификаторов городов для сайта superjob.ru.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    city_ids = []
    normalized_city_names = [city.lower() for city in city_names]

    for city in data:
        if city['title'].lower() in normalized_city_names:
            city_ids.append(city['id'])

    return sorted(city_ids)
