import json
import logging
import subprocess
from time import sleep
import pexpect
import sys
from .constant import RESOURCE_FOLDER
from .utils import run_bash


class GCPVPN:

    def __init__(self):
        with open(f'{RESOURCE_FOLDER}/config.json') as f:
            config = json.load(f)
            self.gmail = config['gmail']
            self.system = config['system']
        self.ssh_command = None
        self.frp_process = None
        self.ssh_session = None

    def refresh(self):
        logging.info('开始启动frp server')
        self.frp_process = subprocess.Popen(f'cd {RESOURCE_FOLDER}/local/{self.system} && ./frps --config ./frps.toml', shell=True)
        logging.info('开始刷新GCP ssh登陆命令')
        # result = run_bash(f'export ALL_PROXY=socks5://localhost:8888 && gcloud alpha cloud-shell ssh --dry-run --account={self.gmail} --authorize-session', timeout=60)
        # result = run_bash(f'gcloud config set proxy/type socks5 && gcloud config set proxy/address localhost && gcloud config set proxy/port 8888 && gcloud alpha cloud-shell ssh --dry-run --account={self.gmail} --authorize-session', print_output_realtime=True, timeout=12000)
        result = run_bash(f'gcloud config set proxy/type socks5 && gcloud config set proxy/address 192.168.0.8 && gcloud config set proxy/port 9999 && gcloud alpha cloud-shell ssh --dry-run --account={self.gmail} --authorize-session', print_output_realtime=True, timeout=12000)
        # assert result.returncode == 0
        # result = run_bash(f'gcloud alpha cloud-shell ssh --dry-run --account={self.gmail} --authorize-session', print_output_realtime=False, timeout=90)
        # self.ssh_command = 'export ALL_PROXY=socks5://localhost:8888 && ' + result.stdout.strip().replace('/ssh ', '/ssh -R localhost:7100:localhost:7100 ')
        self.ssh_command = result.stdout.strip().replace('/ssh ', '/ssh -R localhost:7100:localhost:7100 ')

    def start(self):
        logging.info(f"开始登陆GCP shell: {self.ssh_command}")
        logging.info(f"请耐心等待...")
        # sleep(999999)
        self.ssh_session = pexpect.spawn(f'bash -c "{self.ssh_command}"', timeout=90, logfile=sys.stdout.buffer)
        # pexpect.TIMEOUT, 
        self.ssh_session.expect(['@cloudshell', pexpect.EOF])
        logging.info('开始启动GCP VPN')
        sleep(3)
        self.ssh_session.sendline('curl -O "https://raw.githubusercontent.com/ChenZaichuang/free-vpn/main/build/install_on_gcp.sh" && bash install_on_gcp.sh zcchen666')
        logging.info('成功启动GCP VPN')

    def stop(self):
        logging.info('开始停止GCP VPN')
        self.frp_process.terminate()
        self.frp_process.wait()
        self.ssh_session.close()
        logging.info('成功停止GCP VPN')
