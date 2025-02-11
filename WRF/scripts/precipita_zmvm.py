import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def extract_precipitation_timeseries(filename, lon_bounds, lat_bounds):
    """
    Extract precipitation time series from WRF output for a specific area
    
    Parameters:
    -----------
    filename : str
        Path to WRF netCDF file
    lon_bounds : list
        [min_lon, max_lon]
    lat_bounds : list
        [min_lat, max_lat]
    
    Returns:
    --------
    times : list
        List of datetime objects
    precip_mean : numpy array
        Mean precipitation values for the area
    """
    
    # Open the WRF netCDF file
    ds = nc.Dataset(filename)
    
    # Extract coordinates
    lats = ds.variables['XLAT'][0, :, :]  # Assuming time-invariant grid
    lons = ds.variables['XLONG'][0, :, :]
    
    # Create mask for the area of interest
    mask = (lons >= lon_bounds[0]) & (lons <= lon_bounds[1]) & \
           (lats >= lat_bounds[0]) & (lats <= lat_bounds[1])
    
    # Get times
    time_var = ds.variables['Times'][:]
    times = []
    for t in time_var:
        timestr = b''.join(t).decode('utf-8')
        times.append(datetime.strptime(timestr, '%Y-%m-%d_%H:%M:%S'))
    
    # Extract precipitation (assuming RAINNC is accumulated precipitation)
    rainnc = ds.variables['RAINNC'][:]
    
    # Calculate hourly precipitation (difference between timesteps)
    precip = np.zeros_like(rainnc)
    precip[0] = rainnc[0]  # First timestep remains as is
    precip[1:] = np.diff(rainnc, axis=0)  # Calculate differences for subsequent timesteps
    
    # Calculate mean precipitation for the area of interest
    precip_mean = np.array([np.mean(p[mask]) for p in precip])
    
    ds.close()
    return times, precip_mean

def create_timeseries_plot(times, precip, output_file):
    """
    Create and save time series plot
    
    Parameters:
    -----------
    times : list
        List of datetime objects
    precip : numpy array
        Precipitation values
    output_file : str
        Output file path for PNG
    """
    
    plt.figure(figsize=(12, 6))
    plt.plot(times, precip, 'b-', linewidth=2)
    plt.grid(True)
    plt.xlabel('Time')
    plt.ylabel('Precipitation (mm)')
    plt.title('WRF Precipitation Time Series\n' + 
             f'Region: {lon_bounds[0]}°E to {lon_bounds[1]}°E, ' +
             f'{lat_bounds[0]}°N to {lat_bounds[1]}°N')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    # Define the area of interest
    lon_bounds = [-99.26, -98.88]
    lat_bounds = [19.3, 19.75]
    
    # Input and output files
    wrf_file = "wrfout_d02_2022-06-12_00.nc"  # Replace with your file path
    output_file = "precipitation_timeseries.png"
    
    # Extract data and create plot
    times, precip = extract_precipitation_timeseries(wrf_file, lon_bounds, lat_bounds)
    create_timeseries_plot(times, precip, output_file)
    print(f"Plot saved as {output_file}")
