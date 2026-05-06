import pandas as pd 
from pathlib import Path
from logging_src import log
from utils import Output_dir
import openpyxl
import matplotlib.pyplot as plt
from abc import (ABC,abstractmethod)
from dotenv import load_dotenv
import smtplib 
from email.message import EmailMessage
import os


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
    

class exportador (ABC):
    @abstractmethod
    def exportar(self,df,path):
        pass

class exportar_excel(exportador):
    def exportar(self, df, nombre=None):
        df.to_excel(f"{Output_dir/nombre}.xlsx",index=True)
        log.debug("Excel exportado con exito")

class exportar_csv(exportador):
    def exportar(self, df, nombre=None):
        df.to_csv(f"{Output_dir/nombre}.csv",index=True)
    

def estadisticas_pd(df):
    return df.describe()

def merge(df_i,df_d,how,on):
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

def export_graph(df, x=None, y=None, tipo="line",nombre=None,save_path=Output_dir):
    df.plot(x=x, y=y, kind=tipo)
    if save_path and nombre:
        path=save_path/f"{nombre}.png"
        plt.savefig(f"{path}")
        log.debug("Grafica exportada con éxito")
    plt.show()
    

load_dotenv()
EMAIL_USER=os.getenv("EMAIL_USER")
EMAIL_PASS=os.getenv("EMAIL_PASS")
def enviar_correo (asunto,cuerpo,destinatario,archivos=None):
    email=EmailMessage()
    email["To"]=destinatario
    email["From"]=EMAIL_USER
    email["Subject"]=asunto

    email.set_content(cuerpo)

    if archivos:
        for ruta in archivos:
            try:
                with open(ruta, "rb") as f:
                    file_data = f.read()
                    file_name = os.path.basename(ruta)

                email.add_attachment(
                    file_data,
                    maintype="application",
                    subtype="octet-stream",
                    filename=file_name
                )
            except Exception as e:
                print(f"Error adjuntando {ruta}: {e}")

    # 🚀 Enviar correo
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(email)

        log.debug("Correo enviado correctamente")

    except Exception as e:
        log.error(f"Error enviando correo: {e}")
    