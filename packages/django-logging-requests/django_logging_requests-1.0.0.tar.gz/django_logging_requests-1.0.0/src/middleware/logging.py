import traceback
import json

from django.http import HttpRequest
from django.conf import settings

from logging import getLogger


ERROR_LOGGER = getLogger('error_logger')
INFO_LOGGER = getLogger('info_logger')


class LoggingMiddleware:
    """Класс middleware который производит логирование всех запросов на endpoint и возникших ошибок."""

    def __init__(self, get_response):
        self.get_response = get_response

    def request_parse(self, http_request: HttpRequest) -> str:
        """Функция достает общую информацию из объекта запроса.

        Args:
            http_request (HttpRequest): Запрос, на основании которого будет сформировано сообщение;

        Returns:
            str: Сформированное сообщение для логов
        """

        def anonymize_token(token) -> str:
            if token is None:
                return 'Anonymous'
            return f'{token[:4]}....{token[-4:]}'

        user_agent = http_request.headers.get('User_agent', None)
        ip = http_request.META.get('HTTP_X_FORWARDED_FOR', 'None')
        user_token = http_request.headers.get('Authorization', None)

        body_info = ''
        if hasattr(http_request, 'body'):
            body_unicode = http_request.body.decode('utf-8')
            body = json.loads(body_unicode) if body_unicode else dict()
            for param_key in body:
                value = body[param_key]
                if isinstance(value, str) and len(value) > 100:
                    value = f'{value[0:99]}...'
                if param_key == 'password':
                    value = '********'
                body_info += f'\n\t\t\t{param_key}: {value}'

        if hasattr(http_request, 'GET'):
            query_params = dict(http_request.GET)
        else:
            query_params = dict()

        return (
            f'\n\tUser agent: {user_agent};'
            f'\n\tip: {ip.split(",", 1)[0]};'
            f'\n\ttoken: {anonymize_token(user_token)}'
            f'\n\tRequest: "{http_request.path}" Method: "{http_request.method}" Query params: {query_params};'
            f'\n\tBody: {body_info};'
            f'\n\tServer name: {settings.LOGGING_SERVER_NAME};'
        )

    def __call__(self, request):
        INFO_LOGGER.info(self.request_parse(request))
        response = self.get_response(request)

        return response

    def process_exception(self, request, exception):
        """Метод вызывается в случае ошибки внутри django view."""
        ERROR_LOGGER.error(f'{self.request_parse(request)}\n{traceback.format_exc().strip()};')
