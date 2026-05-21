from app.core.logger import app_logger as logger
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.modules.code_review.schemas import (
    CodeCheckEvaluation
    # CodeEvaluationResponse
)
from app.modules.code_review.service import CodeReviewService
from app.core.exceptions import BaseAPIException
# from app.modules.code_review.prompts.prompt import CODE_ANALYSER_PROMPT as code_eval_prompt

code_review_router = APIRouter(
    prefix="/reviews_ai",
    tags=["Code Evaluation"]
)


service = CodeReviewService()

@code_review_router.post(
    "/code-evaluation",
    status_code = status.HTTP_200_OK
    # response_model=CodeEvaluationResponse
)
async def generate_evaluation_for_code(payload:CodeCheckEvaluation):
    try:
        
        logger.info("Running code review with code analyser agent...")
        review_results = await service.code_evaluation_with_gemini(payload.content, payload.language)
        logger.info(f"Code Analysing finished with Review results: {review_results}")
        return {
            "status": {
                "success": True,
                "error_message": None
            },
            "message": "Answer stored and review generated successfully",
            "data": review_results,
        }
    except BaseAPIException as exc:

        logger.warning(exc.message)

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": {
                    "success": False,
                    "error_message": exc.message
                },
                "message": (
                    "Code review generation failed"
                ),
                "data": None
            }
        )
        
    except Exception as e:
        logger.exception(f"Unexpected error occurred during code review --> {e} ")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": {
                    "success": False,
                    "error_message": (
                        "Unexpected error occurred"
                    )
                },
                "message": (
                    "Code review generation failed"
                ),
                "data": None
            }
        )
