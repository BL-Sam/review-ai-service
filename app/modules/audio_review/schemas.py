from pydantic import BaseModel, HttpUrl
from typing import List, Optional


class AudioReviewRequestItem(BaseModel):
    question_text: str
    audio_file_url: str


class AudioReviewRequest(BaseModel):
    review_list: List[AudioReviewRequestItem]


class EvaluationStatus(BaseModel):
    success: bool
    error_message: Optional[str] = None


class AudioEvaluationResult(BaseModel):
    question_text: str
    transcription: str
    feedback_text: str
    improvement_suggestions: List[str]
    correctness_score: float


class AudioReviewResponse(BaseModel):
    status: EvaluationStatus
    evaluations: List[AudioEvaluationResult]