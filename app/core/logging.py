import json
import logging
from datetime import datetime
from typing import Any, Dict


class JsonFormatter(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:

        base: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }

        if hasattr(record, "extra") and isinstance(record.extra, dict):
            base.update(record.extra)

        return json.dumps(base, ensure_ascii=False)


def get_logger(name: str = "app") -> logging.Logger:

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    logger.addHandler(handler)
    logger.propagate = False

    return logger
