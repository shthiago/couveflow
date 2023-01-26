from rest_framework import serializers


class AskActionSerializer(serializers.Serializer):
    """Using a serializer just to make it easier/obvious to expand on future features"""
    action = serializers.CharField()
