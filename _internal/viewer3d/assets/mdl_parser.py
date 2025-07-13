import os
import logging
import struct
import traceback
import numpy as np
from typing import Optional, BinaryIO, NamedTuple
from io import BytesIO

logger = logging.getLogger(__name__)

# Константы из studiomdl.h
STUDIOHDR_SIGNATURE = 0x54534449  # "IDST" в little-endian
MAX_NUM_BONES = 128
MAX_NUM_LODS = 8
MAX_NUM_MESHES = 32

class SourceVertex(NamedTuple):
    """Вершина в формате Source Engine"""
    position: np.ndarray  # float[3]
    normal: np.ndarray   # float[3]
    texcoord: np.ndarray # float[2]
    bone_weights: np.ndarray  # float[3]
    bone_indices: np.ndarray  # int[3]

class ConvertedModel(NamedTuple):
    """Данные модели, готовые для загрузки в OpenGL"""
    vertices: np.ndarray  # Массив вершин (N, 3) float32
    indices: np.ndarray   # Массив индексов uint32
    normals: Optional[np.ndarray] = None  # Массив нормалей (N, 3) float32
    uvs: Optional[np.ndarray] = None      # Массив текстурных координат (N, 2) float32

class StudioBone:
    """Структура кости"""
    def __init__(self):
        self.name = ""
        self.parent_bone = 0
        self.flags = 0
        self.position = np.zeros(3)
        self.rotation = np.zeros(3)
        self.scale = np.ones(3)

class StudioMesh:
    """Структура меша"""
    def __init__(self):
        self.material_index = 0
        self.vertex_offset = 0
        self.vertex_count = 0
        self.index_offset = 0
        self.index_count = 0

class MDLHeader:
    """Заголовок MDL файла"""
    def __init__(self):
        self.id = 0
        self.version = 0
        self.name = ""
        self.length = 0
        
        # Основные смещения
        self.bone_offset = 0
        self.bone_count = 0
        self.bone_controller_offset = 0
        self.hitbox_offset = 0
        self.sequence_offset = 0
        self.sequence_group_offset = 0
        self.texture_offset = 0
        self.texture_count = 0
        self.skin_reference_offset = 0
        self.skin_reference_count = 0
        self.mesh_offset = 0
        self.mesh_count = 0
        
        # Геометрия
        self.vertex_offset = 0
        self.vertex_count = 0
        self.index_offset = 0
        self.index_count = 0
        
    @staticmethod
    def read_null_terminated_string(data: bytes, encoding='latin1') -> str:
        """Читает null-terminated строку из байтов"""
        try:
            null_pos = data.find(b'\0')
            if null_pos != -1:
                data = data[:null_pos]
            return data.decode(encoding, errors='replace').rstrip()
        except Exception as e:
            logger.warning(f"Ошибка при декодировании строки: {str(e)}")
            return ""
        
    @classmethod
    def from_file(cls, f: BinaryIO) -> Optional['MDLHeader']:
        """Читает заголовок из бинарного файла"""
        try:
            header = cls()
            
            # Сохраняем начальную позицию
            start_pos = f.tell()
            logger.debug(f"Начальная позиция в файле: {start_pos}")
            
            # Читаем базовые поля заголовка
            header.id = struct.unpack("<I", f.read(4))[0]
            header.version = struct.unpack("<I", f.read(4))[0]
            
            # Проверяем сигнатуру
            if header.id != STUDIOHDR_SIGNATURE:
                logger.error(f"Неверная сигнатура MDL файла: {hex(header.id)}")
                return None
                
            # Читаем имя (64 байта)
            name_bytes = f.read(64)
            header.name = cls.read_null_terminated_string(name_bytes)
            logger.debug(f"Прочитано имя модели: {header.name}")
            
            # Размер файла
            header.length = struct.unpack("<I", f.read(4))[0]
            
            # Позиция в мировом пространстве
            f.seek(12, 1)  # eyeposition (3 float)
            f.seek(12, 1)  # illumposition (3 float)
            f.seek(12, 1)  # hull_min (3 float)
            f.seek(12, 1)  # hull_max (3 float)
            f.seek(12, 1)  # view_bbmin (3 float)
            f.seek(12, 1)  # view_bbmax (3 float)
            
            # Флаги
            flags = struct.unpack("<I", f.read(4))[0]
            
            # Кости
            header.bone_count = struct.unpack("<I", f.read(4))[0]
            header.bone_offset = struct.unpack("<I", f.read(4))[0]
            
            # Контроллеры костей
            bone_controller_count = struct.unpack("<I", f.read(4))[0]
            header.bone_controller_offset = struct.unpack("<I", f.read(4))[0]
            
            # Хитбоксы и т.д.
            hitbox_count = struct.unpack("<I", f.read(4))[0]
            header.hitbox_offset = struct.unpack("<I", f.read(4))[0]
            
            # Геометрия
            header.mesh_count = struct.unpack("<I", f.read(4))[0]
            header.mesh_offset = struct.unpack("<I", f.read(4))[0]
            
            # Вершины
            header.vertex_count = struct.unpack("<I", f.read(4))[0]
            header.vertex_offset = struct.unpack("<I", f.read(4))[0]
            
            # Индексы
            header.index_count = struct.unpack("<I", f.read(4))[0]
            header.index_offset = struct.unpack("<I", f.read(4))[0]
            
            logger.debug(f"Прочитан заголовок MDL:")
            logger.debug(f"- Смещение вершин: {header.vertex_offset}")
            logger.debug(f"- Количество вершин: {header.vertex_count}")
            logger.debug(f"- Смещение индексов: {header.index_offset}")
            logger.debug(f"- Количество индексов: {header.index_count}")
            logger.debug(f"- Размер файла: {header.length}")
            
            return header
            
        except Exception as e:
            logger.error(f"Ошибка при чтении заголовка MDL: {str(e)}")
            logger.error(traceback.format_exc())
            return None

class MDLParser:
    """Парсер MDL файлов Source Engine"""
    def __init__(self):
        self.header = None
        self.bones = []
        self.meshes = []
        self.vertices = None
        self.indices = None
        self.normals = None
        self.uvs = None
        
    def _read_bones(self, f: BinaryIO) -> bool:
        """Читает кости из файла"""
        try:
            if not self.header.bone_count:
                return True
                
            f.seek(self.header.bone_offset)
            for i in range(self.header.bone_count):
                bone = StudioBone()
                name_bytes = f.read(32)
                bone.name = MDLHeader.read_null_terminated_string(name_bytes)
                bone.parent_bone = struct.unpack("<i", f.read(4))[0]
                bone.flags = struct.unpack("<I", f.read(4))[0]
                bone.position = np.array(struct.unpack("<3f", f.read(12)))
                bone.rotation = np.array(struct.unpack("<3f", f.read(12)))
                bone.scale = np.array(struct.unpack("<3f", f.read(12)))
                self.bones.append(bone)
            return True
        except Exception as e:
            logger.error(f"Ошибка при чтении костей: {str(e)}")
            return False
            
    def _read_meshes(self, f: BinaryIO) -> bool:
        """Читает меши из файла"""
        try:
            if not self.header.mesh_count:
                return True
                
            f.seek(self.header.mesh_offset)
            for i in range(self.header.mesh_count):
                mesh = StudioMesh()
                mesh.material_index = struct.unpack("<i", f.read(4))[0]
                mesh.vertex_offset = struct.unpack("<I", f.read(4))[0]
                mesh.vertex_count = struct.unpack("<I", f.read(4))[0]
                mesh.index_offset = struct.unpack("<I", f.read(4))[0]
                mesh.index_count = struct.unpack("<I", f.read(4))[0]
                self.meshes.append(mesh)
            return True
        except Exception as e:
            logger.error(f"Ошибка при чтении мешей: {str(e)}")
            return False
            
    def parse(self, mdl_data: bytes) -> Optional[ConvertedModel]:
        """Разбор MDL файла и конвертация для OpenGL"""
        try:
            logger.info("Начало разбора MDL файла")
            
            # Создаем BytesIO для работы с бинарными данными как с файлом
            f = BytesIO(mdl_data)
            
            # Читаем заголовок
            self.header = MDLHeader.from_file(f)
            if not self.header:
                logger.error("Не удалось прочитать заголовок MDL")
                return None
                
            logger.debug(f"Загружен заголовок MDL: {self.header.name}")
            
            # Читаем кости и меши
            if not self._read_bones(f) or not self._read_meshes(f):
                return None
                
            # Читаем геометрию
            try:
                # Читаем вершины
                f.seek(self.header.vertex_offset)
                vertices_size = self.header.vertex_count * 12  # 3 float32 на вершину
                if f.tell() + vertices_size > len(mdl_data):
                    logger.error(f"Некорректное смещение вершин: {self.header.vertex_offset}, выходит за пределы файла")
                    return None
                    
                vertices_raw = f.read(vertices_size)
                if len(vertices_raw) != vertices_size:
                    logger.error(f"Размер блока вершин не совпадает: ожидалось {vertices_size}, получено {len(vertices_raw)}")
                    logger.error(f"vertex_offset={self.header.vertex_offset}, vertex_count={self.header.vertex_count}")
                    return None
                    
                self.vertices = np.frombuffer(vertices_raw, dtype=np.float32).reshape(-1, 3)
                
                # Читаем индексы
                f.seek(self.header.index_offset)
                indices_size = self.header.index_count * 4  # uint32
                if f.tell() + indices_size > len(mdl_data):
                    logger.error(f"Некорректное смещение индексов: {self.header.index_offset}, выходит за пределы файла")
                    return None
                    
                indices_raw = f.read(indices_size)
                if len(indices_raw) != indices_size:
                    logger.error(f"Размер блока индексов не совпадает: ожидалось {indices_size}, получено {len(indices_raw)}")
                    logger.error(f"vertex_offset={self.header.vertex_offset}, index_offset={self.header.index_offset}, vertex_count={self.header.vertex_count}, index_count={self.header.index_count}, file_len={len(mdl_data)}")
                    return None
                    
                self.indices = np.frombuffer(indices_raw, dtype=np.uint32)
                
                # Проверяем валидность данных
                if len(self.vertices) == 0 or len(self.indices) == 0:
                    logger.error("Не удалось прочитать вершины или индексы")
                    return None
                    
                # Проверяем, что индексы не выходят за пределы массива вершин
                if np.any(self.indices >= len(self.vertices)):
                    logger.error("Индексы выходят за пределы массива вершин")
                    return None
                
                logger.info(f"Разбор MDL файла успешно завершен:")
                logger.info(f"- Вершин: {len(self.vertices)}")
                logger.info(f"- Индексов: {len(self.indices)}")
                logger.info(f"- Костей: {len(self.bones)}")
                logger.info(f"- Мешей: {len(self.meshes)}")
                
                return ConvertedModel(
                    vertices=self.vertices,
                    indices=self.indices,
                    normals=self.normals,
                    uvs=self.uvs
                )
                
            except Exception as e:
                logger.error(f"Ошибка при чтении геометрии: {str(e)}")
                logger.error(traceback.format_exc())
                return None
                
        except Exception as e:
            logger.error(f"Ошибка при разборе MDL файла: {str(e)}")
            logger.error(traceback.format_exc())
            return None
