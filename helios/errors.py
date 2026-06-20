"""Common error types for the Helios language toolchain."""


class HeliosError(Exception):
    """Base class for all Helios errors."""
    pass


class HeliosRuntimeError(HeliosError):
    pass


class HeliosTypeError(HeliosError):
    pass


class HeliosNameError(HeliosError):
    pass


class HeliosIndexError(HeliosError):
    pass


class HeliosAttributeError(HeliosError):
    pass


class HeliosImportError(HeliosError):
    pass
