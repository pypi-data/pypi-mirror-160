#!/usr/bin/env python

# Copyright 2020 Unlimited Robotics

import argparse
import os
import sys
import platform

from rayasdk.connect import URConnect

from rayasdk.logger import log, LogLevels, log_error, log_verbose, set_logger_level
from rayasdk.scanner import URScanner
from rayasdk.initializer import URInitializer
from rayasdk.runner import URRunner
from rayasdk.simulator import URSimulator
from rayasdk.killer import URKiller
from rayasdk.constants import *

from rayasdk.container_handlers.docker_handler import check_container

class URSDK:
    def __init__(self):
        self.command_objects = []
        self.command_objects.append(URInitializer())
        self.command_objects.append(URScanner())
        self.command_objects.append(URConnect())
        self.command_objects.append(URRunner())
        self.command_objects.append(URSimulator())
        self.command_objects.append(URKiller())
        self.init_parser()
    
    def init_parser(self):
        # Init top parser
        self.argparser = argparse.ArgumentParser(description='Unlimited Robotics SDK')
        group = self.argparser.add_mutually_exclusive_group()
        group.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity.")
        group.add_argument("-q", "--quiet", action="store_true", help="don't print on stdout.")
        subparsers = self.argparser.add_subparsers(help='SDK Command', dest='command')
        subparsers.required = True
        # Init subparsers
        for obj in self.command_objects:
            obj.init_parser(subparsers)
        # Parse arguments
        self.args, self.unknownargs = self.argparser.parse_known_args()
        # Setup Logger
        set_logger_level(self.args.verbose, self.args.quiet)

    def init_ursdk_folder(self):
        if not os.path.exists(URSDK_TEMP_PATH):
            log_verbose(f'Folder {URSDK_TEMP_PATH} does not exists, creating it.')
            try:
                os.mkdir(URSDK_TEMP_PATH)
            except OSError as exc:
                log_error(f'Folder {URSDK_TEMP_PATH} could not be created.')
                return False
            return True
        else:
            log_verbose(f'Folder {URSDK_TEMP_PATH} found.')
            return True

    def run(self):
        if not self.init_ursdk_folder():
            return False
        if not check_container():
            return False
        for obj in self.command_objects:
            if self.args.command == type(obj).COMMAND:
                return obj.run(self.args, self.unknownargs)

def main():
    if platform.system() not in ['Linux', 'Windows']:
        print(f'Platform \'{platform.system()}\' not supported.')
        exit(1)
    ursdk = URSDK()
    ret = ursdk.run()
    if not ret:
        log_verbose('Finished with error.')
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()