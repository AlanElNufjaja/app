# asteroides.py
import pandas as pd

# Función para cargar y combinar los CSVs
def cargar_meteoritos(base_csv="datos_base.csv", limpios_csv="datos_limpios.csv"):
    df_base = pd.read_csv(base_csv)
    df_limpios = pd.read_csv(limpios_csv)
    df_completo = pd.merge(df_base, df_limpios, on='id', how='inner')
    return df_completo

# Función para obtener la lista de IDs de meteoritos
def lista_ids():
    df = cargar_meteoritos()
    return df['id'].tolist()

# Función para obtener datos de un meteorito por ID
def datos_meteorito(id_meteorito):
    df = cargar_meteoritos()
    df_sel = df[df['id'] == id_meteorito]
    if not df_sel.empty:
        return df_sel.iloc[0].to_dict()
    else:
        return None
