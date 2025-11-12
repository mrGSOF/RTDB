import sys, os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__))))
from signalBase import signalBase

class signalDiscrete(signalBase):
    def __init__(self, maxHistorySize=32, isPaused=None):
        super().__init__(maxHistorySize, "Discrete", isPaused)

