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

"""Test of calendar parser and renderer"""
# pylint: disable=too-few-public-methods

import glob
import io
import os
import unittest

from scal import __DATE__, VERSION, calendar, errors
from scal.template import generate_tex


class ParserRenderer(unittest.TestCase):
    """Test .scl files renderer"""

    maxDiff = None

    def test_generate_tex(self):
        """Test scl output."""
        for scl in glob.iglob(os.path.join(os.path.dirname(__file__), "*.scl")):
            with self.subTest(msg=f"Testing '{scl}'"):
                basename = scl[: -len(".scl")]
                with open(f"{basename}.tex", "r", encoding="utf8") as expectfile:
                    self.assertMultiLineEqual(
                        generate_tex(
                            calendar.Calendar.from_file(f"{basename}.scl")
                        ).strip(),
                        (
                            expectfile.read()
                            .replace("@COPYRIGHTDATE@", str(__DATE__))
                            .replace("@VERSION@", str(VERSION))
                            .strip()
                        ),
                    )


class TestErrors(unittest.TestCase):
    """Test some errors"""

    def test_empty(self):
        """Test parsing an empty scl file."""
        self.assertRaises(errors.ConfigError, calendar.Calendar, io.StringIO(""))
