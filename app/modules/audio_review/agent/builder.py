from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings
from app.modules.audio_review.schemas import AudioEvaluationResult
from app.core.config import settings
from app.integrations.llms.gemini_client import (
    GeminiClient
)


class AudioReviewAgentBuilder:

    @staticmethod
    def build(system_prompt: str) -> Agent:

        return Agent(
            model=GeminiClient.get_model(),
            system_prompt=system_prompt,
            model_settings=ModelSettings(
                temperature=settings.GEMINI_TEMPERATURE
            ),
            output_type = AudioEvaluationResult
        )