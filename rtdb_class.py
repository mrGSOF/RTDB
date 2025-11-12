### Real Time Data Base....
### By: Guy Soffer (GSOF) 2025

class RTDB(dict):
    def __init__(self):
        super().__init__()

    def addSignal(name, signalType):
        self["name"] =signalType

if __name__ == "__main__":
    import signals
    #from signals import *

    try:
        import pysole
    except:
        pysole = False
    if pysole:
        pysole.probe(runRemainingCode=True, printStartupCode=False, fontSize=16)

    rtdb = RTDB()
    
