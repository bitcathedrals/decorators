from decorator import logging

import time

@logging.crumb
def foo():
    return {
        'test': 'this',
        'monkey': [1,2,3],
    }


foo()


@logging.crumb
def bar():
    time.sleep(1)

    return {
        'foo': 'bar',
    }

bar()

