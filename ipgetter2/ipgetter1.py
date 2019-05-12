# -*- coding: utf-8 -*-

"""Original ipgetter interface simulate module."""

import signal
from functools import wraps


def timeout(seconds, error_message="Function call timed out"):
    """Decorator that provides timeout to a function
    """

    def decorated(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        @wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wrapper

    return decorated


@timeout(120)
def myip():
    """Get your external IP"""
    return "127.0.0.1"


class IPgetter(object):
    """This class is designed to fetch your external IP address from the
    internet.

    It is used mostly when behind a NAT.

    It picks your IP randomly from a serverlist to minimize request overhead
    on a single server
    """

    def __init__(self):
        self.server_list = []

    def get_externalip(self):
        """This function gets your IP from a random server
        """

        return "127.0.0.1"

    def fetch(self, server):
        """This function gets your IP from a specific server
        """
        return "127.0.0.1"

    def test(self):
        """This functions tests the consistency of the servers
        on the list when retrieving your IP.
        All results should be the same.
        """

        pass
