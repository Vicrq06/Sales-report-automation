import pandas as pd 
from pathlib import Path
from logging_src import log
from utils import Output_dir
import openpyxl
import matplotlib.pyplot as plt

def limpieza_carga (archivo):
    if archivo.is_file() :
        df=pd.read_excel(archivo)
        df["Fecha"]=pd.to_datetime(df["Fecha"],errors="coerce")
        df=df.dropna(axis=0,subset=["Id_producto","Precio","Cantidad"])
        df["Precio"]=df["Precio"].astype(float)
        df["Cantidad"]=df["Cantidad"].astype(int)
        df["Total"]=df["Precio"]*df["Cantidad"]
        df["Id_producto"]=df["Id_producto"].astype(int)
        log.debug(f"Se ha limpieado el archivo {archivo.name}")
        return df
    else:
        log.error(f"Error en la limpieza del archivo {archivo.name}")
        return None

def combinar_data(files):
    dataframes=[]
    for file in files:
        df=limpieza_carga(file)
        dataframes.append(df)
    df=pd.concat(dataframes,axis=0)
    log.debug("Dataframe combinado.")
    return df

def exportar(df,to=None):
    try:
        if to=="Excel":
            df.to_excel(Output_dir/"df_final",index=True)
            log.debug("Se ha exportado el excel del dataframe")
        elif to=="csv":
            df.to_csv(Output_dir/"df_final")
            log.debug("Se ha exportado el csv del dataframe")
    except Exception as e:
        log.error(f"Ha ocurrido un error al exportar a {to}: ", e)

def estadisticas_pd(df):
    return df.describe()

def merge(df_i,df_d,how):
    try:
        df_merge=pd.merge(df_i,df_d,how=how)
        log.debug("Se ha hecho merge del dataframe")
        return df_merge
    except Exception as e:
        log.error(f"Error al agrupar el dataframe: {e}")
        return None

def pivot_pd(df,indice,columna,valores):
    try:
        df1=df.pivot(index=indice,columns=columna,values=valores).copy()
        log.debug("Se ha hecho pivot del dataframe")
        return df1
    except Exception as e:
        log.error(f"Error al agrupar el dataframe: {e}")
        return None


def pivot_table_pd(df,indice,columna,valores,funcion,marg:bool):
    try:
        df_pivot=df.pivot_table(index=indice,columns=columna,values=valores,aggfunc=funcion,margins=marg).copy()
        log.debug("Se ha hecho pivot_table del dataframe")
        return df_pivot
    except Exception as e:
        log.error(f"Error al agrupar el dataframe: {e}")
        return None

def group_by(df:pd.DataFrame,
             columnas_a_agrupar:list[str],
             agregaciones):
    try:
        log.debug("Se ha hecho groupby del dataframe")
        resultado = df.groupby(columnas_a_agrupar).agg(agregaciones).copy()
        return resultado
    except Exception as e:
        log.error(f"Error al agrupar el dataframe: {e}")
        return None

def export_graph(df,tipo):
    df.plot(kind=tipo)
    plt.title("Producto vs precio")
    plt.ylabel("Precio")
    plt.show()
    

