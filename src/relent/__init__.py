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

import argparse
import json

import jsonschema

from pkg_resources import resource_filename


__version__ = '0.0.1'


def main():
    """
    Main entry point.
    """
    parser = argparse.ArgumentParser(version=__version__)
    parser.add_argument(
        'playbooks', metavar='PLAYBOOKS', type=str, nargs='+',
        help='The playbook(s) to lint.')

    args = parser.parse_args()

    schema_validation_results = {}
    all_valid = True
    # Load the playbook schema
    with open(resource_filename(
            'relent', 'schemas/playbook_schema.json'), 'r') as schema_fp:
        schema = json.load(schema_fp)
        # Do checks against playbooks
        for playbook in args.playbooks:
            try:
                with open(playbook, 'r') as pb:
                    # Schema check
                    jsonschema.validate(json.load(pb), schema)
            except jsonschema.ValidationError, e:
                all_valid = False
                schema_validation_results[playbook] = (
                    False, e.message, list(e.schema_path))
            except ValueError, e:
                all_valid = False
                schema_validation_results[playbook] = (
                    False, 'JSON is invalid.', str(e))

    # If all_valid is True then return back happy results
    if all_valid is True:
        raise SystemExit(0)
    else:
        for problem_playbook in schema_validation_results.keys():
            parser._print_message('%s: E: %s %s\n' % (
                problem_playbook,
                schema_validation_results[problem_playbook][1],
                schema_validation_results[problem_playbook][2]))
        raise SystemExit(1)


if __name__ == '__main__':
    main()
