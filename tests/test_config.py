"""Tests del módulo de configuración."""

import pytest
from pydantic import SecretStr

from docsbot.config import Settings, get_settings


class TestSettings:
    """Tests de la clase Settings."""

    def test_defaults_load(self) -> None:
        """Los valores por defecto deben cargar sin errores."""
        settings = Settings()
        assert settings.environment == "development"
        assert settings.chunk_size == 500
        assert settings.top_k == 5

    def test_secret_is_secret_str(self) -> None:
        """openai_api_key debe ser SecretStr (no expone valor en repr)."""
        settings = Settings(openai_api_key=SecretStr("sk-test-fake"))
        assert isinstance(settings.openai_api_key, SecretStr)
        # SecretStr oculta el valor en su repr.
        assert "sk-test-fake" not in repr(settings)
        # Pero permite acceder al valor explícitamente.
        assert settings.openai_api_key.get_secret_value() == "sk-test-fake"

    def test_invalid_environment_rejected(self) -> None:
        """Un environment fuera de los valores permitidos debe fallar."""
        with pytest.raises(ValueError):
            Settings(environment="invalid")  # type: ignore[arg-type]

    def test_chunk_size_validation(self) -> None:
        """chunk_size debe respetar los rangos ge=100, le=2000."""
        with pytest.raises(ValueError):
            Settings(chunk_size=50)
        with pytest.raises(ValueError):
            Settings(chunk_size=5000)

    def test_get_settings_is_cached(self) -> None:
        """get_settings() debe retornar la misma instancia siempre."""
        s1 = get_settings()
        s2 = get_settings()
        assert s1 is s2  # mismo objeto en memoria


@pytest.mark.parametrize(
    "field_name,invalid_value",
    [
        ("chunk_overlap", -1),
        ("top_k", 0),
        ("embedding_dim", 32),
    ],
)
def test_field_validation(field_name: str, invalid_value: int) -> None:
    """Validaciones de rango en campos numéricos."""
    with pytest.raises(ValueError):
        Settings(**{field_name: invalid_value})
