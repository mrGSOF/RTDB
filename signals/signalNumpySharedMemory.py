## By: Tzur Soffer (TSOF) 16/March/2026
__version__ = "1.0.0"
__author__ = "Tzur Soffer"
__copyright__ = ""
__credits__ = [""]
__license__ = "MIT"
__maintainer__ = ""
__email__ = "tzur.soffer@gmail.com"
__status__ = "Development"

from multiprocessing import shared_memory
import sys, os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__))))
from signalBase import signalBase
import numpy as np

class signalNumpySharedMemory(signalBase):
    def __init__(self, name, shape, dtype, maxHistorySize=32, isPaused=None, getTime=None):
        super().__init__(maxHistorySize, "NumpySharedMemory", isPaused, getTime)
        try:
            self.shm = shared_memory.SharedMemory(name=name)  #< must use self to avoid getting garbage collected
            print("signal already created, binding to it")
        except FileNotFoundError:
            self.shm = shared_memory.SharedMemory(name=name, create=True, size=int(np.prod(shape) * np.dtype(dtype).itemsize))
            print("Creating signal with name "+self.shm.name)

        self.time = 0
        self.value = np.ndarray(shape, dtype=dtype, buffer=self.shm.buf)

    def print(self):
        print("%1.3f | %1.3f\n"%(self.time, self.value))

    def _addValue(self, time, val) -> None:
        self.time = time
        self.value[:] = val

    def getMaxLen(self) -> int:
        return 1

    def getLen(self) -> int:
        return 1

    def getHistory(self, stIdx=0, endIdx=-1):
        return [(self.time, self.getLatest())]

    def getLatest(self):
        return self.value.copy()

    def getValueAtIndex(self, idx):
        raise NotImplementedError("History isn't implemented in this class")

    def getValueClosestToTime(self, at):
        raise NotImplementedError("History isn't implemented in this class")