from typing import List, Dict, Any
import re
from pathlib import Path
import json
from datetime import datetime
from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text
from config import PROCESSED_DIR, setup_logging

logger = setup_logging()

class LegalPDFProcessor:
    def __init__(self):
        self.document_types = {
            "reglamento": r"(?i)reglamento",
            "otro_si": r"(?i)otro\s+s[ií]",
            "resolucion": r"(?i)resoluci[oó]n",
            "circular": r"(?i)circular",
            "acuerdo": r"(?i)acuerdo",
            "decreto": r"(?i)decreto"
        }
        
        self.legal_entities = {
            "colsubsidio": r"(?i)colsubsidio",
            "compensar": r"(?i)compensar",
            "cafam": r"(?i)cafam",
            "comfacundi": r"(?i)comfacundi",
            "comcaja": r"(?i)comcaja"
        }
        
        self.section_patterns = {
            "considerandos": r"(?i)considerando[s]?",
            "objetivo": r"(?i)objetivo[s]?",
            "definiciones": r"(?i)definici[oó]n[es]?",
            "alcance": r"(?i)alcance",
            "vigencia": r"(?i)vigencia",
            "disposiciones": r"(?i)disposici[oó]n[es]?\s+final[es]?"
        }
    
    def _detect_document_type(self, text: str) -> str:
        for doc_type, pattern in self.document_types.items():
            if re.search(pattern, text):
                return doc_type
        return "desconocido"
    
    def _detect_legal_entity(self, text: str) -> str:
        for entity, pattern in self.legal_entities.items():
            if re.search(pattern, text):
                return entity
        return "desconocida"
    
    def _extract_date(self, text: str) -> str:
        date_patterns = [
            r"(\d{1,2})\s+de\s+([a-z]+)\s+de\s+(\d{4})",
            r"(\d{1,2})/(\d{1,2})/(\d{4})",
            r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})"
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                if "/" in pattern or "-" in pattern:
                    if len(match.groups()) == 3:
                        if len(match.group(1)) == 4:  # Formato YYYY/MM/DD
                            year, month, day = map(int, match.groups())
                        else:  # Formato DD/MM/YYYY
                            day, month, year = map(int, match.groups())
                else:
                    day = int(match.group(1))
                    month = self._spanish_month_to_number(match.group(2))
                    year = int(match.group(3))
                
                try:
                    return datetime(year, month, day).strftime("%Y-%m-%d")
                except ValueError:
                    continue
        
        return "desconocida"
    
    def _spanish_month_to_number(self, month: str) -> int:
        months = {
            "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
            "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
            "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
        }
        return months.get(month.lower(), 1)
    
    def _extract_sections(self, text: str) -> Dict[str, str]:
        sections = {}
        current_section = "introduccion"
        current_content = []
        
        # Dividir el texto en líneas
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Verificar si la línea indica una nueva sección
            section_found = False
            for section_name, pattern in self.section_patterns.items():
                if re.search(pattern, line):
                    if current_content:
                        sections[current_section] = '\n'.join(current_content)
                    current_section = section_name
                    current_content = []
                    section_found = True
                    break
            
            if not section_found:
                current_content.append(line)
        
        # Agregar la última sección
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def _extract_articles(self, text: str) -> List[Dict[str, Any]]:
        articles = []
        article_pattern = r"(?i)art[ií]culo\s+(\d+)[.:]\s*(.*?)(?=\n\n|$)"
        
        for match in re.finditer(article_pattern, text, re.DOTALL):
            article_text = match.group(0).strip()
            article_number = match.group(1)
            content = match.group(2).strip()
            
            # Extraer párrafos del artículo
            paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
            
            articles.append({
                "text": article_text,
                "metadata": {
                    "article": f"Artículo {article_number}",
                    "is_amendment": "modifica" in article_text.lower(),
                    "paragraphs": paragraphs
                }
            })
        
        return articles
    
    def _extract_references(self, text: str) -> List[str]:
        reference_pattern = r"(?i)(?:art[ií]culo|art\.)\s+\d+"
        return list(set(re.findall(reference_pattern, text)))
    
    def process_pdf(self, pdf_path: Path) -> Dict[str, Any]:
        logger.info(f"Procesando PDF: {pdf_path.name}")
        
        # Extraer texto usando pdfminer
        text = extract_text(str(pdf_path))
        
        # Extraer metadatos básicos
        doc_type = self._detect_document_type(text)
        legal_entity = self._detect_legal_entity(text)
        effective_date = self._extract_date(text)
        
        # Extraer secciones
        sections = self._extract_sections(text)
        
        # Extraer artículos
        articles = self._extract_articles(text)
        modified_articles = [
            article["metadata"]["article"]
            for article in articles
            if article["metadata"]["is_amendment"]
        ]
        
        # Extraer referencias cruzadas
        references = self._extract_references(text)
        
        # Construir resultado
        result = {
            "metadata": {
                "legal_entity": legal_entity,
                "document_type": doc_type,
                "effective_date": effective_date,
                "articles_modified": modified_articles,
                "jurisdiction": "Bogotá",  # Por defecto
                "references": references,
                "total_articles": len(articles),
                "total_sections": len(sections)
            },
            "content": {
                "sections": sections,
                "articles": articles
            }
        }
        
        # Guardar resultado
        output_path = PROCESSED_DIR / f"{pdf_path.stem}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        logger.info(f"PDF procesado y guardado en: {output_path}")
        return result 