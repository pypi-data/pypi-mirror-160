# Copyright 2020 Unlimited Robotics

import tempfile
import platform
from pathlib import Path

# Json SCAN Keys
JSON_SCAN_IP = 'ip-address'
JSON_SCAN_SERIAL = 'serial'
JSON_SCAN_DDSCH = 'dds-domain'

# Json SDK Info Keys
JSON_EXECINFO_APPID = 'app-id'
JSON_EXECINFO_APPNAME = 'app-name'
JSON_EXECINFO_SIM = 'simulation'
JSON_EXECINFO_DEVMODE = 'dev-mode'
JSON_EXECINFO_ROBCONN = 'robot-connection'
JSON_EXECINFO_ROBID = 'robot-id'
JSON_EXECINFO_ROBIP = 'ip-address'
JSON_EXECINFO_ROBDDSCH = 'dds-domain'
JSON_EXECINFO_ROBSERIAL = 'robot-serial'
JSON_EXECINFO_LOG = 'logging'
JSON_EXECINFO_LOG_FILEENA = 'file_enabled'
JSON_EXECINFO_LOG_FOLDER = 'folder'

# folders
TEMP_URSDK_FOLDER = 'ursdk'
TEMPLATES_FOLDER = 'template'
DAT_FOLDER = 'dat'
DOC_FOLDER = 'doc'
LOG_FOLDER = 'log'
RES_FOLDER = 'res'
SRC_FOLDER = 'src'

# files
LAST_SCANNING_FILE = 'last_scanning.json'
ENTRYPOINT_FILE = '__main__.py'
APP_FILE = 'app.py'
MANIFEST_FILE = 'manifest.json'
EXECSETTINGS_FILE = 'exec_settings.json'

# system paths
TEMP_PATH = Path(tempfile.gettempdir())
CURRENT_PATH = Path().absolute()
URSDK_PATH = Path(__file__).parent.absolute()
UR_HOME = Path.home() / '.ur'

# derived folder paths
URSDK_TEMP_PATH = TEMP_PATH / TEMP_URSDK_FOLDER
TEMPLATES_PATH = URSDK_PATH / TEMPLATES_FOLDER
DAT_PATH = CURRENT_PATH / DAT_FOLDER
DOC_PATH = CURRENT_PATH / DOC_FOLDER
LOG_PATH = CURRENT_PATH / LOG_FOLDER
RES_PATH = CURRENT_PATH / RES_FOLDER
SRC_PATH = CURRENT_PATH / SRC_FOLDER

# derived files paths
LAST_SCANNING_PATH = URSDK_TEMP_PATH / LAST_SCANNING_FILE
ENTRYPOINT_PATH_ORIG = TEMPLATES_PATH / ENTRYPOINT_FILE
ENTRYPOINT_PATH_DEST = CURRENT_PATH / ENTRYPOINT_FILE
APP_PATH_ORIG = TEMPLATES_PATH / APP_FILE
APP_PATH_DEST = SRC_PATH / APP_FILE
MANIFEST_PATH_ORIG = TEMPLATES_PATH / MANIFEST_FILE
MANIFEST_PATH_DEST = CURRENT_PATH / MANIFEST_FILE
EXECSETTINGS_PATH = CURRENT_PATH / EXECSETTINGS_FILE

RAYASIM_UI_URL = 'https://chest-web.web.app/app/ex_ui_controller'

# Docker Environment
RAYAENV_DOCKER_IMGNAME = 'raya_os'
RAYAENV_DOCKER_VERSION = '1.0.4'
RAYAENV_DOCKER_URL = 'https://storage.googleapis.com/raya_files/Common/docker_images/raya_os_1.0.4.tar'
RAYAENV_DOCKER_SHA256 = 'd3e23ecf22f75a899a6e45bf9f3f3c2bfe6507923843df26803148ad907700d7'
RAYAENV_DOCKER_IMGFILE = f'{RAYAENV_DOCKER_IMGNAME}_{RAYAENV_DOCKER_VERSION}.tar'
RAYAENV_DOCKER_IMGPATH = URSDK_TEMP_PATH / RAYAENV_DOCKER_IMGFILE

RAYAENV_DOCKER_CONTAINERPREFIX = 'raya_os'

# Gary Simulator
GARYSIM_VERSION = '1.0.3'

if platform.system() == 'Linux':
    GARYSIM_URL = 'https://storage.googleapis.com/raya_files/Linux/raya_simulator_1.0.3_linux.tar.gz'
    GARYSIM_SHA256 = 'fc5a36929abeceffd6f0c341ad5bff942d8e94b0c8f61fc62efe17e6d4a7a225'

    SIMS_HOME = UR_HOME / 'simulator'
    SIM_PATH = SIMS_HOME / f'raya_simulator_{GARYSIM_VERSION}_linux'
    SIM_VERSION_FILE = SIM_PATH / 'VERSION.txt'
    SIM_TARPATH = SIMS_HOME / f'raya_simulator_{GARYSIM_VERSION}_linux.tar.gz'
    SIM_BINARY = SIM_PATH / 'Linux.x86_64'

elif platform.system() == 'Windows':
    GARYSIM_URL = 'https://storage.googleapis.com/raya_files/Windows/raya_simulator_1.0.3_windows.tar.gz'
    GARYSIM_SHA256 = 'a66aa2812a556322d369a1e639d101d69f06ca77470a52ab6063b6df11d3180a'

    SIMS_HOME = UR_HOME / 'simulator'
    SIM_PATH = SIMS_HOME / f'raya_simulator_{GARYSIM_VERSION}_windows'
    SIM_VERSION_FILE = SIM_PATH / 'VERSION.txt'
    SIM_TARPATH = SIMS_HOME / f'raya_simulator_{GARYSIM_VERSION}_windows.tar.gz'
    SIM_BINARY = SIM_PATH / 'Windows.exe'

# TODO: MAC version

# https://storage.googleapis.com/raya_files/Mac/raya_simulator_1.0.2_mac.tar.gz
# 