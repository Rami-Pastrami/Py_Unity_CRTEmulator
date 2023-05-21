import Unity_CRTEmulator
from Unity_CRTEmulator.CRT import CustomerRenderTexture
import numpy as np
from PIL import Image

# A poorly made test program

def TestFunc(eCRT: CustomerRenderTexture, xCoord, yCoord) -> np.ndarray:

    curPix: np.ndarray = eCRT.GetPixel(xCoord, yCoord)
    return 255.0 - curPix

test1 = Image.open("test.png")

CRT = CustomerRenderTexture(10, 20, 3, np.dtype(np.half), initTexture=test1)

CRT.ExectuteUpdate(3,3,5,5,TestFunc)

print("done")


