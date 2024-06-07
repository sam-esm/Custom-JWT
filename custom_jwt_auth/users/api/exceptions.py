from rest_framework.views import exception_handler


def core_exception_handler(exc, context):
    """
    handles exceptions that occur in the application.
    It uses the built-in exception handler provided by Django Rest Framework,
    and extends it by adding custom error handling for specific exception types.
    """

    response = exception_handler(exc, context)
    # Define custom exception handlers
    handlers = {
       
        "ValidationError": _handle_generic_error,
    }
    # Get the type of the current exception
    exception_class = exc.__class__.__name__

    # If this exception type has a custom handler, use it; otherwise, return the default response
    if exception_class in handlers:

        return handlers[exception_class](exc, context, response)

    return response


def _handle_generic_error(exc, context, response):
    """
        handles generic errors. It modifies the response data to include the errors.
    """
    # Update the structure of the response data for generic errors
    response.data = {"errors": response.data}

    return response
