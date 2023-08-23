from subprocess import PIPE, STDOUT, CalledProcessError, CompletedProcess, Popen


def call_script(command, logger):
    with Popen(command, text=True, stdout=PIPE, stderr=STDOUT) as process:
        for line in process.stdout:
            logger.info(line[:-1])
    retcode = process.poll()
    if retcode:
        raise CalledProcessError(retcode, process.args)
    return CompletedProcess(process.args, retcode)
