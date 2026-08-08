import logging
import sys
from datetime import datetime

# формат логов: время, уровень, модуль, сообщение
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
# формат времени: год-месяц-день часы:минуты:секунды,миллисекунды
DATE_FORMAT = "%Y-%m-%d %H:%M:%S,%f"[:-3]

def setup_logging(level: str = "INFO") -> None:
    """
    Настраивает логирование для всего приложения.
    :param level: уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # создаём корневой логгер
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level.upper()))

    # очищаем существующие хендлеры (чтобы не было дублей при перезагрузке)
    if logger.hasHandlers():
        logger.handlers.clear()

    # создаём хендлер для вывода в консоль (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))

    # устанавливаем формат
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    console_handler.setFormatter(formatter)

    # добавляем хендлер к корневому логгеру
    logger.addHandler(console_handler)

    # отключаем логгеры сторонних библиотек (чтобы не было шума)
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    # логируем запуск
    logger.info("Логирование настроено (уровень: %s)", level)