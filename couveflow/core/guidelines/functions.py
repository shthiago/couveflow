"""Functions for guidelines"""
from datetime import datetime
from typing import Callable, Dict, Optional

from couveflow.core.models import Interaction, Measure

GUIDELINES_GLOBAL_VAR = '__GUIDELINE_FUNCTIONS'


def get_functions() -> Dict[str, Callable]:
    return globals().get(GUIDELINES_GLOBAL_VAR, {})


def guideline_function(func):
    '''Wrapper to set guideline valid functions'''
    funcs = globals().get(GUIDELINES_GLOBAL_VAR, {})
    funcs[func.__name__] = func
    globals()[GUIDELINES_GLOBAL_VAR] = funcs

    return func


@guideline_function
def last_interaction_timestamp(declared_id: str) -> Optional[datetime]:
    last_interaction = Interaction.objects.filter(
        device__declared_id=declared_id).last()

    if last_interaction is not None:
        return last_interaction.created

    return None


@guideline_function
def last_measure_for(declared_id: str, source_label: str) -> Optional[float]:
    measure = Measure.objects.filter(
        device__declared_id=declared_id, source_label=source_label).last()

    if measure is not None:
        return measure.value

    return None


@guideline_function
def now() -> datetime:
    return datetime.now()


FUNCTIONS = get_functions()
