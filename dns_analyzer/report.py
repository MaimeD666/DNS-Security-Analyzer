"""Представление и сохранение результатов. Ответственный: Миша.

Заготовка. Контракт: docs/contract.md. Реализация отсутствует.
"""


def build_report(metadata: dict, counters: dict, stats: dict, windows: list[dict], evaluations: list[dict], incidents: list[dict]) -> dict:
    raise NotImplementedError("build_report: требуется реализация по ТЗ версии 2.0")


def show_report(report: dict) -> None:
    raise NotImplementedError("show_report: требуется реализация по ТЗ версии 2.0")


def save_report(report: dict, prefix: str, overwrite: bool = False) -> None:
    raise NotImplementedError("save_report: требуется реализация по ТЗ версии 2.0")
