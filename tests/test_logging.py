"""Tests para el módulo de logging."""

from pathlib import Path

import pytest

from docsbot.logging import logger, setup_logging


class TestSetupLogging:
    """Tests de la función setup_logging."""

    def test_setup_logging_default(self) -> None:
        """setup_logging() sin args no debe fallar."""
        setup_logging()
        logger.info("test message")

    def test_setup_logging_with_file(self, tmp_path: Path) -> None:
        """setup_logging con archivo debe crear el archivo y escribir en él."""
        log_file = tmp_path / "test.log"
        setup_logging(level="DEBUG", log_file=log_file, enable_console=False)

        logger.info("mensaje de prueba")
        logger.debug("mensaje debug")

        # Forzamos flush cerrando los handlers.
        logger.remove()

        assert log_file.exists()
        content = log_file.read_text(encoding="utf-8")
        assert "mensaje de prueba" in content
        assert "mensaje debug" in content

    @pytest.mark.parametrize("level", ["DEBUG", "INFO", "WARNING", "ERROR"])
    def test_setup_logging_levels(self, level: str) -> None:
        """setup_logging debe aceptar todos los niveles estándar."""
        setup_logging(level=level, enable_console=False)
