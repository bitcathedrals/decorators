from functools import wraps

from json import dumps

import time
from datetime import date, datetime

def _get_formatted_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")

def _get_delta_seconds(start, end):
     delta = end - start
     return delta.total_seconds()

def crumb(func):

    @wraps(func)
    def log_crumb(*args, correlation_id="NoID", **kwargs):
        run_date = date.today()

        start_time = _get_formatted_time()

        name = func.__name__

        module = 'unknown'
        if '__module__' in func:
             module = func.__module__

        mark = time.time()

        start_data = {
            'date': run_date.strftime('%d-%b-%Y'),
            'start_time':  _get_formatted_time(),
            'module': module,
            'name': name,
            'correlation_id': correlation_id, 
            'arg_list': args,
            'arg_keys': kwargs,
            'timestamp': mark
        }

        print(dumps(start_data, indent=4))

        retval = func(*args, correlation_id, **kwargs)

        end_time = _get_formatted_time()

        end_data = {
            'timestamp': mark,
            correlation_id: correlation_id,
            'end_time': end_time, 
            'module': module,
            'name': name,
            'runtime': _get_delta_seconds(start_time, end_time),
            'returned': retval
        }

        print(dumps(end_data, indent=4))

        return retval

