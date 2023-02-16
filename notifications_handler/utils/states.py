import abc
import json
from typing import Any, Optional


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path

    def save_state(self, state: dict):
        with open(self.file_path, "w") as f:
            json.dump(state, f)

    def retrieve_state(self):
        try:
            with open(self.file_path, "r") as f:
                r = json.load(f)
        except FileNotFoundError:
            r = {}
        return r


class State:
    """
    Класс для хранения состояния при работе с данными, чтобы постоянно не перечитывать данные с начала.
    Здесь представлена реализация с сохранением состояния в файл.
    В целом ничего не мешает поменять это поведение на работу с БД или распределённым хранилищем.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage.retrieve_state()
        self.file_path = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        self.storage[key] = value
        state = self.storage
        self.file_path.save_state(state=state)
        pass

    def get_state(self, key: str) -> Any:
        try:
            return self.storage.get(key)
        except KeyError:
            return None
