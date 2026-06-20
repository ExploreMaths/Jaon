"""Common error types for the Jaon language toolchain."""


class JaonError(Exception):
    """Base class for all Jaon errors."""
    pass


class JaonRuntimeError(JaonError):
    pass


class JaonTypeError(JaonError):
    pass


class JaonNameError(JaonError):
    pass


class JaonIndexError(JaonError):
    pass


class JaonAttributeError(JaonError):
    pass


class JaonImportError(JaonError):
    pass
