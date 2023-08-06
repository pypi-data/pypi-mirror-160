# Copyright 2020 Unlimited Robotics
import json

from rayasdk.container_handlers.docker_handler import run_simulator_bridge
from rayasdk.logger import log_error, log_verbose, log_info
from rayasdk.constants import *


class URSimulator:

    COMMAND = 'simulator'


    def __init__(self):
        pass


    def init_parser(self, subparser):
        self.parser = subparser.add_parser(type(self).COMMAND, help="run the simulator bridge.")


    def run(self, args, unknownargs):
        self.args = args
        self.unknownargs = unknownargs
        run_simulator_bridge()
        return True
