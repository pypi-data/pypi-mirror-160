import time

import pytest

from democritus_timer import timer_start, timer_stop, timer_get_time


def test_timer_get_time_1():
    timer_name = 'foo'
    timer_start(timer_name)
    time.sleep(2)
    current_time = timer_get_time(timer_name)
    assert 2 < current_time < 3
    timer_stop(timer_name)


def test_generic_timer_1():
    timer_name = timer_start()
    time.sleep(2)
    elapsed_time = timer_stop(timer_name)
    assert elapsed_time > 2
    assert elapsed_time < 3


def test_named_timer_1():
    timer_name = timer_start()

    with pytest.raises(RuntimeError):
        timer_start(timer_name)

    timer_start('bar')

    time.sleep(2)

    generic_elapsed_time = timer_stop(timer_name)
    assert 2 < generic_elapsed_time < 3

    time.sleep(2)

    bar_elapsed_time = timer_stop('bar')
    assert 4 < bar_elapsed_time < 5
