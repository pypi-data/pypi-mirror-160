from enum import Enum

verbose = False
quiet = False

class LogLevels(Enum):
    VERBOSE = 1
    INFO = 2
    ERROR = 3

def set_logger_level(_verbose, _quiet):
    global verbose, quiet
    verbose = _verbose
    quiet = _quiet

def log(level, msg, end='\n', flush=False):
    if not quiet:
        if level==LogLevels.INFO or (level==LogLevels.VERBOSE and verbose):
            print(msg, end=end, flush=flush)
    if level==LogLevels.ERROR:
        print(msg, end=end, flush=flush)

def log_verbose(msg, end='\n', flush=False):
    log(LogLevels.VERBOSE, msg, end=end, flush=flush)

def log_info(msg, end='\n', flush=False):
    log(LogLevels.INFO, msg, end=end, flush=flush)

def log_error(msg, end='\n', flush=False):
    log(LogLevels.ERROR, 'ERROR: '+msg, end=end, flush=flush)
