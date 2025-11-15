## By: Guy Soffer (GSOF) 11/Nov/2025
__version__ = "1.0.0"
__author__ = "Guy Soffer"
__copyright__ = ""
__credits__ = ["Tzur Soffer"]
__license__ = "MIT"
__maintainer__ = ""
__email__ = "gsoffer@yahoo.com"
__status__ = "Development"

import json

def addFileExtention(filename, ext) -> str:
    return filename

class RTDB():
    def __init__(self, name="noname", getTime=None):
        self.name = name
        self.pause()
        self.setGetTime(getTime)
        self.resetTime()
        self._signals = {}

    def addSignal(self, name, signal) -> None:
        """Add new signal object the RTDB"""
        signal.setIsPaused( self.isPaused ) #< All signals should monitor the RTDB's pause state
        signal.setGetTime( self.getTime )   #< All signals should reference the RTDB's time source
        self._signals[name] = signal

    def __setitem__(self, name, signal) -> None:
        """Add new signal object the RTDB"""
        self._signals[name]
        self.addSignal(name, signal)

    def getSignal(self, name):
        """Return a reference to the signal object"""
        return self._signals.get(name, None)

    def __getitem__(self, name):
        """Return a reference to the signal object"""
        return self.getSignal(name)

    def isSignalExists(self, name) -> bool:
        """Return True if signal name exists in RTDB"""
        return name in self.signals()

    def signals(self) -> list:
        """Return the list of signals names"""
        return self._signals.keys()

    def list(self) -> list:
        """Return the list of signals names"""
        return self.signals()

    def keys(self) -> list:
        """Return the list of signals names"""
        return self.signals()

    def size(self) -> int:
        """Return the number of signals in the RTDB"""
        return len(self._signals)

    def print(self) -> None:
        """Print the structure of the RTDB"""
        s = "RTDB (%s) content:\n"%(self.name)
        for i, key in enumerate(self.signals()):
            sig = self.getSignal(key)
            s += "%3d. %s (%s %d/%d)\n"%(i+1,
                                         key,
                                         sig.getType(),
                                         sig.getLen(),
                                         sig.getMaxLen()
                                         )
        print("\n"+s)
        
    def pause(self):
        """Disable all signals from new appending"""
        self.pause = True
        return self

    def resume(self):
        """Enable all signals for new appending"""
        self.pause = False
        return self

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

    def playback(self, dt) -> None:
        """TBD"""
        raise NotImplementedError("Playback isn't implemented yet")
        self.pause = False

    def loadJson(self, filename) -> bool:
        """Load and init a saved RTDB structure without the data"""
        # Opening and reading the JSON file
        with open(filename, 'r') as f:
            # Parsing the JSON file into a Python dictionary
            rtdb_json = json.load(f)

        for sigName in rtdb_json.keys():
            sig = rtdb_json[sigName]
            if sigName == "name":
                self.name = sig
            else:
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
        filename = addFileExtention(filename, "json")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.getJson())
        print("RTDB saved to file <%s>"%(filename))

    def getJson(self) -> str:
        """Return the JSON string of the RTDB structure without the data"""
        signalsN = self.size()
        s = '{\n' #< Start of JSON string
        s += '"name": "%s",\n'%(str(self.name))
        for i, key in enumerate(self.signals()):
            sig = self[key]
            s += '"%s": {"type": "%s", "maxSize": %d}'%(key, sig.getType(), sig.getMaxLen())
            if i < (signalsN -1):
                s += ','
            s += '\n'
        s += '}\n'
        return s

    def getStateHdf5(self):
        """TBD"""
        raise NotImplementedError("HDF5 support isn't implemented yet")

    def saveStateHdf5(self, filename) -> bool:
        """Save the RTDB structure and data"""
        try:
            filename = addFileExtention(filename, "csv")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.getStateHdf5)
            print("RTDB saved to file <%s>"%(filename))
            return True
        except:
            print("Error: RTDB wasn't saved to <%s>"%(filename))
            return False

    def getStateCsv(self) -> str:
        """Save the RTDB structure and data"""
        maxSamples = 0
        csv = ""
        for sig in self.list():
            csv += "%s_s, %s_v, "%(sig, sig)
            sigSamples = self.getSignal(sig).getLen()
            if maxSamples < sigSamples:
                maxSamples = sigSamples
        csv += "\n"
        for i in range(maxSamples):
            for sig in self.list():
                signal = self.getSignal(sig)
                if i < signal.getLen():
                    csv += "%1.6f, %s, "%(signal.time[i], str(signal.value[i]))
                else:
                    csv += ", , "
            csv += "\n"
        return csv

    def saveStateCsv(self, filename) -> bool:
        """Save the RTDB structure and data"""
        try:
            filename = addFileExtention(filename, "csv")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.getStateCsv())
            print("RTDB saved to file <%s>"%(filename))
            return True
        except:
            print("Error: RTDB wasn't saved to <%s>"%(filename))
            return False
            

if __name__ == "__main__":
    #import signals
    import time
    from signals import *

    try:
        import pysole
    except:
        pysole = False
#    if pysole:
#        pysole.probe(runRemainingCode=True, printStartupCode=False, fontSize=16)

    rtdb = RTDB(name="DEMO", getTime=time.time)
    rtdb.addSignal("alt_m",       signalContinuous(maxHistorySize=48))
    rtdb.addSignal("pitch_r",     signalContinuous(maxHistorySize=48))
    rtdb.addSignal("message_str", signalMessage(maxHistorySize=48))
    rtdb.addSignal("state_enum",  signalDiscrete(maxHistorySize=48))
    rtdb.addSignal("bus_struct",  signalMessage(maxHistorySize=48))
    rtdb.print()
    
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
    rtdb.saveStateCsv("rtdb.csv")
    
    rtdb["alt_m"].print()
    print(rtdb.getJson())
    rtdb.saveJson("rtdb_save.json")
    
    rtdb = RTDB(getTime=time.time)
    rtdb.loadJson("./unitTest/rtdb_load.json")
    rtdb.print()

    if None == rtdb["new"]:
        print("Signal not exists return None - passed")

    if False == rtdb.isSignalExists("new"):
        print("Signal not isSignalExists() return False - passed")
