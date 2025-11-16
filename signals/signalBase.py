## By: Guy Soffer (GSOF) 11/Nov/2025
__version__ = "1.0.0"
__author__ = "Guy Soffer"
__copyright__ = ""
__credits__ = [""]
__license__ = "MIT"
__maintainer__ = ""
__email__ = "gsoffer@yahoo.com"
__status__ = "Development"

from collections import deque

def encode(raw):
    return raw

def decode(encoded):
    return encoded

class signalBase():
    def __init__(self, maxHistorySize=32, typeName="Base", isPaused=None, getTime=None):
        self._typeName = str(typeName)
        self.time = deque(maxlen=maxHistorySize)
        self.value = deque(maxlen=maxHistorySize)
        self.setIsPaused(isPaused) #< Reference to function
        self.setGetTime(getTime)   #< Reference to system time

    def print(self):
        s = "Type: %s\n"%(self._typeName)
        s += "time | value\n"
        for i in range(len(self.time)):
            s += "%1.3f | %1.3f\n"%(self.time[i], self.value[i])
        print("\n"+s)

    def setIsPaused(self, isPaused):
        self._isPaused = isPaused

    def setGetTime(self, getTime):
        self.getTime = getTime

    def isPaused(self) -> bool:
        if (self._isPaused == None):
            return False
        return self._isPaused()

    def _addValue(self, time, val) -> None:
        self.time.append(time)
        self.value.append(val)

    def getMaxLen(self) -> int:
        return self.time.maxlen

    def getLen(self) -> int:
        return len(self.time)

    def getType(self) -> str:
        return self._typeName

    def getHistory(self, stIdx=0, endIdx=-1):
        if endIdx == -1:
            endIdx = self.getLen()
        return list(zip(list(self.time)[stIdx:endIdx], list(self.value)[stIdx:endIdx]))

    def getValueAtIndex(self, idx):
        return self.value.get(idx,-1)

    def append(self, val) -> None:
        if not self.isPaused():
            self._addValue(self.getTime(), val)

    def appendEncoded(self, val) -> None:
        self.append(val)

    def getAt(self, at):
        return self.getValueClosestToTime(at)

    def getRawAt(self, at):
        """Return the encoded value"""
        return self.getAt(at)

    def getLatest(self):
        return self.value[-1]

    def getValueClosestToTime(self, at):
        if len(self.time) == 0:
            return -1

        if at < 0:
            at += self.getTime() #< convert relative time to abs time

        ### Future value does not exist yet
        if at > self.time[-1]:
            return self.value[-1]

        ### Too old, older than first data point
        if at < self.time[0]:
            return self.value[0]

        ### Find closest value by absolute time
        MAX_POSSIBLE_DT = self.getTime()
        lastDt = MAX_POSSIBLE_DT
        for i in range(len(self.time)):
            dt = abs(at -self.time[i])
            if dt < lastDt:
                lastDt = dt
            else:
                return self.value[i -1]
        return self.value[-1]

    def getValueInterpolatedAtTime(self, at):
        raise NotImplementedError("Interpolation isn't implemented in the base class")

if __name__ == "__main__":
    import importlib.util, os, sys, time
    mdl = ""
    path = os.path.join("../unitTest", "test.py" )
    #print(path)
    spec = importlib.util.spec_from_file_location(mdl, path)
    #print(spec)
    ut = importlib.util.module_from_spec(spec)
    sys.modules[mdl] = ut
    spec.loader.exec_module(ut)

    try:
        import pysole
    except:
        pysole = False
    if pysole:
        pysole.probe(runRemainingCode=True, printStartupCode=False, fontSize=16)

    signal = signalBase(maxHistorySize=6, getTime=time.time)
    Tst = time.time()
    for i in range(4):
        signal.append(i+1)
        time.sleep(0.1)
    Tend = time.time()

    ut.test("First element", 1, signal.getAt(Tst))
    ut.test("Last element", 4, signal.getAt(Tend))
    ut.test("Element at 0.12 sec", 2, signal.getAt(Tst +0.12))
    ut.test("Element at 0.18 sec", 3, signal.getAt(Tst +0.18))
    ut.test("Element at 0.28 sec", 3, signal.getAt(-0.22))
    ut.test("Element at 0.3 sec",  4, signal.getAt(-0.1))
    signal.print()

    print(signal.getHistory())
    print(signal.getHistory(stIdx=0, endIdx=1))
