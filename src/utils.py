import logging
import os
import subprocess
import sys
from types import SimpleNamespace
import pexpect


def run_bash(cmd, timeout=3600, raise_exception=True, print_output_realtime=False):
    logging.info(f"Start running cmd: {cmd}\r\n")

    if print_output_realtime:
        process = pexpect.spawn(os.environ.get('SHELL', '/bin/bash'), args=['-c', cmd], timeout=timeout, logfile=sys.stdout.buffer)
        process.expect([pexpect.TIMEOUT,  pexpect.EOF])
        output = process.before.decode('utf-8')
        process.close()
        result = SimpleNamespace(returncode=process.exitstatus, stdout=output, stderr='')
    else:
        process = subprocess.run(f"{cmd}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8",
                                timeout=timeout, executable=os.environ.get('SHELL', '/bin/bash'))
        result = SimpleNamespace(returncode=process.returncode, stdout=process.stdout, stderr=process.stderr)

    if raise_exception and result.returncode != 0:
        raise RuntimeError(f"Run bash command failed :{cmd} | {result.stdout} \n {result.stderr}")
    else:
        logging.info(f"Successfully run cmd: {cmd}\r\n")
    return result
