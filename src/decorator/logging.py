from functools import wraps

from json import dumps

import time
from datetime import date, datetime

def _get_formatted_time(time):
    return time.strftime("%H:%M:%S")

def _get_delta_seconds(start, end):
     delta = end - start
     return delta.total_seconds()

def crumb(func):

    @wraps(func)
    def log_crumb(*args, correlation_id="None", **kwargs):
        run_date = date.today()

        start_time = datetime.now()

        name = func.__name__

        module = 'unknown'

        if func.__module__:
             module = func.__module__

        mark = time.time()

        start_data = {
            'date': run_date.strftime('%d-%b-%Y'),
            'start_time':  _get_formatted_time(start_time),
            'module': module,
            'name': name,
            'correlation_id': correlation_id, 
            'arg_list': args,
            'arg_keys': kwargs,
            'timestamp': mark
        }

        print(dumps(start_data, indent=4))

        if correlation_id != "None":
            kwargs[correlation_id] = correlation_id

        retval = func(*args, **kwargs)

        end_time = datetime.now()

        end_data = {
            'timestamp': mark,
            correlation_id: correlation_id,
            'end_time': _get_formatted_time(end_time), 
            'module': module,
            'name': name,
            'runtime': "{:.3f}".format(_get_delta_seconds(start_time, end_time)),
            'returned': retval
        }

        print(dumps(end_data, indent=4))

        return retval

    return log_crumb
