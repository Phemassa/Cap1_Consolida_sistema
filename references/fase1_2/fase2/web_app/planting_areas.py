"""
Módulo de Gerenciamento de Áreas de Plantio
Carrega e processa dados dos CSVs da Fase 1
"""

import csv
import os
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class PlantingArea:
    """Representa uma área de plantio do CSV"""
    id: int
    culture: str  # "banana" ou "milho"
    area: float  # área em m²
    insumo: str
    qtd_insumo: float
    unidade: str
    # Dimensões (podem variar conforme figura)
    raio: Optional[float] = None
    comprimento: Optional[float] = None
    largura: Optional[float] = None
    figura: Optional[int] = None  # 1=retangulo, 2=triangulo, 3=circulo
    
    def get_dimensions_text(self) -> str:
        """Retorna texto com dimensões formatadas"""
        if self.figura == 3 and self.raio:
            return f"Raio: {self.raio}m"
        elif self.comprimento and self.largura:
            return f"{self.comprimento}m × {self.largura}m"
        return "Dimensões não especificadas"
    
    def get_shape_text(self) -> str:
        """Retorna nome da figura geométrica"""
        shapes = {1: "Retângulo", 2: "Triângulo", 3: "Círculo"}
        return shapes.get(self.figura, "Desconhecida")

class PlantingAreaManager:
    """Gerencia áreas de plantio dos CSVs"""
    
    def __init__(self, csv_base_path: str):
        """
        Inicializa o gerenciador
        
        Args:
            csv_base_path: Caminho base onde estão os CSVs (python_app)
        """
        self.csv_base_path = csv_base_path
        self.areas: Dict[str, List[PlantingArea]] = {
            "banana": [],
            "milho": []
        }
        self.load_all_areas()
    
    def load_all_areas(self):
        """Carrega áreas de todas as culturas"""
        self.areas["banana"] = self._load_culture_csv("banana")
        self.areas["milho"] = self._load_culture_csv("milho")
    
    def _load_culture_csv(self, culture: str) -> List[PlantingArea]:
        """Carrega dados de um CSV específico"""
        csv_path = os.path.join(self.csv_base_path, f"{culture}.csv")
        areas = []
        
        if not os.path.exists(csv_path):
            print(f"Aviso: CSV não encontrado: {csv_path}")
            return areas
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for idx, row in enumerate(reader, start=1):
                    # Converte valores, tratando strings vazias
                    def safe_float(value):
                        if value and value.strip():
                            return float(value)
                        return None
                    
                    def safe_int(value):
                        if value and value.strip():
                            return int(float(value))
                        return None
                    
                    area = PlantingArea(
                        id=idx,
                        culture=culture,
                        area=safe_float(row.get('area', 0)) or 0,
                        insumo=row.get('insumo', '').strip(),
                        qtd_insumo=safe_float(row.get('qtd_insumo', 0)) or 0,
                        unidade=row.get('unidade', '').strip(),
                        raio=safe_float(row.get('raio')),
                        comprimento=safe_float(row.get('comprimento')),
                        largura=safe_float(row.get('largura')),
                        figura=safe_int(row.get('figura'))
                    )
                    areas.append(area)
            
            print(f"✓ Carregadas {len(areas)} áreas de {culture}")
            
        except Exception as e:
            print(f"Erro ao carregar CSV de {culture}: {e}")
        
        return areas
    
    def get_areas_by_culture(self, culture: str) -> List[PlantingArea]:
        """Retorna todas as áreas de uma cultura"""
        return self.areas.get(culture.lower(), [])
    
    def get_area_by_id(self, culture: str, area_id: int) -> Optional[PlantingArea]:
        """Retorna uma área específica por ID"""
        areas = self.get_areas_by_culture(culture)
        for area in areas:
            if area.id == area_id:
                return area
        return None
    
    def get_cultures(self) -> List[str]:
        """Retorna lista de culturas disponíveis"""
        return ["banana", "milho"]
    
    def get_total_area(self, culture: str) -> float:
        """Retorna área total plantada de uma cultura"""
        areas = self.get_areas_by_culture(culture)
        return sum(area.area for area in areas)
    
    def get_statistics(self, culture: str) -> Dict:
        """Retorna estatísticas sobre uma cultura"""
        areas = self.get_areas_by_culture(culture)
        
        if not areas:
            return {
                "count": 0,
                "total_area": 0,
                "avg_area": 0,
                "min_area": 0,
                "max_area": 0,
                "insumos": []
            }
        
        area_values = [a.area for a in areas]
        insumos = list(set(a.insumo for a in areas if a.insumo))
        
        return {
            "count": len(areas),
            "total_area": round(sum(area_values), 2),
            "avg_area": round(sum(area_values) / len(area_values), 2),
            "min_area": round(min(area_values), 2),
            "max_area": round(max(area_values), 2),
            "insumos": sorted(insumos)
        }
