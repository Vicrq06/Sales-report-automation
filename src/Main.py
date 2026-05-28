from utils import get_xslx
from logging_src import log
from utils import get_xslx
from logging_src import log

from process import (
    DataLoader,
    DataProcessor,
    GraphExporter,
    ExportarExcel,
    ExportarCSV
)


if __name__ == "__main__":

    # OBTENER ARCHIVOS
    archivos = get_xslx()
    if not archivos:
        log.error("No hay archivos XLSX")
        exit()

    # CARGA Y LIMPIEZA
    df = DataLoader.combinar_data(archivos)
    if df is None:
        log.error("No se pudo crear el DataFrame")
        exit()
    print("DF combinado")
    print(df)

    # ESTADÍSTICAS
    print("Ejecutando análisis estadístico")
    df_estadisticas = DataProcessor.estadisticas(df)
    print(df_estadisticas)

    # PIVOT
    print("Cambiando formato largo a ancho (pivot)")
    df_pivot = DataProcessor.pivot(
        df,
        indice="Fecha",
        columna="Id_producto",
        valores="Total"
    )
    print(df_pivot)

    # GROUPBY
    print("Agrupando por producto")
    df_groupby = DataProcessor.group_by(
        df,
        ["Id_producto"],
        {"Total": "sum"}
    )
    print(df_groupby)

    # PIVOT TABLE
    print("Pivot table")
    df_pivot_table = DataProcessor.pivot_table(
        df,
        indice="Id_producto",
        columna="Producto",
        valores="Total",
        funcion=sum,
        marg=False
    )

    df_pivot_table = df_pivot_table.fillna(0)

    print(df_pivot_table)


    # GRÁFICAS
    print("Exportando gráfica pivot table")
    GraphExporter.export_graph(
        df_pivot_table,
        tipo="bar",
        nombre="grafico_pivot"
    )
    print("Exportando gráfica estadísticas")
    GraphExporter.export_graph(
        df_estadisticas,
        tipo="bar",
        nombre="grafico_estadisticas"
    )


    # EXPORTACION

    print("Exportando Excel")
    excel = ExportarExcel()
    excel.exportar(
        df_pivot_table,
        "estadisticas"
    )
    print("Exportando CSV")
    csv = ExportarCSV()
    csv.exportar(
        df_pivot_table,
        "estadisticas_csv"
    )

    print("Exportando estadísticas generales")
    excel.exportar(
        df_estadisticas,
        "estadisticas_generales"
    )