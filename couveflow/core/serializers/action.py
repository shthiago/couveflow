from rest_framework import serializers

from couveflow.core.guidelines.evaluator import GuidelineEvaluator
from couveflow.core.models import Action


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ('expression', 'code')

    def validate_expression(self, value: str):
        """Check if the expression is valid using the parser"""
        evaluator = GuidelineEvaluator()
        try:
            evaluator.evaluate(value)
        except ValueError as exc:
            raise serializers.ValidationError('Invalid expression') from exc

        return value
