"""Командная строка DNS Security Analyzer. Ответственный: Кирилл.

Предмет анализа и целевое поведение описаны в docs/technical_specification.md.
Сейчас доступна справка; путь анализа намеренно не реализован.
"""

import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="DNS Security Analyzer: выявление признаков DNS-туннелирования",
        epilog="Состояние: подготовлено ТЗ; анализ и обучение ещё не реализованы.",
    )
    parser.add_argument("pcap", type=Path, help="исходный файл PCAP")
    parser.add_argument("--config", type=Path, default=Path("config.json"))
    parser.add_argument("--mode", choices=("rules", "model", "hybrid"), default="rules")
    parser.add_argument("--model", type=Path, help="файл модели для model и hybrid")
    parser.add_argument("--output", type=Path, default=Path("reports/analysis"), help="префикс TXT и JSON")
    parser.add_argument("--overwrite", action="store_true", help="разрешить замену отчётов")
    parser.parse_args()
    print("Анализ ещё не реализован. Требования: docs/technical_specification.md", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
