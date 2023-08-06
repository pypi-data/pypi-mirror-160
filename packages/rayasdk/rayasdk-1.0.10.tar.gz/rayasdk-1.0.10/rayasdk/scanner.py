# Copyright 2020 Unlimited Robotics

import json
from tabulate import tabulate

from rayasdk.container_handlers.docker_handler import scanner
from rayasdk.logger import log_error, log_info, log_verbose
from rayasdk.constants import *


class URScanner:
    COMMAND = 'scan'

    def __init__(self):
        pass

    def init_parser(self, subparser):
        self.parser = subparser.add_parser(type(self).COMMAND, help="discover robots in the local network.")

    def run(self, args, unknownargs):
        self.args = args
        self.unknownargs = unknownargs
        log_info('Scanning local network for robots (press Ctrl+C to stop)...', )
        robots_info_dict = scanner(1, 100)
        robots_info = []

        for robot_id in robots_info_dict:
            robots_info.append([
                robot_id,
                robots_info_dict[robot_id][JSON_SCAN_SERIAL],
                robots_info_dict[robot_id][JSON_SCAN_DDSCH],
                str(robots_info_dict[robot_id][JSON_SCAN_IP]),
            ])

        # Write json output file
        try:
            with open(LAST_SCANNING_PATH, 'w', encoding='utf-8') as f:
                json.dump(robots_info_dict, f, ensure_ascii=False, indent=4)
        except FileNotFoundError:
            log_error(f'Could not write file {LAST_SCANNING_PATH} .')
            return False

        # Screen out all the robot found in scan
        if robots_info:
            log_info('')
            log_info(tabulate(robots_info, headers=['Robot ID', 'Serial', 'DDS Domain', 'IP Address']))
        else:
            log_info('No robots found.')

        log_verbose('\nCorrect!')
        return True
