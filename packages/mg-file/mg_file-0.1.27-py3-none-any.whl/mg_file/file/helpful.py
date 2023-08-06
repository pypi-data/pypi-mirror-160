import importlib.util
import re
from hashlib import sha256
from importlib.machinery import ModuleSpec
from os.path import splitext
from pathlib import Path
from types import ModuleType
from typing import Optional, Union


class BaseHash:

    @staticmethod
    def file(path_file: str):
        """
        Получить хеш сумму данных в файле, по его пути

        :param path_file: Путь к файлу
        """
        h = sha256()
        b = bytearray(128 * 1024)
        mv = memoryview(b)
        with open(path_file, 'rb', buffering=0) as f:
            for n in iter(lambda: f.readinto(mv), 0):
                h.update(mv[:n])
        return h.hexdigest()

    @staticmethod
    def text(text: str) -> str:
        """
        Получить хеш сумму текста
        """
        return sha256(text.encode()).hexdigest()

    @staticmethod
    def check_hash_sum(unknown_hash_sum: str, true_hash_sum: str):
        """
        Сравить хеш суммы

        :param unknown_hash_sum: Полученная(неизвестная) хеш сумма
        :param true_hash_sum: Требуемая хеш сумма
        """
        if unknown_hash_sum != true_hash_sum:
            raise ValueError(f"{unknown_hash_sum} != {true_hash_sum}")
        return True


def read_file_by_module(_path: str) -> ModuleType:
    """
    Импортировать файл как модуль `python`

    :param _path: Путь к `python` файлу
    :return: Модуль `python`
    """
    # Если не нужно проверять имя расширения
    if splitext(_path)[1] != ".py":  # Проверяем расширение файла
        raise ValueError(f"Файл должен иметь расширение .py")
    # указать модуль, который должен быть импортируется относительно пути модуль
    spec: Optional[ModuleSpec] = importlib.util.spec_from_file_location("my_module", _path)
    # создает новый модуль на основе спецификации
    __module: ModuleType = importlib.util.module_from_spec(spec)
    # выполняет модуль в своем собственном пространстве имен,
    # когда модуль импортируется или перезагружается.
    spec.loader.exec_module(__module)
    return __module


def concat_absolute_dir_path(_file: str, _path: str) -> str:
    """
    Получить абсолютный путь папки и объединить с другим путем

    :param _file:
    :param _path:
    :return:
    """
    return str(Path(_file).resolve().parent / _path)


def absolute_path_dir(_file: str, back: int = 1) -> Path:
    """
    Получить абсолютный путь к своей директории

    :param _file: Путь
    :param back: Сколько отступить назад
    """
    res = Path(_file).resolve()
    for _ in range(back):
        res = res.parent
    return res


def toBitSize(size: Union[str, int]) -> int:
    """
    :param size:
    можно указать:
        - kb - Например 10kb
        - mb - Например 1mb

    >>> toBitSize("10kb")
    10240
    >>> toBitSize("1mb")
    1048576
    >>> toBitSize("1gb")
    Traceback (most recent call last):
    ValueError: Не верный тип 1gb
    """
    match size:
        case int():
            return size
        case str() as _res if _r := re.match("([\d_]+)kb|KB", _res):
            return int(_r.group(1)) * 1024
        case str() as _res if _r := re.match("([\d_]+)mb|MB", _res):
            return int(_r.group(1)) * 1048576
        case _:
            raise ValueError(f"Не верный тип {size}")


class T_CryptoAes:
    """
    Источник кода

    https://github.com/denisxab/mg_crp.git
    """

    def __init__(self, key: str): ...

    def encodeAES(self): ...

    def dencodeAES(self): ...

    def __call__(self, *args, **kwargs): ...
