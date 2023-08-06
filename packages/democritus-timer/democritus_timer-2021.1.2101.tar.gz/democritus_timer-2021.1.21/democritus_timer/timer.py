import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))


class Timer(object):
    def __init__(self):
        self.timers = {}

    def has_timer(self, name: str, print_errors: bool = True) -> bool:
        """Return whether or not the timer object has a timer with the given name in its timers."""
        if name not in self.timers:
            if print_errors:
                print(
                    f'There is no timer with the name "{name}". Use the `timer_start(\'{name}\')` function to start the timer.'
                )
            return False
        else:
            return True


_timer_object = Timer()


def timer_start(name: str = None) -> str:
    """Start a timer with the given name. Timers can be stopped with the `timer_stop` function."""
    from democritus_dates import time_now
    from democritus_uuids import uuid4

    # if there is no name given, use a generic name
    if name is None:
        name = uuid4()

    # if a timer with the given name already exists, ask the user if he/she would like to replace that timer
    if _timer_object.timers.get(name):
        message = f'A timer with the name "{name}" already exists. If you want to end it, use: `timer_stop("{name}")\ntimer_start("{name}")`.'
        raise RuntimeError(message)

    # record the start time for the timer
    _timer_object.timers[name] = time_now()
    return name


def _get_time_difference(timer_time: int) -> float:
    """Get the difference between the given timer_time and the current time."""
    from democritus_dates import time_now

    current_time = time_now()
    return current_time - timer_time


def timer_get_time(name: str) -> float:
    """Get the current time for the timer with the given name."""
    if not _timer_object.has_timer(name, print_errors=True):
        return

    time_difference = _get_time_difference(_timer_object.timers[name])
    return time_difference


def timer_stop(name: str) -> float:
    """Stop a timer (you can start a timer with the `timer_start` function)."""
    if not _timer_object.has_timer(name, print_errors=True):
        return

    time_difference = _get_time_difference(_timer_object.timers[name])
    # remove the timer after it has been stopped
    del _timer_object.timers[name]

    return time_difference
