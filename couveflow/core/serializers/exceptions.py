from rest_framework import status
from rest_framework.exceptions import APIException

class DeviceRecreationAttemptException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'To re-create a device, please delete the old one'
    default_code = 'recreation_attempt'
