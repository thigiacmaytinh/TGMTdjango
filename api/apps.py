from django.apps import AppConfig
from rest_framework.response import Response
import json

ERROR_CODE = 399
SUCCESS_CODE = 200

####################################################################################################

class ApiConfig(AppConfig):
    name = 'api'

####################################################################################################

class ErrorResponse(Response):
    def __init__(self, message):
        Response.__init__(self,
            {'Error': message},
            status=ERROR_CODE, content_type="application/json")

####################################################################################################

class SuccessResponse(Response):
    def __init__(self, message):
        Response.__init__(self,
            {'Success': message},
            status=SUCCESS_CODE, content_type="application/json")

####################################################################################################

class JsonResponse(Response):
    def __init__(self, jsonString):
        Response.__init__(self,
            json.loads(jsonString),
            status=SUCCESS_CODE, content_type="application/json")