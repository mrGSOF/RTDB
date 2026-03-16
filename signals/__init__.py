from .signalBase import *
from .signalMessage import *
from .signalDiscrete import *
from .signalContinuous import *
from .signalEncodedMulaw import *
try:
    from .signalNumpySharedMemory import *
except:
    signalNumpySharedMemory = signalBase
    print("numpy not installed, signalNumpySharedMemory will not work")