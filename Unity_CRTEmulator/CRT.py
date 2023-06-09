import numpy as np
from PIL import Image
import copy
import math


class CustomerRenderTexture():

    data: np.ndarray
    data_dBuffered: np.ndarray
    _xSize: int
    _ySize: int
    _isNormalized: bool
    _numChannels: int
    _numType: np.dtype

    def __init__(self, xDim: int, yDim: int, numColorChannels: int, numType: np.dtype = np.single,
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

        self.data = np.zeros([numColorChannels, yDim, xDim], numType)

        if initTexture != None:
            self.data = self._ConvertFromImage(initTexture)

        self.data_dBuffered = copy.copy(self.data)

    def GetPixel(self, X: float or int, Y: float or int) -> np.ndarray:
        '''
        Returns (R G B A) "pixel" at a specific coordinate
        :param X:
        :param Y:
        :return:
        '''

        #TODO add in clamping / mirroring / repeating

        return self.data[:, Y, X]

    def ExectuteUpdate(self, centerPointX: float, centerPointY: float, sizeX: float, sizeY: float, shaderPass):
        '''
        Pass in a "shaderpass" function here to have it iterate over the selected area, much like a shader.
        Not well-made or optimized
        :param centerPointX:
        :param centerPointY:
        :param sizeX:
        :param sizeY:
        :param shaderPass:
        :return:
        '''

        whereToRun: np.ndarray = self.GetBooleanRegion(centerPointX, centerPointY, sizeX, sizeY)

        # Yes, I am doing the war-crime of using for loops in python. Too Bad!
        for x in range(self._xSize):
            for y in range(self._ySize):
                if not whereToRun[y, x]: continue
                self.data_dBuffered[:, y, x] = shaderPass(self, x, y)



    def _ConvertFromImage(self, img: Image) -> np.ndarray:

        img = img.resize((int(self._xSize), int(self._ySize)), Image.NEAREST)
        npData: np.ndarray = np.asarray(img)
        npData = np.transpose(npData, (2, 0, 1))
        return npData

    def _ConvertToImage(self, raw: np.ndarray) -> Image:

        npData: np.ndarray = np.transpose(raw, (1, 2, 0))
        image: Image = Image.fromarray(npData)
        return image

    def GetBooleanRegion(self, centerPointX: float, centerPointY: float,
        sizeX: float, sizeY: float) -> np.ndarray:
        '''
        Returns a true/false 2D array of selected region of pixels on the eCRT
        :param centerPointX: X center point of selected region
        :param centerPointY: Y center point of selected region
        :param sizeX: X size of selected region
        :param sizeY: Y size of selected region
        :return:
        '''

        left: int; right: int; down: int; up: int

        if self._isNormalized:
            left: int = math.floor((centerPointX * self._xSize) - ((sizeX * self._xSize) / 2.0))
            right: int = math.ceil((centerPointX * self._xSize) + ((sizeX * self._xSize) / 2.0))
            down: int = math.floor((centerPointY * self._ySize) - ((sizeY * self._ySize) / 2.0))
            up: int = math.ceil((centerPointY * self._ySize) + ((sizeY * self._ySize) / 2.0))
        else:
            left: int = math.floor(centerPointX - (sizeX / 2.0))
            right: int = math.ceil(centerPointX + (sizeX / 2.0))
            down: int = math.floor(centerPointY - (sizeY / 2.0))
            up: int = math.ceil(centerPointY + (sizeY / 2.0))

        selected: np.ndarray = np.zeros((int(self._ySize), int(self._xSize)), dtype=bool)
        selected[down:up, left:right] = True
        return selected
