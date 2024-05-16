from decorator import logging

import time

@logging.crumb
def foo():
    return {
        'test': 'this',
        'monkey': [1,2,3],
    }

@logging.crumb
def bar():
    time.sleep(1)

    return {
        'foo': 'bar',
    }

@logging.flare
def baz():
    time.sleep(1)

    return ['baz', 'bingo!', 'test?']

