from utils import get_xslx
from logging_src import log
from process import combinar_data
import process


if __name__=="__main__":
    archivos=get_xslx()
    if not archivos: 
        log.error("No hay archivos XLSX")
    df=combinar_data(archivos)
    df_estadisticas=process.estadisticas_pd(df)
    
    print ("Df combinado")
    print (df)


    print ("Ejecutando analisis de estadisticas básicas (describe)")
    print (df_estadisticas)

    print ("Cambiando formato largo a ancho (pivot)")
    df_pivot=process.pivot_pd(df,indice="Fecha",columna="Id_producto",valores="Total")
    print (df_pivot)

    print ("Agrupando por id y usando suma como metodo de agregacion:")
    df_groupby=process.group_by(df,("Id_producto"),{"Total":"sum"})
    print (df_groupby)

    print ("Pivot table usando suma como método de agregacion sin margins:")
    df_pivot_table=process.pivot_table_pd(df,("Id_producto"),"Producto","Total",sum,False).fillna(0)
    print (df_pivot_table)     #Este método no es necesario aqui ya que no existen productos distintos con el mismo id, asi que conviene mas usar groupby
    
    print ("Exportando gráfica de pivot table")
    process.export_graph(df_pivot_table,tipo="bar",nombre="Grafico")

    print ("Exportacion de excel")
    excel=process.exportar_excel()
    excel.exportar(df_pivot_table,"estadisticas")


    
    