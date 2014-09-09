# Copyright (C) 2014 SEE AUTHORS FILE
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Unittests.
"""
import mock

from argparse import Namespace

from . import TestCase, unittest

from relent import main


class TestMain(TestCase):
    """
    Tests for the main relent entry point.
    """

    def test_with_no_playbooks(self):
        """
        Good playbooks should react as expectd.
        """
        with mock.patch('argparse.ArgumentParser') as ap:
            ap().parse_args.return_value = Namespace(
                playbooks=[], verbose=False, header=False)
            try:
                main()
            except SystemExit, se:
                assert se.code == 0

    def test_with_good_plabook(self):
        """
        Good playbooks should react as expectd.
        """
        with mock.patch('argparse.ArgumentParser') as ap:
            ap().parse_args.return_value = Namespace(
                playbooks=['tests/playbook_schema_valid.json'],
                verbose=False, header=False)
            try:
                main()
            except SystemExit, se:
                assert se.code == 0

    def test_verbose_with_good_plabook(self):
        """
        Good playbooks should return good header.
        """
        with mock.patch('argparse.ArgumentParser') as ap:
            ap().parse_args.return_value = Namespace(
                playbooks=['tests/playbook_schema_valid.json'],
                verbose=True, header=False)
            try:
                main()
            except SystemExit, se:
                assert se.code == 0
            ap()._print_message.called_once()

    def test_with_bad_plabook(self):
        """
        Bad playbooks should return error information.
        """
        with mock.patch('argparse.ArgumentParser') as ap:
            ap().parse_args.return_value = Namespace(
                playbooks=['tests/playbook_schema_invalid.json'],
                verbose=False, header=False)
            try:
                main()
            except SystemExit, se:
                assert se.code == 1
            ap()._print_message.assert_called_once()

    def test_verbose_with_bad_plabook(self):
        """
        Bad playbooks should return too much error information.
        """
        with mock.patch('argparse.ArgumentParser') as ap:
            ap().parse_args.return_value = Namespace(
                playbooks=['tests/playbook_schema_invalid.json'],
                verbose=True, header=False)
            try:
                main()
            except SystemExit, se:
                assert se.code == 1
            assert ap()._print_message.call_count == 3
