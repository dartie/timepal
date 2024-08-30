# -*- coding: utf-8 -*-
#
# Author:   Dario Necco
#
import os
import sys
import yaml
import argparse
import pytz
import dateutil.parser
import datetime
from typing import Literal
from colorama import init as init_colorama, Fore, Back, Style

init_colorama()

# set version and author
__version__ = '1.0'
intern_version = '0001'

# I obtain the app directory
if getattr(sys, 'frozen', False):
    # frozen
    dirapp = os.path.dirname(sys.executable)
    dirapp_bundle = sys._MEIPASS
    executable_name = os.path.basename(sys.executable)
else:
    # unfrozen
    dirapp = os.path.dirname(os.path.realpath(__file__))
    dirapp_bundle = dirapp
    executable_name = os.path.basename(__file__)

##############################################################################################

def invert_key_values_dict(my_dict):
    my_dict_value_key = {}

    # Iterate over the dictionary
    for key, values in my_dict.items():
        for v in values:
            # Map each name to its corresponding timezone
            my_dict_value_key[v] = key

    return my_dict_value_key


def mprint(message, status: Literal["success", "warning", "error", "info", "none"] = "success"):
    # mprint -> message print
    if status == "success":
        color = Fore.GREEN
    elif status == "warning":
        color = Fore.YELLOW
    elif status == "error":
        color = Fore.RED
    elif status == "info":
        color = Fore.CYAN
    else:
        color = ""
    print(f'{Style.BRIGHT}{color}{message}{Style.RESET_ALL}')


def cprint(message, status: Literal["local", "target", "people", "none"]):
    # cprint -> color print
    if status == "local":
        color = Fore.GREEN
    elif status == "target":
        color = Fore.MAGENTA
    elif status == "people":
        color = Fore.CYAN
    else:
        color = ""
    print(f'{Style.NORMAL}{color}{message}{Style.RESET_ALL}')


def check_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description="""
    Display the time for all timezones set in the settings file. 

    """)

    # Options
    parser.add_argument("-S", "--settings", dest="settings", help="File containing all settings with times to get", default=os.path.join(dirapp, "settings.yml"))
    parser.add_argument("-t", "--local-timezone", dest="local_timezone", help="Overrides the local timezone", default=None)
    parser.add_argument("-s", "--search", dest="search", help="Search person for using his/her timezone as local.", default=None)
    parser.add_argument("local_date_time", nargs='*', default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), help="Local datetime formatted as %%Y-%%m-%%d %%H:%%M[:%%S]")

    args = parser.parse_args()  # it returns input as variables (args.dest)

    # end check args

    return args


def main(args=None):
    if args is None:
        args = check_args()

    if not os.path.exists(args.settings):
        mprint(f"File {args.settings} does not exist.\nExiting!", "error")
        sys.exit(1)

    if isinstance(args.local_date_time, list):
        args.local_date_time = args.local_date_time[0]

    with open(args.settings) as yaml_stream:
        try:
            yaml_content = yaml.safe_load(yaml_stream)
        except yaml.YAMLError as exc:
            print(exc)

    # Define the local time and time zone
    # local_time_str = '2024-08-23 15:00:00'
    if args.search is None:
        if args.local_timezone:
            local_timezone_str = args.local_timezone
        else:
            local_timezone_str = yaml_content["local"]
    else:
        person_timezone_dict = invert_key_values_dict(yaml_content["targets"])
        local_timezone_str = person_timezone_dict.get(args.search, None)

        if local_timezone_str is None:
            mprint("The user doesn't exist in your settings.\nExiting!", "error")
            sys.exit(2)

        print()

    local_timezone = pytz.timezone(local_timezone_str)

    # Parse the string into a datetime object
    # local_time = datetime.datetime.strptime(args.local_date_time, '%Y-%m-%d %H:%M:%S')
    local_time = dateutil.parser.parse(args.local_date_time)  # automatically detect the datetime format

    # Localize the datetime to the local time zone
    localized_time = local_timezone.localize(local_time)
    cprint(f"Local time:\n{local_timezone_str} {localized_time.strftime('%Y-%m-%d %H:%M %Z')}", "local")
    print()  # blank line

    for timezone, people in yaml_content["targets"].items():
        # Convert to the target time zone
        target_timezone = pytz.timezone(timezone)
        target_time = localized_time.astimezone(target_timezone)

        # Print the result
        cprint(f"{timezone}: {target_time.strftime('%Y-%m-%d %H:%M %Z')}", "target")
        [cprint(p, "people") for p in people]  # print people for the current timezone
        print()  # blank line


if __name__ == '__main__':
    try:
        main(args=None)
    except KeyboardInterrupt:
        print('\n\nBye!')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
