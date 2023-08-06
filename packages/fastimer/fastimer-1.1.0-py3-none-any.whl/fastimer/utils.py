#!/usr/bin/env python3

import datetime


def get_time_difference(
    start_date: datetime.datetime, end_date: datetime.datetime
) -> tuple:

    seconds_per_hour = 3600
    seconds_per_minute = 60

    seconds = (end_date - start_date).total_seconds()

    hours = int(seconds // seconds_per_hour)
    minutes = int(seconds % seconds_per_hour // seconds_per_minute)

    return hours, minutes


def print_with_alignment(title: str, value: str, width: int = 15) -> None:

    title = f"{title}:".ljust(width)
    string = "{} {}".format(title, value)

    print(string)


def get_active_fast(fasts: list) -> dict | None:

    return fasts[-1] if len(fasts) > 0 and fasts[-1].get("stopped") is None else None
