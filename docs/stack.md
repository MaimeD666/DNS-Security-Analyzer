# Стек и окружение

CPython 3.12, 64-разрядная версия. Базовая платформа — Linux x86-64. Зависимости устанавливаются в отдельное виртуальное окружение из requirements.txt; этот файл закрепляет основные и транзитивные зависимости.

| Компонент | Версия | Применение |
| --- | --- | --- |
| dpkt | 1.9.8 | Чтение и запись PCAP, разбор Ethernet II, IPv4, UDP и DNS |
| tldextract | 5.3.0 | Публичные суффиксы и базовые домены |
| NumPy | 2.3.5 | Массивы десяти числовых признаков |
| scikit-learn | 1.8.0 | StandardScaler, Pipeline, MLPClassifier, метрики |
| SciPy | 1.17.0 | Численные процедуры, используемые классификатором |
| joblib | 1.5.3 | Сериализация обученного конвейера и метаданных |
| threadpoolctl | 3.6.0 | Управление потоками численных библиотек |

dpkt применяется для офлайн-разбора готовых файлов. Вход анализатора ограничен классическим PCAP с Ethernet II, IPv4 и UDP/53. Собственный бинарный парсер и средства сетевого захвата не разрабатываются.

tldextract создаётся с suffix_list_urls=(), cache_dir=None, include_psl_private_domains=True. Используется встроенный снимок PSL, закреплённый версией библиотеки; обращения к серверам обновления отключены. Неизвестные суффиксы обрабатываются явным выделением последних двух меток, как установлено в ТЗ.

ML-конвейер: StandardScaler и MLPClassifier(hidden_layer_sizes=(16, 8), activation="relu", solver="lbfgs", max_iter=1000, random_state=42). Это небольшая полносвязная сеть по числовым признакам. Обучение, оценка и применение выполняются на CPU. Для команд, файлов, конфигурации и проверок используются argparse, pathlib, json, csv и unittest стандартной библиотеки.

## Установка

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/check_environment.py
```

check_environment.py проверяет запись и чтение временного PCAP, встроенный PSL, обучение Pipeline и совпадение оценок после загрузки. Во время проверок сетевые соединения блокируются. Искусственные числовые данные используются для проверки API библиотек.

Документация: [dpkt](https://dpkt.readthedocs.io/en/latest/), [tldextract 5.3.0](https://pypi.org/project/tldextract/5.3.0/), [scikit-learn 1.8](https://scikit-learn.org/1.8/modules/neural_networks_supervised.html).
