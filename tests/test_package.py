"""Tests básicos del paquete docsbot."""

import docsbot


class TestPackageBasics:
    """Tests que validan la salud básica del paquete."""

    def test_version_is_string(self) -> None:
        """La versión debe ser un string."""
        assert isinstance(docsbot.__version__, str)

    def test_version_format(self) -> None:
        """La versión debe seguir formato semántico X.Y.Z."""
        parts = docsbot.__version__.split(".")
        assert len(parts) == 3, f"Esperado X.Y.Z, recibido {docsbot.__version__}"
        for part in parts:
            assert part.isdigit(), f"Cada parte debe ser numérica, recibido {part}"

    def test_author_is_defined(self) -> None:
        """El autor debe estar definido."""
        assert hasattr(docsbot, "__author__")
        assert isinstance(docsbot.__author__, str)
        assert len(docsbot.__author__) > 0


def test_fixture_works(sample_text: str) -> None:
    """Verifica que los fixtures de conftest se cargan correctamente."""
    assert "Pandas" in sample_text
    assert isinstance(sample_text, str)
