from pydantic import BaseModel, Field
from typing import List, Optional


class CodeCheckPayload(BaseModel):
    question_text:str
    answer_text:str
    instructions: Optional[str] = None

class CodeCheckEvaluation(BaseModel):
    content:List[CodeCheckPayload] = Field(..., description="Can be one or more questions")
    language:str


# Status Response
class StatusResponse(BaseModel):

    success: bool
    error_message: Optional[str] = None

# Score Response
class ReviewScores(BaseModel):

    correctness_score: float
    code_quality_score: float
    efficiency_score: float
    overall_score: float


# Individual Review
class IndividualReview(BaseModel):

    question_text: str

    correctness_feedback: str
    improvement_suggestions: str
    corrected_code: str

    scores: ReviewScores



# Summary Review
class SummaryReview(BaseModel):

    overall_average_score: float
    overall_quality_label: str

    common_errors: str
    strengths: str
    weaknesses: str
    recommendations: str

# Evaluation Data
class EvaluationData(BaseModel):

    individual_reviews: List[IndividualReview]

    summary_review: SummaryReview



# Success Response
class CodeEvaluationSuccessResponse(BaseModel):

    status: StatusResponse

    message: str

    data: EvaluationData


# Failure Response
class CodeEvaluationFailureResponse(BaseModel):

    status: StatusResponse

    evaluations: List = []