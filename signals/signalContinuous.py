from signalBase import signalBase

class signalContinuous(signalBase):
    def __init__(self, maxHistorySize=32, degree=1):
        super().__init__(maxHistorySize)
        self.degree = 1
        
    def getAt(self, at):
        return self.getValueInterpolatedAtTime(at)

    def _intr(self, t0, t1, v0, v1, t):
        slope = (v1 -v0)/(t1 -t0)
        ### Past value extrapolation or mid value interpolation
        if t > t1:
            ### Future value extrapolation
            v0 = v1
            t0 = t1
        return v0 +slope*(t -t0)

    def getValueInterpolatedAtTime(self, at):
        if len(self.time) == 0:
            return -1

        if at < 0:
            at += time.time() #< convert relative time to abs time

        ### Future value extrapolation
        if at >= self.time[-1]:
            return self._intr(self.time[-2], self.time[-1],
                              self.value[-2], self.value[-1],
                              at)

        ### Past value extrapolation
        if at <= self.time[0]:
            return self._intr(self.time[0], self.time[1],
                              self.value[0], self.value[1],
                              at)

        ### Mid value interpolation
        MAX_POSSIBLE_DT = time.time()
        lastDt = MAX_POSSIBLE_DT
        for i in range(len(self.time) -1):
            if (at >= self.time[i]) and (at < self.time[i+1]):
                return self._intr(self.time[i], self.time[i+1],
                                  self.value[i], self.value[i+1],
                                  at)
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

    tol = 0.05
    inc_per_dt = 0.5
    dt = 0.5
    Tst = time.time()
    for i in range(4):
        signal.append(i*inc_per_dt)
        time.sleep(dt)
    Tend = time.time() -dt
    ut.test("Element 0.1 sec ago",  1.4, signal.getAt(-0.1-dt), tol)
    ut.test("Element 0.1 sec ago",  1.4, signal.getAt(Tend-0.1), tol)
    ut.test("Element at -1.0 sec", -1,   signal.getAt(Tst -1.0), tol)
    ut.test("Element at 0.0 sec",   0,   signal.getAt(Tst +0.0), tol)
    ut.test("Element at 0.12 sec", 0.12, signal.getAt(Tst +0.12), tol)
    ut.test("Element at 0.18 sec", 0.18, signal.getAt(Tst +0.18), tol)
    ut.test("Element at 0.28 sec", 0.28, signal.getAt(Tst +0.28), tol)
    signal.print()
