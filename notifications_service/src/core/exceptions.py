from dataclasses import dataclass


class ApiException(Exception):
    pass


@dataclass
class BadRequestException(ApiException):
    message: str = "Invalid request data"
    extra_information: str = "None"
    code: str = "B001"
