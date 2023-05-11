import numpy as np
from enum import Enum

class CustomerRenderTexture():

    # enums for dropdowns
    Dim = Enum('Dimension', ['TwoD', 'TwoDArray', 'Cube', 'ThreeD'])  # Can't start with numbers lol, UNIMPLEMENTED
    AA = Enum('Enum', ['NoSamples', 'TwoSamples', 'FourSamples', 'EightSamples'])  # Can't use None, UNIMPLEMENTED
    Wrap = Enum('Wrap', ['Repeat', 'Clamp', 'Mirror', 'MirrorOnce', 'PerAxis'])
    SSM = Enum('SSM', ['None', 'CompareDepths'])  # UNIMPLEMENTED
    DSF = Enum('DSF', ['R8_UInt'])  # Only one that works




    '''
    CF = Enum('CF', ['ARGB32', 'Depth', 'ARGBHalf', 'Shadowmap', 'RGB565', 'ARGB4444', 'ARGB1555', 'ARGB2101010',
                     'ARGB64', 'ARGBFloat', 'RGFloat', 'RGHalf', 'RFloat', 'RHalf', 'R8', 'ARGBInt', 'RGInt', 'RInt',
                     'BGRA32', 'RGB111110Float', 'RG32', 'RGBAUShort', 'RG16', 'BGRA10101010_XR', 'BGR101010_XR', 'R16'])
    '''

    @property
    def Dimension(self):
        return self._Dimension
    @Dimension.setter
    def Dimension(self, x):
        self._Dimension = x





    # Private vars

    _Dimension: Dim = Dim.TwoD
    _Size: np.ndarray = np.array([1, 1]).astype(int)
    _ColorFormat: CF = CF.R8
    # The following are unused
    _AntiAliasing: AA = AA.NoSamples




