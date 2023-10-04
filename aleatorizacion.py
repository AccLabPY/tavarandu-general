# Importando las bibliotecas
import pandas as pd
import numpy as np
import itertools
import threading
import time
import sys

# Carga del dataset 
df = pd.read_csv('Colegios_Secciones.csv')

# Filtrar las filas donde la columna aleatorización tiene el valor "SI" 
df_filtered = df[(df["incluido"] == "SI")]
df_filtered_copy = df_filtered.copy()


def stratified_randomization(data, strata_cols, treatment_col, seed_value=10):
    # Inicialización de la columna de tratamiento
    data[treatment_col] = None
    
    # Obtener valores únicos para cada estrato
    unique_strata = data[strata_cols].drop_duplicates()
    
    # Iterar sobre cada combinación única de estratos
    for _, stratum in unique_strata.iterrows():
        mask = (data[strata_cols] == stratum).all(axis=1)
        subset = data[mask]

        # Si solo hay una observación en el estrato, asignamos aleatoriamente
        if len(subset) == 1:
            assignments = ["no" if np.random.rand() < 0.5 else "si"]
        else:
            n_control = len(subset) // 2
            n_treatment = len(subset) - n_control
            assignments = ["no"] * n_control + ["si"] * n_treatment
            np.random.shuffle(assignments)

        data.loc[mask, treatment_col] = assignments

    return data

# Animación para simular que se está cargando algo
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rsorteando ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rSorteado!     ')


# Especificar las columnas de estrato, acá se puede agregar más estratos en el futuro con más casos
strata_columns = ['Institución','Año']

# Se elige un número de sorteos a realizar en público
num_sorteos = 10

# Aplicar la aleatorización por bloques, en N sorteos a definir según caso.
# Se utiliza como nombre de columna para la asignación el término "participa"
# que es más fácil de entender en un sorteo en vivo
# El valor "no" representa el control
# El valor "si" representa el tratamiento
for index in range (1,num_sorteos+1):
    done = False
    print("\n\nRealizando sorteo # ",index)
    seed = np.random.randint(100, 1000)
    print("La semilla utilizada para este sorteo es: ", seed)
    df_randomized = stratified_randomization(df_filtered_copy, strata_columns, 'participa', )
    print(df_randomized.loc[:,["Institución","Año","Sección","participa"]])

    # Simular una animación que indique que se está sorteando
    t = threading.Thread(target=animate)
    t.start()
    time.sleep(2)
    done = True
