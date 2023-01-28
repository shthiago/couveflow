from django.contrib.auth.models import User
from django.db import models

from couveflow.core.constants import INTERACTION_CHOICES


class CreatedMixin(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)


class CreatedUpdatedMixin(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Device(CreatedUpdatedMixin):
    declared_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.declared_id


class Action(CreatedMixin):
    device = models.ForeignKey(
        Device, on_delete=models.PROTECT, related_name='actions')
    expression = models.TextField()
    code = models.CharField(max_length=255)

    def __str__(self):
        return f'IF ({self.expression}) THEN {self.code}'


class Measure(CreatedMixin):
    value = models.DecimalField(decimal_places=2, max_digits=100)
    device = models.ForeignKey(
        Device, on_delete=models.PROTECT, related_name='measures')
    source_label = models.TextField()


class Interaction(CreatedMixin):
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, related_name='interactions')
    type = models.CharField(
        max_length=2,
        choices=INTERACTION_CHOICES
    )


class Variable(CreatedUpdatedMixin):
    name = models.CharField(max_length=255)
    value = models.JSONField()
