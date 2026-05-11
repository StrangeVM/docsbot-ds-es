"""Configuración compartida de pytest. Aquí van los fixtures globales."""

import pytest


@pytest.fixture
def sample_text() -> str:
    """Texto de ejemplo para tests que necesiten una cadena."""
    return "Pandas es una librería de Python para manipulación de datos."
