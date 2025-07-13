import struct
import logging
import numpy as np
from typing import List, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class VtxVertex:
    """Вершина в VTX файле"""
    bone_weight_indices: List[int]  # до 3 индексов костей
    bone_weights: List[float]      # веса костей
    original_mesh_vertex_index: int # индекс вершины в оригинальном меше
    
    @classmethod
    def from_bytes(cls, data: bytes, offset: int) -> 'VtxVertex':
        """Читает вершину из байтов"""
        # Читаем индексы костей (3 байта)
        bone_indices = list(data[offset:offset+3])
        offset += 3
        
        # Читаем веса костей (3 байта, нормализованные)
        weights_raw = list(data[offset:offset+3])
        weights = [w/255.0 for w in weights_raw]
        offset += 3
        
        # Индекс вершины в меше
        mesh_vertex_index = struct.unpack('H', data[offset:offset+2])[0]
        
        return cls(bone_indices, weights, mesh_vertex_index)

@dataclass 
class VtxStripGroup:
    """Группа стрипов в VTX"""
    vertices: List[VtxVertex]
    indices: List[int]
    
    @classmethod
    def from_bytes(cls, data: bytes, offset: int) -> 'VtxStripGroup':
        """Читает группу стрипов из байтов"""
        # Количество вершин
        vertex_count = struct.unpack('i', data[offset:offset+4])[0]
        vertex_offset = struct.unpack('i', data[offset+4:offset+8])[0]
        
        vertices = []
        for i in range(vertex_count):
            vertex = VtxVertex.from_bytes(data, vertex_offset + i * 8)  # 8 = размер структуры вершины
            vertices.append(vertex)
            
        # Количество индексов
        index_count = struct.unpack('i', data[offset+8:offset+12])[0] 
        index_offset = struct.unpack('i', data[offset+12:offset+16])[0]
        
        indices = []
        for i in range(index_count//2):  # 2 байта на индекс
            idx = struct.unpack('H', data[index_offset+i*2:index_offset+i*2+2])[0]
            indices.append(idx)
            
        return cls(vertices, indices)

class VtxFile:
    """Парсер VTX файла"""
    
    SIGNATURE = b'IDSV'  # VTX signature
    VERSION = 7         # Версия TF2
    
    def __init__(self):
        self.version = 0
        self.strip_groups = []
        
    def load(self, vtx_path: str) -> bool:
        """
        Загружает VTX файл
        
        Args:
            vtx_path (str): Путь к VTX файлу
            
        Returns:
            bool: True если загрузка успешна
        """
        try:
            with open(vtx_path, 'rb') as f:
                data = f.read()
                
            # Проверяем заголовок
            signature = data[0:4]
            if signature != self.SIGNATURE:
                logger.error(f"Invalid VTX signature: {signature}")
                return False
                
            self.version = struct.unpack('i', data[4:8])[0]
            if self.version != self.VERSION:
                logger.error(f"Unsupported VTX version: {self.version}")
                return False
                
            # Читаем общую информацию
            vertex_count = struct.unpack('i', data[8:12])[0]
            index_count = struct.unpack('i', data[12:16])[0]
            
            # Читаем strip groups
            strip_group_count = struct.unpack('i', data[16:20])[0]
            strip_group_offset = struct.unpack('i', data[20:24])[0]
            
            for i in range(strip_group_count):
                group = VtxStripGroup.from_bytes(data, strip_group_offset + i * 16)
                self.strip_groups.append(group)
                
            logger.info(f"VTX loaded successfully: {vertex_count} vertices, {index_count} indices")
            return True
            
        except Exception as e:
            logger.error(f"Error loading VTX: {e}")
            return False
            
    def get_vertex_indices(self) -> List[int]:
        """Возвращает список всех индексов вершин из strip groups"""
        indices = []
        for group in self.strip_groups:
            indices.extend(idx.original_mesh_vertex_index for idx in group.vertices)
        return indices

@dataclass
class VvdVertex:
    """Вершина в VVD файле"""
    position: np.ndarray    # [x, y, z]
    normal: np.ndarray     # [nx, ny, nz] 
    uv: np.ndarray         # [u, v]
    
    @classmethod
    def from_bytes(cls, data: bytes, offset: int) -> 'VvdVertex':
        """Читает вершину из байтов"""
        # Position
        pos = np.array(struct.unpack('fff', data[offset:offset+12]))
        offset += 12
        
        # Normal  
        normal = np.array(struct.unpack('fff', data[offset:offset+12]))
        offset += 12
        
        # UV
        uv = np.array(struct.unpack('ff', data[offset:offset+8]))
        
        return cls(pos, normal, uv)

class VvdFile:
    """Парсер VVD файла"""
    
    SIGNATURE = b'IDSV'  # VVD signature
    VERSION = 4         # Версия TF2
    
    def __init__(self):
        self.version = 0
        self.vertices = []
        
    def load(self, vvd_path: str) -> bool:
        """
        Загружает VVD файл
        
        Args:
            vvd_path (str): Путь к VVD файлу
            
        Returns:
            bool: True если загрузка успешна
        """
        try:
            with open(vvd_path, 'rb') as f:
                data = f.read()
                
            # Проверяем заголовок
            signature = data[0:4]
            if signature != self.SIGNATURE:
                logger.error(f"Invalid VVD signature: {signature}")
                return False
                
            self.version = struct.unpack('i', data[4:8])[0]
            if self.version != self.VERSION:
                logger.error(f"Unsupported VVD version: {self.version}")
                return False
                
            # Читаем вершины
            vertex_count = struct.unpack('i', data[8:12])[0]
            vertex_data_offset = struct.unpack('i', data[12:16])[0]
            
            for i in range(vertex_count):
                vertex = VvdVertex.from_bytes(data, vertex_data_offset + i * 32)  # 32 = размер структуры вершины
                self.vertices.append(vertex)
                
            logger.info(f"VVD loaded successfully: {len(self.vertices)} vertices")
            return True
            
        except Exception as e:
            logger.error(f"Error loading VVD: {e}")
            return False
            
    def get_vertices(self) -> List[VvdVertex]:
        """Возвращает список всех вершин"""
        return self.vertices
