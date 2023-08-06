# Copyright 2020 Unlimited Robotics
import json
import subprocess
import sys
import os
from rayasdk.constants import *
from rayasdk.logger import *
from rayasdk.container_handlers.docker_handler import scanner, launch_app


class URRunner:

    COMMAND = 'run'


    def __init__(self):
        pass


    def init_parser(self, subparser):
        self.parser = subparser.add_parser(type(self).COMMAND,
                                           help="connect current raya project to a robot or simulator.")


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
        # open exec_settings file
        try:
            with open(EXECSETTINGS_PATH, 'r', encoding='utf-8') as f:
                exec_settings = json.load(f)
        except OSError as exc:
            log_error(f'Could  not open "{EXECSETTINGS_FILE}" file, no project initialized in this folder.')
            return False

        app_id = exec_settings[JSON_EXECINFO_APPID]
        try:
            robot_id = exec_settings[JSON_EXECINFO_ROBCONN][JSON_EXECINFO_ROBID]
            dds_domain = exec_settings[JSON_EXECINFO_ROBCONN][JSON_EXECINFO_ROBDDSCH]
            robot_serial = exec_settings[JSON_EXECINFO_ROBCONN][JSON_EXECINFO_ROBSERIAL]
        except KeyError:
            print("Not connected to any robot, run \'rayasdk connect\' first")
            return

        # Verify exec_settings configured, if so, check if robot is still available
        if robot_id == '':
            print("Not connected to any robot, run \'rayasdk connect\' first")
            return
        
        if not self.robot_available(robot_id, dds_domain, robot_serial):
            print(f"Robot \'{robot_id}\' with serial \'{robot_serial} is not available, run \'rayasdk connect\' again")
            return
        
        launch_app(app_id, dds_domain, self.unknownargs)
