#!/usr/bin/env python3

# noinspection PyPackageRequirements
from consolemenu import ConsoleMenu, PromptUtils, Screen

# noinspection PyPackageRequirements
from consolemenu.items import FunctionItem as Item

from .show_fast import show_fast
from .show_statistics import show_statistics
from .start_fast import start_fast
from .stop_fast import stop_fast


def main() -> None:

    prompt = PromptUtils(Screen())
    params = [prompt]

    menu = ConsoleMenu("FASTING LOG")

    menu.append_item(Item("Start New Fast", start_fast, params))
    menu.append_item(Item("End Active Fast", stop_fast, params))
    menu.append_item(Item("Display Active Fast", show_fast, params))
    menu.append_item(Item("Display Fasting Statistics", show_statistics, params))

    menu.show()
