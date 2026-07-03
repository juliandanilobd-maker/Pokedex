"""
Configuración centralizada del sistema de logging.
Se importa una vez al arrancar la app (en main.py) y todos los módulos
obtienen su logger con logging.getLogger(__name__).
"""

import logging
import sys
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parents[2] / "logs"
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(level: str = "INFO") -> None:
    """Configura el sistema de logging global de la aplicación.

    Args:
        level: nivel mínimo de log (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Formateador compartido por todos los handlers
    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

    # Handler 1: consola (stdout) — útil en desarrollo y en CLI
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)

    # Handler 2: fichero rotativo — no crece indefinidamente
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler(
        LOG_DIR / "pokedex.log",
        maxBytes=5 * 1024 * 1024,  # 5 MB por fichero
        backupCount=3,  # máximo 3 ficheros de backup
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # Configuramos el logger raíz de la app (solo el namespace "backend")
    # para no capturar logs internos de httpx, uvicorn, etc. salvo WARNING+
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Silenciamos librerías ruidosas en nivel INFO
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
