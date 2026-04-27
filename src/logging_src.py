import logging as log 

log.basicConfig(level=log.DEBUG,
                format="%(asctime)s : %(levelname)s : %(message)s",
                datefmt="%I %M %S: %p",
                handlers=[
                    log.FileHandler(r"C:\Users\power\OneDrive\Escritorio\archivos_t\Proyectos\Proyecto Informe ventas\output\registros.log"),
                    log.StreamHandler()
                ]
)

