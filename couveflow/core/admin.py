from django.contrib import admin
from django.db.models import QuerySet

from couveflow.core import models


class ActionInline(admin.StackedInline):
    model = models.Action
    extra = 0


class InteractionInline(admin.TabularInline):
    LIMIT_ACTIONS_ON_DEVICE_ADMIN = 5

    model = models.Interaction
    verbose_name = f'Last {LIMIT_ACTIONS_ON_DEVICE_ADMIN} interactions'
    fields = ('type', 'created')
    readonly_fields = ('created',)

    def has_add_permission(self, *args, **kwargs) -> bool:
        return False

    def has_delete_permission(self, *args, **kwargs) -> bool:
        return False

    def has_change_permission(self, *args, **kwargs) -> bool:
        return False

    def get_queryset(self, *args, **kwargs) -> QuerySet[models.Interaction]:
        qs = super().get_queryset(*args, **kwargs).order_by('-created')
        last_ids = qs[:self.LIMIT_ACTIONS_ON_DEVICE_ADMIN].values_list('id')
        return qs.filter(id__in=last_ids)


class SensorInline(admin.TabularInline):
    model = models.Sensor
    fields = ('label', 'created')
    readonly_fields = ('created',)
    extra = 0

    def has_change_permission(self, *args, **kwargs) -> bool:
        return False


class MeasuresInline(admin.TabularInline):
    LIMIT_MEASURES_ON_DEVICE_ADMIN = 10

    model = models.Measure
    verbose_name = f'Last {LIMIT_MEASURES_ON_DEVICE_ADMIN} measures'
    fields = ('value', 'created',)
    readonly_fields = ('created',)

    def has_add_permission(self, *args, **kwargs) -> bool:
        return False

    def has_delete_permission(self, *args, **kwargs) -> bool:
        return False

    def has_change_permission(self, *args, **kwargs) -> bool:
        return False

    def get_queryset(self, *args, **kwargs) -> QuerySet[models.Interaction]:
        qs = super().get_queryset(*args, **kwargs).order_by('-created')
        last_ids = qs[:self.LIMIT_MEASURES_ON_DEVICE_ADMIN].values_list('id')
        return qs.filter(id__in=last_ids)


@admin.register(models.Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = [
        'declared_id',
        'name',
        'created',
    ]
    inlines = [
        ActionInline,
        InteractionInline,
        SensorInline,
    ]


@admin.register(models.Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = [
        'label',
        'created',
    ]

    inlines = [
        MeasuresInline,
    ]
