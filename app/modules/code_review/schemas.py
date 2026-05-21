from pydantic import BaseModel, Field
from typing import List, Optional

class CodeCheckPayload(BaseModel):
    question_text:str
    answer_text:str
    instructions: Optional[str] = None

class CodeCheckEvaluation(BaseModel):
    content:List[CodeCheckPayload] = Field(..., description="Can be one or more questions")
    language:str