class DjangoDocutilsException(Exception):
    pass


class DocutilsNotInstalled(DjangoDocutilsException):
    def __init__(
        self,
        message: str = "The Python docutils library isn't installed",
        *args: object,
        **kwargs: object
    ) -> None:
        return super().__init__(message, *args, **kwargs)
