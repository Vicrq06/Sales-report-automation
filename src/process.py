from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from logging_src import log
from utils import Output_dir
from utils import Raw_dir

# SETEO
log.basicConfig(level=log.DEBUG)


# CARGA Y LIMPIEZA
class DataLoader:

    @staticmethod
    def limpieza_carga(archivo: Path):

        if archivo.is_file():
            df = pd.read_excel(archivo)
            df["Fecha"] = pd.to_datetime(
                df["Fecha"],
                errors="coerce"
            )
            df = df.dropna(
                axis=0,
                subset=["Id_producto", "Precio", "Cantidad"]
            )
            df["Precio"] = df["Precio"].astype(float)
            df["Cantidad"] = df["Cantidad"].astype(int)
            df["Id_producto"] = df["Id_producto"].astype(int)
            df["Total"] = df["Precio"] * df["Cantidad"]
            log.debug(f"Archivo limpio: {archivo.name}")
            return df
        else:
            log.error(f"Error al cargar archivo: {archivo.name}")
            return None

    @classmethod
    def combinar_data(cls, files: list[Path]):
        dataframes = []
        for file in files:
            df = cls.limpieza_carga(file)
            if df is not None:
                dataframes.append(df)

        df_final = pd.concat(dataframes, axis=0)
        log.debug("DataFrames combinados")
        return df_final


# TRANSFORMACIONES
class DataProcessor:

    @staticmethod
    def estadisticas(df):
        return df.describe()

    @staticmethod
    def merge(df_i, df_d, how, on):

        try:
            df_merge = pd.merge(
                df_i,
                df_d,
                how=how,
                on=on
            )
            log.debug("Merge realizado")
            return df_merge

        except Exception as e:
            log.error(f"Error en merge: {e}")
            return None

    @staticmethod
    def pivot(df, indice, columna, valores):

        try:
            df_pivot = df.pivot(
                index=indice,
                columns=columna,
                values=valores
            ).copy()
            log.debug("Pivot realizado")
            return df_pivot

        except Exception as e:
            log.error(f"Error en pivot: {e}")
            return None

    @staticmethod
    def pivot_table(
        df,
        indice,
        columna,
        valores,
        funcion,
        marg: bool
    ):

        try:
            df_pivot = df.pivot_table(
                index=indice,
                columns=columna,
                values=valores,
                aggfunc=funcion,
                margins=marg
            ).copy()
            log.debug("Pivot table realizado")
            return df_pivot

        except Exception as e:

            log.error(f"Error en pivot_table: {e}")

            return None

    @staticmethod
    def group_by(
        df: pd.DataFrame,
        columnas_a_agrupar: list[str],
        agregaciones
    ):

        try:
            resultado = (
                df.groupby(columnas_a_agrupar)
                .agg(agregaciones)
                .copy()
            )
            log.debug("Groupby realizado")
            return resultado

        except Exception as e:
            log.error(f"Error en groupby: {e}")
            return None

# EXPORTADORES
class Exportador(ABC):

    @abstractmethod
    def exportar(self, df, nombre):
        pass


class ExportarExcel(Exportador):
    def exportar(self, df, nombre):
        path = Output_dir / f"{nombre}.xlsx"
        df.to_excel(path, index=True)
        log.debug("Excel exportado")


class ExportarCSV(Exportador):

    def exportar(self, df, nombre):
        path = Output_dir / f"{nombre}.csv"
        df.to_csv(path, index=True)
        log.debug("CSV exportado")

# GRÁFICAS
class GraphExporter:

    @staticmethod
    def export_graph(
        df,
        x=None,
        y=None,
        tipo="line",
        nombre=None,
        save_path=Output_dir
    ):

        df.plot(
            x=x,
            y=y,
            kind=tipo
        )

        if save_path and nombre:

            path = save_path / f"{nombre}.png"

            plt.savefig(path)

            log.debug("Gráfica exportada")

        plt.show()


# EJEMPLO DE USO
if __name__ == "__main__":

    archivos = [
        (Raw_dir/"ventas_enero.xlsx"),
        (Raw_dir/"ventas_febrero.xlsx"),
        (Raw_dir/"ventas_marzo.xlsx")
    ]

    # cargar y combinar
    df = DataLoader.combinar_data(archivos)

    # estadísticas
    print(DataProcessor.estadisticas(df))

    # groupby
    agrupado = DataProcessor.group_by(
        df,
        ["Id_producto"],
        {"Total": "sum"}
    )

    # exportar
    exportador = ExportarExcel()
    exportador.exportar(agrupado, "ventas_agrupadas")

    # gráfica
    GraphExporter.export_graph(
        agrupado,
        y="Total",
        nombre="grafica_ventas"
    )
    