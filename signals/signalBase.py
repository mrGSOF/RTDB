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

    ### The _encoder method shall change between different implementation
    def _encode(self, raw):
        """Default encoder function"""
        return raw

    ### The _decoder method shall change between different implementation
    def _decode(self, encoded):
        """Default decoder function"""
        return encoded

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

    def toSeconds(self, idx=0) -> float:
        """Convert from index units to seconds"""
        return self.time[idx-1]

    def getAtIndex(self, idx=0):
        try:
            return self.value[idx-1]
        except IndexError:
            return -1

    def append(self, val) -> None:
        if not self.isPaused():
            if type(val) in (list, tuple):
                for pair in val:
                    self._addValue(pair[0], pair[1])
            else:
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

    def getIndexClosestToTime(self, at):
        if len(self.time) == 0:
            return -1

        if at < 0:
            at += self.getTime() #< convert relative time to abs time

        ### Future value does not exist yet
        if at > self.time[-1]:
            return -1

        ### Too old, older than first data point
        if at < self.time[0]:
            return 0

        ### Find closest value by absolute time
        MAX_POSSIBLE_DT = self.getTime()
        lastDt = MAX_POSSIBLE_DT
        for i in range(len(self.time)):
            dt = abs(at -self.time[i])
            if dt < lastDt:
                lastDt = dt
            else:
                return i -1
        return -1

    def getValueClosestToTime(self, at):
        return self.value[self.getIndexClosestToTime(at)]

    def getValueInterpolatedAtTime(self, at):
        raise NotImplementedError("Interpolation isn't implemented in the base class")

    def isTransition(self, i=0) -> bool:
        """Return True if the signal changes its value (edge detection)"""
        if self.getLen() < abs(i) +1:
            return False
        i -= 1 #< Start from the end
        return self.value[i] != self.value[i-1]

    def isChanging(self, stepsBack=None) -> bool:
        """Return True if the signal changes its value (edge detection)"""
        if stepsBack == None:
            return self.isTransition()
        else:
            chg = False
            for j in range(0, stepsBack):
                chg = chg or self.isTransition(-j)
            return chg

    def isInTolerance(self, i=0, Min=None, Max=None, Ref=None, tol=None) -> bool:
        """Returns True if the signal is within the tolerance at index i"""
        if (Ref != None) and (tol != None):
            Min = Ref -tol
            Max = Ref +tol

        val = self.value[i-1]
        if (Min != None) and (Max != None):
            return (val > Min) and (val < Max)
        elif Min != None:
            return val > Min
        elif Max != None:
            return val < Max

    def isOutOfTolerance(self, i=0, Min=None, Max=None, Ref=None, tol=None) -> bool:
        """Returns True if the signal is within the tolerance at index i"""
        if (Ref != None) and (tol != None):
            Min = Ref -tol
            Max = Ref +tol

        val = self.value[i-1]
        if (Min != None) and (Max != None):
            return (val < Min) and (val > Max)
        elif Min != None:
            return val < Min
        elif Max != None:
            return val > Max

    def isInState(self, i, value) -> bool:
        """Returns True if the signal equal the value at this moment"""
        return self.value[i-1] == value

    def measureTimeInTolerance(self, Min, Max, maxT = None) -> float:
        """Returns the time duration that the signal was within the tolerance (calculation is done backward in sec units)"""
        i = 0 #< Start at last element
        T0 = self.toSeconds(i)
        elements = -(self.getLen() -1)
        # maxT is the maximum time in tolerance needs to be calculated (prevents loop from running longer than needed)
        if maxT == None:
            maxT = T0 -self.toSeconds(elements)
        while self.isInTolerance(i, Min, Max) and (i > elements) and ((T0 -self.toSeconds(i)) < maxT):
            i -= 1 #< Count in reverse
        return T0 -self.toSeconds(i) #< Duration in tolerance

    def measureTimeOutOfTolerance(self, Min, Max, maxT = None) -> bool:
        """Returns the time duration that the signal was outside the tolerance (calculation is done backward in sec units)"""
        i = 0 #< Start at last element
        T0 = self.toSeconds(i)
        elements = -(self.getLen() -1)
        # maxT is the maximum time in tolerance needs to be calculated (prevents loop from running longer than needed)
        if maxT == None:
            maxT = T0 -self.toSeconds(elements)
        while self.isOutOfTolerance(i, Min, Max) and (i > elements) and ((T0 -self.toSeconds(i)) < maxT):
            i -= 1 #< Count in reverse
        return T0 -self.toSeconds(i) #< Duration outside of tolerance

if __name__ == "__main__":
    import importlib.util, os, sys
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
        pysole.probe(runRemainingCode=True, printStartupCode=False, fontSize=12)

    time = ut.Clock(100.12)
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
    ut.test("Element at 0.18 sec", 3, signal.getAt(-0.22))
    ut.test("Element at 0.3 sec",  4, signal.getAt(-0.1))

    ut.test("Latest -3 element", 1, signal.getAtIndex(-3))
    ut.test("Latest -2 element", 2, signal.getAtIndex(-2))
    ut.test("Latest -1 element", 3, signal.getAtIndex(-1))
    ut.test("Latest -0 element", 4, signal.getAtIndex(0))


    ut.test("isInState(-1,3) == True", True, signal.isInState(-1,3))
    ut.test("isInState(0,4) == True", True, signal.isInState(0,4))
    ut.test("isInState(5) == False", False, signal.isInState(0,5))
    ut.test("isChanging() == True", True, signal.isChanging())
    signal.append(4)
    ut.test("isChanging() == False", False, signal.isChanging())
    ut.test("isChanging(3) == True", True, signal.isChanging(3))

    ut.test("Duration between 5 to 2 is 0.3", 0.3, signal.measureTimeInTolerance(Min=2, Max=5, maxT=None), tol=0.01)
    ut.test("Duration bigger than 0 0.4", 0.4, signal.measureTimeOutOfTolerance(Min=None, Max=0, maxT=None), tol=0.01)
    signal.print()

    print(signal.getHistory())
    print(signal.getHistory(stIdx=0, endIdx=1))

    signal.append(((0.5,5),(0.6,6),(0.7,7)))
    signal.print()
