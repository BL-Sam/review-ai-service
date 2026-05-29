import json
from loguru import logger
from google.api_core import exceptions as google_exceptions
from pydantic_ai.exceptions import ModelHTTPError
from app.modules.utils.agent_ouput import extract_json_from_model_output
# from app.modules.audio_review.schemas import AudioEvaluationResult
from app.modules.audio_review.agent.builder import AudioReviewAgentBuilder
from app.modules.audio_review.agent.prompts import SYSTEM_PROMPT
from .schemas import AudioEvaluationResult
# from .downloader.object_storage_downloader import download_audio_from_url
from .downloader.audio_loader import get_audio_bytes
from .transcribers.audio_processor import process_audio
from .agent.audio_review_prompt_builder import AudioReviewPromptBuilder
from app.core.exceptions.custom_exceptions import (
    GeminiAPIException,
    InvalidResponseException,
    GeminiAPIResourceExhausted
)
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)


class AudioReviewService:

    async def evaluate_audio_reviews(
        self,
        review_list: list
    ) -> list[AudioEvaluationResult]:

        evaluations = []

        for review in review_list:

            logger.info(f"Processing audio review for question: {review.question_text}")

            audio_bytes = get_audio_bytes(review.audio_file_url)

            transcript = process_audio(audio_bytes)

            try:
                agent = (AudioReviewAgentBuilder.build(system_prompt = SYSTEM_PROMPT))
                logger.info("Gemini audio evaluation agent initialized")
                user_prompt = AudioReviewPromptBuilder.build(
                    question_text=review.question_text,
                    transcript=transcript
                )
                logger.info(f" user_prompt --> {user_prompt}")
                result = await self._run_agent_with_retry(agent, user_prompt)
                logger.info(f" result --> {result}")
                # parsed_output = json.loads(result.output)
                # parsed_output = self._parse_response(result.output)
                # logger.info(f" parsed_output --> {parsed_output}")

            except ModelHTTPError as exc:
                logger.exception("Gemini model unavailable")
                raise GeminiAPIException("AI Service Timeout. Please retry request.") from exc
            except google_exceptions.ResourceExhausted:
                logger.exception("Api Key exhausted")
                raise GeminiAPIResourceExhausted("Api Key exhausted")
            except google_exceptions.GoogleAPICallError:
                logger.exception("Gemini API error during audio evaluation")
                raise GeminiAPIException("Gemini API error during audio evaluation")

            except Exception:
                logger.exception("Unexpected error during audio evaluation")
                raise ValueError("Unexpected error during audio evaluation")
            

            # evaluations.append(
            #     AudioEvaluationResult(
            #         question_text=review.question_text,
            #         transcription=transcript,
            #         feedback_text=parsed_output["feedback_text"],
            #         improvement_suggestions=parsed_output["improvement_suggestions"],
            #         correctness_score=parsed_output["correctness_score"]
            #     )
            # )
            evaluation = result.output
            evaluations.append(
                AudioEvaluationResult(
                    question_text=review.question_text,
                    transcription=transcript,
                    feedback_text=evaluation.feedback_text,
                    improvement_suggestions=evaluation.improvement_suggestions,
                    correctness_score=evaluation.correctness_score
                )
            )

        return evaluations
    
    @staticmethod
    def _parse_response(output: str) -> dict:

        text_output = (extract_json_from_model_output(output))

        try:

            return json.loads(text_output)

        except json.JSONDecodeError as exc:
            logger.error("Gemini returned invalid JSON response")
            raise InvalidResponseException("Invalid JSON returned from Gemini") from exc
    
    @staticmethod
    @retry(
        retry=retry_if_exception_type(
            (
                google_exceptions.ResourceExhausted,
                google_exceptions.ServiceUnavailable,
                google_exceptions.DeadlineExceeded,
                ModelHTTPError
            )
        ),
        wait=wait_exponential(
            multiplier=1,
            min=2,
            max=10
        ),
        stop=stop_after_attempt(5),
        reraise=True
    )
    async def _run_agent_with_retry(agent, user_prompt):

        logger.warning("Executing Gemini request with retry")

        return await agent.run(user_prompt)
            
