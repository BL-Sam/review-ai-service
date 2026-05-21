from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import (
    GoogleGLAProvider
)

from app.core.config import settings


class GeminiClient:

    _provider = GoogleGLAProvider(
        api_key=settings.GEMINI_API_KEY
    )

    _model = GeminiModel(
        settings.GEMINI_MODEL,
        provider=_provider
    )

    @classmethod
    def get_model(cls) -> GeminiModel:

        return cls._model
