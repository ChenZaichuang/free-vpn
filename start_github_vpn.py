import signal
import sys
from time import sleep
from src.github_vpn import GithubVPN

if __name__ == '__main__':
    github_vpn = GithubVPN()
    github_vpn.start()

    def signal_handler(sig, frame):
        github_vpn.stop()
        sys.exit(0)

    for sig in [signal.SIGINT, signal.SIGTERM]:
        signal.signal(sig, signal_handler)

    while True:
        sleep(99999)
