import numpy as np
from PIL import Image
import copy
import math

class CustomerRenderTexture():

    _data: np.ndarray
    _data_dBuffered: np.ndarray
    _xSize: int
    _ySize: int
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

        self._xSize = xDim; self._ySize = yDim
        self._numChannels = numColorChannels
        self._isNormalized = isUpdateZoneNormalized
        self._numType = numType

        self._data = np.zeros([numColorChannels, yDim, xDim], numType)

        if initTexture != None:
            self._data = self._ConvertFromImage(initTexture)
            self._GetBooleanRegion_N(0.5,0.5,0.25,0.25)

        if isBuffered:
            self.__data_dBuffered = copy.copy(self._data)




    def _ConvertFromImage(self, img: Image) -> np.ndarray:

        img = img.resize((int(self._xSize), int(self._ySize)), Image.NEAREST)
        npData: np.ndarray = np.asarray(img)
        npData = np.transpose(npData, (2, 0, 1))
        return npData

    def _ConvertToImage(self, raw: np.ndarray) -> Image:

        npData: np.ndarray = np.transpose(raw, (1, 2, 0))
        image: Image = Image.fromarray(npData)
        return image

    def _GetBooleanRegion_N(self, centerPointX: float, centerPointY: float,
        sizeX: float, sizeY: float) -> np.ndarray:

        left: int = math.floor((centerPointX * self._xSize) - ((sizeX * self._xSize) / 2.0))
        right: int = math.ceil((centerPointX * self._xSize) + ((sizeX * self._xSize) / 2.0))
        down: int = math.floor((centerPointY * self._ySize) - ((sizeY * self._ySize) / 2.0))
        up: int = math.ceil((centerPointY * self._ySize) + ((sizeY * self._ySize) / 2.0))

        selected: np.ndarray = np.zeros((int(self._ySize), int(self._xSize)), dtype=bool)
        selected[down:up, left:right,] = True
        return selected





test1 = Image.open("test1.png")

CRT = CustomerRenderTexture(10, 20, 3, np.dtype(np.half), initTexture=test1)