import json
from typing import Optional, Dict, List


def load_json(file_path: str) -> Optional[Dict]:
    """
    Загружает данные из JSON-файла.

    Parameters:
    file_path (str): Путь к JSON-файлу.

    Returns:
    dict or None: Содержимое JSON-файла в виде словаря. Возвращает None при ошибке загрузки.

    Raises:
    FileNotFoundError: Если указанный файл не найден.
    json.JSONDecodeError: Если произошла ошибка декодирования JSON.
    Exception: Для любых других исключений при загрузке файла.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as e:
        print(f"Ошибка: Файл '{file_path}' не найден.")
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON в файле '{file_path}': {e}")
    except Exception as e:
        print(f"Произошла ошибка при загрузке файла '{file_path}': {e}")
    return None


def find_differences(old_data: Dict, new_data: Dict, diff_keys: List[str]) -> Dict:
    """
    Находит различия между двумя структурами данных.

    Parameters:
    old_data (dict): Исходная структура данных.
    new_data (dict): Обновленная структура данных.
    diff_keys (list): Список ключей для сравнения.

    Returns:
    dict: Словарь с различиями. Ключи - отличающиеся параметры, значения - новые значения из new_data.

    Notes:
    Функция сравнивает значения ключей из diff_keys в структурах данных old_data и new_data.
    Если значение ключа в old_data не равно значению ключа в new_data, оно добавляется в результирующий словарь.
    """

    result = {}

    for key in diff_keys:
        if key in old_data.get("data") and key in new_data.get("data"):
            if old_data.get("data").get(key) != new_data.get("data").get(key):
                result[key] = new_data.get("data").get(key)
    return result


if __name__ == "__main__":
    # Список полей для сравнения
    diff_list = ['services', 'staff', 'datetime']

    # Загружаем данные из файлов
    old_data = load_json("json_data/old.json")
    new_data = load_json("json_data/new.json")

    # Находим различия
    result = find_differences(old_data, new_data, diff_list)

    print("Результат:")
    print(result)
