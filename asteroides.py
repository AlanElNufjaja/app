import pandas as pd

def cargar_meteoritos(base_csv="datos_base.csv", limpios_csv="datos_limpios.csv"):
    """
    Carga y combina los CSVs de meteoritos.
    """
    df_base = pd.read_csv(base_csv)
    df_limpios = pd.read_csv(limpios_csv)
    df_completo = pd.merge(df_base, df_limpios, on='id', how='inner')
    return df_completo

def lista_ids(df_completo):
    return df_completo['id'].tolist()

def datos_meteorito(df_completo, id_meteorito):
    """
    Devuelve un diccionario con los datos del meteorito seleccionado.
    """
    df_sel = df_completo[df_completo['id'] == id_meteorito]
    if not df_sel.empty:
        return df_sel.iloc[0].to_dict()
    return None
