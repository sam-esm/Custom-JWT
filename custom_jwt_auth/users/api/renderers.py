import json

from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    """
    UserJSONRenderer is a class that inherits from JSONRenderer.
    It overrides the render method to customize the JSON output.
    """
    charset = "utf-8"

    def render(self, data, media_type=None, renderer_context=None):

        """
        This method takes a dictionary of data and returns a JSON string.
        It checks for errors and tokens in the data. If a token is present, it decodes it.
        """
        # Checking if there are any errors in the data
        errors = data.get("errors",None)
        if errors:
            return super(UserJSONRenderer, self).render(data)

        token = data.get("token", None)
        # If a token is present and it is a byte string, decode it
        if token is not None and isinstance(token, bytes):

            data["token"] = token.decode("utf-8")

        return json.dumps({"user": data})
