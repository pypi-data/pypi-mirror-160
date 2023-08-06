import numpy
import xarray
class plotshow():
    def __init__(self,DataArray):
        self.DataArray = DataArray
    def spread(self):
        if type(self.DataArray) == xarray.core.dataarray.DataArray:
            print('xarray')
        elif type(self.DataArray) == numpy.ndarray:
            print('numpy array')
        else:
            print("Nonetype :",type(self.DataArray))