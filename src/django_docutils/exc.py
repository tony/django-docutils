"""Exceptions for Django Docutils."""


class DjangoDocutilsException(Exception):
    """Base exception for Django Docutils package."""

    pass


class DocutilsNotInstalled(DjangoDocutilsException):
    """Docutils is not installed."""

    def __init__(
        self,
        message: str = "The Python docutils library isn't installed",
        *args: object,
        **kwargs: object,
    ) -> None:
        return super().__init__(message, *args, **kwargs)
