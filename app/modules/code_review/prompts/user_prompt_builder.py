class UserPromptBuilder:
    
    @staticmethod
    def build(
        language: str,
        ques_ans_content_with_inst: str
    ) -> str:

        return f"""
            The submitted programming language is:

            {language}

            Below are the question-answer pairs submitted by the user.

            Each item may optionally contain SPECIFIC INSTRUCTIONS.
            These instructions represent additional constraints,
            expected approaches, edge cases, evaluation criteria,
            or implementation requirements for that particular question.

            While evaluating each answer:
            - Carefully follow the SPECIFIC INSTRUCTIONS if present
            - Evaluate whether the submitted answer satisfies them
            - Include violations or missed requirements in the feedback

            Submitted Question–Answer Data:

            {ques_ans_content_with_inst}

            Tasks:

            ------------------------------------------------------------
            1. REVIEW EACH QUESTION–ANSWER INDIVIDUALLY
            ------------------------------------------------------------

            For each item:

            - Analyze correctness
            - Identify bugs
            - Evaluate readability
            - Evaluate efficiency
            - Validate adherence to SPECIFIC INSTRUCTIONS (if present)
            - Suggest improvements
            - Provide corrected optimized code

            Scoring (ALL SCORES MUST BE OUT OF 10):
            - correctness_score
            - code_quality_score
            - efficiency_score
            - overall_score

            overall_score formula:
            (0.5 * correctness_score)
            + (0.3 * code_quality_score)
            + (0.2 * efficiency_score)

            ------------------------------------------------------------
            2. SUMMARY REVIEW
            ------------------------------------------------------------

            Provide:

            - overall_average_score (OUT OF 10)
            - overall_quality_label
            - common mistakes
            - strengths
            - weaknesses
            - recommendations

            overall_quality_label mapping:
            - 9–10 → Excellent
            - 7.5–8.9 → Good
            - 6–7.4 → Average
            - 4–5.9 → Poor
            - below 4 → Critical

            ------------------------------------------------------------
            3. OUTPUT FORMAT
            ------------------------------------------------------------

            Return this exact JSON schema:

            {{
                "individual_reviews": [
                    {{
                        "question_text": "",
                        "correctness_feedback": "",
                        "improvement_suggestions": "",
                        "corrected_code": "",
                        "scores": {{
                            "correctness_score": 0,
                            "code_quality_score": 0,
                            "efficiency_score": 0,
                            "overall_score": 0
                        }}
                    }}
                ],
                "summary_review": {{
                    "overall_average_score": 0,
                    "overall_quality_label": "",
                    "common_errors": "",
                    "strengths": "",
                    "weaknesses": "",
                    "recommendations": ""
                }}
            }}

            Rules:
            - All scores must be between 0 and 10
            - Output ONLY valid JSON
            - Do not include markdown
            - Do not include explanations outside JSON
            - Base analysis strictly on the submitted code
            """