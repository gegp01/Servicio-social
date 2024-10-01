import xarray as xr
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import seaborn as sns
import os
# Ruta de entrada en el clúster
file_path = "/storage/ggarcia_g/imandt/Land_and_Ocean_EqualArea.nc"

data = xr.open_dataset(file_path)
latitudes = data['latitude'].values
longitudes = data['longitude'].values
temperature = data['temperature'].values

times = data['time'].values
lat_grid = np.linspace(latitudes.min(), latitudes.max(),100)  # Adjust grid resolution as needed
lon_grid = np.linspace(longitudes.min(), longitudes.max(), 100)
lon_grid_mesh, lat_grid_mesh = np.meshgrid(lon_grid, lat_grid)
# Define the decades based on the time variable (assuming time is in years)
decades = np.floor(times / 10) * 10

# Initialize a dictionary to hold the correlation matrices by decade
correlation_matrices_by_decade = {}

# Process data by decade
unique_decades = np.unique(decades)

# Create a directory to save the data
save_dir = '/storage/ggarcia_g/imandt/decade_correlations_lag_3'
os.makedirs(save_dir, exist_ok=True)

for decade in unique_decades:
    # Extract data for the current decade
    decade_mask = (decades == decade)
    temperature_decade = temperature[decade_mask, :]
    
    # Interpolate the data onto a regular grid for all time points in the decade
    num_time_points_decade = temperature_decade.shape[0]
    temperature_grid_over_time_decade = np.empty((num_time_points_decade, 100, 100))
    
    for t in range(num_time_points_decade):
        temperature_grid_over_time_decade[t] = griddata(
            (latitudes, longitudes), 
            temperature_decade[t], 
            (lat_grid_mesh, lon_grid_mesh), 
            method='linear'
        )
    
    # Reshape the data for correlation calculation
    reshaped_temperature_data_decade = temperature_grid_over_time_decade.reshape(num_time_points_decade, -1)
    
    # Initialize an array to hold the lagged correlation matrices
    correlation_matrix_decade_lag3 = np.empty((reshaped_temperature_data_decade.shape[1], reshaped_temperature_data_decade.shape[1]))
    
    # Calculate the lag-3 correlation matrix for this decade
    for i in range(reshaped_temperature_data_decade.shape[1]):
        for j in range(reshaped_temperature_data_decade.shape[1]):
            if num_time_points_decade > 3:
                correlation_matrix_decade_lag3[i, j] = np.corrcoef(
                    reshaped_temperature_data_decade[:-3, i],  # Datos sin los últimos 3 pasos
                    reshaped_temperature_data_decade[3:, j]   # Datos desplazados 3 pasos hacia adelante
                )[0, 1]
            else:
                correlation_matrix_decade_lag3[i, j] = np.nan  # Manejar cuando no hay suficientes datos para el lag
    
    # Store the correlation matrix in the dictionary
    correlation_matrices_by_decade[int(decade)] = correlation_matrix_decade_lag3
    
    # Save the correlation matrix for this decade
    np.save(os.path.join(save_dir, f'correlation_matrix_lag3_{int(decade)}.npy'), correlation_matrix_decade_lag3)

# Outputting the keys (decades) for confirmation
saved_decades = list(correlation_matrices_by_decade.keys())

# Save the list of decades
np.save(os.path.join(save_dir, 'saved_decades.npy'), np.array(saved_decades))

