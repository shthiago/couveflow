from couveflow.core.models import Device, Interaction


def register_interaction(device: Device, type_: str):
    Interaction.objects.create(device=device, type=type_)
