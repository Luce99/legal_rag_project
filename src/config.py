import os
import logging
from pathlib import Path

# Configuración de directorios
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_PDFS_DIR = DATA_DIR / "raw_pdfs" / "datos"  # Cambiado para apuntar directamente a la carpeta datos
PROCESSED_DIR = DATA_DIR / "processed"

# Configuración de logging
def setup_logging():
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "legal_rag.log"),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

# Crear directorios si no existen
RAW_PDFS_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True) 