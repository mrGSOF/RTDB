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
from processing import MuLaw

##class decoder(MuLaw):
##    def __init__(self, rawSignal):
##        self.raw = rawSignal
##
##    def getAt(self, at):
##        return
##
##class encoder(MuLaw):
##    def __init__(self, rawSignal):
##        self.raw = rawSignal
##
##    def append(self, val):
##        """Encode and append to signal buffer"""
##        return

class signalAudioMulaw(signalBase):
    def __init__(self, maxHistorySize=32, isPaused=None, getTime=None):
        super().__init__(maxHistorySize, "Discrete", isPaused, getTime)
        self.mulaw = MuLaw.MuLaw()

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
            s += "%1.3f | %1.3f\n"%(self.time[i], self.mulaw.decoder(self.value[i]))
        print("\n"+s)

    def appendEncoded(self, val) -> None:
        """Append an encoded value"""
        super().append( val )

    def append(self, val) -> None:
        """Input value will be encoded and appended"""
        self.appendEncoded( self.mulaw.encoder(val) )

    def getRawAtIndex(self, at):
        """"""
        return

    def getRawAt(self, at):
        """Return the encoded value"""
        return super().getAt(at)

    def getRawLatest(self):
        """"""
        return super().getLatest()

    def getAtIndex(self, idx):
        """Decoded value"""
        return self.mulaw.decoder(super().getAtIndex(idx))

    def getAt(self, at):
        """Decoded value"""
        return self.mulaw.decoder(super().getAt(at))

    def getLatest(self):
        """Decoded value"""
        return self.mulaw.decoder(super().getLatest())

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
#    if pysole:
#        pysole.probe(runRemainingCode=True, printStartupCode=False, fontSize=16)

    signal = signalAudioMulaw(maxHistorySize=32, getTime=time.time)
    Tst = time.time()
    for i in range(0,15):
        signal.append(-(2**(15-i)))
        time.sleep(0.1)
    for i in range(16):
        signal.append(2**i)
        time.sleep(0.1)
    Tend = time.time()

    ut.test("First element", 0, signal.getAt(Tst))
    ut.test("Last element", 8, signal.getAt(Tend))
    ut.test("Element at 0.12 sec", 0, signal.getAt(Tst +0.12))
    ut.test("Element at 0.18 sec", 8, signal.getAt(Tst +0.18))
    ut.test("Element at 0.28 sec", 8, signal.getAt(-0.22))
    ut.test("Element at 0.3 sec",  8, signal.getAt(-0.1))
    signal.printRaw()
    signal.print()

    print(signal.getHistory())
    print(signal.getHistory(stIdx=0, endIdx=1))
