from rest_framework import serializers

from couveflow.core.guidelines.evaluator import GuidelineEvaluator


class ActionSerializer(serializers.Serializer):
    expression = serializers.CharField()
    code = serializers.CharField()

    def validate_expression(self, value: str):
        """Check if the expression is valid using the parser"""
        evaluator = GuidelineEvaluator()
        try:
            evaluator.evaluate(value)
        except ValueError:
            raise serializers.ValidationError("Invalid expression")

        return value
