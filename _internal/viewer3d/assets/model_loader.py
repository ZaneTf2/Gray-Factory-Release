import os
import logging
import traceback
import numpy as np
from typing import Tuple, Optional, Dict
from .mdl_converter import MDLConverter 
from .vtx_vvd import VtxFile, VvdFile

logger = logging.getLogger(__name__)

class ModelLoader:
    """Загрузчик моделей Source Engine"""
    
    def __init__(self):
        self.mdl = MDLConverter()
        self.vtx = VtxFile()
        self.vvd = VvdFile()
        
        self.vertices = None
        self.indices = None
        self.materials = None
        self.bones = None
        
    def load_model(self, mdl_path: str) -> bool:
        """
        Загружает все файлы модели (MDL, VTX, VVD)
        
        Args:
            mdl_path (str): Путь к MDL файлу
            
        Returns:
            bool: True если загрузка успешна
        """
        try:
            # Проверяем наличие всех файлов
            base_path = os.path.splitext(mdl_path)[0]
            vtx_path = base_path + '.dx90.vtx'
            vvd_path = base_path + '.vvd'
            
            if not os.path.exists(mdl_path):
                logger.error(f"MDL file not found: {mdl_path}")
                return False
                
            if not os.path.exists(vtx_path):
                logger.error(f"VTX file not found: {vtx_path}")
                return False
                
            if not os.path.exists(vvd_path):
                logger.error(f"VVD file not found: {vvd_path}")
                return False
                
            # Загружаем все файлы
            if not self.mdl.load(mdl_path):
                return False
                
            if not self.vtx.load(vtx_path):
                return False
                
            if not self.vvd.load(vvd_path):
                return False
                
            # Собираем финальную геометрию
            self._build_final_mesh()
            
            # Сохраняем материалы и кости
            self.materials = self.mdl.get_material_info()
            self.bones = self.mdl.get_bones()
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
            
    def _build_final_mesh(self):
        """Строит финальный меш используя данные из VTX и VVD"""
        try:
            logger.debug("Начало сборки финального меша...")
            
            # Получаем вершины из VVD
            vvd_vertices = self.vvd.get_vertices()
            if not vvd_vertices or not isinstance(vvd_vertices, (list, np.ndarray)):
                logger.error(f"Неверный формат вершин из VVD: {type(vvd_vertices)}")
                return False
                
            # Получаем индексы из VTX
            vtx_indices = self.vtx.get_vertex_indices()
            if not vtx_indices or not isinstance(vtx_indices, (list, np.ndarray)):
                logger.error(f"Неверный формат индексов из VTX: {type(vtx_indices)}")
                return False
                
            # Проверяем размеры массивов
            if len(vtx_indices) == 0:
                logger.error("Пустой массив индексов")
                return False
                
            if len(vvd_vertices) == 0:
                logger.error("Пустой массив вершин")
                return False
                
            # Создаем массивы для OpenGL
            vertices = []
            indices = []
            current_index = 0
            
            logger.debug(f"Обработка {len(vtx_indices)} индексов...")
            
            # Обрабатываем каждый индекс из VTX
            for vtx_index in vtx_indices:
                if vtx_index >= len(vvd_vertices):
                    logger.error(f"Некорректный индекс вершины: {vtx_index} >= {len(vvd_vertices)}")
                    continue
                    
                # Берем вершину из VVD
                vertex = vvd_vertices[vtx_index]
                
                # Проверяем формат вершины
                if not hasattr(vertex, 'position') or not hasattr(vertex, 'normal') or not hasattr(vertex, 'texcoord'):
                    logger.error(f"Некорректный формат вершины: {vertex}")
                    continue
                    
                # Добавляем в финальные массивы
                vertices.append([
                    vertex.position[0], vertex.position[1], vertex.position[2],
                    vertex.normal[0], vertex.normal[1], vertex.normal[2],
                    vertex.texcoord[0], vertex.texcoord[1]
                ])
                indices.append(current_index)
                current_index += 1
            
            # Конвертируем в numpy массивы
            self.vertices = np.array(vertices, dtype=np.float32)
            self.indices = np.array(indices, dtype=np.uint32)
            
            logger.info(f"Финальный меш создан: {len(vertices)} вершин, {len(indices)} индексов")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при сборке меша: {str(e)}")
            logger.error(traceback.format_exc())
            return False
            
    def get_mesh_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Возвращает данные меша для рендеринга
        
        Returns:
            Tuple[np.ndarray, np.ndarray]: (vertices, indices)
            vertices: массив [x,y,z, nx,ny,nz, u,v] для каждой вершины
            indices: массив индексов для рендеринга треугольников
        """
        return self.vertices, self.indices
        
    def get_material_info(self) -> Dict:
        """Возвращает информацию о материалах"""
        return self.materials
        
    def get_bones(self) -> Dict:
        """Возвращает информацию о костях"""
        return self.bones
