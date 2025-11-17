import av
import cv2

class MPEGDecoder:
    def __init__(self, codeName="h264"):
        self.decoder = av.CodecContext.create(codeName, "r")
    
    def decode(self, packet):
        """
        Decode a compressed packet (bytes) back into frames.
        Returns a list of frames as NumPy arrays (BGR).
        """
        if type(packet) == bytes:
            packet = av.Packet(packet)
        try:
            frames = self.decoder.decode(packet)
        except:
            # print("Error, likely lost sync")
            return None
        
        if frames == []:
            return None

        frame = frames[-1].to_ndarray(format="rgb24")
        frameBgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return(frameBgr)

class MPEGEncoder:
    def __init__(self, codeName="h264", width=640, height=480, framerate=30, pixFmt="yuv420p"):
        """
        Initialize encoder context.
        :param codec_name: Codec to use ("h264", "hevc", "vp9", etc.)
        :param width: Frame width
        :param height: Frame height
        :param framerate: Frames per second
        :param pixFmt: Pixel format for encoder (default "yuv420p")
        """
        self.codec = av.CodecContext.create(codeName, "w")
        self.codec.width = width
        self.codec.height = height
        self.codec.framerate = framerate
        self.codec.pix_fmt = pixFmt
        self.codec.options = {"g": str(framerate)}

    def encode(self, frameBgr):
        """
        Encode a single OpenCV frame (BGR ndarray).
        Returns a list of encoded packets (bytes).
        """
        frameRgb = cv2.cvtColor(frameBgr, cv2.COLOR_BGR2RGB)

        avFrame = av.VideoFrame.from_ndarray(frameRgb, format="rgb24")

        packets = self.codec.encode(avFrame)
        return packets
        return [bytes(pkt) for pkt in packets]   #< Convert packets to raw bytes

    def flush(self):
        """
        Flush encoder at end of stream.
        Returns remaining packets (bytes).
        """
        packets = self.codec.encode(None)
        return packets
        return [pkt.to_bytes() for pkt in packets]

if __name__ == "__main__":
    import cv2
    import pysole

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    encoder = MPEGEncoder(codeName="h264", width=frame.shape[1], height=frame.shape[0], framerate=30)
    decoder = MPEGDecoder(codeName="h264")

    def imshow(name, frame, sleep=0):
        cv2.imshow(name, frame)
        if cv2.waitKey(sleep):
            return False
        return True

    def encodeFrames(count=30):
        packetsHistory = []
        for _ in range(count):
            ret, frame = cap.read()
            packets = encoder.encode(frame)
            if packets != []:
                packetsHistory.append(packets)
        return packetsHistory
    
    def decodePacket(packet):
        for decodedFrames in decoder.decode(packet):
            print(len(decodedFrames), "frames decoded from packet of size")
            for df in decodedFrames:
                imshow("Decoded", df, 5)
        return decodedFrames
    
    def decodePackets(packets):
        for packet in packets:
            decodePacket(packet)

    def getNextPacket():
        while True:
            ret, frame = cap.read()
            packets = encoder.encode(frame)
            if packets != []:
                return packets

    pysole.probe(runRemainingCode=True, printStartupCode=True, fontSize=16)
    
    # packet = getNextPacket()
    # decodePacket(packet)

    packets = encodeFrames(100)
    decodePackets(packets)