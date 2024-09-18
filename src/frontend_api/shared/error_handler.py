from functools import wraps
from flask import jsonify, request
from pydantic import ValidationError


def error_handler(schema=None):
    """
    Decorator to handle Pydantic validation errors and other exceptions.
    :param schema: Optional Pydantic schema class to validate the request data.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Validate request data using Pydantic schema if provided
                if schema:
                    request_data = schema(**request.json)
                    return func(request_data, *args, **kwargs)
                else:
                    return func(*args, **kwargs)
            except ValidationError as e:
                # Handle Pydantic validation errors
                return (
                    jsonify(
                        {"error": "Invalid data format", "details": e.errors()}
                    ),
                    400,
                )
            except Exception as e:
                # Handle other exceptions
                return (
                    jsonify(
                        {
                            "error": "An unexpected error occurred",
                            "details": str(e),
                        }
                    ),
                    500,
                )

        return wrapper

    return decorator
