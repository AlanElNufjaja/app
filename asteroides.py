import pandas as pd

def cargar_meteoritos(base_csv="datos_base.csv", limpios_csv="datos_limpios.csv"):
    """
    Carga y combina los CSVs de meteoritos.
    Combina por índice si 'datos_limpios.csv' no tiene columna 'id'.
    """
    df_base = pd.read_csv(base_csv)
    df_limpios = pd.read_csv(limpios_csv)

    # Revisar si 'id' existe en df_limpios
    if 'id' in df_limpios.columns:
        df_completo = pd.merge(df_base, df_limpios, on='id', how='inner')
    else:
        # Combinar por índice
        df_completo = pd.concat([df_base.reset_index(drop=True), df_limpios.reset_index(drop=True)], axis=1)

    return df_completo

def lista_ids(df_completo):
    return df_completo['id'].tolist() if 'id' in df_completo.columns else list(range(len(df_completo)))

def datos_meteorito(df_completo, id_meteorito):
    """
    Devuelve un diccionario con los datos del meteorito seleccionado.
    """
    if 'id' in df_completo.columns:
        df_sel = df_completo[df_completo['id'] == id_meteorito]
    else:
        df_sel = df_completo.iloc[[id_meteorito]]  # usar índice como id
    return df_sel.iloc[0].to_dict() if not df_sel.empty else None
