import random
import time


class Timer:
    """
    Utility class for a elapsing timer.
    """

    def __init__(self):
        self.duration = 0.0
        self.start_time = None

    def start(self, duration: float):
        """
        Start the timer.

        Parameters
        ----------
        duration : float
            Duration for the timer in seconds.
        """
        self.duration = duration
        self.start_time = time.time()

    def is_elapsed(self) -> bool:
        """
        Check if the timer is elapsed.

        Raises
        ------
        ValueError
            When attempting to check a timer that was not started.

        Returns
        -------
        bool
            True when the time has elapsed, false otherwise.
        """
        if not self.start_time or not self.duration:
            raise ValueError("Timer was not started")
        return (time.time() - self.start_time) > self.duration


class Backoff:
    """
    Utility class that can be used to trigger an exponential backoff with or without jitter.
    """

    def __init__(
        self,
        base_backoff: float,
        max_backoff: float,
        enable_jitter: bool,
    ):
        self.base_backoff = base_backoff
        self.max_backoff = max_backoff
        self.enable_jitter = enable_jitter

        self.attempt_max_backoff = base_backoff

    def reset(self):
        """
        Reset the exponential backoff.
        """
        self.attempt_max_backoff = self.base_backoff

    def backoff_get_next(self):
        """
        Get the next backoff value in milliseconds.

        Returns
        -------
        float
            The next backoff value (ms).
        """
        if self.enable_jitter:
            next_backoff = random.uniform(0, self.attempt_max_backoff)
        else:
            next_backoff = self.attempt_max_backoff

        # Calculate max backoff for the next attempt (~ 2**attempt)
        self.attempt_max_backoff = min(self.attempt_max_backoff * 2, self.max_backoff)

        return next_backoff
