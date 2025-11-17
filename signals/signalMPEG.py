__version__ = "1.0.0"
__author__ = "Tzur Soffer"
__copyright__ = ""
__credits__ = [""]
__license__ = "MIT"
__maintainer__ = ""
__email__ = "tzur.soffer@gmail.com"
__status__ = "Development"

import sys, os.path
from types import NoneType
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__))))
from signalEncodedBase import signalEncodedBase     #< The Encoded base class
from processing.MPEG import MPEGEncoder             #< The MPEG encoder
from processing.MPEG import MPEGDecoder             #< The MPEG decoder

def encode(raw, encoder):
    return encoder.encode(raw)

def decode(raw, decoder):
    return decoder.decode(raw)

class signalMPEG(signalEncodedBase):
    def __init__(self, maxHistorySize=32, isPaused=None, getTime=None,
                 codeName='h264', width=640, height=480, framerate=30, pixFmt="yuv420p"):
        super().__init__(maxHistorySize, "EncodedMPEG", isPaused, getTime)
        self.codeName = codeName
        self.encoder = MPEGEncoder(codeName=codeName, width=width, height=height, framerate=framerate, pixFmt=pixFmt)
        self.decoder = MPEGDecoder(codeName=codeName)

    ### Overwrite with to pass value through the MPEG encoder 
    def _encode(self, raw):
        return encode(raw, self.encoder)

    ### Overwrite with to pass value through the MPEG decoder 
    def _decodeAtIndex(self, idx):
        # print("Finding last keyframe")
        if idx < 0:
            idx = len(self.time) + idx

        decoder = MPEGDecoder(codeName=self.codeName)
        end = idx
        start = None
        for i in range(max(idx-2, 0), -1, -1):
            frame = self.getRawAtIndex(i)
            if frame == -1:
                return None
            if frame.is_keyframe:
                start = i
                break
        if start == None:
            return None

        img = None
        for i in range(start, end + 1):
            img = decode(self.getRawAtIndex(i), decoder)
        return img

    def _decode(self, idx):
        try:
            if idx == -1 or idx == len(self.time) - 1:
                image = decode(self.getRawAtIndex(idx), self.decoder)
                if type(image) != NoneType:
                    return image
        finally:
            return self._decodeAtIndex(idx)

    def print(self):
        s = "Type: %s\n"%(self._typeName)
        s += "time | value\n"
        for i in range(len(self.time)):
            s += "%1.3f | %1.3f\n"%(self.time[i], self._decode(i))
        print("\n"+s)

    def append(self, val) -> None:
        """Input value will be encoded and appended"""
        packets = self._encode(val)
        if packets != []:
            for packet in packets:
                self.appendEncoded( packet )

    def getAtIndex(self, idx):
        """Decoded value"""
        return self._decode(idx)

    def getAt(self, at):
        """Decoded value"""
        return self._decode(self.getIndexClosestToTime(at))

    def getLatest(self):
        """Decoded value"""
        return self._decode(-1)

if __name__ == "__main__":
    import cv2
    import time
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

    def imshow(name, frame, sleep=0):
        try:
            cv2.imshow(name, frame)
            if cv2.waitKey(sleep):
                return False
            return True
        except:
            print(f"Faulty image for {name} {frame}")
            return False

    cap = cv2.VideoCapture("../unitTest/test.mp4")
    _, frame = cap.read()
    signal = signalMPEG(maxHistorySize=67, getTime=time.time, width=frame.shape[1], height=frame.shape[0], framerate=30)  #< 4135642 compressed
    Tst = time.time()
    for i in range(90):
        img = cap.read()[1]
        signal.append(img)
        time.sleep(1/30)
    Tend = time.time()

    print(signal.getLen())
    for i in range(signal.getLen()):
        frame = signal.getAtIndex(i)
        if type(frame) == list or type(frame) == type(None):
            continue
        imshow(f"frame", frame)

    imshow("frame0", signal.getAtIndex(0))       #< error
    imshow("frame-1", signal.getAtIndex(-1))     #< latest (57)
    imshow("frame-15", signal.getAtIndex(-15))   #< 42
    imshow("frame33", signal.getAtIndex(33))     #< 32