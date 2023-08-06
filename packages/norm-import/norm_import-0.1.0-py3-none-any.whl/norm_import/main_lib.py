import importlib.util
from importlib.machinery import ModuleSpec
from os import sep
from os.path import splitext, join
from pathlib import Path, PosixPath
from types import ModuleType
from typing import Optional, Union


class ObjFrom:
    def __init__(self, module: ModuleType):
        self.module: ModuleType = module

    def From(self, *obj):
        """
        Выбрать определяя объекты из модуля

        :param obj:
        :return:
        """
        return tuple(v for k, v in self.module.__dict__.items() if k in obj)


def iimport(self_file: str = None,
            count_up: int = 0,
            module_name: str = None,
            *,
            absolute_path: Union[str, Path] = None) -> ObjFrom:
    """
    Импортировать файл как модуль `python`

    :param self_file: Обычно это __file__
    :param count_up: Насколько папок поднять вверх
    :param module_name: Имя импортируемого модуля
    :param absolute_path: Путь к `python` файлу
    :return: Модуль `python`
    """
    path: str = ''
    if absolute_path is not None:
        if isinstance(absolute_path, PosixPath):
            absolute_path = absolute_path.__str__()
        path = absolute_path
    else:
        path = join(sep.join(Path(self_file).parts[:(count_up + 1) * -1]), f"{module_name}.py")
    if splitext(path)[1] != ".py":
        raise ValueError(f"Файл должен иметь расширение .py")
    spec: Optional[ModuleSpec] = importlib.util.spec_from_file_location("my_module", path)
    __module: ModuleType = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(__module)
    return ObjFrom(__module)