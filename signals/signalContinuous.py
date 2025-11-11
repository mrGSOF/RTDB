from signalBase import signalBase

class signalContinuous(signalBase):
    def __init__(self, degree=1):
        self.degree = 1
        
    def getAt(self, at):
        return self.getValueInterpulatedAtTime(at)

    def getValueInterpulatedAtTime(self, at):
        if len(self.time) == 0:
            return -1

        if at < 0:
            at += time.time() #< convert relative time to abs time

        ### Future value does not exist yet
        if at > self.time[-1]:
            return self.value[-1]
        
        ### Too old, older than first data point
        if at < self.time[0]:
            return self.value[0]

        ### Find closest value by absolute time
        MAX_POSSIBLE_DT = time.time()
        lastDt = MAX_POSSIBLE_DT
        for i in range(len(self.time)):
            dt = abs(at -self.time[i])
            if dt < lastDt:
                lastDt = dt
            else:
                return self.value[i -1]
        return self.value[-1]

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
    signal = signalContinuous(maxHistorySize=6)
    Tst = time.time()
    for i in range(4):
        signal.append(i+1)
        time.sleep(0.1)
    Tend = time.time()
    tol = 0.05
    ut.test("First element", 1, signal.getAt(Tst), tol)
    ut.test("Last element", 4, signal.getAt(Tend), tol)
    ut.test("Element at 0.12 sec", 2, signal.getAt(Tst +0.12), tol)
    ut.test("Element at 0.18 sec", 3, signal.getAt(Tst +0.18), tol)
    ut.test("Element at 0.28 sec", 3, signal.getAt(-0.22), tol)
    ut.test("Element at 0.3 sec",  4, signal.getAt(-0.1), tol)
