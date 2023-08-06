#!/usr/bin/env python3

import datetime
import sys
from collections import namedtuple
from os.path import isfile

from consolemenu import ConsoleMenu, PromptUtils, Screen
from consolemenu.items import FunctionItem
from consolemenu.validators.regex import RegexValidator
from yaml import parser, safe_dump, safe_load

from .fast import display_fast


def show() -> None:
    data = namedtuple("data", "journal")

    read_journal(data)
    display_menu(data)


def get_journal_file_name() -> str:
    return "journal.yaml"


def read_journal(data: namedtuple):

    yaml_file_name = get_journal_file_name()

    data.journal = []

    if isfile(yaml_file_name):

        try:

            with open(yaml_file_name, encoding="utf-8-sig") as yaml_file:
                data.journal = safe_load(yaml_file)

        except parser.ParserError:

            print(f"Unable to parse: {yaml_file_name}")
            sys.exit(1)


def write_journal(data: namedtuple):
    yaml_file_name = get_journal_file_name()

    with open(yaml_file_name, encoding="utf-8-sig", mode="w") as yaml_file:
        safe_dump(data.journal, yaml_file)


def display_menu(data: namedtuple):
    """
    Builds and then displays main menu of the application.
    """

    prompt_utils = PromptUtils(Screen())
    items_params = [data, prompt_utils]

    menu = ConsoleMenu("FASTING LOG")

    menu.append_item(FunctionItem("Display Fast", display_active_fast, items_params))
    menu.append_item(FunctionItem("Start Fast", start_new_fast, items_params))
    menu.append_item(FunctionItem("End Fast", end_active_fast, items_params))

    menu.show()


def display_active_fast(data: namedtuple, prompt_utils: PromptUtils):
    fast = get_current_fast(data)

    if fast is None:
        print("No current fast to display.")
    else:
        display_fast(fast)

    print()
    prompt_utils.enter_to_continue()


def start_new_fast(data: namedtuple, prompt_utils: PromptUtils):
    fast = get_current_fast(data)

    if fast is not None:

        print("Fast is already on.")
        prompt_utils.enter_to_continue()

    else:

        length = None
        length_validator = RegexValidator("^[0-9]*$")

        while length is None:
            input_result = prompt_utils.input(
                prompt="Enter fast length: ", default="16", validators=length_validator
            )
            if input_result.validation_result:
                length = int(input_result.input_string)
                fast = {
                    "length": length,
                    "started": datetime.datetime.now(),
                    "stopped": None,
                }

                data.journal.append(fast)
                write_journal(data)
            else:
                print("Please enter a valid number.")


def end_active_fast(data: namedtuple, prompt_utils: PromptUtils):
    fast = get_current_fast(data)

    if fast is not None:

        if prompt_utils.prompt_for_yes_or_no("Do you want to end your ongoing fast?"):

            data.journal[-1]["stopped"] = datetime.datetime.now()
            write_journal(data)

    else:

        print("No current fast to end.")
        print()

        prompt_utils.enter_to_continue()


def get_current_fast(data: namedtuple):
    return (
        data.journal[-1]
        if len(data.journal) > 0 and data.journal[-1]["stopped"] is None
        else None
    )
