import numpy as np
from PIL import Image
import copy

class CustomerRenderTexture():

    _data: np.ndarray
    _data_dBuffered: np.ndarray
    _xSize: float
    _ySize: float
    _isNormalized: bool
    _numChannels: int
    _numType: np.dtype

    def __init__(self, xDim: int, yDim: int, numColorChannels: int, numType: np.dtype = np.single, isBuffered=True,
                 isUpdateZoneNormalized=False, initTexture: Image = None):
        '''
        Initializes the eCRT (2D only for time being)
        :param xDim: X size of the eCRT
        :param yDim: Y size of the eCRT
        :param numColorChannels: number of (color channels), in inclusive range 1-4
        :param numType: See https://numpy.org/doc/stable/user/basics.types.html
        :param isBuffered: Are we double buffering the CRT?
        :param isUpdateZoneNormalized: is Update zone normalized instead of by pixel?
        :param initTexture: initial texture to load with
        '''

        self._xSize = float(xDim); self._ySize = float(yDim)
        self._numChannels = numColorChannels
        self._isNormalized = isUpdateZoneNormalized
        self._numType = numType

        self._data = np.zeros([numColorChannels, yDim, xDim], numType)

        if initTexture != None:
            self._data = self._convertFromImage(initTexture)

        if isBuffered:
            self.__data_dBuffered = copy.copy(self._data)




    def _convertFromImage(self, img: Image) -> np.ndarray:

        img = img.resize((int(self._xSize), int(self._ySize)), Image.NEAREST)
        npData: np.ndarray = np.asarray(img)
        npData = np.transpose(npData, (2, 0, 1))
        return npData

    def _convertToImage(self, raw: np.ndarray) -> Image:

        npData: np.ndarray = np.transpose(raw, (1, 2, 0))
        image: Image = Image.fromarray(npData)
        return image





test1 = Image.open("test1.png")

CRT = CustomerRenderTexture(10, 20, 3, np.dtype(np.half), initTexture=test1)