import functools
import logging
import platform
import os
import signal
import time
import pmg

log = logging.getLogger(__name__)

SIGNALS = {1: 'SIGHUP', 2: 'SIGINT', 15: 'SIGTERM'}

class SignalException(Exception):
    def __init__(self, signum):
        self.signum = signum

class SignalHandler():
    def __init__(self, watch_signals=None):
        self.received_signal = None
        self.raise_exc = False
        self.signaled = False
        for sig in pmg.coalesce(watch_signals, [signal.SIGINT, signal.SIGTERM]):
            signal.signal(sig, self.handle_signal)

    def handle_signal(self, signum, frame):
        self.signaled = True
        self.received_signal = SIGNALS.get(signum, str(signum))
        if self.raise_exc:
            raise SignalException(signum)

    def sleep_interruptably(self, seconds):
        self.raise_exc = True
        try:
            time.sleep(seconds)
            return None
        except SignalException as e:
            return e.signum
        finally:
            self.raise_exc = False

def mainloop(sleep_seconds, exec_condition=None, terminate_on=None):
    def wraploop(func):
        @functools.wraps(func)
        def looping_function(*args, **kwargs):
            sig = SignalHandler(terminate_on)
            if exec_condition is None:
                log.info(f'Main loop started for {func.__name__}; executing every {sleep_seconds} seconds.')
            else:
                log.info(f'Main loop started for {func.__name__}; checking for run condition every {sleep_seconds} seconds.')
            while not sig.signaled:
                if exec_condition is None or exec_condition():
                    func(*args, **kwargs)
                sig.sleep_interruptably(sleep_seconds)
            log.info(f'Main loop terminated after receiving signal {sig.received_signal}.')
        return looping_function
    return wraploop

def get_os_name():
    os_name = f"{platform.system()} {platform.version()}"
    try:
        if os.path.isfile('/etc/os-release'):
            for r in pmg.read_records('/etc/os-release', '\n', '='):
                if r[0] == 'PRETTY_NAME':
                    os_name = r[1][1:-1]
    except Exception:
        pass
    return f'{os_name} ({platform.platform()})'

def get_package_versions(*packages_start_with):
    versions = []
    import pkg_resources
    for pkg in iter(pkg_resources.working_set):
        dist = pkg_resources.get_distribution(pkg)
        if any([dist.project_name.startswith(package_name) for package_name in packages_start_with]):
            versions.append('{} {}'.format(dist.project_name, dist.version))
    return sorted(versions)
