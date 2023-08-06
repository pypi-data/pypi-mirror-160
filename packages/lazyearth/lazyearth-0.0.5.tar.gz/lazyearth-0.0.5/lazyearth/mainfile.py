import matplotlib.pyplot as plt
class plotshow():
    def __init__(self,DataArray):
        self.DataArray = DataArray
        plt.imshow(self.DataArray)