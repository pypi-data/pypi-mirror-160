#!/usr/bin/env python3
from collections import namedtuple
import datetime


def display_fast(fast: dict) -> None:
    goal = fast["started"] + datetime.timedelta(hours=fast["length"])

    elapsed_time = __get_elapsed_time(fast)
    remaining_time = __get_time(datetime.datetime.today(), goal)

    started = fast["started"].strftime("%a, %H:%M")

    goal = goal.strftime("%a, %H:%M")

    print(f'CURRENT FAST:    {fast["length"]} HOURS')
    print()
    print(f"Elapsed time:    {elapsed_time}")
    print(f"Remaining:       {remaining_time}")
    print()
    print(f"Started:  {started}")
    print(f"Goal:     {goal}")


def __get_time(start_date: datetime, end_date: datetime) -> str:
    seconds = (end_date - start_date).total_seconds()
    hours = int(seconds / 60 / 60)
    minutes = int((seconds - hours * 60 * 60) / 60)
    seconds = int(seconds - hours * 60 * 60 - minutes * 60)

    hours = str(hours).zfill(2)
    minutes = str(minutes).zfill(2)
    seconds = str(seconds).zfill(2)

    return f"{hours}:{minutes}:{seconds}"


def __get_elapsed_time(fast: dict) -> str:
    date1 = fast["started"]
    date2 = datetime.datetime.today() if fast["stopped"] is None else fast["stopped"]

    return __get_time(date1, date2)
