# Тестово задание для Бьюти Бот

## 1. Задание:
Необходимо провести верификацию введенных пользователем данных.
Проверяются ключи на предмет соответствия написания с определенными в list_keys значениями ,
а также наличие открывающих и закрывающих скобок.

Решение: [task_1.py](./task_1.py)

## 2. Задание:
Сгрупировать по уникальности пары id, version в list_version

Решение: [task_2.py](./task_2.py)

## 3. Задание:
Найти различия между 2мя json. Если различающиеся параметры входят в diff_list,
вывести различие. Иными словами, нужно отловить изменение определенных параметров
и вывести значение что изменилось и на что. Набор ключей в обоих json идентичный, различаются лишь значения


Решение: [task_3.py](./task_3.py)


## 4. Задание:
Предложите систему для очистки данных из MongoDB по истечению заданного времени


Решение:
1. Перед началом удаления документов по времени необходимо убедиться, 
что поле времени (например, "created_at") имеет индекс.
Индексация поля времени ускоряет операции выборки и удаления документов,
основанных на временных критериях.

```
db.collection.createIndex({ created_at: 1 })
```
2. Написать скрипт для удаления устаревших данных:

```python
from pymongo import MongoClient
from datetime import datetime, timedelta

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
collection = db['mycollection']

# Задаем временной порог (например, удалять документы, созданные более 24 часов назад)
expiration_date = datetime.utcnow() - timedelta(hours=24)

# Удаляем документы, у которых поле created_at меньше expiration_date
result = collection.delete_many({'created_at': {'$lt': expiration_date}})
print(f'{result.deleted_count} документов удалено')

# Закрываем соединение с MongoDB
client.close()
```

3. Автоматизировать процесс по очистке данных
```python
import schedule
import time

def cleanup():
    from pymongo import MongoClient
    from datetime import datetime, timedelta

    # Подключение к MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['mydatabase']
    collection = db['mycollection']

    # Задаем временной порог (например, удалять документы, созданные более 24 часов назад)
    expiration_date = datetime.utcnow() - timedelta(hours=24)

    # Удаляем документы, у которых поле created_at меньше expiration_date
    result = collection.delete_many({'created_at': {'$lt': expiration_date}})
    print(f'{result.deleted_count} документов удалено')

    # Закрываем соединение с MongoDB
    client.close()

# Запускаем очистку данных каждый день в 2:00 AM
schedule.every().day.at('02:00').do(cleanup)

while True:
    schedule.run_pending()
    time.sleep(1)

```

## 5. Задание:
Предложите архитектуру обработки входящих веб хуков с использованием одного endpoint


Решение:

#### Структура проекта

- **`app/`**: Основной каталог приложения.
  - **`configuration/`**: Пакет с модулями конфигурации приложения.
    - **`__init__.py`**
    - **`events.py`**: Cодержит функции, которые вызываются при попытке сервера начать и завершить работу.
    - **`server.py`**: Настройки конфигурации приложения.
  - **`internal/`**: Пакет содержащий пакеты и модули для реализации бизнесс логики приложения.
    - **`__init__.py`**
    - **`repository/`**: Пакет в котором создаються репозитории.
      - **`__init__.py`** 
      - **`mongodb/`**: Например на проекте мы будем работать с MongoDB.
        - **`__init__.py`**
        - **`connection.py`**: Описание создания подключения к MongoDB.
        - **`webhooks.py`**: Репозиторий для webhook.
      - **`repository.py`**: Абстрактный интерфейс репозитория, от которого будут наследоваться репозитории.
    - **`routes/`**: Пакет в котором создаются модули роутеров с которыми будет работать наше приложение.
      - **`__init__.py`**
      - **`webhooks.py`**: Роутеры для webhooks.
    - **`services/`**: Пакет в котором создаються сервисы выполняющие бизнес логику.
      - **`__init__.py`**
      - **`webhooks.py`**: Сервис выполняющий бизнес логику.
  - **`pkg/`**: Пакеты, которые имеют минимальную привязку к конкретной бизнес-логике.
    - **`__init__.py`**
    - **`connectors/`**: Пакет для описания подключения к бд.
      - **`mongodb/`** К примеру описываем логику работы с MongoDB
      - **`connectors.py`**: Описание абстрактного подключения.
    - **`models/`**: Пакет в котором описывается  поведение бизнес сущности.
      - **`app/`**: Пакет в котором создаються бизнесс сущности.
        - **`webhooks.py`**: Модели для webhooks
      - **`exceptions/`**: Пакет в котором описываються кастомные ошибки.
        - **`__init__.py`**
        - **`webhooks.py`**: Создание ошибок 
    - **`settings/`**: Глобальная точка для кешированных настроек
      - **`__init__.py`**
      - **`settings.py`**: Модуль для загрузки настроек из .env
  - **`__init__.py`**: Инициализационный файл для пакета `app`.

#### Код
Напишу не полную реализацию кода, а примерную.

В app/pkg/models/app/webhooks.py создадим бизнес сущность для Webhooks

```python
from pydantic import BaseModel
from typing import Dict

class Webhook(BaseModel):
    function: str
    data: Dict[str, any]
```

В app/internal/routes/webhooks.py создать endpoint который будет принимать входящие веб хуки(в примерном коде используеться DI описывать его логику и как она создаеться не буду, а то полчуться слишком много кода):

```python
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status, Request

from app.internal.services import WebhookService, Services
from app.pkg import models

router = APIRouter(
    tags=["Webhook"],
    prefix="/v1/webhook",
)


@router.post(
    "/Datalore",
    response_model=models.Webhook,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def handle_webhook(
    models: models.Webhook,
    webhook_service: WebhookService = Depends(Provide[Services.webhook_service]),
):
    return await webhook_service.message_handler(models=models)

```

В app/internal/service/webhooks.py cоздадим сервис WebhookService который
инициализирует объект для управления вебхуками, используя словарь
для отображения имен функций на их методы обработки,
а также предоставляет метод message_handler для обработки входящих вебхуков
с использованием заданных функций

```python
import typing
from fastapi import HTTPException

from app.internal.repository.mongodb import weebhooks
from app.internal.repository.repository import BaseRepository
from app.pkg import models


class WebhookService:
    """Service for managing webhooks."""



    def __init__(self, weebhooks_repository: BaseRepository):
        """
        Initialize WebhookService.

        Args:
            weebhooks_repository: Base repository for webhooks.
        """
        self.repository = weebhooks_repository

        #: Mapping of function names to their corresponding handler methods.
        self.function_map = {
            "function_a": self.process_function_a,
            "function_b": self.process_function_b,
        }

    async def message_handler(self, model: models.Webhook):
        """Handle incoming webhook message.

        Args:
            model: Webhook model containing function type and data.

        Returns:
            Result of the corresponding function processing.

        Raises:
            HTTPException: If the function is not found in the mapping.
        """
        if model.function not in self.function_map:
            raise HTTPException(status_code=400, detail="Invalid function")

        return await self.function_map[model.function](model.data)

    async def process_function_a(self, data: typing.Dict[str, typing.Any]):
        """Process data for function A.

        Args:
            data: Dictionary containing webhook data.

        Returns:
            Dict[str, Any]: Response with message and data.
        """

        # Простой пример работы функции. Функция к примеру может переходить
        # в слой репозитория и выполнять логику вставки данныхх
        return {"message": "Processed by function A", "data": data}

    async def process_function_b(self, data: typing.Dict[str, typing.Any]):
        """Process data for function B.

        Args:
            data: Dictionary containing webhook data.

        Returns:
            Dict[str, Any]: Response with message and data.
        """
        return {"message": "Processed by function B", "data": data}
```