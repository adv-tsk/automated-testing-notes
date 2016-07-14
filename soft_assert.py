# -*- coding: utf-8 -*-

from threading import local

import pytest


# Use a thread-local store for failed soft asserts, making it thread-safe
# in parallel testing and shared among the functions in this module.
_thread_locals = local()


class SoftAssertionError(AssertionError):
    """Exception class containing failed assertions"""

    def __init__(self, failed_assertions):
        """
        :type failed_assertions: list
        """
        self.failed_assertions = failed_assertions
        super(SoftAssertionError, self).__init__(str(self))

    def __str__(self):
        return '\n'.join(self.failed_assertions)


@pytest.yield_fixture
def soft_assert():
    """
    Soft assert fixture

    Example usage:
    >>> soft_assert(1 == 2)
    >>> soft_assert('hello' == 'world')
    >>> soft_assert(True is False, 'It is not equivalent!')
    """

    def soft_assert_func(expr, fail_message=''):
        try:
            assert expr, fail_message
        except AssertionError as ex:
            _thread_locals.caught_asserts.append(ex)
        return bool(expr)

    _thread_locals.caught_asserts = []
    yield soft_assert_func
    if _thread_locals.caught_asserts:
        raise SoftAssertionError(_thread_locals.caught_asserts)
