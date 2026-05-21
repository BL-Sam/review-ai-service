import json
from google.api_core import exceptions as google_exceptions
from app.core.logger import app_logger as logger
from app.modules.utils.agent_ouput import (
    extract_json_from_model_output
)
from app.modules.code_review.agent.builder import (
    CodeReviewAgentBuilder
)
from app.modules.code_review.prompts.prompt import SYSTEM_PROMPT
from app.modules.code_review.prompts.user_prompt_builder import UserPromptBuilder
from app.core.exceptions import (
    GeminiAPIException,
    InvalidResponseException,
    PromptGenerationException,
    GeminiAPIResourceExhausted
)
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

class CodeReviewService:

    async def code_evaluation_with_gemini(
        self,
        content: list,
        language: str,
    ) -> dict:

        logger.info(f"Starting code evaluation for language: {language}")

        try:

            formatted_qa_with_ins = self._build_qa_block(content)

            user_prompt = UserPromptBuilder.build(
                language=language,
                ques_ans_content_with_inst=formatted_qa_with_ins
            )
        except Exception as exc:

            logger.exception("Prompt generation failed")
            raise PromptGenerationException("Failed to generate review prompt") from exc

        try:
            agent = (
                CodeReviewAgentBuilder
                .build(system_prompt = SYSTEM_PROMPT)
            )

            logger.info("Gemini code evaluation agent initialized")

            # response = await agent.run(user_prompt)
            response = await self._run_agent_with_retry(
                agent=agent,
                user_prompt=user_prompt
            )

            logger.info("Code evaluation completed")

            parsed_response = self._parse_response(response.output)

            return parsed_response

        except google_exceptions.ResourceExhausted:
            logger.exception("Api Key exhausted")
            raise GeminiAPIResourceExhausted("Api Key exhausted")
        except google_exceptions.GoogleAPICallError:
            logger.exception("Gemini API error during code evaluation")
            raise GeminiAPIException("Gemini API error during code evaluation")

        except Exception:
            logger.exception("Unexpected error during code evaluation")
            raise ValueError("Unexpected error during code evaluation")


    @staticmethod
    def _build_qa_block(content_list: list) -> str:

        formatted_block = ""

        for item in content_list:

            instruction_block = ""

            if (
                hasattr(item, "instructions")
                and item.instructions
                and item.instructions.strip()
            ):

                instruction_block = f"""
                    SPECIFIC INSTRUCTIONS:
                    {item.instructions}
                    """

            formatted_block += f"""
                QUESTION:
                {item.question_text}

                ANSWER:
                {item.answer_text}
                
                {instruction_block}

                --- END ITEM ---
                """

        return formatted_block

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
                google_exceptions.DeadlineExceeded
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
            

