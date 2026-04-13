#! /usr/bin/env python
# Copyright 2026 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License GPL-3.0 or later (https://www.gnu.org/licenses/gpl-3.0).

import argparse
import configparser
import sys
import os
import requests
from pprint import pprint

BRIDGE_VERSION = '2025-01-15'
BASE_URL = 'https://api.bridgeapi.io/v3'
DEFAULT_CONFIG_FILE = "/etc/bridgeapi_filter.conf"

__author__ = "Alexis de Lattre <alexis.delattre@akretion.com>"
__date__ = "April 13th 2026"
__version__ = "0.1"


def generate_credentials(args):
    config_file = args.config_file
    if not os.path.exists(config_file):
        print(f"File {config_file} doesn't exist.")
        sys.exit(1)
    cparser = configparser.ConfigParser()
    cparser.read(config_file)
    client_id = cparser['bridge_api']['client_id']
    client_secret = cparser['bridge_api']['secret']
    headers = {
        'Bridge-Version': BRIDGE_VERSION,
        'Client-Id': client_id,
        'Client-Secret': client_secret,
        'accept': 'application/json',
        'content-type': 'application/json',
    }
    list_user_res = requests.get(f"{BASE_URL}/aggregation/users", headers=headers)
    if list_user_res.status_code != 200:
        print(f"Failed to list users. HTTP error code: {list_user_res.status_code}.")
        sys.exit(1)
    user_list_json = list_user_res.json()
    pprint(user_list_json)
    print('List of BridgeAPI users:')
    user_list = user_list_json.get('resources', [])
    count = 0
    for user in user_list:
        count += 1
        print(f"User '{user['external_user_id']}' UUID {user['uuid']}")
    print(f'Total number of users: {count}')
    if user_list_json['pagination']['next_uri']:
        print('More than one page. TODO implement multi-page')
        sys.exit(1)


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    usage = "bridgeapi_list_users.py"
    epilog = "Author: %s - Version: %s" % (__author__, __version__)
    description = "List Bridge API users. "
    parser = argparse.ArgumentParser(
        usage=usage, epilog=epilog, description=description)
    parser.add_argument(
        '-c', '--config', dest="config_file", default=DEFAULT_CONFIG_FILE,
        help=f"Path to the BridgeAPI filter configuration file. "
        f"Default value: {DEFAULT_CONFIG_FILE}")
    args = parser.parse_args()
    generate_credentials(args)


def run():
    if __name__ == '__main__':
        main()


run()
