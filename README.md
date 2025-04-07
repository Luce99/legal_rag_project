# Procesador de Documentos Legales

Este proyecto procesa documentos legales en formato PDF, extrayendo información estructurada y metadatos relevantes para su uso en sistemas RAG (Retrieval-Augmented Generation).

## Características

- Extracción de texto de documentos PDF
- Detección automática de:
  - Tipo de documento (Reglamento, Otro Sí, Resolución, etc.)
  - Entidad emisora (Colsubsidio, Compensar, etc.)
  - Fechas de vigencia
  - Artículos y modificaciones
- Normalización de fechas a formato ISO
- Extracción de secciones y referencias cruzadas
- Generación de JSON estructurado para uso en RAG

## Estructura del Proyecto

```
/legal_rag_project
  ├── /data
  │   ├── /raw_pdfs
  │   └── /processed
  ├── /src
  │   ├── config.py
  │   ├── pdf_processor.py
  │   └── main.py
  ├── requirements.txt
  └── README.md
```

## Requisitos

- Python 3.10+
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/legal_rag_project.git
cd legal_rag_project
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Colocar los PDFs a procesar en la carpeta `data/raw_pdfs/datos/`

2. Ejecutar el procesador:
```bash
python src/main.py
```

3. Los archivos procesados se guardarán en `data/processed/` en formato JSON.

## Estructura del JSON de Salida

```json
{
    "metadata": {
        "legal_entity": "nombre_entidad",
        "document_type": "tipo_documento",
        "effective_date": "fecha_formato_ISO",
        "articles_modified": ["Artículo 1", "Artículo 2"],
        "jurisdiction": "Bogotá",
        "references": ["Artículo 3", "Artículo 4"],
        "total_articles": 10,
        "total_sections": 5
    },
    "content": {
        "sections": {
            "considerandos": "texto...",
            "objetivo": "texto...",
            "definiciones": "texto..."
        },
        "articles": [
            {
                "text": "Artículo 1. Contenido...",
                "metadata": {
                    "article": "Artículo 1",
                    "is_amendment": true,
                    "paragraphs": ["párrafo 1", "párrafo 2"]
                }
            }
        ]
    }
}
```

## Contribución

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir los cambios propuestos.

## Licencia

Este proyecto está bajo la Licencia MIT. 