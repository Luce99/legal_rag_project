import argparse
from pathlib import Path
from pdf_processor import LegalPDFProcessor
from config import setup_logging, RAW_PDFS_DIR

logger = setup_logging()

def main():
    parser = argparse.ArgumentParser(description="Procesador de documentos legales")
    args = parser.parse_args()
    
    try:
        # Procesar PDFs
        processor = LegalPDFProcessor()
        # Buscar PDFs recursivamente en todas las subcarpetas
        pdf_files = list(RAW_PDFS_DIR.rglob("*.pdf"))
        
        if not pdf_files:
            logger.warning("No se encontraron archivos PDF para procesar")
            return
        
        logger.info(f"Iniciando procesamiento de {len(pdf_files)} archivos PDF...")
        
        for pdf_path in pdf_files:
            try:
                logger.info(f"Procesando: {pdf_path}")
                processor.process_pdf(pdf_path)
            except Exception as e:
                logger.error(f"Error al procesar {pdf_path}: {str(e)}")
        
        logger.info("Procesamiento completado")
        
    except Exception as e:
        logger.error(f"Error en la ejecución: {str(e)}")
        raise

if __name__ == "__main__":
    main() 