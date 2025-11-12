## By: Guy Soffer (GSOF) 11/Nov/2025
__version__ = "1.0.0"
__author__ = "Guy Soffer"
__copyright__ = ""
__credits__ = [""]
__license__ = "MIT"
__maintainer__ = ""
__email__ = "gsoffer@yahoo.com"
__status__ = "Development"

import json

class RTDB(dict):
    def __init__(self, getTime=None):
        super().__init__()
        self.pause()
        self.setGetTime(getTime)
        self.resetTime()

    def print(self) -> None:
        """Print the structure of the RTDB"""
        s = "RTDB contant:\n"
        for i, key in enumerate(self.keys()):
            sig = self[key]
            s += "%3d. %s (%s %d/%d)\n"%(i+1,
                                         key,
                                         sig.getType(),
                                         sig.getLen(),
                                         sig.getMaxLen()
                                         )
        print("\n"+s)
        
    def pause(self) -> None:
        """Disable all signals from new appendings"""
        self.pause = True

    def resume(self) -> None:
        """Enable all signals for new appendings"""
        self.pause = False

    def isPaused(self) -> bool:
        """Returns TRUE if the RTDB is paused from appending new values"""
        return self.pause

    def setGetTime(self, getTime) -> None:
        """Set the time source of the RTDB"""
        self._getTime = getTime #< Should return a number

    def resetTime(self) -> None:
        """Reset the time stamp to zero. Should be called once and before first append"""
        if self.getTime != None:
            self.T0 = self._getTime()
        else:
            self.T0 = 0.0
            print("Time source isn't set")

    def getTime(self) -> float:
        """Returns the RTDB current time (shared with all signals)"""
        return self._getTime() -self.T0

    def playback(dt) -> None:
        """TBD"""
        self.pause = False

    def addSignal(self, name, signal) -> None:
        """Add new signal object the RTDB"""
        signal.setIsPaused( self.isPaused ) #< All signals should monitor the RTDB's pause state
        signal.setGetTime( rtdb.getTime )   #< All signals should reference the RTDB's time source
        self[name] = signal

    def loadJson(self, filename) -> bool:
        """Load and init a saved RTDB structure without the data"""
        # Opening and reading the JSON file
        with open(filename, 'r') as f:
            # Parsing the JSON file into a Python dictionary
            rtdb_json = json.load(f)

        for sigName in rtdb_json.keys():
            sig = rtdb_json[sigName]
            maxSize = sig["maxSize"]
            if sig["type"] == "Continuous":
                signal = signalContinuous(maxHistorySize=maxSize)
            elif sig["type"] == "Discrete":
                signal = signalDiscrete(maxHistorySize=maxSize)
            elif sig["type"] == "Message":
                signal = signalMessage(maxHistorySize=maxSize)
            else:
                signal = signalBase(maxHistorySize=maxSize)
            self.addSignal(sigName, signal)
        print("Append to RTDB from file <%s>"%(filename))
    
    def saveJson(self, filename) -> bool:
        """Save the RTDB structure without the data"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.getJson())
        print("RTDB saved to file <%s>"%(filename))

    def getJson(self) -> str:
        """Return the JSON string of the RTDB structure without the data"""
        signals = self.keys()
        signalsN = len(signals)
        s = '{\n' #< Start of JSON string
        for i, key in enumerate(signals):
            sig = self[key]
            s += '"%s": {"type": "%s", "maxSize": %d}'%(key, sig.getType(), sig.getMaxLen())
            if i < (signalsN -1):
                s += ','
            s += '\n'
        s += '}\n'
        return s

    def exportToHdf5(self, filename) -> bool:
        """Save the RTDB structure and data"""
        return False

if __name__ == "__main__":
    #import signals
    import time
    from signals import *

    try:
        import pysole
    except:
        pysole = False
    if pysole:
        pysole.probe(runRemainingCode=True, printStartupCode=False, fontSize=16)

    rtdb = RTDB(time.time)
    rtdb.addSignal("alt_m",       signalContinuous(maxHistorySize=48))
    rtdb.addSignal("pitch_r",     signalContinuous(maxHistorySize=48))
    rtdb.addSignal("message_str", signalMessage(maxHistorySize=48))
    rtdb.addSignal("state_enum",  signalDiscrete(maxHistorySize=48))
    rtdb.addSignal("bus_struct",  signalMessage(maxHistorySize=48))

    rtdb.resume()
    rtdb["alt_m"].append(1000.0)
    rtdb["state_enum"].append(1)
    rtdb["message_str"].append("start")
    time.sleep(0.1)

    rtdb["alt_m"].append(1100.0)
    rtdb["state_enum"].append(2)
    rtdb["message_str"].append("mid")
    time.sleep(0.1)
    
    rtdb["alt_m"].append(1200.0)
    rtdb["state_enum"].append(3)
    rtdb["message_str"].append("end")
    rtdb["bus_struct"].append([1,2,3,4])
    time.sleep(0.1)
    
    rtdb.print()
    rtdb["alt_m"].print()
    print(rtdb.getJson())
    rtdb.saveJson("rtdb_save.json")
    
    rtdb = RTDB(time.time)
    rtdb.loadJson("./unitTest/rtdb_load.json")
    rtdb.print()
