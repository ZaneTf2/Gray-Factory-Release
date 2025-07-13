from dataclasses import dataclass
import numpy as np
import struct
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)

@dataclass
class Bone:
    """Структура кости"""
    name: str
    parent: int
    flags: int
    pos: np.ndarray    # [x, y, z]
    quat: np.ndarray   # [x, y, z, w] 
    
    @classmethod
    def from_bytes(cls, data: bytes, offset: int) -> 'Bone':
        """Читает структуру кости из байтов"""
        # Имя (32 байта)
        name = data[offset:offset+32].split(b'\x00')[0].decode('ascii')
        offset += 32
        
        # Parent bone
        parent = struct.unpack('i', data[offset:offset+4])[0]
        offset += 4
        
        # Flags
        flags = struct.unpack('i', data[offset:offset+4])[0]
        offset += 4
        
        # Position
        pos = np.array(struct.unpack('fff', data[offset:offset+12]))
        offset += 12
        
        # Rotation (quaternion)
        quat = np.array(struct.unpack('ffff', data[offset:offset+16]))
        
        return cls(name, parent, flags, pos, quat)

@dataclass
class Material:
    """Структура материала"""
    name: str
    flags: int
    width: int
    height: int
    
    @classmethod
    def from_bytes(cls, data: bytes, offset: int) -> 'Material':
        """Читает структуру материала из байтов"""
        # Имя (64 байта)
        name = data[offset:offset+64].split(b'\x00')[0].decode('ascii')
        offset += 64
        
        # Flags
        flags = struct.unpack('i', data[offset:offset+4])[0]
        offset += 4
        
        # Width & Height 
        width = struct.unpack('i', data[offset:offset+4])[0]
        offset += 4
        height = struct.unpack('i', data[offset:offset+4])[0]
        
        return cls(name, flags, width, height)

@dataclass 
class Mesh:
    """Структура одного меша внутри модели"""
    material_index: int
    vertices: np.ndarray      # [x, y, z, nx, ny, nz, u, v]
    indices: np.ndarray       # [i0, i1, i2, ...]
    
    @classmethod
    def from_bytes(cls, data: bytes, mesh_header_offset: int) -> 'Mesh':
        """Читает структуру меша из байтов"""
        # Material index
        material_index = struct.unpack('i', data[mesh_header_offset:mesh_header_offset+4])[0]
        
        # Vertex data
        vertex_offset = struct.unpack('i', data[mesh_header_offset+4:mesh_header_offset+8])[0]
        vertex_count = struct.unpack('i', data[mesh_header_offset+8:mesh_header_offset+12])[0]
        
        vertices = []
        
        # Читаем позиции, нормали и UV
        for i in range(vertex_count):
            offset = vertex_offset + i * 32  # 12 (pos) + 12 (normal) + 8 (uv) = 32
            
            # Position (float x 3)
            pos = struct.unpack('fff', data[offset:offset+12])
            offset += 12
            
            # Normal (float x 3)
            normal = struct.unpack('fff', data[offset:offset+12])
            offset += 12
            
            # UV (float x 2)
            uv = struct.unpack('ff', data[offset:offset+8])
            
            vertex = list(pos) + list(normal) + list(uv)
            vertices.append(vertex)
            
        # Index data
        index_offset = struct.unpack('i', data[mesh_header_offset+12:mesh_header_offset+16])[0]
        index_count = struct.unpack('i', data[mesh_header_offset+16:mesh_header_offset+20])[0]
        
        indices = []
        for i in range(0, index_count, 3):
            # Читаем по три индекса за раз (треугольник)
            idx = struct.unpack('HHH', data[index_offset+i*2:index_offset+(i+3)*2])
            indices.extend(idx)
            
        return cls(
            material_index=material_index,
            vertices=np.array(vertices, dtype=np.float32),
            indices=np.array(indices, dtype=np.uint32)
        )

@dataclass
class Model:
    """Структура модели (часть тела)"""
    name: str
    meshes: List[Mesh]
    
    @classmethod
    def from_bytes(cls, data: bytes, model_offset: int) -> 'Model':
        """Читает структуру модели из байтов"""
        # Имя модели (64 байта)
        name = data[model_offset:model_offset+64].split(b'\x00')[0].decode('ascii')
        model_offset += 64
        
        # Количество мешей
        mesh_count = struct.unpack('i', data[model_offset:model_offset+4])[0]
        mesh_offset = struct.unpack('i', data[model_offset+4:model_offset+8])[0]
        
        meshes = []
        # Читаем каждый меш
        for i in range(mesh_count):
            mesh = Mesh.from_bytes(data, mesh_offset + i * 116)  # 116 - размер заголовка меша
            meshes.append(mesh)
            
        return cls(name, meshes)

@dataclass
class BodyPart:
    """Структура части тела"""
    name: str
    models: List[Model]
    
    @classmethod
    def from_bytes(cls, data: bytes, bodypart_offset: int) -> 'BodyPart':
        """Читает структуру части тела из байтов"""
        # Имя части тела (64 байта)
        name = data[bodypart_offset:bodypart_offset+64].split(b'\x00')[0].decode('ascii')
        bodypart_offset += 64
        
        # Количество моделей
        model_count = struct.unpack('i', data[bodypart_offset:bodypart_offset+4])[0]
        model_offset = struct.unpack('i', data[bodypart_offset+4:bodypart_offset+8])[0]
        
        models = []
        # Читаем каждую модель
        for i in range(model_count):
            model = Model.from_bytes(data, model_offset + i * 148)  # 148 - размер заголовка модели
            models.append(model)
            
        return cls(name, models)
