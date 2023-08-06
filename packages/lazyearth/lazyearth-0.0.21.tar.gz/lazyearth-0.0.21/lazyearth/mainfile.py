import numpy
import xarray
import matplotlib.pyplot as plt



class objearth():
    def __init__(self):
        pass

    def clearcloud(self,Dataset0,Dataset1):
        self.Dataset0 = Dataset0
        self.Dataset1 = Dataset1
        pixel0 = self.Dataset0.pixel_qa
        mask1 = xarray.where(pixel0==352,1,0)    
        mask2 = xarray.where(pixel0==480,1,0)
        mask3 = xarray.where(pixel0==944,1,0)
        sum = mask1+mask2+mask3
        mask0 = xarray.where(sum.data>0,1,0)
        blue        = xarray.where(mask0,self.Dataset1.blue,self.Dataset0.blue)
        green       = xarray.where(mask0,self.Dataset1.green,self.Dataset0.green)
        red         = xarray.where(mask0,self.Dataset1.red,self.Dataset0.red)
        nir         = xarray.where(mask0,self.Dataset1.nir,self.Dataset0.nir)
        pixel_qa    = xarray.where(mask0,self.Dataset1.pixel_qa,self.Dataset0.pixel_qa)
        # Create DataArray
        return xarray.merge([blue,green,red,nir,pixel_qa])

    def plotshow(self,DataArray,lst=True):
        self.DataArray = DataArray
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

    def percentcloud(self,Dataset):
        self.Dataset = Dataset
        FashCloud = [352,480,944]
        dstest    = self.Dataset.pixel_qa
        dsnew     = xarray.where(dstest == FashCloud[0],numpy.nan,dstest)
        dsnew     = xarray.where(dsnew  == FashCloud[1],numpy.nan,dsnew)
        dsnew     = xarray.where(dsnew  == FashCloud[2],numpy.nan,dsnew)
        Cpixel    = (numpy.isnan(dsnew.to_numpy())).sum()
        Allpixel  = int(self.Dataset.pixel_qa.count())
        Cloudpercent = (Cpixel/Allpixel)*100
        print("Percent Cloud : %.4f"%Cloudpercent,"%")



    

