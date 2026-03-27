#! /usr/bin/env python
# Copyright 2026 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License GPL-3.0 or later (https://www.gnu.org/licenses/gpl-3.0).


import argparse
import configparser
import sys
import os
from cryptography.fernet import Fernet

DEFAULT_CONFIG_FILE = "/etc/bridgeapi_filter.conf"

__author__ = "Alexis de Lattre <alexis.delattre@akretion.com>"
__date__ = "March 27th 2026"
__version__ = "0.1"


def decrypt_user_uuid(args):
    config_file = args.config_file
    if not os.path.exists(config_file):
        print(f"File {config_file} doesn't exist. Exiting.")
        sys.exit(1)
    with open(config_file, 'r+') as f:
        cparser = configparser.ConfigParser()
        cparser.read_file(f)
    if "config" not in cparser:
        print(f"Missing section [config] in {config_file}. Exiting.")
        sys.exit(1)
    if "encryption_key" not in cparser['config']:
        print(f"Missing key 'encryption_key' in section [config] of {config_file}. Exiting.")
        sys.exit(1)
    encryption_key_str = cparser['config']['encryption_key']
    encryption_key_bin = encryption_key_str.encode('utf-8')
    cipher = Fernet(encryption_key_bin)

    encrypted_uuid_str = args.encrypted_uuid and args.encrypted_uuid[0]
    if not encrypted_uuid_str:
        encrypted_uuid_str = input("Enter encrypted UUID: ")
        encrypted_uuid_str = encrypted_uuid_str.strip()
    if not encrypted_uuid_str:
        print('Encrypted UUID is empty. Exiting.')
        sys.exit(1)
    encrypted_uuid_bytes = encrypted_uuid_str.encode('utf-8')
    decrypted_uuid_bytes = cipher.decrypt(encrypted_uuid_bytes)
    decrypted_uuid_str = decrypted_uuid_bytes.decode('utf-8')
    print(f'Decrypted UUID: {decrypted_uuid_str}')


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    usage = "bridgeapi_decrypt_user_uuid.py <encrypted_uuid>"
    epilog = "Author: %s - Version: %s" % (__author__, __version__)
    description = "Decrypt the user UUID by hand. Useful for debugging. "
    "If will read the encryption key from the Bridge API filter configuration file "
    "given with the --config or -c option."
    parser = argparse.ArgumentParser(
        usage=usage, epilog=epilog, description=description)
    parser.add_argument(
        '-c', '--config', dest="config_file", default=DEFAULT_CONFIG_FILE,
        help=f"Path to the BridgeAPI filter configuration file. "
        f"Default value: {DEFAULT_CONFIG_FILE}")
    parser.add_argument(
        "encrypted_uuid", nargs='*', help="Encrypted Bridge API user UUID.")
    args = parser.parse_args()
    decrypt_user_uuid(args)


def run():
    if __name__ == '__main__':
        main()


run()
