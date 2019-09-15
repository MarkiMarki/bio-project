try:
    import qnapstats
except ImportError:
    from pip._internal import main as pip

    pip(['install', 'qnapstats'])
from qnapstats import QNAPStats
from ..settings.qnap_routing import *


class QnapHelper:
    def __init__(self, ip=QNAP_IP2, port=QNAP_PORT, username=QNAP_USERNAME2, password=QNAP_PASSWORD2):
        self.qnap = QNAPStats(ip, 443, username, password, verify_ssl=False)
        self.qnap.get_volumes()
        pass
