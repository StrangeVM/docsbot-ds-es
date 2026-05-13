"""Configuración centralizada del proyecto usando pydantic-settings.

La configuración se carga en este orden de precedencia (mayor a menor):

1. Argumentos pasados explícitamente al instanciar Settings.
2. Variables de entorno del sistema.
3. Archivo .env en la raíz del proyecto.
4. Valores por defecto definidos abajo.

Uso típico:

    >>> from docsbot.config import get_settings
    >>> settings = get_settings()
    >>> print(settings.openai_api_key)
    >>> print(settings.chunk_size)

NUNCA hardcodear secretos en el código. SIEMPRE cargarlos vía `.env` o variables
de entorno. El archivo `.env` está en `.gitignore` y NUNCA debe commitearse.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# Directorio raíz del proyecto (3 niveles arriba de este archivo).
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Configuración global de la aplicación."""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,  # OPENAI_API_KEY == openai_api_key
        extra="ignore",  # ignora variables de entorno no definidas aquí
    )

    # ========== Entorno ==========
    environment: Literal["development", "production", "test"] = Field(
        default="development",
        description="Entorno de ejecución. Cambia comportamientos como logging y caching.",
    )

    debug: bool = Field(
        default=False,
        description="Modo debug. Activa logs verbosos.",
    )

    # ========== Paths ==========
    data_dir: Path = Field(
        default=PROJECT_ROOT / "data",
        description="Directorio donde se almacenan datos crudos y procesados.",
    )

    # ========== LLM ==========
    openai_api_key: SecretStr = Field(
        default=SecretStr(""),
        description="API key de OpenAI. Se carga de la variable de entorno OPENAI_API_KEY.",
    )

    openai_model: str = Field(
        default="gpt-4o-mini",
        description="Modelo de OpenAI a usar para generación.",
    )

    # ========== Embeddings ==========
    embedding_model: str = Field(
        default="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        description="Modelo de embeddings. Default multilingüe con buen soporte de español.",
    )

    embedding_dim: int = Field(
        default=384,
        ge=64,
        le=4096,
        description="Dimensión de los embeddings. Debe coincidir con el modelo.",
    )

    # ========== Chunking ==========
    chunk_size: int = Field(
        default=500,
        ge=100,
        le=2000,
        description="Tamaño máximo de cada chunk en tokens.",
    )

    chunk_overlap: int = Field(
        default=50,
        ge=0,
        le=500,
        description="Tokens de solapamiento entre chunks consecutivos.",
    )

    # ========== Retrieval ==========
    top_k: int = Field(
        default=5,
        ge=1,
        le=50,
        description="Número de chunks a recuperar por query.",
    )

    # ========== Vector store ==========
    vector_store_path: Path = Field(
        default=PROJECT_ROOT / "data" / "chroma_db",
        description="Path donde ChromaDB persiste sus datos.",
    )

    # ========== Logging ==========
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Nivel mínimo de logs a registrar.",
    )

    log_file: Path | None = Field(
        default=None,
        description="Si se especifica, los logs se guardan también en este archivo.",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Retorna la instancia global de Settings (cached).

    Usar esta función en lugar de instanciar Settings directamente.
    El cache asegura que solo se lee `.env` una vez en toda la app.
    """
    return Settings()
