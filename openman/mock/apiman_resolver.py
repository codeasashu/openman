from connexion.mock import MockResolver
from connexion.apis.flask_api import FlaskApi

MIME_TYPES = {
    'json': 'application/json',
    'xml' : 'application/xml',
    'text': 'text/plain',
    'html': 'text/html',
}
class ApimanMockResolver(MockResolver):
    def __init__(self, mock_all):
        super().__init__(mock_all)

    def mock_operation(self, operation, *args, **kwargs):
        request = FlaskApi.get_request()
        status_code = request.query.get('__code', None)
        content_type = request.query.get('__type', None)

        resp, code = operation.example_response(status_code, content_type)
        if resp is not None:
            return resp, int(code)
        return 'No example response was defined.', int(code)
