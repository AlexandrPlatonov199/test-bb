import re
from typing import List


def is_valid_key(key: str, valid_keys: List[str]) -> bool:
    """
    Проверяет, является ли ключ допустимым.
    """
    return key in valid_keys


def verify_text(test_text: str, valid_keys: List[str]) -> str:
    """
    Проверяет текст на правильность использования ключей и скобок.

    Args:
    test_text (str): Текст для проверки.
    valid_keys (list): Список допустимых ключей.

    Returns:
    str: Результат проверки.
    """

    # Проверка на наличие незакрытых скобок
    if test_text.count('{') != test_text.count('}'):
        return "Ошибка: Несовпадение количества открывающих и закрывающих скобок"

    # Проверка каждого найденного ключа
    pattern = re.compile(r'\{([^}]+)\}')
    for match in pattern.findall(test_text):
        if not is_valid_key(match, valid_keys):
            return f"Ошибка: Некорректный ключ '{match}'"

    return "Тест пройден: Все данные корректны"


if __name__ == "__main__":
    valid_keys = ['name', 'day_month', 'day_of_week', 'start_time', 'end_time', 'master', 'services']

    # Тест 1: Корректный текст
    test_text_1 = """
    {name}, ваша запись изменена:
    ⌚️ {day_month} в {start_time}
    👩 {master}
    Услуги:
    {services}
    """
    result_1 = verify_text(test_text_1, valid_keys)
    assert result_1 == "Тест пройден: Все данные корректны", f"Failed Test 1: {result_1}"

    # Тест 2: Некорректный ключ
    test_text_2 = """
    {name}, ваша запись изменена:
    ⌚️ {day_month} в {start_time}
    👩 {master}
    Услуги:
    {services}
    управление записью {record_link}
    """
    result_2 = verify_text(test_text_2, valid_keys)
    assert result_2 == "Ошибка: Некорректный ключ 'record_link'", f"Failed Test 2: {result_2}"

    # Тест 3: Некорректный ключ (с большой буквы)
    test_text_3 = """
    {Name}, ваша запись изменена:
    ⌚️ {day_month} в {start_time}
    👩 {master}
    Услуги:
    {services}
    """
    result_3 = verify_text(test_text_3, valid_keys)
    assert result_3 == "Ошибка: Некорректный ключ 'Name'", f"Failed Test 3: {result_3}"

    # Тест 4: Несовпадение количества скобок
    test_text_4 = """
    {name, ваша запись изменена:
    ⌚️ {day_month} в {start_time}
    👩 {master}
    Услуги:
    {services}
    """
    result_4 = verify_text(test_text_4, valid_keys)
    assert result_4 == "Ошибка: Несовпадение количества открывающих и закрывающих скобок", f"Failed Test 4: {result_4}"

    # Тест 5: Некорректный ключ
    test_text_5 = """
    {nme}, ваша запись изменена:
    ⌚️ {day_month} в {start_time}
    👩 {master}
    Услуги:
    {services}
    """
    result_5 = verify_text(test_text_5, valid_keys)
    assert result_5 == "Ошибка: Некорректный ключ 'nme'", f"Failed Test 5: {result_5}"

    print("Все тесты пройдены успешно.")
