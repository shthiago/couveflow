from couveflow.core.models import Device, Interaction, Sensor


def register_interaction(device: Device, type_: str):
    Interaction.objects.create(device=device, type=type_)


def get_or_create_sensor(device: Device, label: str) -> Sensor:
    sensor, _ = Sensor.objects.get_or_create(device=device, label=label)
    return sensor
