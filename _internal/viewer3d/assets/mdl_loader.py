import os
import logging
import struct
from dataclasses import dataclass
from typing import List, Tuple, Optional
import numpy as np
from OpenGL.GL import *

logger = logging.getLogger(__name__)

# Константы формата MDL
MDL_IDENT = 0x54534449  # "IDST"
MDL_VERSION = 48        # Версия формата
MAX_NUM_BONES = 128     # Максимальное количество костей

@dataclass
class MDLHeader:
    """Заголовок MDL файла"""
    ident: int          # Идентификатор формата (IDST)
    version: int        # Версия формата
    name: str          # Имя модели (64 байта)
    file_size: int     # Размер файла
    
    eyeposition: Tuple[float, float, float]  # Позиция глаз
    illumposition: Tuple[float, float, float]  # Позиция освещения
    hull_min: Tuple[float, float, float]  # Минимальная точка bbox
    hull_max: Tuple[float, float, float]  # Максимальная точка bbox
    
    view_bbox_min: Tuple[float, float, float]  # Минимальная точка view bbox
    view_bbox_max: Tuple[float, float, float]  # Максимальная точка view bbox
    
    flags: int  # Флаги модели
    
    # Смещения до различных секций данных
    bone_count: int
    bone_offset: int
    bodypart_count: int
    bodypart_offset: int
    
    # Другие поля заголовка...

class MDLLoader:
    """Загрузчик моделей формата MDL"""
    
    def __init__(self):
        self.header: Optional[MDLHeader] = None
        self.vertices: List[Tuple[float, float, float]] = []
        self.normals: List[Tuple[float, float, float]] = []
        self.uvs: List[Tuple[float, float]] = []
        self.indices: List[int] = []
        self.bones: List[dict] = []
        
    def load(self, filepath: str) -> bool:
        """Загрузка MDL файла"""
        try:
            logger.info(f"Загрузка MDL файла: {filepath}")
            
            if not os.path.exists(filepath):
                logger.error(f"Файл не найден: {filepath}")
                return False
                
            with open(filepath, 'rb') as f:
                # Читаем заголовок
                self.header = self._read_header(f)
                
                if not self._validate_header():
                    return False
                    
                # Читаем данные модели
                self._read_bones(f)
                self._read_vertices(f)
                self._read_indices(f)
                
                logger.info(f"MDL файл успешно загружен: {len(self.vertices)} вершин")
                return True
                
        except Exception as e:
            logger.error(f"Ошибка при загрузке MDL файла: {str(e)}")
            logger.error(f"Путь к файлу: {filepath}")
            import traceback
            logger.error(traceback.format_exc())
            return False
            
    def _read_header(self, f) -> MDLHeader:
        """Чтение заголовка MDL файла"""
        # Читаем базовые поля заголовка
        ident = struct.unpack("I", f.read(4))[0]
        version = struct.unpack("I", f.read(4))[0]
        name = f.read(64).decode('ascii').rstrip('\x00')
        file_size = struct.unpack("I", f.read(4))[0]
        
        # Читаем векторы позиций
        eyeposition = struct.unpack("fff", f.read(12))
        illumposition = struct.unpack("fff", f.read(12))
        hull_min = struct.unpack("fff", f.read(12))
        hull_max = struct.unpack("fff", f.read(12))
        view_bbox_min = struct.unpack("fff", f.read(12))
        view_bbox_max = struct.unpack("fff", f.read(12))
        
        flags = struct.unpack("I", f.read(4))[0]
        
        # Читаем информацию о костях
        bone_count = struct.unpack("I", f.read(4))[0]
        bone_offset = struct.unpack("I", f.read(4))[0]
        
        # Читаем информацию о частях тела
        bodypart_count = struct.unpack("I", f.read(4))[0]
        bodypart_offset = struct.unpack("I", f.read(4))[0]
        
        return MDLHeader(
            ident=ident,
            version=version,
            name=name,
            file_size=file_size,
            eyeposition=eyeposition,
            illumposition=illumposition,
            hull_min=hull_min,
            hull_max=hull_max,
            view_bbox_min=view_bbox_min,
            view_bbox_max=view_bbox_max,
            flags=flags,
            bone_count=bone_count,
            bone_offset=bone_offset,
            bodypart_count=bodypart_count,
            bodypart_offset=bodypart_offset
        )
            
    def _validate_header(self) -> bool:
        """Проверка корректности заголовка"""
        if not self.header:
            logger.error("Заголовок не загружен")
            return False
            
        if self.header.ident != MDL_IDENT:
            logger.error(f"Неверный идентификатор формата: {hex(self.header.ident)}")
            return False
            
        if self.header.version != MDL_VERSION:
            logger.warning(f"Версия формата {self.header.version} может быть несовместима")
            
        logger.info(f"Заголовок MDL файла:")
        logger.info(f"- Имя модели: {self.header.name}")
        logger.info(f"- Версия: {self.header.version}")
        logger.info(f"- Размер файла: {self.header.file_size} байт")
        logger.info(f"- Количество костей: {self.header.bone_count}")
        
        return True
        
    def _read_bones(self, f):
        """Чтение данных о костях"""
        if not self.header:
            return
            
        f.seek(self.header.bone_offset)
        
        for i in range(self.header.bone_count):
            # Читаем данные кости
            name = f.read(32).decode('ascii').rstrip('\x00')
            parent_bone = struct.unpack("i", f.read(4))[0]
            flags = struct.unpack("I", f.read(4))[0]
            
            # Позиция и поворот
            pos = struct.unpack("fff", f.read(12))
            rot = struct.unpack("fff", f.read(12))
            
            self.bones.append({
                'name': name,
                'parent': parent_bone,
                'flags': flags,
                'position': pos,
                'rotation': rot
            })
            
    def _read_vertices(self, f):
        """Чтение вершин модели"""
        if not self.header or self.header.bodypart_count == 0:
            return
            
        # Переходим к секции bodyparts
        f.seek(self.header.bodypart_offset)
        
        for bodypart_idx in range(self.header.bodypart_count):
            # Читаем информацию о части тела
            name = f.read(64).decode('ascii').rstrip('\x00')
            num_models = struct.unpack("I", f.read(4))[0]
            base = struct.unpack("I", f.read(4))[0]
            model_offset = struct.unpack("I", f.read(4))[0]
            
            # Сохраняем текущую позицию
            current_pos = f.tell()
            
            # Переходим к данным модели
            f.seek(self.header.bodypart_offset + model_offset)
            
            for model_idx in range(num_models):
                # Читаем информацию о меше
                mesh_count = struct.unpack("I", f.read(4))[0]
                mesh_offset = struct.unpack("I", f.read(4))[0]
                vertex_offset = struct.unpack("I", f.read(4))[0]
                vertex_count = struct.unpack("I", f.read(4))[0]
                
                # Читаем вершины
                f.seek(vertex_offset)
                for i in range(vertex_count):
                    # Позиция
                    pos = struct.unpack("fff", f.read(12))
                    self.vertices.append(pos)
                    
                    # Нормаль
                    normal = struct.unpack("fff", f.read(12))
                    self.normals.append(normal)
                    
                    # Текстурные координаты
                    uv = struct.unpack("ff", f.read(8))
                    self.uvs.append(uv)
                    
                # Восстанавливаем позицию для следующего меша
                f.seek(current_pos)
            
    def _read_indices(self, f):
        """Чтение индексов модели"""
        if not self.header or self.header.bodypart_count == 0:
            return
            
        # Переходим к секции bodyparts
        f.seek(self.header.bodypart_offset)
        
        vertex_offset = 0  # Смещение для индексов
        
        for bodypart_idx in range(self.header.bodypart_count):
            # Читаем информацию о части тела
            name = f.read(64).decode('ascii').rstrip('\x00')
            num_models = struct.unpack("I", f.read(4))[0]
            base = struct.unpack("I", f.read(4))[0]
            model_offset = struct.unpack("I", f.read(4))[0]
            
            # Сохраняем текущую позицию
            current_pos = f.tell()
            
            # Переходим к данным модели
            f.seek(self.header.bodypart_offset + model_offset)
            
            for model_idx in range(num_models):
                # Читаем информацию о меше
                mesh_count = struct.unpack("I", f.read(4))[0]
                mesh_offset = struct.unpack("I", f.read(4))[0]
                
                # Читаем данные мешей
                for mesh_idx in range(mesh_count):
                    # Читаем количество треугольников
                    num_triangles = struct.unpack("I", f.read(4))[0]
                    
                    # Читаем индексы
                    for i in range(num_triangles * 3):  # 3 вершины на треугольник
                        index = struct.unpack("I", f.read(4))[0]
                        self.indices.append(index + vertex_offset)
                        
                vertex_offset += len(self.vertices)  # Обновляем смещение
                
                # Восстанавливаем позицию для следующего меша
                f.seek(current_pos)
        
    def create_gl_buffers(self) -> Tuple[int, int]:
        """Создание буферов OpenGL для модели"""
        # Создаем VAO
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        
        # Создаем VBO для вершин
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        
        # Преобразуем данные в numpy массивы
        vertices = np.array(self.vertices, dtype=np.float32)
        normals = np.array(self.normals, dtype=np.float32)
        uvs = np.array(self.uvs, dtype=np.float32)
        
        # Загружаем данные в буфер
        buffer_size = (vertices.nbytes + normals.nbytes + uvs.nbytes)
        glBufferData(GL_ARRAY_BUFFER, buffer_size, None, GL_STATIC_DRAW)
        
        # Копируем данные в буфер
        offset = 0
        glBufferSubData(GL_ARRAY_BUFFER, offset, vertices.nbytes, vertices)
        offset += vertices.nbytes
        glBufferSubData(GL_ARRAY_BUFFER, offset, normals.nbytes, normals)
        offset += normals.nbytes
        glBufferSubData(GL_ARRAY_BUFFER, offset, uvs.nbytes, uvs)
        
        # Настраиваем атрибуты
        stride = 0
        offset = 0
        
        # Вершины
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(0)
        offset += vertices.nbytes
        
        # Нормали
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(1)
        offset += normals.nbytes
        
        # Текстурные координаты
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(2)
        
        # Создаем IBO
        ibo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo)
        indices = np.array(self.indices, dtype=np.uint32)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        
        glBindVertexArray(0)
        return vao, len(self.indices)
