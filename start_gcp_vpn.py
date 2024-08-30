import signal
import sys
from time import sleep

from src.gcp_vpn import GCPVPN
from src.github_vpn import GithubVPN

if __name__ == '__main__':
    # github_vpn = GithubVPN()
    gcp_vpn = GCPVPN()

    # github_vpn.start()
    gcp_vpn.refresh()
    # github_vpn.stop()
    try:
        gcp_vpn.start()
    except:
        gcp_vpn.stop()
        sys.exit(1)

    def signal_handler(sig, frame):
        gcp_vpn.stop()
        sys.exit(0)

    for sig in [signal.SIGINT, signal.SIGTERM]:
        signal.signal(sig, signal_handler)

    while True:
        sleep(99999)

