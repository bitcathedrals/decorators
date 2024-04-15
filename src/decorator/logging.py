import inspect


from functools import wraps

from json import dumps

import time
from datetime import date, datetime

def _format_time(dt):
    return dt.strftime("%H:%M:%S")

def _format_date(now_object):
    return dt.strftime("%Y-%B-%d")

def _get_delta_seconds(start, end):
     delta = end - start
     return delta.total_seconds()

SERVICE = os.getenv("SERVICE")
ENVIRONMENT = os.getenv("ENVIRONMENT")

def crumb(func):
    src_function = func.__name__

    module = None
    src_module = 'unknown'

    if func.__module__:
        module = func.__module__
        src_module = module.__name__

    src_file = 'unknown'

    # the line is the second element in the tuple of func,line
    src_line = inspect.getsourcelines(func)[1]

    if module:
        src_file = inspect.getfile(module)

    @wraps(func)
    def log_crumb(*args, correlation_id="None", **kwargs):
        start_dt = datetime.now()
        iso9660 = start_dt.iso_format(),

        call_id = src_function + "-" + str(time.time_ns())

        start_data = {
            '@timestamp': iso9660,
            'log.level': "DEBUG",
            'log.logger': "crumb",
            'log.origin.file.name': src_file,
            'log.origin.file.line': src_line,
            'log.origin.function': src_function,

            'message': "call"

            'service.name': SERVICE,
            'service.environment': ENVIRONMENT,

            'gauge.correlation_id': correlation_id, 

            'gauge.arg_list': repr(args),
            'gauge.arg_keys': repr(kwargs),

            'gauge.call.id' = call_id
        }

        print(dumps(start_data, indent=4))

        if correlation_id != "None":
            kwargs[correlation_id] = correlation_id

        retval = func(*args, **kwargs)

        end_dt = datetime.now()

        end_data = {
            '@timestamp': iso9660,
            'log.level': "DEBUG",
            'log.logger': "crumb",
            'log.origin.file.name': src_file,
            'log.origin.file.line': src_line,
            'log.origin.function': src_function,

            'message': "return"

            'service.name': SERVICE,
            'service.environment': ENVIRONMENT,

            'gauge.correlation_id': correlation_id, 

            'gauge.return': repr(retval),

            'gauge.call.id' = call_id,

            'gauge.runtime': "{:.3f}".format(_get_delta_seconds(start_dt, end_dt)),
        }

        print(dumps(end_data, indent=4))

        return retval

    return log_crumb
