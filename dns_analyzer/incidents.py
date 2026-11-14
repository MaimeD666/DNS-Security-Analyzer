"""Режимы решения и объединение подозрительных окон. Ответственный: Кохан Илья.

Заготовка. Контракт: docs/contract.md. Реализация отсутствует.
"""


def combine_results(windows: list[dict], rule_results: list[dict], model_results: list[dict], mode: str) -> list[dict]:
    raise NotImplementedError("combine_results: требуется реализация по ТЗ версии 2.1")


def build_incidents(windows: list[dict], evaluations: list[dict]) -> list[dict]:
    raise NotImplementedError("build_incidents: требуется реализация по ТЗ версии 2.1")
