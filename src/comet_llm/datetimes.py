# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2023 Comet ML INC
#  This file can not be copied and/or distributed without the express
#  permission of Comet ML Inc.
# *******************************************************

import calendar
import datetime
from typing import Optional


class Timer:
    def __init__(self) -> None:
        self._start_timestamp = local_timestamp()
        self._end_timestamp: Optional[int] = None
        self._duration: Optional[int] = None

    def stop(self) -> None:
        self._end_timestamp = local_timestamp()
        self._duration = self._end_timestamp - self._start_timestamp

    @property
    def start_timestamp(self) -> int:
        return self._start_timestamp

    @property
    def end_timestamp(self) -> Optional[int]:
        return self._end_timestamp

    @property
    def duration(self) -> Optional[int]:
        return self._duration


def local_timestamp() -> int:
    now = datetime.datetime.utcnow()
    timestamp_in_seconds = calendar.timegm(now.timetuple()) + (now.microsecond / 1e6)
    timestamp_in_milliseconds = int(timestamp_in_seconds * 1000)
    return timestamp_in_milliseconds