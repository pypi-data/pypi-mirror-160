#!/usr/bin/env python3

# Copyright Louis Paternault 2011-2022
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>. 1

"""Command line options"""

import argparse
import sys
import textwrap

from scal import VERSION


def commandline_parser():
    """Return a command line parser."""

    parser = argparse.ArgumentParser(
        prog="scal",
        description="A year calendar producer.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent(
            #  pylint: disable=line-too-long
            """\
                Here is an example configuration files. It is a YAML file. Most of the option are optional (excepted stard and end date of the calendar).

                ~~~
                calendar:

                  # Start and end date of the calendar
                  start: 2022-08-01
                  end: 2023-07-31

                  # Template to use, either:
                  # - default calendar.tex: one page calendar;
                  # - weekly.tex: weekly planner;
                  # - any other file in the current directory.
                  template: calendar.tex

                  # Which week numbers should be displayed?
                  # - iso: ISO week numbers
                  # - work: number of worked weeks since the beginning of the calendar
                  weeks:
                    iso: yes
                    work: yes

                variables:
                  language: french
                  papersize: a4paper

                holidays:
                  # Single day
                  2022-12-25: Christmas

                  # Single day, any year
                  05-01: International Workers' Day

                  # Several days
                  2023-02-04 2023-02-18: Winter holidays.
                ~~~
                """
        ),
    )

    parser.add_argument(
        "--version",
        help="Show version",
        action="version",
        version="%(prog)s " + VERSION,
    )

    parser.add_argument(
        "FILE",
        help="Configuration file",
        nargs=1,
        type=argparse.FileType("r"),
        default=sys.stdin,
    )

    return parser
