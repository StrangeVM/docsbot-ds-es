"""Configuración centralizada de logging para docsbot.

Usamos loguru en lugar de la librería estándar `logging` por tres razones:

1. Sintaxis más simple: un solo objeto `logger` global, sin handlers manuales.
2. Salida formateada con colores por defecto en consola.
3. Configuración por código (no por dict ni YAML como el `logging` estándar).

Uso típico:

    >>> from docsbot.logging import logger
    >>> logger.info("Procesando {n} documentos", n=42)
    >>> logger.error("Falló la conexión: {err}", err=str(e))

NUNCA usar `print()` en código de producción. Para outputs temporales de
debug, usar `logger.debug(...)` que se puede silenciar en producción.
"""

from __future__ import annotations

import sys
from pathlib import Path

from loguru import logger

# Re-exportamos `logger` para que los módulos hagan `from docsbot.logging import logger`.
__all__ = ["logger", "setup_logging"]


def setup_logging(
    *,
    level: str = "INFO",
    log_file: Path | None = None,
    enable_console: bool = True,
) -> None:
    """Configura el logger global de docsbot.

    Args:
        level: Nivel mínimo de logs a mostrar. Uno de DEBUG/INFO/WARNING/ERROR/CRITICAL.
        log_file: Si se proporciona, los logs también se guardan en este archivo
            con rotación automática.
        enable_console: Si False, no muestra logs en consola (útil para tests).
    """
    # Limpiamos los handlers por defecto de loguru.
    logger.remove()

    # Formato custom para consola: timestamp | nivel | módulo | mensaje.
    console_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    if enable_console:
        logger.add(
            sys.stderr,
            format=console_format,
            level=level,
            colorize=True,
            backtrace=True,  # stacktrace completo en excepciones
            diagnose=True,  # muestra variables locales en stacktraces (solo dev!)
        )

    if log_file is not None:
        # En archivo: sin colores, con rotación cuando llega a 10 MB.
        log_file.parent.mkdir(parents=True, exist_ok=True)
        logger.add(
            log_file,
            format=(
                "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}"
            ),
            level=level,
            rotation="10 MB",
            retention="30 days",
            compression="gz",
            backtrace=True,
            diagnose=False,  # en archivos no exponemos variables locales
        )

    logger.info("Logging configurado | level={} | log_file={}", level, log_file)
