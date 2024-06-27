from collections import defaultdict
from typing import List, Union


def group_by_version(
        list_version: List[List[Union[str, int]]]
) -> List[List[Union[str, int, int]]]:
    """
    Группирует и подсчитывает уникальные пары [id, version] из списка list_version.

    Args:
    list_version (List[List[Union[str, int]]]): Список пар [id, version].

    Returns:
    List[List[Union[str, int, int]]]: Список списков в формате [id, version, count],
    где count - количество одинаковых пар [id, version].
    """
    try:
        # Создание defaultdict для подсчета пар [id, version]
        count_dict = defaultdict(int)

        # Проход по каждой паре [id, version] в списке list_version
        for pair in list_version:
            # Проверка на корректное количество элементов в паре
            if len(pair) != 2:
                raise ValueError(f"Неправильное количество элементов в списке: {pair}")

            # Разделение элементов пары на id_ и version
            id_, version = pair

            # Проверка на корректные типы данных в паре
            if not isinstance(id_, str) or not isinstance(version, int):
                raise TypeError(f"Некорректные типы данных в паре: {pair}")

            # Увеличение счетчика для текущей пары [id_, version]
            count_dict[(id_, version)] += 1

        # Создание результирующего списка в формате [id_, version, count]
        result = [[id_, version, count] for (id_, version), count in count_dict.items()]

        # Возврат результата
        return result

    except (ValueError, TypeError) as e:
        print(f"Ошибка: Некорректные данные в list_version. Подробности: {str(e)}")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return []


if __name__ == "__main__":
    list_version = [['665587', 1], ['669532', 1], ['669537', 2], ['669532', 1], ['665587', 1]]
    result = group_by_version(list_version)
    print(result)
