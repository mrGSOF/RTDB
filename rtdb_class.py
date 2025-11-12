### Real Time Data Base....
### By: Guy Soffer (GSOF) 2025
import time

class RTDB(dict):
    def __init__(self):
        super().__init__()
        self.T0 = time.time()
        self.pause()

    def print(self):
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
        
    def pause(self):
        self.pause = True
        
    def isPaused(self) -> bool:
        return self.pause

    def getTime(self) -> float:
        return time.time() -self.T0

    def resume(self):
        self.pause = False

    def playback(dt):
        self.pause = False

    def addSignal(self, name, signal) -> None:
        signal.setIsPaused( self.isPaused ) #< All signals should monitor the RTDB's pause state
        signal.setGetTime( rtdb.getTime )   #< All signals should reference the RTDB's time source
        self[name] = signal

    def loadJson(self, filename) -> bool:
        """Save the RTDB structure without the data"""
        return False

    def saveJson(self, filename) -> bool:
        """Load and init a saved RTDB structure without the data"""
        return False

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

    rtdb = RTDB()
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
    
