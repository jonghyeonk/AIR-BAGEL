from copy import deepcopy

import pandas

import pm4py
from pm4py import util as pmutil
from pm4py.objects.conversion.log import constants
from pm4py.objects.log import log as log_instance
from pm4py.util import xes_constants as xes
from pm4py.objects.conversion.log.variants import to_event_stream
from copy import copy
from enum import Enum
import deprecation

class Parameters(Enum):
    DEEP_COPY = False


# this parameter is deprecated should be removed...
DEEPCOPY = constants.DEEPCOPY

@deprecation.deprecated(deprecated_in='1.3.0', removed_in='2.0.0', current_version='',
                        details='conversion versions are deprecated; use conversion variants instead')
def apply(log, parameters=None):
    if parameters is None:
        parameters = {}
    if DEEPCOPY in parameters:
        parameters[Parameters.DEEP_COPY] = parameters[DEEPCOPY]
    if isinstance(log, pandas.core.frame.DataFrame):
        log = to_event_stream.apply(log, parameters=parameters)
    if isinstance(log, pm4py.objects.log.log.EventStream) and (not isinstance(log, pm4py.objects.log.log.EventLog)):
        parameters = parameters if parameters is not None else dict()
        if pmutil.constants.PARAMETER_CONSTANT_CASEID_KEY in parameters:
            glue = parameters[pmutil.constants.PARAMETER_CONSTANT_CASEID_KEY]
        else:
            glue = pmutil.constants.CASE_ATTRIBUTE_GLUE
        if pmutil.constants.PARAMETER_KEY_CASE_ATTRIBUTE_PRFIX in parameters:
            case_pref = parameters[pmutil.constants.PARAMETER_KEY_CASE_ATTRIBUTE_PRFIX]
        else:
            case_pref = pmutil.constants.CASE_ATTRIBUTE_PREFIX
        enable_deepcopy = parameters[DEEPCOPY] if DEEPCOPY in parameters else False

        return transform_event_stream_to_event_log(log, case_glue=glue, include_case_attributes=True,
                                                   case_attribute_prefix=case_pref, enable_deepcopy=enable_deepcopy)
    return log


def transform_event_stream_to_event_log(log, case_glue=pmutil.constants.CASE_ATTRIBUTE_GLUE,
                                        include_case_attributes=True,
                                        case_attribute_prefix=pmutil.constants.CASE_ATTRIBUTE_PREFIX,
                                        enable_deepcopy=False):
    """
    Converts the event stream to an event log

    Parameters
    ----------
    log: :class:`pm4py.log.log.EventLog`
        An event stream
    case_glue:
        Case identifier. Default is 'case:concept:name'
    include_case_attributes:
        Default is True
    case_attribute_prefix:
        Default is 'case:'
    enable_deepcopy
        Enables deepcopy (avoid references between input and output objects)

    Returns
        -------
    log : :class:`pm4py.log.log.EventLog`
        An event log
    """
    if enable_deepcopy:
        log = deepcopy(log)

    traces = {}
    for orig_event in log:
        event = copy(orig_event)
        glue = event[case_glue]
        if glue not in traces:
            trace_attr = {}
            if include_case_attributes:
                for k in event.keys():
                    if k.startswith(case_attribute_prefix):
                        trace_attr[k.replace(case_attribute_prefix, '')] = event[k]
                if xes.DEFAULT_TRACEID_KEY not in trace_attr:
                    trace_attr[xes.DEFAULT_TRACEID_KEY] = glue
            traces[glue] = log_instance.Trace(attributes=trace_attr)

        if include_case_attributes:
            for k in list(event.keys()):
                if k.startswith(case_attribute_prefix):
                    del event[k]

        traces[glue].append(event)
    return log_instance.EventLog(traces.values(), attributes=log.attributes, classifiers=log.classifiers,
                                 omni_present=log.omni_present, extensions=log.extensions)
