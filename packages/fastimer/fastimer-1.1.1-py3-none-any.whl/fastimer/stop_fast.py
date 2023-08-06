#!/usr/bin/env python3

import datetime

# noinspection PyPackageRequirements
from consolemenu import PromptUtils

from .fasts_file import read_fasts, write_fasts
from .utils import get_active_fast


def stop_fast(prompt: PromptUtils) -> None:

    fasts = read_fasts()
    fast = get_active_fast(fasts)

    if fast is not None:

        if prompt.prompt_for_yes_or_no("Do you want to end your ongoing fast?"):

            fasts[-1]["stopped"] = datetime.datetime.now()
            write_fasts(fasts)

    else:

        print("No current fast to end.")
        print()

        prompt.enter_to_continue()
