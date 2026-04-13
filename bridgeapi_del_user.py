#! /usr/bin/env python
# Copyright 2026 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License GPL-3.0 or later (https://www.gnu.org/licenses/gpl-3.0).

import argparse
import configparser
import sys
import os
import requests

BRIDGE_VERSION = '2025-01-15'
BASE_URL = 'https://api.bridgeapi.io/v3'
DEFAULT_CONFIG_FILE = "/etc/bridgeapi_filter.conf"

__author__ = "Alexis de Lattre <alexis.delattre@akretion.com>"
__date__ = "April 13th 2026"
__version__ = "0.1"


def delete_user(args):
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
    }
    user_uuid = args.user_uuid and args.user_uuid[0]
    if not user_uuid:
        user_uuid = input("Enter Bridge User UUID to delete: ")
    if not user_uuid:
        print('No user UUID entered.')
        sys.exit(1)
    confirm = input(f"You are about to delete Bridge user UUID '{user_uuid}'. Do you confirm (yes/no)? ")
    if confirm != 'yes':
        print('Exiting. No user deleted.')
        sys.exit(1)
    url = f"{BASE_URL}/aggregation/users/{user_uuid}"
    print(f'Sending DELETE request on {url}')
    del_user_res = requests.delete(url, headers=headers)
    if del_user_res.status_code == 204:
        print(f"BridgeAPI user UUID '{user_uuid}' successfully deleted.")
    else:
        print(f"Failed to delete user. HTTP error code: {del_user_res.status_code}.")


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    usage = "bridgeapi_del_user.py <user_uuid>"
    epilog = "Author: %s - Version: %s" % (__author__, __version__)
    description = "Delete a Bridge API user. "
    parser = argparse.ArgumentParser(
        usage=usage, epilog=epilog, description=description)
    parser.add_argument(
        '-c', '--config', dest="config_file", default=DEFAULT_CONFIG_FILE,
        help=f"Path to the BridgeAPI filter configuration file. "
        f"Default value: {DEFAULT_CONFIG_FILE}")
    parser.add_argument(
        "user_uuid", nargs='*', help="Bridge API user UUID")
    args = parser.parse_args()
    delete_user(args)


def run():
    if __name__ == '__main__':
        main()


run()
