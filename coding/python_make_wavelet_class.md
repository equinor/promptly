# A wavelet module based on `xarray`
 
Create a module for producing seismic wavelets, for the application of forward modeling active seismic profiles of the subsurface. The class should implement Ricker, Ormsby, and Klauder wavelets, parameterized by duration, sample interval, and frequency. Allow a user to pass an array for frequency, resulting in a wavelet 'bank' (a 2D array). Ensure the wavelets can be convolved with time series to produce synthetic seismic traces. Use xarray throughout, e.g. this should give you plotting almost for free.
