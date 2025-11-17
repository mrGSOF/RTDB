## By: Guy Soffer (GSOF) 16/Nov/2025
__version__ = "1.0.0"
__author__ = "Guy Soffer"
__copyright__ = ""
__credits__ = [""]
__license__ = "MIT"
__maintainer__ = ""
__email__ = "gsoffer@yahoo.com"
__status__ = "Development"

import cv2
import numpy as np

def encode(raw) -> bytes:
    success, jpeg = cv2.imencode(".jpg", raw)
    if success:
        return (np.array(jpeg)).tobytes()
    #print("Error in JPEG encoder")
    return byte(0xff)

def decode(jpeg) -> list:
    np_raw = cv2.imdecode(np.frombuffer(jpeg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    if np_raw is not None:
        return np_raw
    return []

if __name__ == "__main__":
    def generate_image(height=800, width=600, channels=3):
        """Generate Random Image"""
        rng = np.random.default_rng(9)
        arr = rng.integers(0, 255, (height, width, channels), dtype=np.uint8)
        if channels == 1:
            arr = arr[:, :, 0] #< Peak only a single value per pixel (gray value)
        if arr.ndim < 3:
            arr = np.expand_dims(arr, 2)
        return arr

    def disp(image):
        if image is not None:
            cv2.imshow("Original Image", image)
            jpeg = encode(image)
            print(jpeg[0:16])
            img = decode(jpeg)
            if len(img) > 0:
                cv2.imshow("After encode / decode", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    # Load an image from file
    #image = cv2.imread("airplane.jpg")
    #disp(image)

    image = generate_image(height=320, width=240, channels=3)
    disp(image)

    image = generate_image(height=240, width=320, channels=1)
    disp(image)
