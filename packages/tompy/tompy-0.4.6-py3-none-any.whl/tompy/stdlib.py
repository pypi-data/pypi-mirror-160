import datetime
from typing import Optional, Union

import pytz


class Datetime:
    @staticmethod
    def now(tz: Optional[pytz.BaseTzInfo] = None) -> datetime.datetime:
        """
        Return the current timezone datetime.
        """
        utcnow = pytz.utc.localize(datetime.datetime.utcnow())
        if tz is not None:
            return utcnow.astimezone(tz)
        return utcnow

    @staticmethod
    def now_time(tz: Optional[pytz.BaseTzInfo] = None) -> datetime.time:
        return Datetime.now(tz).timetz()

    @staticmethod
    def now_date(tz: Optional[pytz.BaseTzInfo] = None) -> datetime.date:
        return Datetime.now(tz).date()


class Time:
    @staticmethod
    def now(tz: Optional[pytz.BaseTzInfo] = None) -> datetime.time:
        """
        Return the current timezone time.
        """
        return Datetime.now_time(tz)


class Date:
    @staticmethod
    def now(tz: Optional[pytz.BaseTzInfo] = None) -> datetime.date:
        """
        Return the current timezone date.
        """
        return Datetime.now_date(tz)

    @staticmethod
    def add(d: datetime.date, days: int) -> datetime.date:
        """
        days range: -999999999 <= days <= 999999999
        """
        return d + datetime.timedelta(days=days)

    @staticmethod
    def weekday(d: datetime.date) -> int:
        """
        Return the day of the week as an integer, Monday is 0 and Sunday is 6.
        """
        return d.weekday()

    @staticmethod
    def is_weekend(d: datetime.date) -> bool:
        return Date.weekday(d) > 4

    @staticmethod
    def to_str(d: datetime.date) -> str:
        """
        Return a string representing the date in ISO 8601 format, YYYY-MM-DD.
        """
        return d.isoformat()

    @staticmethod
    def from_str(datestr: str, fmt: str = "%Y-%m-%d") -> datetime.date:
        return datetime.datetime.strptime(datestr, fmt).date()

    @staticmethod
    def now_adds(
        list_days: list[int],
        tz: Optional[pytz.BaseTzInfo] = None,
        to_str: bool = False,
    ) -> list[Union[datetime.date, str]]:
        t = Date.now(tz)
        if to_str:
            return [Date.to_str(Date.add(t, days)) for days in list_days]
        return [Date.add(t, days) for days in list_days]
