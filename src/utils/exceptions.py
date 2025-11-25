class NotFoundError(Exception):
    """Raised when an item is not found in the database."""
    pass

class AlreadyExistsError(Exception):
    """Raised when trying to add an item that already exists."""
    pass

class InvalidInputError(Exception):
    """Raised when input data is invalid."""
    pass


import logging
logger = logging.getLogger(__name__)
    