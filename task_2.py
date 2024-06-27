from collections import defaultdict
from typing import List, Union


def group_by_version(list_version: List[List[Union[str, int]]]) -> List[List[Union[str, int, int]]]:
    """
    Группирует и подсчитывает уникальные пары [id, version] из списка list_version.

    Args:
    list_version (List[List[Union[str, int]]]): Список пар [id, version].

    Returns:
    List[List[Union[str, int, int]]]: Список списков в формате [id, version, count],
    где count - количество одинаковых пар [id, version].
    """
    try:
        count_dict = defaultdict(int)

        for pair in list_version:
            if len(pair) != 2:
                raise ValueError(f"Неправильное количество элементов в списке: {pair}")

            id_, version = pair
            if not isinstance(id_, str) or not isinstance(version, int):
                raise TypeError(f"Некорректные типы данных в паре: {pair}")

            count_dict[(id_, version)] += 1

        result = [[id_, version, count] for (id_, version), count in count_dict.items()]

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
