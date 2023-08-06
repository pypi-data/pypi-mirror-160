# Copyright 2020 Unlimited Robotics

import os
import json
from shutil import copyfile

from rayasdk.logger import log_error, log_verbose
from rayasdk.constants import *


class URInitializer:
    COMMAND = 'init'

    def __init__(self):
        pass

    def init_parser(self, subparser):
        self.parser = subparser.add_parser(type(self).COMMAND, help="initialize Raya project in current folder.")
        self.parser.add_argument('--app-id', help='application unique identificator', required=True, type=str)
        self.parser.add_argument('--app-name', help='application name', type=str)

    def create_files_tree(self):
        try:
            os.mkdir(DAT_PATH)
            os.mkdir(DOC_PATH)
            os.mkdir(LOG_PATH)
            os.mkdir(RES_PATH)
            os.mkdir(SRC_PATH)
            copyfile(APP_PATH_ORIG, APP_PATH_DEST)
            copyfile(MANIFEST_PATH_ORIG, MANIFEST_PATH_DEST)
            copyfile(ENTRYPOINT_PATH_ORIG, ENTRYPOINT_PATH_DEST)
        except OSError as exc:
            print(exc)
            return False
        return True

    def create_json_exec_info(self):
        exec_settings = {}
        exec_settings[JSON_EXECINFO_APPID] = self.args.app_id
        exec_settings[JSON_EXECINFO_APPNAME] = self.args.app_name
        exec_settings[JSON_EXECINFO_SIM] = True
        exec_settings[JSON_EXECINFO_DEVMODE] = True
        exec_settings[JSON_EXECINFO_ROBCONN] = {}
        exec_settings[JSON_EXECINFO_ROBCONN][JSON_EXECINFO_ROBID] = ''
        exec_settings[JSON_EXECINFO_ROBCONN][JSON_EXECINFO_ROBIP] = ''
        exec_settings[JSON_EXECINFO_ROBCONN][JSON_EXECINFO_ROBDDSCH] = 0
        exec_settings[JSON_EXECINFO_ROBCONN][JSON_EXECINFO_ROBSERIAL] = ''
        exec_settings[JSON_EXECINFO_LOG] = {}
        exec_settings[JSON_EXECINFO_LOG][JSON_EXECINFO_LOG_FILEENA] = True
        exec_settings[JSON_EXECINFO_LOG][JSON_EXECINFO_LOG_FOLDER] = 'log'
        try:
            with open(EXECSETTINGS_PATH, 'w', encoding='utf-8') as f:
                json.dump(exec_settings, f, ensure_ascii=False, indent=4)
        except FileNotFoundError:
            log_error(f'Could not write file "{EXECSETTINGS_FILE}".')
            return False
        return True

    def run(self, args, unknownargs):
        self.args = args
        self.unknownargs = unknownargs
        if len(os.listdir(CURRENT_PATH)) != 0:
            log_error('Current directory is not empty.')
            return False
        # Files tree
        log_verbose('Creating application files tree...')
        if not self.create_files_tree():
            log_error(f'Could not create files tree')
            return False
        # Json Manifest

        # Json SDK info
        if not self.create_json_exec_info():
            log_error('Could not json sdk info file')
            return False

        log_verbose('\nCorrect!')
        return True
