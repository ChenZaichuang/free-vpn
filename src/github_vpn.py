import logging
import subprocess
from time import sleep
import pexpect
import json
import sys
from .constant import RESOURCE_FOLDER
from .utils import run_bash


class GithubVPN:

    def __init__(self):
        with open(f'{RESOURCE_FOLDER}/config.json') as f:
            self.config = json.load(f)
            self.codespace = self.config['codespace']
            self.github_repo = self.config['github_repo']
            self.github_repo_branch = self.config['github_repo_branch']
        self.ssh_session = None
        self.process = None

    def update_codespace(self, codespace):
        self.config['codespace'] = codespace
        with open(f'{RESOURCE_FOLDER}/config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def delete_all_existing_codespaces(self):
        logging.info('开始清理GitHub codespace')
        result = run_bash(f'gh codespace list --json name', print_output_realtime=False, timeout=60)
        # codespace_str = result.stdout.strip()
        # logging.info(f'codespace_str: {codespace_str}')
        # sleep(999)
        for codespace in json.loads(result.stdout.strip()):
            logging.info('开始删除codespace: ' + codespace['name'])
            run_bash(f'gh codespace delete -c ' + codespace['name'], print_output_realtime=True, timeout=30)

    def create_new_codespace(self):
        logging.info('开始创建GitHub codespace')
        cmd = f"gh codespace create -R {self.github_repo} -b {self.github_repo_branch} --default-permissions --idle-timeout '5m' -l 'SouthEastAsia' -m 'basicLinux32gb'"
        result = run_bash(cmd, print_output_realtime=False, timeout=60)
        codespace = result.stdout.strip()
        self.update_codespace(codespace)
        return codespace
        
    def start(self):
        # self.delete_all_existing_codespaces()
        # codespace = self.create_new_codespace()

        codespace = self.codespace

        for _ in range(3):
            logging.info(f'开始登陆GitHub codespace: {codespace}')
            # sleep(10)
            print(f'gh codespace ssh -c {codespace}')
            # exit(0)
            self.ssh_session = pexpect.spawn(f'gh codespace ssh -c {codespace}', timeout=90, logfile=sys.stdout.buffer)
            try:
                self.ssh_session.expect(['/workspaces/'])
            except Exception as e:
                # 获取输出，包括标准错误输出
                err_msg = self.ssh_session.before.decode()

                logging.error(f'报错信息: {err_msg}')

                if 'HTTP 404: Not Found' in err_msg:
                    logging.error('codebase找不到了，开始重新创建...')
                    self.delete_all_existing_codespaces()
                    codespace = self.create_new_codespace()
                    continue

                logging.error('\n\n！！！！！！【Github登陆超时】！！！！！！\n\n')
                sys.exit(1)

            if 'error getting ssh' in self.ssh_session.before.decode() or \
                'error connecting to codespace' in self.ssh_session.before.decode() or \
                'error making request' in self.ssh_session.before.decode():
                logging.error(self.ssh_session.before.decode())
                logging.error('\n\n！！！！！！【Github登陆失败】！！！！！！\n\n')
                sys.exit(1)
            logging.info('开始启动GitHub的v2ray')
            self.ssh_session.sendline('./v2ray')
            logging.info('开始设置GitHub端口映射')
            self.process = subprocess.Popen(f'gh codespace ports forward 8888:8888 -c {codespace}', shell=True)
            logging.info('成功启动GitHub VPN')
            sleep(3)
            break

    def stop(self):
        logging.info('开始停止GitHub ssh')
        self.ssh_session.close()
        logging.info('开始停止GitHub端口映射')
        self.process.terminate()
        self.process.wait()
        logging.info('开始停止GitHub codespace')
        run_bash(f'gh codespace stop -c {self.codespace}')
        # self.delete_all_existing_codespaces()
        logging.info('成功停止GitHub VPN')
