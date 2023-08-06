import matplotlib.pyplot as plt
class imgshow():
    def __init__(self,DataArray,lst=True):
        self.DataArray = DataArray
        self.lst = lst
        if self.lst==True:
            ymax = 0
            ymin = self.DataArray.shape[0]
            xmin = 0
            xmax = self.DataArray.shape[1]
        else:
            ymax = self.lst[0]
            ymin = self.lst[1]
            xmin = self.lst[2]
            xmax = self.lst[3]
        lon  =  DataArray.longitude.to_numpy()[xmin:xmax]
        lon0 =  lon[0] ; lon1 =  lon[-1]
        lat  =  DataArray.latitude.to_numpy()[ymax:ymin]
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
        ax.imshow(DataArray[ymax:ymin,xmin:xmax],extent=[xmin,xmax,ymin,ymax])
        secax_x = ax.secondary_xaxis('top',functions=(longitude,axis))
        secax_x.set_xlabel('longitude')
        secax_y = ax.secondary_yaxis('right',functions=(latitude,axis))
        secax_y.set_ylabel('latitute')
        plt.grid(color='w', linestyle='-', linewidth=0.1)
        plt.show()