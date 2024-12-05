import xarray as xr
import numpy as np
from sklearn.metrics import mutual_info_score
from sklearn.preprocessing import KBinsDiscretizer
from joblib import Parallel, delayed
from tqdm import tqdm
import os
import sys

def main(decade_to_process):
    # Ruta de entrada en el clúster
    file_path = "/storage/ggarcia_g/imandt/Updated_Land_and_Ocean_EqualArea.nc"

    # Abrir el dataset
    data = xr.open_dataset(file_path)
    latitudes = data['latitude'].values
    longitudes = data['longitude'].values
    temperature = data['temperature'].values

    times = data['time'].values

    # Definir las décadas basadas en la variable de tiempo
    decades = np.floor(times / 10) * 10

    # Crear un directorio para guardar los datos
    save_dir = '/storage/ggarcia_g/imandt/updated_decade_mutual_info_lag1'
    os.makedirs(save_dir, exist_ok=True)

    # Inicializar el discretizador para la información mutua
    discretizer = KBinsDiscretizer(n_bins=10, encode='ordinal', strategy='uniform')

    # Procesar una década específica
    decade = decade_to_process
    print(f"Procesando década: {int(decade)}")
    
    # Extraer datos para la década actual
    decade_mask = (decades == decade)
    temperature_decade = temperature[decade_mask, :]

    # Remover NaN y valores infinitos
    temperature_decade = np.nan_to_num(temperature_decade, nan=np.nanmean(temperature_decade))
    temperature_decade = np.where(np.isfinite(temperature_decade), temperature_decade, np.nanmean(temperature_decade))

    # Reshape de los datos para el cálculo de la información mutua
    num_time_points_decade = temperature_decade.shape[0]
    reshaped_temperature_data_decade = temperature_decade.reshape(num_time_points_decade, -1)

    # Discretizar los datos
    reshaped_temperature_data_discrete = discretizer.fit_transform(reshaped_temperature_data_decade)
    reshaped_temperature_data_discrete = reshaped_temperature_data_discrete.astype(int)

    num_grid_points = reshaped_temperature_data_discrete.shape[1]

    # Definir lag
    lag = 1  # Lag de 1 mes

    # Verificar que el lag no sea mayor que el número de puntos temporales
    if num_time_points_decade <= lag:
        print(f"Error: El lag {lag} es demasiado grande para el número de puntos temporales {num_time_points_decade}")
        sys.exit(1)

    # Preparar pares de índices para calcular información mutua
    pairs = []
    for i in range(num_grid_points):
        for j in range(i, num_grid_points):
            pairs.append((i, j))

    # Definir la función para calcular y almacenar la información mutua con lag
    def compute_mutual_info(pair):
        i, j = pair
        mi = mutual_info_score(
            reshaped_temperature_data_discrete[:-lag, i],
            reshaped_temperature_data_discrete[lag:, j]
        )
        return (i, j, mi)

    # Número de trabajos paralelos, ajusta según los recursos disponibles
    n_jobs = int(os.environ.get('SLURM_CPUS_PER_TASK', 1))  # Obtener número de CPUs desde SLURM

    # Calcular la información mutua en paralelo
    results = Parallel(n_jobs=n_jobs, backend='loky')(
        delayed(compute_mutual_info)(pair) for pair in tqdm(pairs, desc=f"Calculando MI con lag para década {int(decade)}")
    )

    # Inicializar una matriz para la información mutua
    mutual_info_matrix_decade = np.empty((num_grid_points, num_grid_points))
    mutual_info_matrix_decade[:] = np.nan  # Inicializar con NaNs

    # Rellenar la matriz con los resultados
    for i, j, mi in results:
        mutual_info_matrix_decade[i, j] = mi
        mutual_info_matrix_decade[j, i] = mi  # Simetría

    # Guardar la matriz de información mutua para esta década
    np.save(os.path.join(save_dir, f'updated_mutual_info_matrix_decade_{int(decade)}_lag1.npy'), mutual_info_matrix_decade)

    print(f"Década {int(decade)} procesada y guardada exitosamente con lag de 1 mes.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python mutual_info_parallel_single_lag.py <decade>")
        sys.exit(1)
    decade_input = float(sys.argv[1])
    main(decade_input)
