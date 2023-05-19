import numpy as np

class CustomerRenderTexture():

    _data: np.ndarray
    _data_dBuffered: np.ndarray
    _xSize: float
    _ySize: float
    _isNormalized: bool
    _numChannels: int
    _numType: np.dtype

    def __init__(self, xDim: int, yDim: int, numColorChannels: int, numType=np.single, isBuffered=True,
                 isUpdateZoneNormalized=False):
        '''
        Initializes the eCRT (2D only for time being)
        :param xDim: X size of the eCRT
        :param yDim: Y size of the eCRT
        :param numColorChannels: number of (color channels), in inclusive range 1-4
        :param numType: See https://numpy.org/doc/stable/user/basics.types.html
        :param isBuffered: Are we double buffering the CRT?
        :param isUpdateZoneNormalized: is Update zone normalized instead of by pixel?
        '''

        self._xSize = float(xDim); self._ySize = float(yDim)
        self._numChannels = numColorChannels
        self._isNormalized = isUpdateZoneNormalized
        self._numType = numType


