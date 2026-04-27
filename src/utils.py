from pathlib import Path

Base_path=Path(__file__).resolve().parent.parent
Raw_dir=Base_path/"data"/"Raw"
Output_dir=Base_path/"output"
Processed_dir=Base_path/"data"/"Processed"

Processed_dir.mkdir(exist_ok=True)
Output_dir.mkdir(exist_ok=True)

def get_xslx ():
    archivos=list(Raw_dir.glob("*.xlsx"))
    return archivos
