## By: Guy Soffer (GSOF) 11/Nov/2025
__version__ = "1.0.0"
__author__ = "Guy Soffer"
__copyright__ = ""
__credits__ = [""]
__license__ = "MIT"
__maintainer__ = ""
__email__ = "gsoffer@yahoo.com"
__status__ = "Development"

import sys, os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__))))
from signalBase import signalBase

class signalMessage(signalBase):
    def __init__(self, maxHistorySize=32, isPaused=None, getTime=None):
        super().__init__(maxHistorySize, "Message", isPaused, getTime)

