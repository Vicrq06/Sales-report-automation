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

def exportar(df):
    df.to_excel(Output_dir/"df_final",index=True)
    log.debug("Se ha exportado el dataframe")

def estadisticas_pd(df):
    return df.describe()

def merge(df_i,df_d,how):
    df_merge=pd.merge(df_i,df_d,how=how)
    log.debug("Se ha hecho merge del dataframe")
    return df_merge

def pivot_pd(df,indice,columna,valores):
    df1=df.pivot(index=indice,columns=columna,values=valores).copy()
    log.debug("Se ha hecho pivot del dataframe")
    return df1

def pivot_table_pd(df,indice,columna,valores,funcion,marg:bool):
    df_pivot=df.pivot_table(index=indice,columns=columna,values=valores,aggfunc=funcion,margins=marg).copy()
    log.debug("Se ha hecho pivot_table del dataframe")
    return df_pivot

def group_by(df:pd.DataFrame,
             columnas_a_agrupar:list[str],
             agregaciones):
    
    log.debug("Se ha hecho groupby del dataframe")
    resultado = df.groupby(columnas_a_agrupar).agg(agregaciones).copy()

    return resultado

def export_graph(df,columna):
    df[columna].plot(kind="")
    plt.title("")
    plt.ylabel("")
    plt.show()