import subprocess
import threading

from flyers import assets
from flyers.logs import logger


class RunShellResult(object):
    def __init__(self, output, status, message, stdout=None, stderr=None):
        self.output = output
        self.status = status
        self.message = message
        self.stdout = stdout
        self.stderr = stderr


def run_shell(cmd: str) -> bool:
    assets.check_blank(cmd, 'cmd')
    return subprocess.call(cmd, shell=True) == 0


def async_run_shell(cmd: str, callback=None) -> str:
    """
    Executes command asynchronously
    :param cmd: Command
    :param callback:
    :return: Thread name
    """
    assets.check_blank(cmd, 'cmd')

    def runnable():
        ret = subprocess.call(cmd, shell=True) == 0
        if callback:
            callback(ret)

    t = threading.Thread(target=runnable)
    t.start()
    return t.getName()


def run_shell_with_result(cmd: str) -> (str, str):
    assets.check_blank(cmd, 'cmd')

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output = process.communicate()
    if len(output) != 2:
        return RunShellResult(output, status=-1, message='The output is not expected')

    stdout, stderr = str(output[0], encoding='utf-8'), str(output[1], encoding='utf-8')

    logger.debug("Run <{}> command, stdout: {}".format(cmd, stdout))
    logger.debug("Run <{}> command, stderr: {}".format(cmd, stderr))
    return RunShellResult(output, status=0, message=None, stdout=stdout, stderr=stderr)


def async_run_shell_with_result(cmd, callback):
    def listener():
        result = run_shell(cmd)
        callback(result)

    t = threading.Thread(target=listener)
    t.start()
