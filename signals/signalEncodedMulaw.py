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
from signalEncodedBase import signalEncodedBase #< The Encoded base class
from processing.MuLaw import encode             #< The MuLaw encoder
from processing.MuLaw import decode             #< The MuLaw decoder

class signalAudioMulaw(signalEncodedBase):
    def __init__(self, maxHistorySize=32, isPaused=None, getTime=None):
        super().__init__(maxHistorySize, "EncodedMuLaw", isPaused, getTime)

    ### Overwrite with to pass value through the MuLaw encoder 
    def _encode(self, raw):
        return encode(raw)

    ### Overwrite with to pass value through the MuLaw decoder 
    def _decode(self, encoded):
        return decode(encoded)

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
    signal = signalAudioMulaw(maxHistorySize=32, getTime=time.time)
    Tst = time.time()
    for i in range(0,15):
        signal.append(-(2**(15-i)))
        time.sleep(0.1)
    for i in range(16):
        signal.append(2**i)
        time.sleep(0.1)
    Tend = time.time()

    print(signal.getHistory())
    print(signal.getHistory(stIdx=0, endIdx=1))
    signal.printRaw()
    signal.print()

    ut.test("First element", -31373, signal.getAt(Tst))
    ut.test("Last element", 31373, signal.getAt(Tend))
    ut.test("Element at 0.12 sec", -16319, signal.getAt(Tst +0.12))
    ut.test("Element at 0.18 sec", -8095, signal.getAt(Tst +0.18))
    ut.test("Element at -0.22 sec from the latest", 16319, signal.getAt(-0.22))
    ut.test("Element at -0.10 sec from the latest",  31373, signal.getAt(-0.1))
