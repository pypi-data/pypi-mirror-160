import numpy
import xarray
import matplotlib.pyplot as plt


class objearth():
    def __init__(self,DataArray):
        self.DataArray = DataArray
        
    def plotshow(self,lst=True):
        self.lst = lst
        if type(self.DataArray) == xarray.core.dataarray.DataArray:
            if self.lst==True:
                ymax = 0 ; ymin = self.DataArray.shape[0]
                xmin = 0 ; xmax = self.DataArray.shape[1] 
            else:
                ymax = self.lst[0] ; ymin = self.lst[1]
                xmin = self.lst[2] ; xmax = self.lst[3]
            lon  =  self.DataArray.longitude.to_numpy()[xmin:xmax]
            lon0 =  lon[0] ; lon1 =  lon[-1]
            lat  =  self.DataArray.latitude.to_numpy()[ymax:ymin]
            lat0 = -lat[-1] ; lat1 = -lat[0]
            def longitude(lon):
                return [lon0,lon1]
            def latitude(lat):
                return [lat0,lat1]
            def axis(x=0):
                return x
            fig,ax = plt.subplots(constrained_layout=True)
            fig.set_size_inches(7,7)
            ax.set_xlabel('x axis size')
            ax.set_ylabel('y axis size')
            ax.imshow(self.DataArray[ymax:ymin,xmin:xmax],extent=[xmin,xmax,ymin,ymax])
            secax_x = ax.secondary_xaxis('top',functions=(longitude,axis))
            secax_x.set_xlabel('longitude')
            secax_x = ax.secondary_xaxis('top',functions=(longitude,axis))
            secax_x.set_xlabel('longitude')
            secax_y = ax.secondary_yaxis('right',functions=(latitude,axis))
            secax_y.set_ylabel('latitute')
            plt.grid(color='w', linestyle='-', linewidth=0.1)
            plt.show()
        
        elif type(self.DataArray) == numpy.ndarray:
            if self.lst==True:
                ymax = 0 ; ymin = self.DataArray.shape[0]
                xmin = 0 ; xmax = self.DataArray.shape[1]
            else:
                ymax = self.lst[0] ; ymin = self.lst[1]
                xmin = self.lst[2] ; xmax = self.lst[3]
            plt.figure(figsize=(10,10))
            plt.imshow(self.DataArray[ymax:ymin,xmin:xmax],extent=[xmin,xmax,ymin,ymax])
        
        else:
            print("Nonetype :",type(self.DataArray))
            
    def NDVI(self):
        red = xarray.where(self.DataArray.red==-9999,numpy.nan,self.DataArray.red)
        nir = xarray.where(self.DataArray.nir==-9999,numpy.nan,self.DataArray.nir)
        ndvi1 = (nir-red)/(nir+red).to_numpy()
        ndvi3 = numpy.clip(ndvi1,-1,1)
        im_ratio = ndvi3.shape[1]/ndvi3.shape[0]
        plt.figure(figsize=(8,8))
        plt.xticks([]), plt.yticks([])
        plt.imshow(ndvi3,cmap='viridis')
        plt.clim(-1,1)
        plt.colorbar(orientation="vertical",fraction=0.0378*im_ratio)
        plt.show()
        return ndvi3

   
    

