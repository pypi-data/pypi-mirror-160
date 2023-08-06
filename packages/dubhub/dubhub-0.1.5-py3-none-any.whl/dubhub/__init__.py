#!/usr/bin/env python3
import os
import sys
import logging

from .commands import Commands
import argparse
import re
import json

class ArgumentParser(argparse.ArgumentParser):

    def error(self, message):
        self.print_help(sys.stderr)
        self.exit(2, '%s: error: %s\n' % (self.prog, message))

def regex_type_uuid(arg_value, pat=re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError
    return arg_value

parser = argparse.ArgumentParser()
parser.add_argument('clone', type=str, help='Dubhub CLI clone commands')
parser.add_argument('clone_option', type=str, help='Dubhub CLI clone start/stop command')
parser.add_argument('--dubUuid', type=regex_type_uuid, help='Uuid of Dub')
parser.add_argument('--orgToken', type=regex_type_uuid, help='Uuid of Org Token')
parser.add_argument('--cloneUuid', type=regex_type_uuid, help='Uuid of Clone')
parser.add_argument('--output', type=str, help='Output result of start clone')


logger = logging.getLogger(__name__)

DEFAULT_HOST = "https://app.dubhub.io"
DEFAULT_HOST_ENV = "DUBHUB_HOST"


def main():
    host = os.environ.get(DEFAULT_HOST_ENV, DEFAULT_HOST)
    dubhub = Commands(server=host)
    args = parser.parse_args()
    if (args.dubUuid or args.cloneUuid) and not args.orgToken:
        logger.error("Please provide --orgToken")
    elif args.clone == "clone" and args.clone_option == "start":
        output = None
        if args.output is not None:
            output = args.output
        dub_uuid = args.dubUuid
        org_token = args.orgToken
        dubhub.start_clone(dub_uuid, org_token, output)
    elif args.clone == "clone" and args.clone_option == "stop":
            org_token = args.orgToken
            cloneUuid = args.cloneUuid
            dubhub.stop_clone(cloneUuid, org_token)
    elif "--analyse" == sys.argv[1]:
        try:
            file = open("start_clone_output.json", "r")
            clone_conn_json = json.loads(file.read())
            cloneUuid = json.loads(clone_conn_json)["cloneUuid"]
            org_token = sys.argv[3]
            token = sys.argv[5]
            dubhub.analyse_clone(cloneUuid, org_token, token)
        except FileNotFoundError as e:
            logger.error("Error reading JSON file:" + str(e))
    else:
        logger.error("No command found")
        logger.error("To start a clone run: dubhub clone start --orgToken <ORGTOKEN> --dubUuid <DUBUUID>")
        logger.error("To stop a clone run: dubhub clone stop --orgToken <ORGTOKEN> --cloneUuid <DUBUUID>")
        
