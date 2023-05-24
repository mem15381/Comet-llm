import calendar
import datetime


class Timer:
    def __init__(
        self,
    ):
        self._start_timestamp = _local_timestamp()
        self._end_timestamp = None
        self._duration = None

    def stop(self) -> None:
        self._end = _local_timestamp()
        self._duration = self._end_timestamp - self._start_timestamp

    @property
    def start_timestamp(self):
        return self._start_timestamp

    @property
    def end_timestamp(self):
        return self._end_timestamp

    @property
    def duration(self):
        return self._duration


def _local_timestamp() -> int:
    now = datetime.datetime.utcnow()
    timestamp_in_seconds = calendar.timegm(now.timetuple()) + (now.microsecond / 1e6)
    timestamp_in_milliseconds = int(timestamp_in_seconds * 1000)
    return timestamp_in_milliseconds
