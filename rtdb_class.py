### Real Time Data Base....
### By: Guy Soffer (GSOF) 2025

class RTDB(dict):
    def __init__(self):
        super().__init__()
        self.pause()

    def print(self):
        for i, key in enumerate(self.keys()):
            sig = self[key]
            print("%3d. %s (%s %d/%d)"%(i+1,
                                        key,
                                        sig.getType(),
                                        sig.getLen(),
                                        sig.getMaxLen()
                                        ))
    def pause(self):
        self.pause = True
        
    def isPaused(self) -> bool:
        return self.pause

    def resume(self):
        self.pause = False

    def addSignal(self, name, signal) -> None:
        signal.isPaused = self.isPaused #< All signals should monitor the RTDB's pause state 
        self[name] = signal

    def load(self, filename) -> bool:
        return False

    def save(self, filename) -> bool:
        return False

    def exportToHdf5(self, filename) -> bool:
        return False
    
if __name__ == "__main__":
    #import signals
    from signals import *

    try:
        import pysole
    except:
        pysole = False
    if pysole:
        pysole.probe(runRemainingCode=True, printStartupCode=False, fontSize=16)

    rtdb = RTDB()
    rtdb.addSignal("alt_m",   signalContinuous(maxHistorySize=48))
    rtdb.addSignal("pitch_r", signalContinuous(maxHistorySize=48))
    rtdb.addSignal("message", signalMessage(maxHistorySize=48))
    rtdb.addSignal("state",   signalDiscrete(maxHistorySize=48))
    rtdb.print()
    
