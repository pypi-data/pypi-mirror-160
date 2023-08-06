# Copyright 2020 Unlimited Robotics
import json

from rayasdk.container_handlers.docker_handler import kill_all
from rayasdk.logger import log_error, log_verbose, log_info
from rayasdk.constants import *


class URKiller:

    COMMAND = 'kill'


    def __init__(self):
        pass


    def init_parser(self, subparser):
        self.parser = subparser.add_parser(type(self).COMMAND, help="kills all the running Ra-Ya containers.")


    def run(self, args, unknownargs):
        self.args = args
        self.unknownargs = unknownargs
        kill_all()
        return True
