#!/usr/bin/env python3

import datetime

# noinspection PyPackageRequirements
from consolemenu import PromptUtils

from .fasts_file import read_fasts
from .utils import get_time_difference, print_with_alignment


def show_statistics(prompt_utils: PromptUtils) -> None:

    fasts = read_fasts()

    print("FASTING STATISTICS")
    print()

    __print_completed_fasts(fasts)
    __print_total_fasting_time(fasts)
    __print_average_fast_length(fasts)
    __print_longest_fast_length(fasts)
    __print_longest_fasting_streak(fasts)
    __print_current_fasting_streak(fasts)
    print()

    __print_achievements(fasts)
    print()

    prompt_utils.enter_to_continue()


def __print_completed_fasts(fasts: list) -> None:

    value = __get_completed_fasts(fasts)
    value = str(value)

    __print_with_alignment("Completed Fasts", value)


def __print_total_fasting_time(fasts: list) -> None:

    total_hours, total_minutes = __get_total_hours_and_minutes(fasts)

    value = __get_period_string(total_hours, total_minutes)

    __print_with_alignment("Total Fasting Time", value)


def __print_average_fast_length(fasts: list) -> None:

    hours_total, minutes_total = __get_total_hours_and_minutes(fasts)

    minutes_per_hour = 60

    fasts_total = __get_completed_fasts(fasts)
    all_minutes = hours_total * 60 + minutes_total
    avg_minutes = all_minutes / fasts_total

    avg_hours = avg_minutes // minutes_per_hour
    avg_minutes -= avg_hours * minutes_per_hour

    value = __get_period_string(avg_hours, avg_minutes)

    __print_with_alignment("Average Fast Length", value)


def __print_longest_fast_length(fasts: list) -> None:

    hours, minutes = __get_longest_fast_length(fasts)

    value = __get_period_string(hours, minutes)

    __print_with_alignment("Longest Fast Length", value)


def __print_longest_fasting_streak(fasts: list) -> None:

    value = __get_longest_fasting_streak(fasts)
    value = "{} days".format(value)

    __print_with_alignment("Longest Fasting Streak", value)


def __print_current_fasting_streak(fasts: list) -> None:

    value = __get_current_fasting_streak(fasts)
    value = "{} days".format(value)

    __print_with_alignment("Current Fasting Streak", value)


def __print_achievements(fasts: list) -> None:

    print("Achievements:")

    achievements = __get_achievements(fasts)

    if len(achievements) == 0:
        print("- Nothing yet.")
    else:
        for achievement in achievements:
            print("- {}".format(achievement))


def __print_with_alignment(title: str, value: str):

    print_with_alignment(title, value, 24)


def __get_achievements(fasts: list) -> list:

    result = []

    __add_completed_fasts_achievement(result, fasts)
    __add_longest_streak_achievement(result, fasts)
    __add_daily_fasting_achievement(result, fasts)

    return result


def __add_completed_fasts_achievement(achievements: list, fasts: list) -> None:

    completed_fasts = __get_completed_fasts(fasts)

    for number_to_get in [5000, 2500, 1000, 500, 250, 100, 50, 25, 5]:

        if completed_fasts >= number_to_get:

            achievement = "Well Done! {} fasts completed!".format(number_to_get)
            achievements.append(achievement)

            break


def __add_longest_streak_achievement(achievements: list, fasts: list) -> None:

    longest_fasting_streak = __get_longest_fasting_streak(fasts)

    for number_to_get in [365, 250, 100, 50, 25, 10, 5]:

        if longest_fasting_streak >= number_to_get:

            achievement = "Whoa! {} fasts in a row!".format(number_to_get)
            achievements.append(achievement)

            break


def __add_daily_fasting_achievement(achievements: list, fasts: list) -> None:

    hours, _ = __get_longest_fast_length(fasts)

    for number_to_get in [72, 48, 24]:

        if hours >= number_to_get:

            achievement = "Superb! {} hours of continued fasting!".format(number_to_get)
            achievements.append(achievement)

            break


def __get_period(date: datetime.datetime) -> tuple:

    period_from = date.replace(hour=0, minute=0, second=0, microsecond=0)
    period_to = period_from + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)

    return period_from, period_to


def __get_fast_length(fast: dict) -> tuple:

    started = fast["started"]
    stopped = fast.get("stopped")

    if stopped is not None:
        result = get_time_difference(started, stopped)
    else:
        result = 0, 0

    return result


def __get_total_hours_and_minutes(fasts: list) -> tuple:

    total_hours = 0
    total_minutes = 0

    for fast in fasts:

        hours, minutes = __get_fast_length(fast)

        total_hours += hours
        total_minutes += minutes

    minutes_per_hour = 60

    if total_minutes >= minutes_per_hour:
        hours = total_minutes // minutes_per_hour
        total_minutes = total_minutes % minutes_per_hour
        total_hours += hours

    return total_hours, total_minutes


def __get_completed_fasts(fasts: list) -> int:

    result = 0
    number = len(fasts)

    if number > 0:
        result = number - 1 if fasts[-1].get("stopped") is None else number

    return result


def __get_longest_fasting_streak(fasts: list) -> int:

    value = 0
    current_value = 0

    if __get_completed_fasts(fasts) > 0:

        period = __get_period(fasts[0]["started"])

        for fast in fasts:

            if period[0] <= fast["started"] < period[1]:

                current_value += 1

            else:

                if value < current_value:
                    value = current_value

                current_value = 0

            period = __get_period(fast["started"] + datetime.timedelta(days=1))

    if value < current_value:
        value = current_value

    return value


def __get_current_fasting_streak(fasts: list) -> int:

    current_value = 0

    if __get_completed_fasts(fasts) > 0:

        period = __get_period(fasts[0]["started"])

        for fast in fasts:

            if period[0] <= fast["started"] < period[1]:
                current_value += 1
            else:
                current_value = 0

            period = __get_period(fast["started"] + datetime.timedelta(days=1))

    return current_value


def __get_longest_fast_length(fasts: list) -> tuple:

    minutes_per_hour = 60
    max_minutes = 0

    for fast in fasts:

        hours, minutes = __get_fast_length(fast)
        minutes += hours * minutes_per_hour

        if minutes > max_minutes:
            max_minutes = minutes

    hours = max_minutes // minutes_per_hour
    minutes = max_minutes - hours * minutes_per_hour

    return hours, minutes


def __get_period_string(hours: float, minutes: float) -> str:

    return "{hours}h {minutes}m".format(hours=int(hours), minutes=int(minutes))
