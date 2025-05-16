from fastapi import status

from src.core.exceptions import BaseHTTPException


class UserEmailAlreadyExistException(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User with this email already exists."


class UserUsernameAlreadyExistException(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User with this username already exists."


class IncorrectUsernameOrPasswordException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect username or password."


class CredentialsException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Could not validate credentials"
    headers = {"WWW-Authenticate": "Bearer"}


class TokenExpiredException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token expired."


class RefreshTokenNotFound(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Refresh token not found."


class UserNotFoundFromRefreshToken(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "User not found from refresh token."