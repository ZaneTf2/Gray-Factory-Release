import struct
import os
import logging
from typing import Tuple, List, Optional
import numpy as np
import binascii

from .mdl_structs import BodyPart, Model, Mesh, Material, Bone
logger = logging.getLogger(__name__)

class MDLHeader:
    """Заголовок MDL файла Source Engine (v48/v49)"""
    
    # Валидные значения заголовка
    SIGNATURE = b'IDST'  # 0x49445354
    SUPPORTED_VERSIONS = [48, 49]  # TF2 использует v48 или v49
    
    @staticmethod
    def try_decode(data: bytes, encodings=('ascii', 'utf-8', 'latin1')) -> str:
        """
        Пытается декодировать строку в разных кодировках
        """
        for encoding in encodings:
            try:
                return data.decode(encoding).strip('\x00')
            except UnicodeDecodeError:
                continue
        # Если ничего не помогло, используем latin1 с игнорированием ошибок
        return data.decode('latin1', errors='ignore').strip('\x00')
    
    def __init__(self, data: bytes):
        """
        Разбирает заголовок MDL файла.
        Смещения взяты из studio.h (Source SDK)
        """
        # Базовая информация
        self.id = struct.unpack('4s', data[0:4])[0]          # IDST
        self.version = struct.unpack('i', data[4:8])[0]      # 48 или 49
        self.checksum = struct.unpack('i', data[8:12])[0]    # CRC32
        self.name = self.try_decode(data[12:76])             # Имя модели (64 байта)
        self.length = struct.unpack('i', data[76:80])[0]     # Размер файла
        
        # Положение модели
        self.eyeposition = struct.unpack('fff', data[80:92])     # Позиция глаз
        self.illumposition = struct.unpack('fff', data[92:104])  # Позиция освещения
        self.hull_min = struct.unpack('fff', data[104:116])      # Минимум физической коробки
        self.hull_max = struct.unpack('fff', data[116:128])      # Максимум физической коробки
        self.view_bbmin = struct.unpack('fff', data[128:140])    # Минимум BBox
        self.view_bbmax = struct.unpack('fff', data[140:152])    # Максимум BBox
        
        # Флаги модели
        self.flags = struct.unpack('i', data[152:156])[0]
        
        # Данные о костях
        self.bone_count = struct.unpack('i', data[156:160])[0]
        self.bone_offset = struct.unpack('i', data[160:164])[0]
        
        # Данные о вершинах и анимации
        # ВАЖНО: Смещения для TF2 MDL v48/v49
        self.bodypart_count = struct.unpack('i', data[164:168])[0]
        self.bodypart_offset = struct.unpack('i', data[168:172])[0]
        
        # У каждой части тела своя сетка с вершинами
        self.local_vertex_count = 0    # Будет вычислено при чтении частей тела
        self.vertex_count = 0          # Будет вычислено при чтении частей тела
        self.face_count = 0            # Будет вычислено при чтении частей тела
        
        # Материалы/текстуры (168 + 60 = 228)
        self.texture_count = struct.unpack('i', data[228:232])[0]
        self.texture_offset = struct.unpack('i', data[232:236])[0]
        
        # Дамп заголовка для отладки
        logger.debug("=== MDL Header Dump ===")
        logger.debug(f"ID: {self.id} ({binascii.hexlify(self.id)})")
        logger.debug(f"Version: {self.version}")
        logger.debug(f"Checksum: 0x{self.checksum:08x}")
        logger.debug(f"Name: {self.name}")
        logger.debug(f"Length: {self.length} bytes")
        logger.debug(f"Bones: {self.bone_count} at offset {self.bone_offset}")
        logger.debug(f"Body parts: {self.bodypart_count} at offset {self.bodypart_offset}")
        logger.debug(f"Textures: {self.texture_count} at offset {self.texture_offset}")
        logger.debug("===================")
        
    def validate(self) -> bool:
        """
        Проверяет валидность заголовка MDL
        
        Returns:
            bool: True если заголовок валиден
        """
        # Проверяем сигнатуру
        if self.id != self.SIGNATURE:
            logger.error(f"Неверная сигнатура MDL: {self.id} ({binascii.hexlify(self.id)})")
            logger.error(f"Ожидалось: {self.SIGNATURE} ({binascii.hexlify(self.SIGNATURE)})")
            return False
            
        # Проверяем версию
        if self.version not in self.SUPPORTED_VERSIONS:
            logger.error(f"Неподдерживаемая версия MDL: {self.version}")
            logger.error(f"Поддерживаемые версии: {self.SUPPORTED_VERSIONS}")
            return False
            
        # Проверяем размер файла
        if self.length <= 0:
            logger.error(f"Некорректный размер файла: {self.length}")
            return False
            
        # Проверяем смещения
        if (self.bone_offset >= self.length or
            self.bodypart_offset >= self.length or
            self.texture_offset >= self.length):
            logger.error("Некорректные смещения секций в файле")
            logger.error(f"Размер файла: {self.length}")
            logger.error(f"Смещения: bones={self.bone_offset}, bodyparts={self.bodypart_offset}, "
                        f"textures={self.texture_offset}")
            return False
            
        return True

class MDLConverter:
    def __init__(self):
        self.header = None
        self.bones = []
        self.materials = []
        self.bodyparts = []
        self.vertices = None
        self.indices = None
        self.logger = logging.getLogger(__name__)
        
    def load(self, mdl_path: str) -> bool:
        """
        Загружает MDL файл
        
        Args:
            mdl_path (str): Путь к MDL файлу
            
        Returns:
            bool: True если загрузка успешна
        """
        try:
            with open(mdl_path, 'rb') as f:
                data = f.read()
                
            # Читаем заголовок
            self.header = MDLHeader(data)
            
            # Проверяем сигнатуру
            if self.header.id != MDLHeader.SIGNATURE:
                logger.error(f"Invalid MDL signature: {binascii.hexlify(self.header.id)}")
                return False
                
            # Проверяем версию
            if self.header.version not in MDLHeader.SUPPORTED_VERSIONS:
                logger.error(f"Unsupported MDL version: {self.header.version}")
                return False
                
            # Парсим секции
            self._parse_materials(data)
            self._parse_bones(data)
            self._parse_bodyparts(data)
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading MDL file: {e}")
            return False
            
    def get_mesh_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Возвращает данные меша для рендеринга
        
        Returns:
            Tuple[np.ndarray, np.ndarray]: (vertices, indices)
        """
        return self.vertices, self.indices
        
    def get_material_info(self) -> List[Material]:
        """
        Возвращает информацию о материалах
        """
        return self.materials
        
    def get_bones(self) -> List[Bone]:
        """
        Возвращает список костей
        """
        return self.bones
    
    def _parse_materials(self, data: bytes):
        """Парсит секцию материалов"""
        self.materials = [
            Material(
                name="default", 
                texture_path="materials/models/default.vtf",
                diffuse_color=(0.8, 0.8, 0.8, 1.0)
            )
        ]
        
    def _parse_bones(self, data: bytes):
        """Парсит секцию костей"""
        self.bones = [
            Bone(
                name="root",
                parent_index=-1,
                position=(0, 0, 0),
                rotation=(0, 0, 0)
            )
        ]
        
    def _parse_bodyparts(self, data: bytes):
        """Парсит секцию body parts"""
        self.bodyparts = [
            BodyPart(
                name="default",
                models=[
                    Model(
                        name="default",
                        meshes=[
                            Mesh(
                                material_index=0,
                                vertex_offset=0,
                                vertex_count=0,
                                index_offset=0,
                                index_count=0
                            )
                        ]
                    )
                ]
            )
        ]
