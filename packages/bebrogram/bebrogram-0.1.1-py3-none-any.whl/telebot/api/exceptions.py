from dataclasses import dataclass


@dataclass
class Error(Exception):
    def __str__(self):
        return repr(self)


@dataclass
class RequestError(Error):
    error_code: int
    description: str
