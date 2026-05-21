import re

def extract_json_from_model_output(text: str) -> str:
    """
    Removes markdown code fences (```json ... ```).
    Returns cleaned JSON string.
    """
    # Remove leading/trailing whitespace and code fences
    cleaned = re.sub(r"^```(?:json)?\n|\n```$", "", text.strip(), flags=re.MULTILINE)
    return cleaned.strip()
