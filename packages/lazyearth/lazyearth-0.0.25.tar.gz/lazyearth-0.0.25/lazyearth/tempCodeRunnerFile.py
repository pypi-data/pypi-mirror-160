    BAND1    = xarray.where(Dataset1==-9999,numpy.nan,Dataset1)
    band1    = BAND1.to_numpy()/10000*bright
    BAND2    = xarray.where(Dataset2==-9999,numpy.nan,Dataset2)
    band2    = BAND2.to_numpy()/10000*bright
    BAND3    = xarray.where(Dataset3==-9999,numpy.nan,Dataset3)
    band3    = BAND3.to_numpy()/10000*bright
    product  = numpy.stack([band1,band2,band3],axis=2)
    return product