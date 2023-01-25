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
    declared_id = models.TextField()
    name = models.TextField()
    description = models.TextField()


class Action(CreatedMixin):
    device = models.ForeignKey(
        Device, on_delete=models.PROTECT, related_name='actions')
    expression = models.TextField()
    code = models.TextField()


class Measure(CreatedMixin):
    value = models.DecimalField(decimal_places=2, max_digits=100)
    device = models.ForeignKey(
        Device, on_delete=models.PROTECT, related_name='measures')
    source_label = models.TextField()


class Interaction(CreatedMixin):
    device = models.ForeignKey(
        Device, on_delete=models.PROTECT, related_name='interactions')
    type = models.CharField(
        max_length=2,
        choices=INTERACTION_CHOICES
    )


class Variable(CreatedUpdatedMixin):
    name = models.TextField()
    value = models.JSONField()
