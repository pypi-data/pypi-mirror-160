# Copyright 2020 Unlimited Robotics
import json

from rayasdk.container_handlers.docker_handler import scanner
from rayasdk.logger import log_error, log_verbose, log_info
from rayasdk.constants import *


class URConnect:

    COMMAND = 'connect'


    def __init__(self):
        pass


    def init_parser(self, subparser):
        self.parser = subparser.add_parser(type(self).COMMAND, help="execute current Raya project.")
        group = self.parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--robot-id', help='robot identificator (from scan list)', type=str)
        group.add_argument('--simulator', help='connect the project to the simulator', action="store_true")


    def robot_available(self, robot_id, domain, serial):
        robots_info_dict = scanner(domain, domain, silent=True)
        if robot_id not in robots_info_dict:
            return False
        if robots_info_dict[robot_id][JSON_SCAN_DDSCH] != domain:
            return False
        if robots_info_dict[robot_id][JSON_SCAN_SERIAL] != serial:
            return False
        return True


    def run(self, args, unknownargs):
        self.args = args
        self.unknownargs = unknownargs
        try:
            with open(EXECSETTINGS_PATH, 'r', encoding='utf-8') as f:
                exec_settings = json.load(f)
        except OSError as exc:
            log_error(f'Could not open "{EXECSETTINGS_FILE}" file, no project initialized in this folder.')
            return False
        if self.args.simulator:
            exec_settings[JSON_EXECINFO_SIM] = True
            exec_settings[JSON_EXECINFO_ROBCONN][JSON_EXECINFO_ROBID] = ''
            exec_settings[JSON_EXECINFO_ROBCONN][JSON_EXECINFO_ROBIP] = ''
            exec_settings[JSON_EXECINFO_ROBCONN][JSON_EXECINFO_ROBDDSCH] = 0
        else:
            robot_id = self.args.robot_id
            try:
                with open(LAST_SCANNING_PATH, 'r', encoding='utf-8') as f:
                    scanned_robots = json.load(f)
            except OSError as exc:
                log_error(f'Could  not get scanning info, execute "ursdk scan" before this command.')
                return False
            try:
                if robot_id in scanned_robots:
                    # check robot connected to the same serial and domain
                    if self.robot_available(
                                robot_id,
                                scanned_robots[robot_id][JSON_SCAN_DDSCH],
                                scanned_robots[robot_id][JSON_SCAN_SERIAL]
                            ):
                        # if robot exists, register it.
                        exec_settings[JSON_EXECINFO_SIM] = False
                        if JSON_EXECINFO_ROBCONN not in  exec_settings:
                            exec_settings[JSON_EXECINFO_ROBCONN] = {}    
                        exec_settings[JSON_EXECINFO_ROBCONN][JSON_EXECINFO_ROBID] = \
                            robot_id
                        exec_settings[JSON_EXECINFO_ROBCONN][JSON_EXECINFO_ROBIP] = \
                            scanned_robots[robot_id][JSON_SCAN_IP]
                        exec_settings[JSON_EXECINFO_ROBCONN][JSON_EXECINFO_ROBDDSCH] = \
                            scanned_robots[robot_id][JSON_SCAN_DDSCH]
                        exec_settings[JSON_EXECINFO_ROBCONN][JSON_EXECINFO_ROBSERIAL] = \
                            scanned_robots[robot_id][JSON_SCAN_SERIAL]
                        log_info(f'You have successfully connected to {robot_id}')
                    else:
                        log_error(f'{exec_settings[JSON_EXECINFO_ROBCONN][JSON_EXECINFO_ROBID]} is not longer available')
                else:
                    log_error(f'Robot ID "{robot_id}" not found in scan info, verify it or scan again.')
                    return False
            except KeyError as e:
                print(e)
                log_error(f'Scanning info malformed, please scan again by running "rayasdk scan".')
                return False
        try:
            with open(EXECSETTINGS_PATH, 'w', encoding='utf-8') as f:
                json.dump(exec_settings, f, ensure_ascii=False, indent=4)
        except FileNotFoundError:
            log_error(f'Could not write file "{EXECSETTINGS_FILE}".')
            return False

        log_verbose('\nCorrect!')
        return True
