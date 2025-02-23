import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.feature import NaturalEarthFeature

def plot_wrf_domains_single_map(geo_em_files, output_file='wrf_dominios.png', dpi=300):
    """
    
    Grafica los dominios WRF en un solo mapa y los guarda en un archivo PNG
    
    Parametros:
    -----------
    geo_em_files : lista
        Lista de archivos geo_em_d0*.nc 
    output_file : str
        Archivo PNG de salida
    dpi : int
        Resolucion
    """
    # Mercator 
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mercator())
    
    # Division Política Mexico
    states = NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='10m',
        facecolor='none',
        edgecolor='gray'
    )
    ax.add_feature(states, linestyle=':', linewidth=1)
    
    # Detalles
    ax.add_feature(cfeature.COASTLINE, linewidth=1)
    ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=1.5)
    ax.add_feature(cfeature.OCEAN, alpha=0.3)
    ax.add_feature(cfeature.LAND, alpha=0.3)
    
    # Colores por dominio1, dominio2, dominio3
    colors = ['brown', 'orange', 'green']
    line_styles = ['-', '--', ':']
    
    # Get the extent of the outermost domain for map boundaries
    ds_outer = xr.open_dataset(geo_em_files[0])
    outer_lats = ds_outer.XLAT_M[0].values
    outer_lons = ds_outer.XLONG_M[0].values
    
    # Dominios
    for i, file in enumerate(geo_em_files):
        ds = xr.open_dataset(file)
        lats = ds.XLAT_M[0].values
        lons = ds.XLONG_M[0].values
        
        lat_min, lat_max = lats.min(), lats.max()
        lon_min, lon_max = lons.min(), lons.max()
        
        boundary_lats = [lat_min, lat_max, lat_max, lat_min, lat_min]
        boundary_lons = [lon_min, lon_min, lon_max, lon_max, lon_min]
        
        # Plot domain boundary
        ax.plot(boundary_lons, boundary_lats,
                transform=ccrs.PlateCarree(),
                color=colors[i],
                linestyle=line_styles[i],
                linewidth=2,
                label=f'Dominio: {i+1}')
    
    # Set map extent with some padding
    padding = 2  # degrees
    ax.set_extent([
        outer_lons.min() - padding,
        outer_lons.max() + padding,
        outer_lats.min() - padding,
        outer_lats.max() + padding
    ], crs=ccrs.PlateCarree())
    
    # Add gridlines
    gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.5)
    gl.top_labels = False
    gl.right_labels = False
    
    # Add legend
    ax.legend(loc='upper right', framealpha=1)
    
    #plt.title('Dominios del WRF')
    
    # Save figure with high resolution
    plt.savefig(output_file, dpi=dpi, bbox_inches='tight')
    plt.close()  # Close the figure to free memory
    
    print(f"Map saved as {output_file} with {dpi} DPI")

# Example usage
if __name__ == "__main__":
   
    geo_em_files = [
        '/LUSTRE/cursos/2025/semestre2/seminarioiv/p.8510/WRFV4/WPS/geo_em.d01.nc',
        '/LUSTRE/cursos/2025/semestre2/seminarioiv/p.8510/WRFV4/WPS/geo_em.d02.nc',
        #'geo_em.d03.nc'
    ]
    
    # Save the map with custom filename and resolution
    plot_wrf_domains_single_map(
        geo_em_files,
        output_file='wrf_dominios_con_estados.png',
        dpi=300
    )
