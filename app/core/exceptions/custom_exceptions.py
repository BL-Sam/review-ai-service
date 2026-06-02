class BaseAPIException(Exception):

    def __init__(
        self,
        message: str,
        status_code: int = 500
    ):

        self.message = message
        self.status_code = status_code

        super().__init__(message)

class FileNotInBucket(BaseAPIException):
    def __init__(
        self,
        message: str = "File not found in bucket"
    ):
        super().__init__(message = message, status_code = 404)

class AudioDownloadException(BaseAPIException):
    def __init__(
        self,
        message: str = "Failed to access audio file"
    ):
        super().__init__(message = message, status_code = 400)

class InvalidTokenException(BaseAPIException):
    
    def __init__(
        self,
        message: str = "Invalid Token",
        status_code: int = 401
    ):

        super().__init__(message, status_code)

class CodeReviewException(BaseAPIException):

    def __init__(
        self,
        message: str = "Code review failed",
        status_code: int = 400
    ):

        super().__init__(message, status_code)


class GeminiAPIException(CodeReviewException):

    def __init__(
        self,
        message: str = "Gemini API error occurred",
        status_code: int = 503
    ):

        super().__init__(message, status_code)

class GeminiAPIResourceExhausted(CodeReviewException):
    
    def __init__(
        self,
        message: str = "Gemini API error occurred",
        status_code: int = 503
    ):

        super().__init__(message, status_code)


class InvalidResponseException(CodeReviewException):

    def __init__(
        self,
        message: str = "Invalid response returned by model",
        status_code: int = 422
    ):

        super().__init__(message, status_code)


class PromptGenerationException(CodeReviewException):

    def __init__(
        self,
        message: str = "Failed to generate prompt",
        status_code: int = 500
    ):

        super().__init__(message, status_code)



class ValidationException(BaseAPIException):

    def __init__(
        self,
        message: str = "Validation failed",
        status_code: int = 400
    ):

        super().__init__(message, status_code)


class ResourceNotFoundException(BaseAPIException):

    def __init__(
        self,
        message: str = "Requested resource not found",
        status_code: int = 404
    ):

        super().__init__(message, status_code)



class AuthenticationException(BaseAPIException):

    def __init__(
        self,
        message: str = "Authentication failed",
        status_code: int = 401
    ):

        super().__init__(message, status_code)


class AuthorizationException(BaseAPIException):

    def __init__(
        self,
        message: str = "Access denied",
        status_code: int = 403
    ):

        super().__init__(message, status_code)


class RateLimitException(BaseAPIException):

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        status_code: int = 429
    ):

        super().__init__(message, status_code)