# Disable abstract-method for serializers since the project does not intend to use
# update or create method for this serializer
# pylint: disable=W0223
from rest_framework import serializers


class AskActionSerializer(serializers.Serializer):
    """Using a serializer just to make it easier/obvious to expand on future features"""
    action = serializers.CharField()
