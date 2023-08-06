import docker
import hashlib
import pathlib
import subprocess
import json
import os
import shutil
import tarfile
import progressbar
import urllib.request
from simple_file_checksum import get_checksum

from rayasdk.constants import *
from rayasdk.logger import log, LogLevels, log_info, log_error, log_verbose
from rayasdk.logger import set_logger_level
from rayasdk import __version__ as RAYA_VERSION


raya_imgs = {}
docker_client: docker.DockerClient = None


class MyProgressBar():
    def __init__(self):
        self.pbar = None

    def __call__(self, block_num, block_size, total_size):
        if not self.pbar:
            self.pbar=progressbar.ProgressBar(maxval=total_size)
            self.pbar.start()

        downloaded = block_num * block_size
        if downloaded < total_size:
            self.pbar.update(downloaded)
        else:
            self.pbar.finish()


def launch_command(bash_command, suffix, output_file='', silent=False, 
                                        working_dir='', volumes=[], ports=[]):
    complete_bash_command = ''
    if working_dir:
        complete_bash_command += f'cd {working_dir} && '
    complete_bash_command += 'source /opt/raya_os/setup_raya.bash && '
    complete_bash_command += f'{bash_command}'
    if platform.system() == 'Linux':
        sh_command = f'/bin/bash -c "{complete_bash_command}"'
    else: #Windows
        sh_command = f'/bin/bash -c \'{complete_bash_command}\''
    docker_command = ''

    if platform.system() == 'Linux':
        docker_command += 'xhost +local:root >> /dev/null && '
        docker_command += 'docker run -it --rm --privileged --network host '
        docker_command += '-v /tmp/.X11-unix:/tmp/.X11-unix:ro '
        docker_command += '-e DISPLAY=$DISPLAY --env QT_X11_NO_MITSHM=1 --tty '
        docker_command += f'--name {RAYAENV_DOCKER_CONTAINERPREFIX}_{suffix} '
    else: #Windows
        docker_command += 'docker run -it --rm --privileged '
        docker_command += '-v /tmp/.X11-unix:/tmp/.X11-unix:ro '
        docker_command += '-e DISPLAY=host.docker.internal:0.0 --tty '
        docker_command += f'--name {RAYAENV_DOCKER_CONTAINERPREFIX}_{suffix} '
    # TODO: Define for MAC

    for volume in volumes:
        docker_command += f'-v \'{volume}\' '

    for port in ports:
        docker_command += f'-p {port} '

    docker_command += f'{RAYAENV_DOCKER_IMGNAME}:{RAYAENV_DOCKER_VERSION} '
    docker_command += f'{sh_command} '

    if silent:
        if output_file:
            docker_command += f'> {str(output_file)}'
        else:
            docker_command += f'> /dev/null'       
    else:
        if output_file:
            docker_command += f'| tee {str(output_file)}'

    if platform.system() == 'Windows':
        docker_command = f'powershell "{docker_command}"'

    # print(docker_command)

    ret = subprocess.call(docker_command, shell=True)


def download_simulator():
    response = input(('Correct simulator version not found, do you want to'
                                                    ' download it? [Y/n]:'))
    if response not in ['Y', 'y', '']:
        print('aborted')
        return
    print('Removing old versions...')
    try:
        shutil.rmtree(SIMS_HOME)
    except FileNotFoundError:
        pass
    print(f'Downloading Ra-Ya SDK v{GARYSIM_VERSION}...')
    SIMS_HOME.mkdir(parents=True, exist_ok=True)
    try:
        urllib.request.urlretrieve(GARYSIM_URL, str(SIM_TARPATH), 
                                                               MyProgressBar())
    except urllib.error.HTTPError:
        log_error('Download error, try again.')
        return False
    log_info(f'Checking downloaded file...')
    try:
        sha256 = get_checksum(SIM_TARPATH, algorithm="SHA256")
    except FileNotFoundError:
        log_error('Download error, try again.')
        return False
    if GARYSIM_SHA256 != sha256:
        log_error('Download error, try again.')
        return False
    log_info(f'Extracting...')
    simtar = tarfile.open(SIM_TARPATH)
    simtar.extractall(SIMS_HOME)
    # log_info(f'Simulator installed, you can run \'rayasdk simulator\' again')
    return True
    

def run_simulator_bridge():
    
    if not SIM_VERSION_FILE.is_file():
        if not download_simulator():
            return
    sim_file = open(SIM_VERSION_FILE, 'r')
    version = sim_file.readlines()[0]
    sim_file.close()
    if GARYSIM_VERSION not in version:
        if not download_simulator():
            return

    p = subprocess.Popen([str(SIM_BINARY)])

    launch_command(
            ('/opt/raya_os/run_bridge_unity.sh'),
            suffix='simbridge',
            working_dir='/root', 
            ports=['10000:10000', '8789-8890:8789-8890', '8000:8000']
        )
    p.kill()
    p.wait()


def launch_app(app_id, domain, args):
    for container in docker_client.containers.list(all=True):
        if container.name == f'{RAYAENV_DOCKER_CONTAINERPREFIX}_{app_id}':
            container.kill()
            try:
                container.remove()
            except:
                pass

    cmd = f'ROS_DOMAIN_ID={domain} python3 __main__.py ' + ' '.join(args)

    launch_command( cmd, 
                    suffix=app_id, 
                    volumes=[f'{os.getcwd()}:/root/ur/app'], 
                    working_dir='/root/ur/app'
                )


def scanner(min_domain=1, max_domain=100, silent=False):

    for container in docker_client.containers.list(all=True):
        if container.name == f'raya_scanner':
            container.kill()
            try:
                container.remove()
            except:
                pass

    detections = {}
    scan_file = URSDK_TEMP_PATH / 'scan_docker_log.txt'
    launch_command(
            bash_command=('echo ... && ros2 run raya_utils scanner ' 
                          f'{min_domain} {max_domain}'), 
            suffix='scanner', 
            output_file=scan_file, 
            silent=silent
        )
    if not silent:
        log_info('\nFinish scanning')

    try:
        file = open(scan_file, 'r')
        lines = file.readlines()
    except UnicodeDecodeError:
        file = open(scan_file, 'r', encoding='utf_16_le')
        lines = file.readlines()

    for line in lines:
        try:
            if platform.system() == 'Linux':
                line_dict = json.loads(line)
            else: #Windows
                line_dict = json.loads(line.replace('\x00', ''))
            detections[line_dict['id']] = {
                'serial': line_dict['serial'],
                'ip-address': line_dict['ip-address'],
                'dds-domain': line_dict['dds-domain'],
            }
        except json.decoder.JSONDecodeError as e:
            pass
    return detections


def kill_all():
    log_info('Killing all the running Ra-Ya containers...')
    for container in docker_client.containers.list(all=True):
        tags = container.image.tags
        if tags:
            name, tag = tags[0].split(':',1)
            if name=='raya':
                if container.status == 'running':
                    log_info(f'Kill: {container}')    
                    container.kill()
                try:
                    container.remove()
                except:
                    pass


def check_container():
    global raya_imgs, docker_client
    # Check docker installation
    try:
        docker_client = docker.from_env()
    except docker.errors.DockerException:
        log_error(('Docker is not installed or the current user doesn\'t have '
                   'permissions to run it. Please check the Ra-YA '
                   'documentation to install it.'))
        return False
    
    # Check raya images
    for img in docker_client.images.list():
        tags = img.tags
        if tags:
            name, tag = tags[0].split(':',1)
            if name==RAYAENV_DOCKER_IMGNAME:
                raya_imgs[tag] = img

    if RAYAENV_DOCKER_VERSION in raya_imgs:
        return True

    log_info(('Docker image '
                  f'\'{RAYAENV_DOCKER_IMGNAME}:{RAYAENV_DOCKER_VERSION}\' '
                  'not found.'))

    if raya_imgs:
        log_info(('Removing old Ra-Ya containers and images...'))
        for container in docker_client.containers.list(all=True):
            tags = container.image.tags
            if tags:
                name, tag = tags[0].split(':',1)
                if name=='raya':
                    if container.status == 'running':
                        container.kill()
                    try:
                        container.remove()
                    except docker.errors.NotFound:
                        pass
        
        for img_tag in raya_imgs:
            docker_client.images.remove(
                    image=f'{RAYAENV_DOCKER_IMGNAME}:{img_tag}'
                )

    log_info(f'Downloading Ra-Ya OS v{RAYAENV_DOCKER_VERSION} (only once)...')
    try:
        urllib.request.urlretrieve(RAYAENV_DOCKER_URL, str(RAYAENV_DOCKER_IMGPATH),
                                MyProgressBar())
    except urllib.error.HTTPError:
        log_error('Download error, try again.')
        return False
    log_info(f'Checking downloaded file...')
    try:
        sha256 = get_checksum(RAYAENV_DOCKER_IMGPATH, algorithm="SHA256")
    except FileNotFoundError:
        log_error('Download error, try again.')
        return False
    if RAYAENV_DOCKER_SHA256 != sha256:
        log_error('Download error, try again.')
        return False
    log_info(f'Creating image...')
    ret = subprocess.call(
            f'docker load -i {str(RAYAENV_DOCKER_IMGPATH)}', 
            shell=True
        )
    if ret != 0:
        log_error('Error creating the image, try again.')
        return False

    return True

