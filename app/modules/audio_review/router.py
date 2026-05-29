from fastapi import APIRouter, Depends

from app.core.security import auth_handler

from .schemas import (
    AudioReviewRequest,
    AudioReviewResponse,
    EvaluationStatus
)

from .service import AudioReviewService


audio_review_router = APIRouter(
    prefix="/reviews_ai",
    tags=["Audio Review"]
)

audio_review_service = AudioReviewService()


@audio_review_router.post(
    "/audio-review",
    response_model=AudioReviewResponse
)
async def audio_review(
    payload: AudioReviewRequest,
    _: str = Depends(
        auth_handler.verify_api_token
    )
):

    evaluations = await audio_review_service.evaluate_audio_reviews(payload.review_list)

    return AudioReviewResponse(
        status=EvaluationStatus(
            success=True,
            error_message=None
        ),
        evaluations=evaluations
    )