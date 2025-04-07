from pathlib import Path
from config import RAW_PDFS_DIR, PROCESSED_DIR
import json
from datetime import datetime

def check_processing_status():
    print("\n=== Estado de Procesamiento de Documentos ===\n")
    
    # Obtener lista de PDFs
    pdf_files = list(RAW_PDFS_DIR.rglob("*.pdf"))
    processed_files = list(PROCESSED_DIR.glob("*.json"))
    
    print(f"Total PDFs encontrados: {len(pdf_files)}")
    print(f"Total archivos procesados: {len(processed_files)}\n")
    
    # Crear diccionario de archivos procesados
    processed_dict = {f.stem: f for f in processed_files}
    
    # Verificar cada PDF
    for pdf_path in pdf_files:
        status = "✅ Procesado" if pdf_path.stem in processed_dict else "❌ Pendiente"
        print(f"{status} - {pdf_path.name}")
        
        # Si está procesado, mostrar metadatos
        if pdf_path.stem in processed_dict:
            try:
                with open(processed_dict[pdf_path.stem], 'r', encoding='utf-8') as f:
                    metadata = json.load(f)['metadata']
                    print(f"   Entidad: {metadata['legal_entity']}")
                    print(f"   Tipo: {metadata['document_type']}")
                    print(f"   Fecha: {metadata['effective_date']}")
                    print(f"   Artículos modificados: {len(metadata['articles_modified'])}")
                    print()
            except Exception as e:
                print(f"   Error al leer metadatos: {str(e)}\n")

if __name__ == "__main__":
    check_processing_status() 