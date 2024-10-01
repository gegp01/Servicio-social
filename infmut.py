import xarray as xr
import numpy as np
from scipy.interpolate import griddata
import os
import sys
from sklearn.metrics import mutual_info_score
from sklearn.preprocessing import KBinsDiscretizer
from joblib import Parallel, delayed
from tqdm import tqdm

def main(decade_to_process):
    # Ruta de entrada en el clúster
    file_path = "/storage/ggarcia_g/imandt/Land_and_Ocean_EqualArea.nc"

    # Abrir el dataset
    data = xr.open_dataset(file_path)
    latitudes = data['latitude'].values
    longitudes = data['longitude'].values
    temperature = data['temperature'].values

    times = data['time'].values
    lat_grid = np.linspace(latitudes.min(), latitudes.max(), 100)  # Reducido a 50 para mejorar el rendimiento
    lon_grid = np.linspace(longitudes.min(), longitudes.max(), 100)
    lon_grid_mesh, lat_grid_mesh = np.meshgrid(lon_grid, lat_grid)

    # Definir las décadas basadas en la variable de tiempo (asumiendo que el tiempo está en años)
    decades = np.floor(times / 10) * 10

    # Crear un directorio para guardar los datos
    save_dir = '/storage/ggarcia_g/imandt/decade_mutual_info'
    os.makedirs(save_dir, exist_ok=True)

    # Inicializar el discretizador para la información mutua
    # Usaremos 10 bins; ajusta según tus necesidades
    discretizer = KBinsDiscretizer(n_bins=10, encode='ordinal', strategy='uniform')

    # Procesar una década específica
    decade = decade_to_process
    print(f"Procesando década: {int(decade)}")
    # Extraer datos para la década actual
    decade_mask = (decades == decade)
    temperature_decade = temperature[decade_mask, :]

    # Interpolar los datos en una malla regular para todos los puntos temporales en la década
    num_time_points_decade = temperature_decade.shape[0]
    temperature_grid_over_time_decade = np.empty((num_time_points_decade, 100, 100))

    for t in range(num_time_points_decade):
        temperature_grid_over_time_decade[t] = griddata(
            (latitudes, longitudes), 
            temperature_decade[t], 
            (lat_grid_mesh, lon_grid_mesh), 
            method='linear'
        )

    # Manejar posibles NaNs después de la interpolación
    temperature_grid_over_time_decade = np.nan_to_num(
        temperature_grid_over_time_decade, 
        nan=np.nanmean(temperature_grid_over_time_decade)
    )

    # Reshape de los datos para el cálculo de la información mutua
    reshaped_temperature_data_decade = temperature_grid_over_time_decade.reshape(num_time_points_decade, -1)

    # Discretizar los datos
    reshaped_temperature_data_discrete = discretizer.fit_transform(reshaped_temperature_data_decade)
    reshaped_temperature_data_discrete = reshaped_temperature_data_discrete.astype(int)

    num_grid_points = reshaped_temperature_data_discrete.shape[1]

    # Preparar pares de índices para calcular información mutua
    pairs = []
    for i in range(num_grid_points):
        for j in range(i, num_grid_points):
            pairs.append((i, j))

    # Definir la función para calcular y almacenar la información mutua
    def compute_mutual_info(pair):
        i, j = pair
        return (i, j, mutual_info_score(
            reshaped_temperature_data_discrete[:, i],
            reshaped_temperature_data_discrete[:, j]
        ))

    # Número de trabajos paralelos, ajusta según los recursos disponibles
    n_jobs = int(os.environ.get('SLURM_CPUS_PER_TASK', 1))  # Obtener número de CPUs desde SLURM

    # Calcular la información mutua en paralelo
    results = Parallel(n_jobs=n_jobs, backend='loky')(
        delayed(compute_mutual_info)(pair) for pair in tqdm(pairs, desc=f"Calculando MI para década {int(decade)}")
    )

    # Inicializar una matriz para la información mutua
    mutual_info_matrix_decade = np.empty((num_grid_points, num_grid_points))
    mutual_info_matrix_decade[:] = np.nan  # Inicializar con NaNs

    # Rellenar la matriz con los resultados
    for i, j, mi in results:
        mutual_info_matrix_decade[i, j] = mi
        mutual_info_matrix_decade[j, i] = mi  # Simetría

    # Guardar la matriz de información mutua para esta década
    np.save(os.path.join(save_dir, f'mutual_info_matrix_decade_{int(decade)}.npy'), mutual_info_matrix_decade)

    print(f"Década {int(decade)} procesada y guardada exitosamente.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python mutual_info_parallel_single.py <decade>")
        sys.exit(1)
    decade_input = float(sys.argv[1])
    main(decade_input)
