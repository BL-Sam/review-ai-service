class AudioReviewPromptBuilder:
    
    @staticmethod
    def build(
        question_text: str,
        transcript: str
    ) -> str:

        return f"""
            You are a senior technical interviewer evaluating a candidate's spoken response.

            Evaluate the candidate's answer using the following criteria:

            1. Technical correctness
            2. Conceptual clarity
            3. Completeness
            4. Communication effectiveness

            Technical Question:
            {question_text}

            Candidate Response Transcript:
            {transcript}

            Return ONLY valid JSON.

            Do NOT return markdown.
            Do NOT wrap in ```json.
            Do NOT add explanation before or after the JSON.

            Expected JSON format:

            {{
            "feedback_text": "string",
            "improvement_suggestions": [
                "string"
            ],
            "correctness_score": 0.0
            }}

            Rules:
            - correctness_score must be between 0.0 and 10.0
            - improvement_suggestions must always be an array
            - response must be valid parsable JSON only
            """