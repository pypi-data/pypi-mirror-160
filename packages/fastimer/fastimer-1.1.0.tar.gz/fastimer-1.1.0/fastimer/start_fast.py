#!/usr/bin/env python3

import datetime

# noinspection PyPackageRequirements
from consolemenu import PromptUtils
# noinspection PyPackageRequirements
from consolemenu.validators.regex import RegexValidator

from .fasts_file import read_fasts, write_fasts
from .utils import get_active_fast


def start_fast(prompt: PromptUtils) -> None:

    fasts = read_fasts()
    fast = get_active_fast(fasts)

    if fast is not None:

        print("Fast is already on.")
        print()

        prompt.enter_to_continue()

    else:

        __ask_for_fast_length(prompt, fasts)


def __ask_for_fast_length(prompt: PromptUtils, fasts: list) -> None:

    length = None
    length_validator = RegexValidator("^[0-9]*$")

    while length is None:

        input_result = prompt.input(
            prompt="Enter fast length: ", default="16", validators=length_validator
        )

        if input_result.validation_result:

            length = int(input_result.input_string)
            fast = {
                "length": length,
                "started": datetime.datetime.now(),
            }

            fasts.append(fast)
            write_fasts(fasts)

        else:

            print("Please enter a valid number.")
