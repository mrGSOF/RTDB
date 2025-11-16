## By: Guy Soffer (GSOF) 16/Nov/2025
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
from signalBase import signalBase, encode , decode

class signalEncodedBase(signalBase):
    def __init__(self, maxHistorySize=32, name="EncodedBase", isPaused=None, getTime=None):
        super().__init__(maxHistorySize, name, isPaused, getTime)

    ### The _encoder method shall change between different implemantation
    def _encode(self, raw):
        """Default encoder function"""
        return raw

    ### The _decoder method shall change between different implemantation
    def _decode(self, encoded):
        """Default decoder function"""
        return encoded

    def printRaw(self):
        s = "Type: %s\n"%(self._typeName)
        s += "time | value\n"
        for i in range(len(self.time)):
            s += "%1.3f | %1.3f\n"%(self.time[i], self.value[i])
        print("\n"+s)

    def print(self):
        s = "Type: %s\n"%(self._typeName)
        s += "time | value\n"
        for i in range(len(self.time)):
            s += "%1.3f | %1.3f\n"%(self.time[i], self._decode(self.value[i]))
        print("\n"+s)

    def appendEncoded(self, val) -> None:
        """Append an encoded value"""
        super().append( val )

    def append(self, val) -> None:
        """Input value will be encoded and appended"""
        self.appendEncoded( self._encode(val) )

    def getRawAtIndex(self, at):
        """Return the encoded value at index point"""
        return super().getAtIndex(idx)

    def getRawAt(self, at):
        """Return the encoded value"""
        return super().getAt(at)

    def getRawLatest(self):
        """"""
        return super().getLatest()

    def getAtIndex(self, idx):
        """Decoded value"""
        return self._decode(super().getAtIndex(idx))

    def getAt(self, at):
        """Decoded value"""
        return self._decode(super().getAt(at))

    def getLatest(self):
        """Decoded value"""
        return self._decode(super().getLatest())

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
        pysole.probe(runRemainingCode=True, printStartupCode=False, fontSize=16)

    time = ut.Clock(100.12)
    signal = signalEncodedBase(maxHistorySize=32, getTime=time.time)
    Tst = time.time()
    for i in range(0,15):
        signal.append(-(15-i))
        time.sleep(0.1)
    for i in range(16):
        signal.append(i)
        time.sleep(0.1)
    Tend = time.time()

    print(signal.getHistory())
    print(signal.getHistory(stIdx=0, endIdx=1))
    signal.printRaw()
    signal.print()

    ut.test("First element", -15, signal.getAt(Tst))
    ut.test("Last element", 15, signal.getAt(Tend))
    ut.test("Element at 0.12 sec", -14, signal.getAt(Tst +0.12))
    ut.test("Element at 0.18 sec", -13, signal.getAt(Tst +0.18))
    ut.test("Element at -0.22 sec from the latest", 14, signal.getAt(-0.22))
    ut.test("Element at -0.10 sec from the latest",  15, signal.getAt(-0.1))
