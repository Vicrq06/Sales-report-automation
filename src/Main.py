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
    
    print (df)
    print ("PIVOT")

    df_pivot=process.pivot_pd(df,indice="Fecha",columna="Id_producto",valores="Total")
    print (df_pivot)

    df_groupby=process.group_by(df,("Id_producto"),{"Total":"sum"})
    print (df_groupby)

    df_pivot_table=process.pivot_table_pd(df,("Id_producto"),"Producto","Total",sum,False).fillna(0)
    print (df_pivot_table)



    
    