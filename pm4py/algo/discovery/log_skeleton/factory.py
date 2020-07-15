import deprecation

from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.log_skeleton.versions import classic

CLASSIC = "classic"

DEFAULT_VARIANT = CLASSIC

VERSIONS = {CLASSIC: classic.apply}

@deprecation.deprecated(deprecated_in='1.3.0', removed_in='2.0.0', current_version='',
                        details='Use algorithm entrypoint instead')
def apply(log, variant=DEFAULT_VARIANT, parameters=None):
    """
    Discover a log skeleton from an event log

    Parameters
    -------------
    log
        Event log
    variant
        Variant of the algorithm, possible values: classic
    parameters
        Parameters of the algorithm, including:
            - the activity key (pm4py:param:activity_key)
            - the noise threshold (noise_threshold)

    Returns
    -------------
    model
        Log skeleton model
    """
    return VERSIONS[variant](log_converter.apply(log, parameters=parameters), parameters=parameters)
