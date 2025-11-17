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
from processing.Jpeg import encode              #< The JPEG encoder
from processing.Jpeg import decode              #< The JPEG decoder

class signalAudioJpeg(signalEncodedBase):
    def __init__(self, maxHistorySize=32, isPaused=None, getTime=None):
        super().__init__(maxHistorySize, "EncodedMJpeg", isPaused, getTime)

    ### Overwrite to pass value through the Jpeg encoder 
    def _encode(self, raw):
        return encode(raw)

    ### Overwrite to pass value through the Jpeg decoder 
    def _decode(self, encoded):
        return decode(encoded)

if __name__ == "__main__":
    import importlib.util, os, sys
    import cv2
    import numpy as np

    mdl = ""
    path = os.path.join("../unitTest", "test.py" )
    #print(path)
    spec = importlib.util.spec_from_file_location(mdl, path)
    #print(spec)
    ut = importlib.util.module_from_spec(spec)
    sys.modules[mdl] = ut
    spec.loader.exec_module(ut)

    def generate_image(seed=8, height=800, width=600, channels=3):
        """Generate Random Image"""
        rng = np.random.default_rng(seed)
        arr = rng.integers(0, 255, (height, width, channels), dtype=np.uint8)
        if channels == 1:
            arr = arr[:, :, 0] #< Peak only a single value per pixel (gray value)
        if arr.ndim < 3:
            arr = np.expand_dims(arr, 2)
        return arr

    def absoluteDifference(a, b):
        return np.abs(a.astype(np.float32) - b.astype(np.float32))

    def dispDiff(imageA, imageB):
        maxMeanError = 46
        imageDiff = absoluteDifference(imageA, imageB)
        ut.test("Mean error", maxMeanError, imageDiff.mean(), 2)
        if imageDiff.mean() > maxMeanError +1:
            cv2.imshow("Error Image", imageDiff)
            cv2.imshow("Decoded Image", imageB)
            cv2.waitKey(0)

    try:
        import pysole
    except:
        pysole = False
    if pysole:
        pysole.probe(runRemainingCode=True, printStartupCode=False, fontSize=16)

    time = ut.Clock(100.12)
    signal = signalAudioJpeg(maxHistorySize=32, getTime=time.time)
    Tst = time.time()
    for i in range(0,4):
        imgOrg = generate_image(i, height=200*2, width=320*2, channels=3)
        signal.append(imgOrg)
        time.sleep(0.1)
        imgJpg = signal.getLatest()
        dispDiff(imgOrg, imgJpg)
    Tend = time.time()

    cv2.destroyAllWindows()
