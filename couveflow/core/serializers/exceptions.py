from rest_framework import status
from rest_framework.exceptions import APIException


class DeviceRecreationAttempt(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'To re-create a device, please delete the old one'
    default_code = 'recreation_attempt'


class DeviceNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Ensure you have created the device before sending measures'
    default_code = 'device_not_found'
