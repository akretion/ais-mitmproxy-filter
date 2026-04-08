#! /usr/bin/env python
# Copyright 2026 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License GPL-3.0 or later (https://www.gnu.org/licenses/gpl-3.0).

import argparse
import configparser
import sys
import re
import os
import secrets

PROJECT_NAME_MAX_LENGTH = 20
PROJECT_NAME_MIN_LENGTH = 3
DEFAULT_CONFIG_FILE = "/etc/bridgeapi_filter.conf"

__author__ = "Alexis de Lattre <alexis.delattre@akretion.com>"
__date__ = "March 27th 2026"
__version__ = "0.1"


def generate_credentials(args):
    project = args.odoo_project_name and args.odoo_project_name[0]
    if not project:
        project = input("Enter Odoo project name: ")
        project = project.strip()
    print(f"Generating client ID and secret for Odoo project '{project}' ...")
    if len(project) > PROJECT_NAME_MAX_LENGTH:
        print(f"Project name '{project}' has {len(project)} caracters. Maximum is {PROJECT_NAME_MAX_LENGTH}.")
        sys.exit(1)
    if len(project) < PROJECT_NAME_MIN_LENGTH:
        print(f"Project name '{project}' has {len(project)} caracters. Minimum is {PROJECT_NAME_MIN_LENGTH}.")
        sys.exit(1)
    unallowed_chars = re.sub(r"[a-zA-Z0-9_-]+", "", project)
    if unallowed_chars != "":
        print(f"Project name '{project}' contains unallowed caracters.")
        sys.exit(1)
    client_id = f"odoo_bridge_id-{project}-{secrets.token_urlsafe(25)}"
    client_secret = f"odoo_bridge_secret-{project}-{secrets.token_urlsafe(60)}"
    print(f'ClientID: {client_id}')
    print(f'Secret: {client_secret}')

    config_file = args.config_file
    if not os.path.exists(config_file):
        print(f"File {config_file} doesn't exist.")
        sys.exit(1)
    with open(config_file, 'r+') as f:
        cparser = configparser.ConfigParser()
        cparser.optionxform = lambda option: option
        cparser.read_file(f)
        cparser['odoo'][client_id] = client_secret
        f.truncate(0)
        f.seek(0)
        cparser.write(f)
        print(f"Client ID and secret added to section [odoo] of {config_file}")


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    usage = "bridgeapi_gen_odoo_credentials.py <odoo_project_name>"
    epilog = "Author: %s - Version: %s" % (__author__, __version__)
    description = "Generate client ID and secret for a new Odoo server. "
    "If a configuration file is given with the --config or -c option, it will also add "
    "an entry in the [odoo] section of the BridgeAPI filter configuration file."
    parser = argparse.ArgumentParser(
        usage=usage, epilog=epilog, description=description)
    parser.add_argument(
        '-c', '--config', dest="config_file", default=DEFAULT_CONFIG_FILE,
        help=f"Path to the BridgeAPI filter configuration file. "
        f"Default value: {DEFAULT_CONFIG_FILE}")
    parser.add_argument(
        "odoo_project_name", nargs='*',
        help=f"Odoo Project Name. Length {PROJECT_NAME_MIN_LENGTH} to {PROJECT_NAME_MAX_LENGTH}. "
        f"Characters accepted: a-zA-Z0-9_-")
    args = parser.parse_args()
    generate_credentials(args)


def run():
    if __name__ == '__main__':
        main()


run()
