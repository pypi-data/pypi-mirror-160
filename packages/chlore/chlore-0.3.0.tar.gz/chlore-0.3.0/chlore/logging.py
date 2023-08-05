import structlog

from .request import get_request


def request_logger() -> structlog.stdlib.BoundLogger:
    """
    Retrieve the logger associated with the current request
    """
    return structlog.get_logger().bind(request_id=get_request().state.id)
