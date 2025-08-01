from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt
from PIL import Image

from pathlib import Path
import numpy as np
import os
import trimesh
import struct

class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z
    
    def __repr__(self):
        return f"Vector3({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"
    
    def normalize(self):
        length = (self.x**2 + self.y**2 + self.z**2)**0.5
        if length > 0:
            self.x /= length
            self.y /= length
            self.z /= length
        return self

class MDLTexture:
    """Структура текстуры MDL"""
    def __init__(self):
        self.name_offset = 0
        self.flags = 0
        self.used = 0
        self.unused = 0
        self.name = ""

class MDLBodyPart:
    """Структура части тела модели"""
    def __init__(self):
        self.name_offset = 0
        self.nummodels = 0
        self.base = 0
        self.modelindex = 0
        self.name = ""

class MDLModel:
    """Структура модели внутри части тела"""
    def __init__(self):
        self.name = ""
        self.type = 0
        self.boundingradius = 0.0
        self.nummeshes = 0
        self.meshindex = 0
        self.numvertices = 0
        self.vertexindex = 0
        self.tangentsindex = 0

class MDLMesh:
    """Структура меша модели"""
    def __init__(self):
        self.material = 0
        self.modelindex = 0
        self.numvertices = 0
        self.vertexoffset = 0
        self.numflexes = 0
        self.flexindex = 0
        self.materialtype = 0
        self.materialparam = 0
        self.meshid = 0
        self.center = Vector3()

class MDLHeader:
    def __init__(self):
        self.id = 0
        self.version = 0
        self.checksum = 0
        self.name = ""
        self.dataLength = 0
        self.eyeposition = Vector3()
        self.illumposition = Vector3()
        self.hull_min = Vector3()
        self.hull_max = Vector3()
        self.view_bbmin = Vector3()
        self.view_bbmax = Vector3()
        self.flags = 0
        self.bone_count = 0
        self.bone_offset = 0
        self.texture_count = 0
        self.texture_offset = 0

class VVDHeader:
    """Заголовок VVD файла"""
    def __init__(self):
        self.id = 0                    # "IDSV"
        self.version = 0
        self.checksum = 0
        self.numLODs = 0
        self.numLODVertexes = []
        self.numFixups = 0
        self.fixupTableStart = 0
        self.vertexDataStart = 0
        self.tangentDataStart = 0

class VTXHeader:
    """Заголовок VTX файла"""
    def __init__(self):
        self.version = 0
        self.vertCacheSize = 0
        self.maxBonesPerStrip = 0
        self.maxBonesPerTri = 0
        self.maxBonesPerVert = 0
        self.checkSum = 0
        self.numLODs = 0
        self.materialReplacementListOffset = 0
        self.numBodyParts = 0
        self.bodyPartOffset = 0

class VTXBodyPart:
    """Часть тела в VTX файле"""
    def __init__(self):
        self.numModels = 0
        self.modelOffset = 0

class VTXModel:
    """Модель в VTX файле"""
    def __init__(self):
        self.numLODs = 0
        self.lodOffset = 0

class VTXModelLOD:
    """LOD модели в VTX файле"""
    def __init__(self):
        self.numMeshes = 0
        self.meshOffset = 0
        self.switchPoint = 0.0

class VTXMesh:
    """Меш в VTX файле"""
    def __init__(self):
        self.numStripGroups = 0
        self.stripGroupHeaderOffset = 0
        self.flags = 0

class VTXStripGroup:
    """Группа полос в VTX файле"""
    def __init__(self):
        self.numVerts = 0
        self.vertOffset = 0
        self.numIndices = 0
        self.indexOffset = 0
        self.numStrips = 0
        self.stripOffset = 0
        self.flags = 0

class Vertex:
    """Структура вершины"""
    def __init__(self):
        self.m_BoneWeights = [0.0] * 3
        self.m_BoneIndices = [0] * 3
        self.m_vecPosition = Vector3()
        self.m_vecNormal = Vector3()
        self.m_vecTexCoord = [0.0, 0.0]

class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

class MDLHeader:
    def __init__(self):
        self.id = 0
        self.version = 0
        self.checksum = 0
        self.name = ""
        self.length = 0
        self.eyeposition = Vector3()
        self.illumposition = Vector3()
        self.hull_min = Vector3()
        self.hull_max = Vector3()
        self.view_bbmin = Vector3()
        self.view_bbmax = Vector3()
        self.flags = 0
        self.bone_count = 0
        self.bone_offset = 0
        self.bonecontroller_count = 0
        self.bonecontroller_offset = 0
        self.hitbox_count = 0
        self.hitbox_offset = 0
        self.sequence_count = 0
        self.sequence_offset = 0
        self.texture_count = 0
        self.texture_offset = 0
        self.bodypart_count = 0
        self.bodypart_offset = 0

class ImprovedMDLLoader:
    def __init__(self, scale=1.0):
        self.header = None
        self.vertices = []  # Будет содержать координаты [x,y,z, x,y,z, ...]
        self.vertex_positions = []  # Временное хранение для загрузки
        self.indices = []
        self.textures = []
        self.bodyparts = []
        self.models = []
        self.meshes = []
        self.debug_info = {}
        self.scale = scale  # Масштаб модели
        self.vtx_data = None  # Данные из VTX файла
        
    def _parse_model(self, f):
        """Читает данные модели из MDL файла"""
        name = f.read(64).decode('ascii', errors='ignore').rstrip('\x00')
        type = struct.unpack('I', f.read(4))[0]
        boundingradius = struct.unpack('f', f.read(4))[0]
        mesh_count = struct.unpack('I', f.read(4))[0]
        mesh_offset = struct.unpack('I', f.read(4))[0]
        
        # Проверяем валидность данных
        if mesh_count > 1024:  # Разумное ограничение на количество мешей
            print(f"[Model Viewer] Warning: Unusually high mesh count: {mesh_count}, truncating")
            mesh_count = min(mesh_count, 1024)
        
        vertex_count = struct.unpack('I', f.read(4))[0]
        vertex_offset = struct.unpack('I', f.read(4))[0]
        tangent_offset = struct.unpack('I', f.read(4))[0]
        
        attachment_count = struct.unpack('I', f.read(4))[0]
        attachment_offset = struct.unpack('I', f.read(4))[0]
        
        eyeball_count = struct.unpack('I', f.read(4))[0]
        eyeball_offset = struct.unpack('I', f.read(4))[0]
        
        model = {
            'name': name,
            'type': type,
            'boundingradius': boundingradius,
            'mesh_count': mesh_count,
            'mesh_offset': mesh_offset,
            'vertex_count': vertex_count,
            'vertex_offset': vertex_offset,
            'meshes': []
        }
        
        # Сохраняем текущую позицию
        current_pos = f.tell()
        
        # Читаем меши модели
        f.seek(mesh_offset)
        for i in range(mesh_count):
            material_index = struct.unpack('I', f.read(4))[0]
            model_offset = struct.unpack('I', f.read(4))[0]
            vertex_count = struct.unpack('I', f.read(4))[0]
            vertex_offset = struct.unpack('I', f.read(4))[0]
            flex_count = struct.unpack('I', f.read(4))[0]
            flex_offset = struct.unpack('I', f.read(4))[0]
            material_type = struct.unpack('I', f.read(4))[0]
            material_param = struct.unpack('I', f.read(4))[0]
            
            model['meshes'].append({
                'material_index': material_index,
                'model_offset': model_offset,
                'vertex_count': vertex_count,
                'vertex_offset': vertex_offset
            })
            
        # Восстанавливаем позицию
        f.seek(current_pos)
        
        return model
        
    def set_scale(self, scale):
        """Устанавливает новый масштаб модели и пересчитывает геометрию"""
        self.scale = scale
        
        # Если модель уже загружена, пересчитываем вершины
        if self.vertices:
            # Пересчитываем каждую вершину
            for i in range(0, len(self.vertices), 3):
                self.vertices[i] *= scale
                self.vertices[i+1] *= scale
                self.vertices[i+2] *= scale
                
        # Если используется bounding box, пересоздаем его
        if self.header and not self.vertices:
            self._create_bounding_box()
            
    def _parse_bones(self, f):
        """Читает кости модели"""
        if not self.header or not hasattr(self.header, 'bone_offset'):
            return
            
        f.seek(self.header.bone_offset)
        self.bones = []
        
        for i in range(self.header.bone_count):
            bone = {
                'name': f.read(32).decode('ascii', errors='ignore').rstrip('\x00'),
                'parent': struct.unpack('i', f.read(4))[0],
                'bone_controller': struct.unpack('iiiiii', f.read(24)),
                'pos': struct.unpack('fff', f.read(12)),
                'quat': struct.unpack('ffff', f.read(16)),
                'rot': struct.unpack('fff', f.read(12)),
                'pos_scale': struct.unpack('fff', f.read(12)),
                'rot_scale': struct.unpack('fff', f.read(12)),
                'pose_to_bone': [struct.unpack('ffff', f.read(16)) for _ in range(3)],
                'q_alignment': struct.unpack('ffff', f.read(16)),
                'flags': struct.unpack('i', f.read(4))[0],
                'proc_type': struct.unpack('i', f.read(4))[0],
                'proc_index': struct.unpack('i', f.read(4))[0],
                'physics_bone': struct.unpack('i', f.read(4))[0],
            }
            self.bones.append(bone)


    def load_mdl(self, filepath):
        """Загружает MDL файл"""
        try:
            # Читаем MDL файл
            with open(filepath, 'rb') as f:
                # Проверяем сигнатуру
                signature = f.read(4)
                if signature != b'IDST':
                    print("[Model Viewer] Invalid MDL signature")
                    return False
                
                # Читаем заголовок
                f.seek(0)
                self.header = self._parse_mdl_header(f)
                
                if not self._validate_header():
                    return False
                
                # Парсим компоненты модели
                self._parse_textures(f)
                self._parse_bodyparts(f)
            
            # Загружаем VVD файл
            vvd_path = os.path.splitext(filepath)[0] + ".vvd"
            vtx_path = os.path.splitext(filepath)[0] + ".dx90.vtx"
            
            print(f"[Model Viewer] Looking for VVD file: {vvd_path}")
            print(f"[Model Viewer] Looking for VTX file: {vtx_path}")
            
            vvd_loaded = False
            vtx_loaded = False
            
            if os.path.exists(vvd_path):
                if not self.load_vvd(vvd_path):
                    print("[Model Viewer] Failed to load VVD file")
                else:
                    print("[Model Viewer] VVD file loaded successfully")
                    vvd_loaded = True
            else:
                print("[Model Viewer] VVD file not found")
            
            # Загружаем VTX файл для правильных индексов
            if os.path.exists(vtx_path):
                if not self.load_vtx(vtx_path):
                    print("[Model Viewer] Failed to load VTX file")
                else:
                    print("[Model Viewer] VTX file loaded successfully")
                    vtx_loaded = True
            else:
                print("[Model Viewer] VTX file not found")
            
            # Если оба файла загружены, строим правильную геометрию
            if vvd_loaded and vtx_loaded:
                print("[Model Viewer] Building mesh from VTX data...")
                self._build_mesh_from_vtx()
            elif vvd_loaded:
                print("[Model Viewer] Warning: VTX file missing, using fallback mesh generation")
                self._create_fallback_mesh()
            else:
                print("[Model Viewer] Creating bounding box fallback")
                self._create_bounding_box()

            # Выводим информацию
            vertex_count = len(self.vertices) // 3
            print(f"[Model Viewer] Model loaded:")
            print(f"  Name: {self.header.name if hasattr(self.header, 'name') else 'Unknown'}")
            print(f"  Version: {self.header.version if hasattr(self.header, 'version') else 'Unknown'}")
            print(f"  Vertices: {vertex_count}")
            print(f"  Textures: {len(self.textures)}")
            print(f"  Body parts: {len(self.bodyparts)}")
            return True

        except Exception as ex:
            print(f"[Model Viewer] Error loading MDL: {str(ex)}")
            import traceback
            traceback.print_exc()
            return False


    def _create_bounding_box(self):
        """Создает геометрию ограничивающего бокса на основе размеров модели"""
        # Используем размеры из заголовка MDL с учетом масштаба
        min_x = self.header.hull_min.x * self.scale
        min_y = self.header.hull_min.y * self.scale
        min_z = self.header.hull_min.z * self.scale
        max_x = self.header.hull_max.x * self.scale
        max_y = self.header.hull_max.y * self.scale
        max_z = self.header.hull_max.z * self.scale
        
        # Создаем вершины box'а
        self.vertices = [
            min_x, min_y, min_z,  max_x, min_y, min_z,  max_x, max_y, min_z,  min_x, max_y, min_z,
            min_x, min_y, max_z,  max_x, min_y, max_z,  max_x, max_y, max_z,  min_x, max_y, max_z,
        ]
        
        # Индексы для отрисовки граней бокса
        self.indices = [
            0, 1, 2, 2, 3, 0,  # front
            1, 5, 6, 6, 2, 1,  # right
            5, 4, 7, 7, 6, 5,  # back
            4, 0, 3, 3, 7, 4,  # left
            3, 2, 6, 6, 7, 3,  # top
            4, 5, 1, 1, 0, 4,  # bottom
        ]

    def load_vvd(self, filepath):
        """Загрузка данных вершин из VVD файла"""
        try:
            with open(filepath, 'rb') as f:
                # Проверяем сигнатуру
                signature = f.read(4)
                if signature != b'IDSV':
                    print(f"[Model Viewer] Invalid VVD signature: {signature}")
                    return False
                    
                # Читаем заголовок VVD
                f.seek(0)
                vvd_header = self._parse_vvd_header(f)
                
                # Выводим информацию о VVD файле
                print(f"[Model Viewer] VVD Header Info:")
                print(f"  Version: {vvd_header.version}")
                print(f"  Checksum: {vvd_header.checksum}")
                print(f"  LOD Count: {vvd_header.numLODs}")
                print(f"  Vertex Count (LOD0): {vvd_header.numLODVertexes[0]}")
                print(f"  Vertex Data Start: {vvd_header.vertexDataStart}")
                
                # Если контрольные суммы не совпадают, это может быть неправильный файл
                if vvd_header.checksum != self.header.checksum:
                    print(f"[Model Viewer] Warning: VVD checksum mismatch")
                    print(f"  VVD Checksum: {vvd_header.checksum}")
                    print(f"  MDL Checksum: {self.header.checksum}")
                
                # Читаем вершины
                self._parse_vertices(f, vvd_header)
                
                print(f"[Model Viewer] Loaded {len(self.vertices)//3} vertices from VVD")
                return True
                
        except Exception as e:
            print(f"[Model Viewer] Error loading VVD: {e}")
            import traceback
            traceback.print_exc()
            return False
        
    def _convert_vertices(self):
        """Конвертирует загруженные вершины в правильный формат с учетом масштаба"""
        try:
            if not self.vertex_positions:
                print("[Model Viewer] Warning: No vertices to convert")
                return

            self.vertices = []
            for vertex in self.vertex_positions:
                # Проверяем что vertex и его позиция существуют
                if hasattr(vertex, 'm_vecPosition'):
                    # Добавляем координаты X, Y, Z с учетом масштаба
                    self.vertices.extend([
                        vertex.m_vecPosition.x * self.scale,
                        vertex.m_vecPosition.y * self.scale,
                        vertex.m_vecPosition.z * self.scale
                    ])
                else:
                    print(f"[Model Viewer] Warning: Invalid vertex format")

            # Сохраняем копию исходных данных перед очисткой
            self._original_vertices = self.vertex_positions.copy()
            self.vertex_positions.clear()
            
            print(f"[Model Viewer] Converted {len(self.vertices) // 3} vertices")
        except Exception as e:
            print(f"[Model Viewer] Error converting vertices: {str(e)}")
            self.vertices = []
        
    def _parse_vvd_header(self, f):
        """Парсинг заголовка VVD файла"""
        header = VVDHeader()
        header.id = struct.unpack('I', f.read(4))[0]
        header.version = struct.unpack('I', f.read(4))[0]
        header.checksum = struct.unpack('I', f.read(4))[0]
        header.numLODs = struct.unpack('I', f.read(4))[0]
        header.numLODVertexes = [struct.unpack('I', f.read(4))[0] for _ in range(8)]  # Максимум 8 LOD
        header.numFixups = struct.unpack('I', f.read(4))[0]
        header.fixupTableStart = struct.unpack('I', f.read(4))[0]
        header.vertexDataStart = struct.unpack('I', f.read(4))[0]
        header.tangentDataStart = struct.unpack('I', f.read(4))[0]
        return header
        
    def _parse_vertices(self, f, vvd_header):
        """Парсинг данных вершин из VVD файла (только загрузка вершин, индексы будут из VTX)"""
        # Сначала загружаем все вершины из VVD
        f.seek(vvd_header.vertexDataStart)
        
        # Очищаем старые данные
        self.vertices = []
        self.indices = []
        
        # Читаем вершины для LOD0 (самый детальный уровень)
        num_vertices = vvd_header.numLODVertexes[0]
        
        print(f"[Model Viewer] Loading {num_vertices} vertices from VVD...")
        
        # В Source Engine вершина содержит:
        # - boneWeight[3] (12 bytes)
        # - boneIndex[3] (3 bytes)
        # - 1 byte padding
        # - position (12 bytes)
        # - normal (12 bytes)
        # - texcoord (8 bytes)
        vertex_size = 48  # Общий размер вершины в байтах
        vertex_positions = []  # Временное хранилище позиций вершин
        vertex_bones = []     # Веса и индексы костей
        vertex_normals = []   # Нормали
        vertex_texcoords = [] # Текстурные координаты
        
        # Читаем данные вершин
        for i in range(num_vertices):
            try:
                # Читаем блок данных для вершины целиком
                vertex_data = f.read(48)  # 48 байт - размер структуры вершины
                if len(vertex_data) < 48:
                    print(f"[Model Viewer] Warning: Unexpected end of VVD data at vertex {i}")
                    break

                # Распаковываем данные
                bone_weights = struct.unpack('fff', vertex_data[0:12])
                bone_indices = struct.unpack('BBB', vertex_data[12:15])
                # padding байт находится в vertex_data[15]
                position = struct.unpack('fff', vertex_data[16:28])
                normal = struct.unpack('fff', vertex_data[28:40])
                texcoord = struct.unpack('ff', vertex_data[40:48])
                
                # Создаем объект вершины и добавляем его в vertex_positions
                vertex = Vertex()
                vertex.m_BoneWeights = list(bone_weights)
                vertex.m_BoneIndices = list(bone_indices)
                vertex.m_vecPosition = Vector3(*position)
                vertex.m_vecNormal = Vector3(*normal)
                vertex.m_vecTexCoord = list(texcoord)
                self.vertex_positions.append(vertex)

                # Сохраняем данные и сразу применяем масштаб
                scaled_position = (
                    position[0] * self.scale,
                    position[1] * self.scale,
                    position[2] * self.scale
                )
                
                # Добавляем данные в соответствующие списки
                vertex_positions.append(scaled_position)
                vertex_bones.append((bone_weights, bone_indices))
                vertex_normals.append(normal)
                vertex_texcoords.append(texcoord)

            except Exception as e:
                print(f"[Model Viewer] Error parsing vertex {i}: {str(e)}")
                break
            
        # Преобразуем позиции вершин в плоский список для OpenGL
        self.vertices = []
        for pos in vertex_positions:
            self.vertices.extend([pos[0], pos[1], pos[2]])
            
        print(f"[Model Viewer] Successfully loaded {len(self.vertex_positions)} vertices")
        print(f"[Model Viewer] Vertex data will be converted after indices are loaded from VTX")
        
        # НЕ создаем индексы здесь - они будут загружены из VTX файла
        # Это исправляет основную проблему с неправильным соединением полигонов

                        
    def _parse_mdl_header(self, f):
        """Правильный парсинг заголовка MDL согласно studio.h"""
        header = MDLHeader()
        
        # Основные поля
        header.id = struct.unpack('<I', f.read(4))[0]
        header.version = struct.unpack('<I', f.read(4))[0]
        header.checksum = struct.unpack('<I', f.read(4))[0]
        header.name = f.read(64).decode('ascii', errors='ignore').rstrip('\x00')
        header.dataLength = struct.unpack('<I', f.read(4))[0]
        
        # Векторы (по 12 байт каждый - 3 float)
        eye_pos = struct.unpack('<fff', f.read(12))
        header.eyeposition = Vector3(*eye_pos)
        
        illum_pos = struct.unpack('<fff', f.read(12))
        header.illumposition = Vector3(*illum_pos)
        
        hull_min = struct.unpack('<fff', f.read(12))
        header.hull_min = Vector3(*hull_min)
        
        hull_max = struct.unpack('<fff', f.read(12))
        header.hull_max = Vector3(*hull_max)
        
        view_bbmin = struct.unpack('<fff', f.read(12))
        header.view_bbmin = Vector3(*view_bbmin)
        
        view_bbmax = struct.unpack('<fff', f.read(12))
        header.view_bbmax = Vector3(*view_bbmax)
        
        header.flags = struct.unpack('<I', f.read(4))[0]
        
        # Кости
        header.bone_count = struct.unpack('<I', f.read(4))[0]
        header.bone_offset = struct.unpack('<I', f.read(4))[0]
        
        # Контроллеры костей
        header.bonecontroller_count = struct.unpack('<I', f.read(4))[0]
        header.bonecontroller_offset = struct.unpack('<I', f.read(4))[0]
        
        # Hitbox
        header.hitbox_count = struct.unpack('<I', f.read(4))[0]
        header.hitbox_offset = struct.unpack('<I', f.read(4))[0]
        
        # Анимации
        header.localanim_count = struct.unpack('<I', f.read(4))[0]
        header.localanim_offset = struct.unpack('<I', f.read(4))[0]
        
        # Последовательности
        header.localseq_count = struct.unpack('<I', f.read(4))[0]
        header.localseq_offset = struct.unpack('<I', f.read(4))[0]
        
        header.activitylistversion = struct.unpack('<I', f.read(4))[0]
        header.eventsindexed = struct.unpack('<I', f.read(4))[0]
        
        # Текстуры
        header.texture_count = struct.unpack('<I', f.read(4))[0]
        header.texture_offset = struct.unpack('<I', f.read(4))[0]
        
        header.texturedir_count = struct.unpack('<I', f.read(4))[0]
        header.texturedir_offset = struct.unpack('<I', f.read(4))[0]
        
        # Скины
        header.skinreference_count = struct.unpack('<I', f.read(4))[0]
        header.skinrfamily_count = struct.unpack('<I', f.read(4))[0]
        header.skinreference_index = struct.unpack('<I', f.read(4))[0]
        
        # Части тела
        header.bodypart_count = struct.unpack('<I', f.read(4))[0]
        header.bodypart_offset = struct.unpack('<I', f.read(4))[0]
        
        # Вложения
        header.attachment_count = struct.unpack('<I', f.read(4))[0]
        header.attachment_offset = struct.unpack('<I', f.read(4))[0]
        
        return header
        
    def _validate_header(self):
        """Проверка корректности заголовка"""
        if self.header.id != 0x54534449:  # "IDST" в little-endian
            print(f"Invalid header ID: 0x{self.header.id:08X}")
            return False
        
        if self.header.version < 44 or self.header.version > 49:
            print(f"Unsupported version: {self.header.version}")
            return False
        
        return True
        
    def _parse_textures(self, f):
        """Парсинг информации о текстурах"""
        if self.header.texture_count == 0:
            return
        
        f.seek(self.header.texture_offset)
        
        for i in range(self.header.texture_count):
            texture = MDLTexture()
            texture.name_offset = struct.unpack('<I', f.read(4))[0]
            texture.flags = struct.unpack('<I', f.read(4))[0]
            texture.used = struct.unpack('<I', f.read(4))[0]
            texture.unused = struct.unpack('<I', f.read(4))[0]
            
            # Пропускаем указатели материалов (8 байт)
            f.read(8)
            
            # Пропускаем оставшуюся часть структуры (40 байт)
            f.read(40)
            
            self.textures.append(texture)
        
        # Читаем имена текстур
        for texture in self.textures:
            if texture.name_offset > 0:
                current_pos = f.tell()
                f.seek(texture.name_offset)
                name_bytes = b''
                while True:
                    byte = f.read(1)
                    if not byte or byte == b'\x00':
                        break
                    name_bytes += byte
                texture.name = name_bytes.decode('ascii', errors='ignore')
                f.seek(current_pos)
                
    def _parse_bodyparts(self, f):
        """Парсинг частей тела модели"""
        if self.header.bodypart_count == 0:
            return
        
        f.seek(self.header.bodypart_offset)
        
        for i in range(self.header.bodypart_count):
            bodypart = MDLBodyPart()
            bodypart.name_offset = struct.unpack('<I', f.read(4))[0]
            bodypart.nummodels = struct.unpack('<I', f.read(4))[0]
            bodypart.base = struct.unpack('<I', f.read(4))[0]
            bodypart.modelindex = struct.unpack('<I', f.read(4))[0]
            
            self.bodyparts.append(bodypart)
            
            print(f"  BodyPart {i}: {bodypart.nummodels} models")

    def load_vtx(self, filepath):
        """Загрузка индексов треугольников из VTX файла с улучшенной валидацией"""
        try:
            with open(filepath, 'rb') as f:
                # Читаем заголовок VTX
                vtx_header = self._parse_vtx_header(f)
                
                # Улучшенная валидация заголовка VTX
                if not self._validate_vtx_header(vtx_header):
                    print(f"[Model Viewer] Invalid VTX header")
                    return False
                
                print(f"[Model Viewer] VTX Header Info:")
                print(f"  Version: {vtx_header.version}")
                print(f"  Checksum: {vtx_header.checkSum}")
                print(f"  Body Parts: {vtx_header.numBodyParts}")
                print(f"  LODs: {vtx_header.numLODs}")
                print(f"  Vertex Cache Size: {vtx_header.vertCacheSize}")
                print(f"  Max Bones Per Strip: {vtx_header.maxBonesPerStrip}")
                
                # Проверяем контрольную сумму
                if vtx_header.checkSum != self.header.checksum:
                    print(f"[Model Viewer] Warning: VTX checksum mismatch")
                    print(f"  VTX Checksum: {vtx_header.checkSum}")
                    print(f"  MDL Checksum: {self.header.checksum}")
                
                # Парсим данные VTX
                self.vtx_data = self._parse_vtx_data(f, vtx_header)
                
                # Валидация загруженных данных
                if not self._validate_vtx_data():
                    print(f"[Model Viewer] VTX data validation failed")
                    return False
                
                # Выводим статистику загруженных данных
                if self.vtx_data:
                    triangle_indices_count = len(self.vtx_data.get('triangle_indices', []))
                    print(f"[Model Viewer] VTX data loaded:")
                    print(f"  - Total triangle indices: {triangle_indices_count}")
                    print(f"  - Estimated triangles: {triangle_indices_count // 3}")
                
                return True
                
        except Exception as e:
            print(f"[Model Viewer] Error loading VTX: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _validate_vtx_header(self, vtx_header):
        """Валидация заголовка VTX файла"""
        # Проверка версии
        if vtx_header.version != 7:
            print(f"[Model Viewer] Unsupported VTX version: {vtx_header.version}")
            return False
        
        # Проверка разумных значений
        if vtx_header.numBodyParts > 32 or vtx_header.numBodyParts <= 0:
            print(f"[Model Viewer] Invalid body parts count: {vtx_header.numBodyParts}")
            return False
        
        if vtx_header.numLODs > 8 or vtx_header.numLODs <= 0:
            print(f"[Model Viewer] Invalid LOD count: {vtx_header.numLODs}")
            return False
        
        # Проверка контрольной суммы с MDL (если доступна)
        if hasattr(self, 'header') and hasattr(self.header, 'checksum'):
            if vtx_header.checkSum != self.header.checksum:
                print(f"[Model Viewer] VTX checksum mismatch: {vtx_header.checkSum} != {self.header.checksum}")
                # Не возвращаем False, так как это предупреждение, а не критическая ошибка
        
        return True
    
    def _validate_vtx_data(self):
        """Валидация загруженных VTX данных"""
        if not self.vtx_data:
            return False
        
        triangle_indices = self.vtx_data.get('triangle_indices', [])
        if not triangle_indices:
            print(f"[Model Viewer] No triangle indices found in VTX data")
            return False
        
        # Проверка валидности индексов
        if self.vertex_positions:
            max_vertex_index = len(self.vertex_positions) - 1
            invalid_count = sum(1 for idx in triangle_indices if idx > max_vertex_index)
            
            if invalid_count > 0:
                percentage = (invalid_count / len(triangle_indices)) * 100
                print(f"[Model Viewer] Warning: {invalid_count} invalid indices ({percentage:.1f}%)")
                
                # Если слишком много невалидных индексов, считаем данные поврежденными
                if percentage > 50:
                    print(f"[Model Viewer] Too many invalid indices, data may be corrupted")
                    return False
        
        return True
    
    def _parse_vtx_header(self, f):
        """Парсинг заголовка VTX файла"""
        header = VTXHeader()
        header.version = struct.unpack('<I', f.read(4))[0]
        header.vertCacheSize = struct.unpack('<I', f.read(4))[0]
        header.maxBonesPerStrip = struct.unpack('<H', f.read(2))[0]
        header.maxBonesPerTri = struct.unpack('<H', f.read(2))[0]
        header.maxBonesPerVert = struct.unpack('<I', f.read(4))[0]
        header.checkSum = struct.unpack('<I', f.read(4))[0]
        header.numLODs = struct.unpack('<I', f.read(4))[0]
        header.materialReplacementListOffset = struct.unpack('<I', f.read(4))[0]
        header.numBodyParts = struct.unpack('<I', f.read(4))[0]
        header.bodyPartOffset = struct.unpack('<I', f.read(4))[0]
        return header
    
    def _parse_vtx_data(self, f, vtx_header):
        """Парсинг данных VTX файла согласно архитектуре Source Engine"""
        vtx_data = {
            'bodyparts': [],
            'triangle_indices': []  # Финальные индексы треугольников
        }
        
        print(f"[Model Viewer] Parsing VTX data with {vtx_header.numBodyParts} body parts...")
        
        # Переходим к данным частей тела
        f.seek(vtx_header.bodyPartOffset)
        
        for bp_idx in range(vtx_header.numBodyParts):
            bodypart = VTXBodyPart()
            bodypart.numModels = struct.unpack('<I', f.read(4))[0]
            bodypart.modelOffset = struct.unpack('<I', f.read(4))[0]
            
            print(f"[Model Viewer] Body part {bp_idx}: {bodypart.numModels} models")
            
            # Сохраняем текущую позицию
            current_pos = f.tell()
            
            # Читаем модели в части тела
            f.seek(vtx_header.bodyPartOffset + bodypart.modelOffset)
            
            models = []
            for model_idx in range(bodypart.numModels):
                try:
                    model = VTXModel()
                    model.numLODs = struct.unpack('<I', f.read(4))[0]
                    model.lodOffset = struct.unpack('<I', f.read(4))[0]
                    
                    # Валидация количества LOD
                    if model.numLODs > 8 or model.numLODs <= 0:
                        print(f"[Model Viewer] Warning: Invalid LOD count {model.numLODs} for model {model_idx}, skipping")
                        break
                    
                    print(f"[Model Viewer] Model {model_idx}: {model.numLODs} LODs")
                    
                except struct.error as e:
                    print(f"[Model Viewer] Error reading model {model_idx}: {e}")
                    break
                except Exception as e:
                    print(f"[Model Viewer] Unexpected error reading model {model_idx}: {e}")
                    break
                
                # Читаем LOD0 (самый детальный уровень)
                if model.numLODs > 0:
                    lod_pos = f.tell() - 8 + model.lodOffset
                    f.seek(lod_pos)
                    
                    lod = VTXModelLOD()
                    lod.numMeshes = struct.unpack('<I', f.read(4))[0]
                    lod.meshOffset = struct.unpack('<I', f.read(4))[0]
                    lod.switchPoint = struct.unpack('<f', f.read(4))[0]
                    
                    print(f"[Model Viewer] LOD0: {lod.numMeshes} meshes")
                    
                    # Читаем меши
                    mesh_pos = lod_pos + lod.meshOffset
                    f.seek(mesh_pos)
                    
                    for mesh_idx in range(lod.numMeshes):
                        mesh = VTXMesh()
                        mesh.numStripGroups = struct.unpack('<I', f.read(4))[0]
                        mesh.stripGroupHeaderOffset = struct.unpack('<I', f.read(4))[0]
                        mesh.flags = struct.unpack('<B', f.read(1))[0]
                        f.read(3)  # padding
                        
                        print(f"[Model Viewer] Mesh {mesh_idx}: {mesh.numStripGroups} strip groups")
                        
                        # Читаем группы полос
                        sg_pos = mesh_pos + mesh.stripGroupHeaderOffset
                        f.seek(sg_pos)
                        
                        for sg_idx in range(mesh.numStripGroups):
                            strip_group = VTXStripGroup()
                            strip_group.numVerts = struct.unpack('<I', f.read(4))[0]
                            strip_group.vertOffset = struct.unpack('<I', f.read(4))[0]
                            strip_group.numIndices = struct.unpack('<I', f.read(4))[0]
                            strip_group.indexOffset = struct.unpack('<I', f.read(4))[0]
                            strip_group.numStrips = struct.unpack('<I', f.read(4))[0]
                            strip_group.stripOffset = struct.unpack('<I', f.read(4))[0]
                            strip_group.flags = struct.unpack('<B', f.read(1))[0]
                            f.read(3)  # padding
                            
                            print(f"[Model Viewer] Strip group {sg_idx}: {strip_group.numVerts} verts, {strip_group.numIndices} indices, {strip_group.numStrips} strips")
                            
                            # Читаем vertex remapping table
                            vertex_remap = []
                            if strip_group.numVerts > 0:
                                verts_pos = sg_pos + strip_group.vertOffset
                                f.seek(verts_pos)
                                
                                for v in range(strip_group.numVerts):
                                    # Структура OptimizedVertex_t из Source SDK
                                    bone_weight_indices = struct.unpack('<BBB', f.read(3))
                                    num_bones = struct.unpack('<B', f.read(1))[0]
                                    orig_mesh_vert_id = struct.unpack('<H', f.read(2))[0]
                                    bone_ids = struct.unpack('<BBB', f.read(3))
                                    f.read(1)  # padding
                                    
                                    vertex_remap.append(orig_mesh_vert_id)
                            
                            # Читаем strips и конвертируем в треугольники
                            if strip_group.numStrips > 0:
                                strips_pos = sg_pos + strip_group.stripOffset
                                f.seek(strips_pos)
                                
                                for strip_idx in range(strip_group.numStrips):
                                    # Структура StripHeader_t
                                    num_indices = struct.unpack('<I', f.read(4))[0]
                                    index_offset = struct.unpack('<I', f.read(4))[0]
                                    num_verts = struct.unpack('<I', f.read(4))[0]
                                    vert_offset = struct.unpack('<I', f.read(4))[0]
                                    num_bones = struct.unpack('<H', f.read(2))[0]
                                    flags = struct.unpack('<B', f.read(1))[0]
                                    f.read(1)  # padding
                                    
                                    # Читаем индексы для этого strip
                                    if num_indices > 0:
                                        current_pos_backup = f.tell()
                                        indices_pos = sg_pos + strip_group.indexOffset + index_offset
                                        f.seek(indices_pos)
                                        
                                        strip_indices = []
                                        for i in range(num_indices):
                                            local_index = struct.unpack('<H', f.read(2))[0]
                                            # Улучшенная обработка vertex remapping
                                            if local_index < len(vertex_remap):
                                                global_index = vertex_remap[local_index]
                                                # Дополнительная валидация глобального индекса
                                                if global_index < len(self.vertex_positions):
                                                    strip_indices.append(global_index)
                                                else:
                                                    # Используем модуло для циклического переназначения
                                                    corrected_index = global_index % len(self.vertex_positions)
                                                    strip_indices.append(corrected_index)
                                            else:
                                                # Если local_index выходит за границы, используем безопасное значение
                                                safe_index = local_index % len(vertex_remap) if vertex_remap else 0
                                                if safe_index < len(vertex_remap):
                                                    global_index = vertex_remap[safe_index]
                                                    if global_index < len(self.vertex_positions):
                                                        strip_indices.append(global_index)
                                                    else:
                                                        strip_indices.append(global_index % len(self.vertex_positions))
                                        
                                        # Конвертируем triangle strip в треугольники с улучшенной обработкой
                                        self._convert_strip_to_triangles_improved(strip_indices, vtx_data['triangle_indices'])
                                        
                                        f.seek(current_pos_backup)
                        
                        # Возвращаемся к следующему мешу
                        mesh_pos += 16  # размер структуры меша
                        f.seek(mesh_pos)
                
                models.append(model)
            
            vtx_data['bodyparts'].append({
                'bodypart': bodypart,
                'models': models
            })
            
            # Восстанавливаем позицию для следующей части тела
            f.seek(current_pos)
        
        print(f"[Model Viewer] VTX parsing complete. Generated {len(vtx_data['triangle_indices'])} triangle indices")
        return vtx_data
    
    def _convert_strip_to_triangles(self, strip_indices, output_indices):
        """Конвертирует triangle strip в список треугольников согласно алгоритму Source Engine"""
        if len(strip_indices) < 3:
            return
            
        # Алгоритм конвертации triangle strip в треугольники
        for i in range(len(strip_indices) - 2):
            idx1 = strip_indices[i]
            idx2 = strip_indices[i + 1]
            idx3 = strip_indices[i + 2]
            
            # Пропускаем вырожденные треугольники
            if idx1 == idx2 or idx2 == idx3 or idx1 == idx3:
                continue
                
            # В triangle strip каждый четный треугольник имеет нормальный порядок вершин,
            # каждый нечетный - инвертированный для правильной ориентации нормалей
            if i % 2 == 0:
                # Четный треугольник - нормальный порядок
                output_indices.extend([idx1, idx2, idx3])
            else:
                # Нечетный треугольник - инвертированный порядок
                output_indices.extend([idx1, idx3, idx2])
    
    def _convert_strip_to_triangles_improved(self, strip_indices, output_indices):
        """Улучшенная конвертация triangle strips с обработкой degenerate triangles и restart sequences"""
        if len(strip_indices) < 3:
            return
        
        i = 0
        triangle_count = 0
        
        while i < len(strip_indices) - 2:
            idx0 = strip_indices[i]
            idx1 = strip_indices[i + 1]
            idx2 = strip_indices[i + 2]
            
            # Обработка restart primitives (0xFFFF или повторяющиеся индексы)
            if (idx0 == 0xFFFF or idx1 == 0xFFFF or idx2 == 0xFFFF or
                idx0 == idx1 or idx1 == idx2 or idx0 == idx2):
                
                # Пропускаем degenerate triangle и ищем следующий валидный
                i += 1
                continue
            
            # Дополнительная валидация индексов
            max_vertex_index = len(self.vertex_positions) - 1 if self.vertex_positions else 0
            if (idx0 > max_vertex_index or idx1 > max_vertex_index or idx2 > max_vertex_index):
                i += 1
                continue
            
            # Проверяем геометрическую валидность треугольника
            if self._validate_triangle_geometry(idx0, idx1, idx2):
                # Добавляем треугольник с правильной ориентацией
                if triangle_count % 2 == 0:
                    # Четный треугольник - нормальный порядок
                    output_indices.extend([idx0, idx1, idx2])
                else:
                    # Нечетный треугольник - инвертированный порядок
                    output_indices.extend([idx0, idx2, idx1])
                
                triangle_count += 1
            
            i += 1
    
    def _build_mesh_from_vtx(self):
        """Строит правильную геометрию используя данные из VTX файла согласно архитектуре Source Engine"""
        try:
            if not self.vtx_data or not self.vertex_positions:
                print("[Model Viewer] Error: Missing VTX data or vertices")
                return
            
            print("[Model Viewer] Building mesh from VTX data...")
            
            # Очищаем старые индексы
            self.indices = []
            
            # Получаем уже обработанные треугольные индексы из VTX данных
            triangle_indices = self.vtx_data.get('triangle_indices', [])
            
            if not triangle_indices:
                print("[Model Viewer] Warning: No triangle indices found in VTX data")
                return
            
            print(f"[Model Viewer] Processing {len(triangle_indices)} triangle indices from VTX...")
            
            # Валидируем индексы
            max_vertex_index = len(self.vertex_positions) - 1
            valid_indices = []
            invalid_count = 0
            
            for idx in triangle_indices:
                if 0 <= idx <= max_vertex_index:
                    valid_indices.append(idx)
                else:
                    invalid_count += 1
                    if invalid_count <= 10:  # Показываем только первые 10 ошибок
                        print(f"[Model Viewer] Warning: Invalid vertex index {idx}, max is {max_vertex_index}")
                    elif invalid_count == 11:
                        print(f"[Model Viewer] Warning: More invalid indices found, suppressing further warnings...")
            
            if invalid_count > 0:
                print(f"[Model Viewer] Total invalid indices: {invalid_count}/{len(triangle_indices)}")
            
            # Группируем валидные индексы в треугольники и проверяем геометрию
            valid_triangles = 0
            degenerate_triangles = 0
            
            # Обрабатываем треугольники (по 3 индекса)
            for i in range(0, len(valid_indices) - 2, 3):
                if i + 2 < len(valid_indices):
                    idx1 = valid_indices[i]
                    idx2 = valid_indices[i + 1]
                    idx3 = valid_indices[i + 2]
                    
                    # Проверяем на вырожденные треугольники
                    if idx1 != idx2 and idx2 != idx3 and idx1 != idx3:
                        # Дополнительная проверка на геометрическую валидность
                        if self._validate_triangle_geometry(idx1, idx2, idx3):
                            self.indices.extend([idx1, idx2, idx3])
                            valid_triangles += 1
                        else:
                            degenerate_triangles += 1
                    else:
                        degenerate_triangles += 1
            
            print(f"[Model Viewer] Mesh building results:")
            print(f"  - Valid triangles: {valid_triangles}")
            print(f"  - Degenerate triangles skipped: {degenerate_triangles}")
            print(f"  - Total indices: {len(self.indices)}")
            
            if valid_triangles == 0:
                print("[Model Viewer] Warning: No valid triangles created!")
                return
            
            # Конвертируем вершины в финальный формат
            self._convert_vertices()
            print("[Model Viewer] Mesh building completed successfully")
            
        except Exception as e:
            print(f"[Model Viewer] Error building mesh from VTX: {str(e)}")
            import traceback
            traceback.print_exc()
            # Если не удалось построить из VTX, используем fallback
            print("[Model Viewer] Falling back to simple mesh generation")
            self._create_fallback_mesh()
    
    def _create_fallback_mesh(self):
        """Создает простую геометрию когда VTX файл недоступен"""
        try:
            if not self.vertex_positions:
                print("[Model Viewer] No vertex data for fallback mesh")
                self._create_bounding_box()
                return
            
            print(f"[Model Viewer] Creating fallback mesh from {len(self.vertex_positions)} vertices")
            
            # Очищаем старые данные
            self.indices = []
            
            # Создаем простые треугольники из последовательных вершин
            # Это не идеально, но лучше чем ничего
            vertex_count = len(self.vertex_positions)
            
            # Группируем вершины по 3 для создания треугольников
            for i in range(0, vertex_count - 2, 3):
                if i + 2 < vertex_count:
                    # Проверяем что треугольник не вырожденный
                    if self._validate_triangle_geometry(i, i+1, i+2):
                        self.indices.extend([i, i+1, i+2])
            
            print(f"[Model Viewer] Created fallback mesh with {len(self.indices) // 3} triangles")
            
            # Конвертируем вершины в финальный формат
            self._convert_vertices()
            
        except Exception as e:
            print(f"[Model Viewer] Error creating fallback mesh: {str(e)}")
            self._create_bounding_box()
    
    def _validate_triangle_geometry(self, idx1, idx2, idx3):
        """Проверяет геометрическую валидность треугольника"""
        try:
            # Получаем позиции вершин
            v1 = self.vertex_positions[idx1].m_vecPosition
            v2 = self.vertex_positions[idx2].m_vecPosition
            v3 = self.vertex_positions[idx3].m_vecPosition
            
            # Вычисляем векторы сторон
            edge1 = (v2.x - v1.x, v2.y - v1.y, v2.z - v1.z)
            edge2 = (v3.x - v1.x, v3.y - v1.y, v3.z - v1.z)
            
            # Векторное произведение для получения нормали
            normal = (
                edge1[1] * edge2[2] - edge1[2] * edge2[1],
                edge1[2] * edge2[0] - edge1[0] * edge2[2],
                edge1[0] * edge2[1] - edge1[1] * edge2[0]
            )
            
            # Проверяем длину нормали (если близка к 0, треугольник вырожденный)
            normal_length = (normal[0]**2 + normal[1]**2 + normal[2]**2)**0.5
            
            # Пороговое значение для проверки вырожденных треугольников
            return normal_length > 1e-6
            
        except (IndexError, AttributeError):
            return False

class ModelViewer(QOpenGLWidget):
    def __init__(self, parent=None):
        super(ModelViewer, self).__init__(parent)
        # Базовые параметры
        self.models = []  # List to hold loaded models
        self.textures = {}  # Dictionary to hold textures
        self.display_lists = {}  # Кэш для display lists
        
        # Параметры камеры и отображения
        self.rotation = [0, 0]  # Rotation angles for the model
        self.zoom = 120  # Camera distance from the center
        self.camera_target = [0, 0, 0]  # The point camera is looking at
        self.camera_position = [0, 50, self.zoom]  # Initial camera position
        
        # Параметры управления
        self.last_mouse_position = None  # Track last mouse position for dragging
        self.is_shift_pressed = False  # Track if Shift is pressed
        
        # Параметры отображения
        self.background_color = (0.15, 0.15, 0.15, 1)  # Default background color
        self.default_model_color = (0.7, 0.7, 0.7, 1.0)  # Светло-серый
        
        # Флаги инициализации
        self._gl_initialized = False
        print("[Model Viewer] Viewer initialized")
        
    def cleanup_resources(self):
        """Очистка OpenGL ресурсов"""
        try:
            # Удаляем display lists
            for display_list in self.display_lists.values():
                if display_list != 0:
                    try:
                        glDeleteLists(display_list, 1)
                    except Exception as e:
                        print(f"[Model Viewer] Error deleting display list {display_list}: {str(e)}")
            self.display_lists.clear()
            
            # Удаляем текстуры
            for texture_id in self.textures.values():
                if texture_id is not None:
                    try:
                        glDeleteTextures(texture_id)
                    except Exception as e:
                        print(f"[Model Viewer] Error deleting texture {texture_id}: {str(e)}")
            self.textures.clear()
            
        except Exception as e:
            print(f"[Model Viewer] Error during cleanup: {str(e)}")
            
    def initializeGL(self):
        """Инициализация OpenGL с улучшенными настройками освещения."""
        try:
            print("[Model Viewer] Initializing OpenGL...")
            
            # Очищаем старые ресурсы при повторной инициализации
            if self._gl_initialized:
                self.cleanup_resources()
            
            glClearColor(*self.background_color)
            
            # Базовые настройки
            glEnable(GL_DEPTH_TEST)
            glEnable(GL_CULL_FACE)  # Включаем отсечение невидимых граней
            glEnable(GL_NORMALIZE)   # Нормализация нормалей
            
            # Настройки освещения
            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            glShadeModel(GL_SMOOTH)  # Плавное освещение
            
            # Общие настройки материала
            glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
            glEnable(GL_COLOR_MATERIAL)
            
            # Настройка света
            self.setup_lighting()
            
            # Настройки текстурирования
            glEnable(GL_TEXTURE_2D)
            glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
            glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
            
            self._gl_initialized = True
            print("[Model Viewer] OpenGL initialized successfully with enhanced settings.")
            
        except Exception as e:
            print(f"[Model Viewer] Error during OpenGL initialization: {str(e)}")
            import traceback
            traceback.print_exc()
        
    def setup_lighting(self):
        """Настройка параметров освещения для более тусклого освещения моделей."""
        # Основной свет (GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])  # Направленный свет сверху-сбоку

        # Настройка компонентов света - значения уменьшены в 2 раза
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])   # Мягкий фоновый свет (было 0.4)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.4, 0.4, 0.4, 1.0])   # Умеренный рассеянный свет (было 0.8)
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.5, 0.5, 0.5, 1.0])  # Яркие блики (было 1.0)

        # Второй источник света для заполняющего света
        glEnable(GL_LIGHT1)
        glLightfv(GL_LIGHT1, GL_POSITION, [-0.5, 0.5, 0.2, 0.0])  # Дополнительный свет
        glLightfv(GL_LIGHT1, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])    # Было 0.2
        glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.15, 0.15, 0.15, 1.0]) # Было 0.3
        glLightfv(GL_LIGHT1, GL_SPECULAR, [0.15, 0.15, 0.15, 1.0])# Было 0.3

        # Настройки затухания света - отключаем для направленного света
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.0)
        glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.0)

        # Общее освещение сцены - ambient уменьшен в 2 раза
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.1, 0.1, 0.1, 1.0])  # Было 0.2
        glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)  # Освещение с обеих сторон
        print("[Model Viewer] Lighting setup completed with dimmer parameters.")
        
    def set_material(self, color=None, shininess=32.0):
        """Установка параметров материала с реалистичными настройками."""
        if color is None:
            color = self.default_model_color
            
        # Более реалистичные параметры материала
        ambient = [c * 0.2 for c in color[:3]] + [color[3]]   # Умеренное фоновое отражение
        diffuse = [c * 0.8 for c in color[:3]] + [color[3]]   # Основной цвет материала
        specular = [0.8, 0.8, 0.8, 1.0]                       # Яркие блики
        emission = [0.0, 0.0, 0.0, 1.0]                       # Без самосвечения
        
        # Применяем настройки материала
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, ambient)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, diffuse)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specular)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, emission)
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, shininess)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, width / height, 0.1, 5000.0)  # Увеличили дальность
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        """Отрисовка сцены с правильной ориентацией модели"""
        try:
            print("[Model Viewer] Starting scene render")
            # Отладочная информация
            if hasattr(self, 'mdl_loader'):
                print(f"[Model Viewer] Render debug:")
                print(f"  - Model loaded: Yes")
                print(f"  - Vertices available: {len(self.mdl_loader.vertices)}")
                print(f"  - Indices available: {len(self.mdl_loader.indices)}")
            else:
                print("[Model Viewer] No model data available")
            
            # Очистка буферов
            glClearColor(*self.background_color)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            # Включаем нужные функции OpenGL
            glEnable(GL_DEPTH_TEST)
            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            
            # Настройка камеры
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            
            print("[Model Viewer] Setting up camera...")
            gluLookAt(
                self.camera_position[0], self.camera_position[1], self.camera_position[2],
                self.camera_target[0], self.camera_target[1], self.camera_target[2],
                0.0, 1.0, 0.0
            )
            
            print("[Model Viewer] Setting up model transformation...")
            # Сохраняем текущую матрицу перед трансформациями модели
            glPushMatrix()
            
            try:
                # Базовая ориентация модели
                glRotatef(-90, 1, 0, 0)  # Поворачиваем модель, чтобы она стояла вертикально
                
                # Проверяем наличие моделей для отрисовки
                if not self.models:
                    print("[Model Viewer] No models to render")
                    return
                
                print("[Model Viewer] Rendering models...")
                # Отрисовываем каждую модель
                for model_path, position, material_info in self.models:
                    if model_path not in self.display_lists:
                        print(f"[Model Viewer] No display list for model: {model_path}")
                        continue
                    
                    display_list_id = self.display_lists[model_path]
                    if display_list_id == 0 or display_list_id is None:
                        print(f"[Model Viewer] Invalid display list ID for model: {model_path}")
                        continue
                        
                    glPushMatrix()
                    try:
                        # Применяем позицию модели
                        if position is not None:
                            glTranslatef(*position)
                            
                        # Применяем повороты модели
                        glRotatef(self.rotation[0], 1, 0, 0)
                        glRotatef(self.rotation[1], 0, 1, 0)
                        
                        # Устанавливаем материал
                        self.set_material()
                        
                        # Отрисовываем модель только если display list валиден
                        print(f"[Model Viewer] Calling display list {display_list_id} for model {model_path}")
                        glCallList(display_list_id)
                        
                    except Exception as e:
                        print(f"[Model Viewer] Error rendering model {model_path}: {str(e)}")
                        import traceback
                        traceback.print_exc()
                        
                    finally:
                        glPopMatrix()
                        
            finally:
                # Восстанавливаем матрицу после всех трансформаций
                glPopMatrix()
                
        except Exception as e:
            print(f"[Model Viewer] Error in paintGL: {str(e)}")
            import traceback
            traceback.print_exc()
            
        finally:
            # Отключаем состояния OpenGL
            glDisable(GL_LIGHTING)
            glDisable(GL_LIGHT0)

        # Настраиваем освещение
        glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
        glLightfv(GL_LIGHT1, GL_POSITION, [-0.5, 0.5, 0.2, 0.0])

        # Применяем трансформации для правильной ориентации модели
        glRotatef(-90, 1, 0, 0)  # Поворачиваем модель, чтобы она стояла вертикально
        
        # Проверяем наличие данных для отрисовки
        if not hasattr(self, 'vertices') or not hasattr(self, 'indices') or not self.vertices or not self.indices:
            print("[Model Viewer] No mesh data to render")
            return
            
        # Отрисовываем все модели в сцене
        for model_path, position, material_info in self.models:
            if model_path in self.display_lists:
                glPushMatrix()
                try:
                    # Применяем позицию если она задана
                    if position is not None:
                        glTranslatef(*position)
                    
                    # Применяем поворот модели
                    glRotatef(self.rotation[0], 1, 0, 0)  # Поворот вокруг X
                    glRotatef(self.rotation[1], 0, 1, 0)  # Поворот вокруг Y
                    
                    # Вызываем display list для отрисовки модели
                    glCallList(self.display_lists[model_path])
                except Exception as e:
                    print(f"[Model Viewer] Error rendering model {model_path}: {str(e)}")
                finally:
                    glPopMatrix()

    def load_texture(self, path):
        """Load texture from file with error handling and mipmap support."""
        try:
            if path in self.textures:
                return self.textures[path]

            print(f"[Model Viewer] Loading texture: {path}")
            image = Image.open(path)

            # Проверяем, что изображение не перевёрнуто по вертикали заранее
            if hasattr(image, 'is_flipped') and image.is_flipped:
                print(f"[Model Viewer] Warning: Image already flipped!")

            # Конвертируем в RGBA для единообразной обработки
            if image.mode != 'RGBA':
                print(f"[Model Viewer] Converting {image.mode} to RGBA")
                image = image.convert('RGBA')
            else:
                print(f"[Model Viewer] Image already in RGBA format")

            # Получаем размеры, кратные степени 2
            width = 1
            while width < image.width:
                width *= 2
            height = 1
            while height < image.height:
                height *= 2

            if width != image.width or height != image.height:
                print(f"[Model Viewer] Resizing texture to {width}x{height}")
                image = image.resize((width, height), Image.Resampling.LANCZOS)

            # Переворачиваем изображение по вертикали (OpenGL требует)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            # Помечаем, что flip был произведён
            image.is_flipped = True
            
            # Создаем текстуру OpenGL
            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            
            # Настраиваем параметры текстуры
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            
            # Загружаем данные текстуры
            img_data = image.tobytes("raw", "RGBA", 0, -1)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
            glGenerateMipmap(GL_TEXTURE_2D)
            
            # Сохраняем ID текстуры
            self.textures[path] = texture_id
            return texture_id

        except Exception as e:
            print(f"[Model Viewer] Error loading texture {path}: {str(e)}")
            return None

            # Получаем данные в формате RGBA
            img_data = image.tobytes('raw', 'RGBA', 0, -1)

            # Генерируем текстуру в OpenGL
            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)

            # Устанавливаем параметры фильтрации и wrap mode
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

            # Загружаем текстуру с поддержкой mipmap
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
            glGenerateMipmap(GL_TEXTURE_2D)

            self.textures[path] = texture_id
            print(f"[Model Viewer] Texture loaded successfully, ID: {texture_id}")
            return texture_id

        except Exception as e:
            print(f"[Model Viewer Error] Failed to load texture {path}: {e}")
            return None
            
    def load_mtl(self, mtl_path):
        """Загрузка MTL файла с поддержкой различных кодировок.
        
        Args:
            mtl_path (str): путь к MTL файлу
            
        Returns:
            dict: словарь с материалами и их текстурами
        """
        materials = {}
        base_dir = os.path.dirname(mtl_path)
        
        # Пробуем различные кодировки
        encodings = ['utf-8', 'latin1', 'cp1251']
        content = None
        
        for encoding in encodings:
            try:
                with open(mtl_path, 'r', encoding=encoding) as file:
                    content = file.readlines()
                    break
            except UnicodeDecodeError:
                continue
        
        if not content:
            print(f"[Model Viewer Error] Не удалось прочитать MTL файл: {mtl_path}")
            return materials
            
        current_material = None
        for line in content:
            try:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                    
                parts = line.split()
                if not parts:
                    continue

                if parts[0] == 'newmtl':
                    current_material = parts[1]
                    materials[current_material] = {}
                elif parts[0] == 'map_Kd' and current_material:
                    # Получаем путь к текстуре
                    texture_path = ' '.join(parts[1:])  # Поддержка пробелов в пути
                    
                    # Пробуем различные варианты путей
                    texture_variants = [
                        texture_path,  # Как есть
                        os.path.join(base_dir, texture_path),  # Относительный путь
                        os.path.abspath(texture_path)  # Абсолютный путь
                    ]
                    
                    # Пробуем найти текстуру
                    found_texture = None
                    for path in texture_variants:
                        if os.path.exists(path):
                            found_texture = path
                            break
                            
                    if found_texture:
                        try:
                            texture_id = self.load_texture(found_texture)
                            materials[current_material]['texture'] = texture_id
                        except Exception as e:
                            print(f"[Model Viewer Error] Ошибка загрузки текстуры {found_texture}: {e}")
                    else:
                        print(f"[Model Viewer Warning] Текстура не найдена: {texture_path}")
                        
            except Exception as e:
                print(f"[Model Viewer Error] Ошибка при обработке строки MTL: {e}")
                continue

        return materials
            
    def render_model(self, model, material_info=None):
        """Оптимизированный рендер модели с использованием VBO."""
        try:
            print("[Model Viewer] Starting model rendering...")
            # Проверяем тип модели
            if isinstance(model, ImprovedMDLLoader):
                if not model.vertices:
                    print("[Model Viewer] No vertices to render")
                    return
                    
                print("[Model Viewer] Preparing OpenGL state...")
                # Основные настройки OpenGL для MDL
                glEnable(GL_DEPTH_TEST)
                glEnable(GL_LIGHTING)
                glEnable(GL_LIGHT0)
                glEnable(GL_NORMALIZE)
                
                # Устанавливаем материал
                self.set_material()
                
                print("[Model Viewer] Converting vertex data...")
                # Конвертируем данные в нужный формат
                import numpy as np
                import ctypes
                
                # Создаем VBO для вершин
                vbo_vertices = glGenBuffers(1)
                glBindBuffer(GL_ARRAY_BUFFER, vbo_vertices)
                vertices = np.array(model.vertices, dtype=np.float32)
                glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
                
                # Создаем VBO для нормалей
                vbo_normals = glGenBuffers(1)
                glBindBuffer(GL_ARRAY_BUFFER, vbo_normals)
                normals = np.array([0.0, 1.0, 0.0] * (len(model.vertices) // 3), dtype=np.float32)
                glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
                
                try:
                    print("[Model Viewer] Setting up vertex arrays...")
                    # Включаем и настраиваем массивы
                    glEnableClientState(GL_VERTEX_ARRAY)
                    glEnableClientState(GL_NORMAL_ARRAY)
                    
                    # Настраиваем указатели на данные
                    glBindBuffer(GL_ARRAY_BUFFER, vbo_vertices)
                    glVertexPointer(3, GL_FLOAT, 0, None)
                    
                    glBindBuffer(GL_ARRAY_BUFFER, vbo_normals)
                    glNormalPointer(GL_FLOAT, 0, None)
                    
                    print("[Model Viewer] Drawing model...")
                    # Отрисовываем модель
                    if model.indices:
                        indices = np.array(model.indices, dtype=np.uint32)
                        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, indices)
                    else:
                        glDrawArrays(GL_TRIANGLES, 0, len(vertices) // 3)
                        
                except Exception as e:
                    print(f"[Model Viewer] Error during rendering: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    
                finally:
                    print("[Model Viewer] Cleaning up OpenGL state...")
                    # Отключаем массивы и VBO
                    glDisableClientState(GL_VERTEX_ARRAY)
                    glDisableClientState(GL_NORMAL_ARRAY)
                    
                    glBindBuffer(GL_ARRAY_BUFFER, 0)
                    glDeleteBuffers(2, [vbo_vertices, vbo_normals])
                    
                    glDisable(GL_LIGHTING)
                    glDisable(GL_NORMALIZE)
                    glDisable(GL_DEPTH_TEST)
                glDisableClientState(GL_NORMAL_ARRAY)
                return
            
            # Для остальных типов моделей
            materials = {}
            if isinstance(material_info, str) and material_info.endswith('.mtl'):
                materials = self.load_mtl(material_info)
            elif isinstance(material_info, dict):
                materials = material_info

            # Основные настройки OpenGL
            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            glEnable(GL_LIGHT1)
            glEnable(GL_DEPTH_TEST)
            glEnable(GL_NORMALIZE)

            # Оптимизированный рендеринг для каждого меша

            for mesh in model.mesh_list:
                material_name = getattr(mesh, 'material', None)
                texture_id = materials.get(material_name, {}).get('texture') if material_name else None

                if texture_id:
                    glEnable(GL_TEXTURE_2D)
                    glBindTexture(GL_TEXTURE_2D, texture_id)
                    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
                    glColor4f(1.0, 1.0, 1.0, 1.0)
                    self.set_material(color=(1.0, 1.0, 1.0, 1.0), shininess=64.0)
                else:
                    glDisable(GL_TEXTURE_2D)
                    self.set_material(self.default_model_color, shininess=32.0)

                glBegin(GL_TRIANGLES)

                has_normals = hasattr(mesh, 'normals') and mesh.normals is not None and np.size(mesh.normals) > 0
                has_texcoords = (
                    texture_id
                    and hasattr(mesh, 'tex_coords')
                    and mesh.tex_coords is not None
                    and np.size(mesh.tex_coords) > 0
                )

                for face in mesh.faces:
                    # Ensure face has at least 3 vertices (triangle)
                    if len(face) < 3:
                        continue

                    # Only use the first three indices for triangle faces
                    indices = face[:3]

                    if not has_normals:
                        try:
                            vertices = [model.vertices[i] for i in indices]
                            v1 = np.subtract(vertices[0], vertices[1])
                            v2 = np.subtract(vertices[2], vertices[0])
                            face_normal = np.cross(v1, v2)
                            norm = np.linalg.norm(face_normal)
                            if norm > 0:
                                face_normal = face_normal / norm
                                glNormal3fv(face_normal)
                        except Exception as e:
                            print(f"[Model Viewer Error] Invalid vertex index in face: {face} - {e}")
                            continue

                    for idx, vertex_index in enumerate(indices):
                        # Check index bounds for normals
                        if has_normals and vertex_index < len(mesh.normals):
                            glNormal3fv(mesh.normals[vertex_index])
                            
                        if texture_id and has_texcoords:
                            tex_coords = mesh.tex_coords
                            if vertex_index < len(tex_coords):
                                u, v = tex_coords[vertex_index]
                                glTexCoord2f(u, v)


                        # Check index bounds for vertices
                        if vertex_index < len(model.vertices):
                            glVertex3fv(model.vertices[vertex_index])
                        else:
                            print(f"[Model Viewer Warning] Vertex index {vertex_index} out of range for vertices array.")

                glEnd()

                if texture_id:
                    glDisable(GL_TEXTURE_2D)

        except Exception as e:
            print(f"[Model Viewer Error] Rendering error: {e}")
            import traceback
            print(traceback.format_exc())
    
    def set_light_params(self, ambient=None, diffuse=None, specular=None, position=None):
        """Установка параметров освещения"""
        if ambient is not None:
            glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
        if diffuse is not None:
            glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
        if specular is not None:
            glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
        if position is not None:
            glLightfv(GL_LIGHT0, GL_POSITION, position)

    def set_light_ambient(self, value):
        self.set_light_params(ambient=[value]*3+[1.0])
        self.update()

    def set_light_diffuse(self, value):
        self.set_light_params(diffuse=[value]*3+[1.0])
        self.update()

    def set_light_specular(self, value):
        self.set_light_params(specular=[value]*3+[1.0])
        self.update()

    def set_light_position(self, pos):
        self.set_light_params(position=pos)
        self.update()

    def add_model_to_scene(self, obj_file, position=(0, 0, 0), mtl_path=None, texture_path=None):
        try:
            obj_file = str(obj_file) if isinstance(obj_file, Path) else obj_file
            if not obj_file or not os.path.exists(obj_file):
                raise FileNotFoundError(f"Model file not found: {obj_file}")

            # --- Используем trimesh вместо pywavefront ---
            model = trimesh.load(obj_file, force='mesh')

            # Для совместимости с остальным кодом эмулируем pywavefront-like интерфейс
            class MeshStub:
                def __init__(self, faces, normals, tex_coords, material=None, name=None):
                    self.faces = faces
                    self.normals = normals
                    self.tex_coords = tex_coords
                    self.material = material
                    self.name = name

            # trimesh.faces — индексы, trimesh.vertices — вершины, trimesh.visual.uv — UV
            mesh_list = [MeshStub(model.faces, getattr(model, 'vertex_normals', None),
                                  getattr(model.visual, 'uv', None), material="default", name="trimesh_mesh")]
            model.mesh_list = mesh_list
            model.vertices = model.vertices

            # Центрируем камеру по Y
            if not self.models:
                y_coords = [v[1] for v in model.vertices]
                if y_coords:
                    self.camera_target[1] = sum(y_coords) / len(y_coords)

            # Создаем материал
            if texture_path and os.path.exists(str(texture_path)):
                material_info = {
                    "default": {
                        "texture": self.load_texture(str(texture_path))
                    }
                }
                for mesh in model.mesh_list:
                    mesh.material = "default"
            else:
                material_info = str(mtl_path) if mtl_path else None

            # Создаём display list для ускоренного рендера
            display_list = self.create_display_list(model, material_info)
            self.display_lists[obj_file] = display_list
            self.models.append((obj_file, position, material_info))
            self.update()
        except Exception as e:
            print(f"[Model Viewer Error] Error adding model: {e}")
            import traceback
            print(traceback.format_exc())

    def remove_model(self):
        if self.models:
            self.models.pop()
            self.update()
            #print("[Model Viewer] Сцена очищена")

    def rotate(self, delta_x, delta_y):
        self.rotation[0] -= delta_y * 0.25
        self.rotation[1] += delta_x * 0.25

        # Update camera position based on spherical coordinates
        distance = self.zoom
        theta = np.radians(self.rotation[1])
        phi = np.radians(self.rotation[0])

        self.camera_position[0] = distance * np.cos(phi) * np.sin(theta) + self.camera_target[0]
        self.camera_position[1] = distance * np.sin(phi) + self.camera_target[1]
        self.camera_position[2] = distance * np.cos(phi) * np.cos(theta) + self.camera_target[2]

        self.update()

    def zoom_camera(self, delta):
        self.zoom -= delta * 15  # Adjust zoom speed
        self.zoom = max(1.0, min(self.zoom, 500.0))  # Clamp zoom
        self.rotate(0, 0)  # Refresh camera position

    def move_camera(self, delta_x, delta_y):
        right = np.cross([0, 1, 0], np.subtract(self.camera_position, self.camera_target))
        right = right / np.linalg.norm(right)

        up = [0, 1, 0]

        self.camera_target = np.subtract(self.camera_target, np.multiply(right, delta_x * 0.1))
        self.camera_target = np.subtract(self.camera_target, np.multiply(up, delta_y * 0.1))
        self.rotate(0, 0)  # Refresh camera position

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.last_mouse_position = event.position()
        elif event.button() == Qt.MouseButton.LeftButton:
            self.last_mouse_position = event.position()

    def mouseMoveEvent(self, event):
        if self.last_mouse_position is not None:
            delta = event.position() - self.last_mouse_position

            if event.buttons() == Qt.MouseButton.LeftButton:
                if self.is_shift_pressed:
                    self.move_camera(delta.x(), -delta.y())
                else:
                    self.rotate(-delta.x(), -delta.y())
            elif event.buttons() == Qt.MouseButton.RightButton:
                self.zoom_camera(-delta.y() / 120.0)  # Zoom based on vertical mouse movement

            self.last_mouse_position = event.position()

    def mouseReleaseEvent(self, event):
        if event.button() in (Qt.MouseButton.RightButton, Qt.MouseButton.LeftButton):
            self.last_mouse_position = None
        self.is_shift_pressed = False

    def wheelEvent(self, event):
        pass  # Disable wheel-based zoom
    
    def create_new_model(self, model_path, texture_path=None, mtl_path=None):
        """Create a new model, replacing any existing ones.
        Args:
            model_path (str or Path): путь к .obj файлу
            texture_path (str or Path, optional): путь к текстуре или .mtl файлу
            mtl_path (str or Path, optional): путь к MTL файлу
        """
        print(f"[Model Viewer] Attempting to create new model:")
        print(f"[Model Viewer] - Model path: {model_path}")
        print(f"[Model Viewer] - Texture path: {texture_path}")
        print(f"[Model Viewer] - MTL path: {mtl_path}")
        
        self.remove_model()
        
        # Преобразуем Path в str, если нужно
        model_path = str(model_path) if isinstance(model_path, Path) else model_path
        texture_path = str(texture_path) if isinstance(texture_path, Path) and texture_path is not None else texture_path
        
        if not os.path.exists(model_path):
            print(f"[Model Viewer Error] Model file not found: {model_path}")
            return
            
        print(f"[Model Viewer] Model file exists, checking format...")
        
        # Проверяем расширение файла
        extension = os.path.splitext(model_path)[1].lower()
        if extension == '.mdl':
            try:
                print(f"[Model Viewer] Loading MDL file: {model_path}")
                mdl_loader = ImprovedMDLLoader()
                if mdl_loader.load_mdl(model_path):
                    print(f"[Model Viewer] MDL file loaded, checking data...")
                    print(f"  - Vertices: {len(mdl_loader.vertices)}")
                    print(f"  - Indices: {len(mdl_loader.indices)}")
                    
                    # Проверяем что у нас есть данные для рендеринга
                    if not mdl_loader.vertices or not mdl_loader.indices:
                        print("[Model Viewer] Warning: No geometry data in MDL model")
                        return False
                    
                    # Если модель успешно загружена
                    position = (0, 0, 0)
                    
                    # Создаем display list для оптимизации рендеринга
                    print("[Model Viewer] Creating display list...")
                    display_list_id = self.create_display_list(mdl_loader, None)
                    
                    if display_list_id == 0:
                        print("[Model Viewer] Error: Failed to create display list")
                        return False
                    
                    # Сохраняем загруженную модель
                    self.mdl_loader = mdl_loader  # Сохраняем загрузчик
                    self.display_lists[model_path] = display_list_id
                    self.models.append((model_path, position, None))
                    
                    print(f"[Model Viewer] Successfully loaded MDL model: {model_path}")
                    print(f"  - Display list ID: {display_list_id}")
                    print(f"  - Models in scene: {len(self.models)}")
                    
                    # Обновляем отображение
                    self.vertices = mdl_loader.vertices
                    self.indices = mdl_loader.indices
                    self.update()
                    return True
                else:
                    print(f"[Model Viewer Error] Failed to load MDL model")
                    return False
            except Exception as e:
                print(f"[Model Viewer Error] Error loading MDL model: {e}")
                import traceback
                traceback.print_exc()
                return False
            
        if os.path.exists(model_path):
            # Определяем тип файла текстуры по расширению
            if texture_path and os.path.exists(texture_path):
                ext = os.path.splitext(texture_path)[1].lower()
                print(f"[Model Viewer] Found texture with extension: {ext}")
                if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tga']:
                    print(f"[Model Viewer] Loading model with texture: {texture_path}")
                    self.add_model(model_path, position=(0, 10, 0), texture_path=texture_path, mtl_path=mtl_path)
                elif ext == '.mtl':
                    print(f"[Model Viewer] Loading model with MTL: {texture_path}")
                    self.add_model(model_path, position=(0, 10, 0), mtl_path=texture_path)
            else:
                if texture_path:
                    print(f"[Model Viewer] Warning: Texture file not found: {texture_path}")
                print(f"[Model Viewer] Loading model without texture")
                self.add_model(model_path, position=(0, 10, 0), mtl_path=mtl_path)
        else:
            print(f"[Model Viewer Error] Model not found: {model_path}")

    def add_model(self, model_path, texture_path=None, mtl_path = None, position=(0, 10, 0)):
        """Add a cosmetic model on top of existing ones.
        Args:
            model_path (str): путь к .obj файлу
            texture_path (str): путь к текстуре или .mtl файлу
        """
        if os.path.exists(model_path):
            self.add_model_to_scene(model_path, 
                                    position = position,
                                    mtl_path=mtl_path, 
                                    texture_path=texture_path)
    def create_vbo(self, data, target=GL_ARRAY_BUFFER):
        """Создает VBO из данных numpy array."""
        try:
            buffer_id = glGenBuffers(1)
            glBindBuffer(target, buffer_id)
            glBufferData(target, data.nbytes, data, GL_STATIC_DRAW)
            glBindBuffer(target, 0)
            return buffer_id
        except Exception as e:
            print(f"[Model Viewer] Error creating VBO: {str(e)}")
            return 0
            
    def create_display_list(self, model, material_info):
        """Создание display list для оптимизированного рендеринга."""
        try:
            print("[Model Viewer] Creating display list...")
            
            # Проверяем тип модели и наличие данных
            if isinstance(model, ImprovedMDLLoader):
                # Обработка MDL модели
                print(f"[Model Viewer] Processing MDL model...")
                print(f"  - Vertex count: {len(model.vertices) // 3}")
                print(f"  - Index count: {len(model.indices)}")
                print(f"  - Triangle count: {len(model.indices) // 3}")
                
                if not model.vertices:
                    print("[Model Viewer] Error: No vertex data in MDL model")
                    return 0
                    
                if not model.indices:
                    print("[Model Viewer] Error: No index data in MDL model")
                    return 0
                
                # Проверяем корректность индексов
                max_vertex_index = max(model.indices) if model.indices else -1
                vertex_count = len(model.vertices) // 3
                print(f"  - Max vertex index: {max_vertex_index}")
                print(f"  - Available vertices: {vertex_count}")
                
                if max_vertex_index >= vertex_count:
                    print(f"[Model Viewer] Error: Index out of range detected!")
                    return 0
                
                return self._create_mdl_display_list(model, material_info)
                
            else:
                # Обработка других типов моделей (OBJ, etc.)
                print(f"[Model Viewer] Processing non-MDL model...")
                if not hasattr(model, 'vertices') or not model.vertices:
                    print("[Model Viewer] Error: No vertex data in model")
                    return 0
                
                return self._create_generic_display_list(model, material_info)
                
        except Exception as e:
            print(f"[Model Viewer] Error creating display list: {str(e)}")
            import traceback
            traceback.print_exc()
            return 0
    
    def _create_mdl_display_list(self, model, material_info):
        """Создает display list для MDL модели"""
        try:
            # Создаем новый display list
            display_list = glGenLists(1)
            if display_list == 0:
                print("[Model Viewer] Error: Could not create display list")
                return 0
                
            print(f"[Model Viewer] Generated MDL display list ID: {display_list}")
            
            # Начинаем компиляцию display list
            glNewList(display_list, GL_COMPILE)
            
            try:
                # Сохраняем состояние OpenGL
                glPushAttrib(GL_ALL_ATTRIB_BITS)
                
                # Включаем нужные состояния OpenGL
                glEnable(GL_LIGHTING)
                glEnable(GL_LIGHT0)
                glEnable(GL_DEPTH_TEST)
                glEnable(GL_NORMALIZE)
                
                # Устанавливаем режим плоского затенения
                glShadeModel(GL_FLAT)
                
                # Устанавливаем материал
                if material_info:
                    self.set_material(material_info.get('color'))
                else:
                    self.set_material()
                
                print(f"[Model Viewer] Compiling {len(model.indices) // 3} triangles...")
                
                # Конвертируем вершины и индексы в numpy массивы для удобства
                import numpy as np
                vertices = np.array(model.vertices, dtype=np.float32).reshape(-1, 3)
                indices = np.array(model.indices, dtype=np.uint32)
                
                # Начинаем отрисовку треугольников
                glBegin(GL_TRIANGLES)
                try:
                    for i in range(0, len(indices), 3):
                        if i + 2 >= len(indices):
                            break
                            
                        # Получаем индексы вершин
                        idx1, idx2, idx3 = indices[i], indices[i + 1], indices[i + 2]
                        
                        # Проверяем валидность индексов
                        if idx1 >= len(vertices) or idx2 >= len(vertices) or idx3 >= len(vertices):
                            continue
                            
                        # Получаем вершины треугольника
                        v1 = vertices[idx1]
                        v2 = vertices[idx2]
                        v3 = vertices[idx3]
                        
                        # Вычисляем нормаль для треугольника
                        edge1 = v2 - v1
                        edge2 = v3 - v1
                        normal = np.cross(edge1, edge2)
                        norm = np.linalg.norm(normal)
                        if norm > 1e-6:
                            normal = normal / norm
                        else:
                            normal = np.array([0.0, 1.0, 0.0])
                        
                        # Устанавливаем нормаль один раз для всего треугольника
                        glNormal3f(*normal)
                        
                        # Отрисовываем вершины треугольника
                        glVertex3f(*v1)
                        glVertex3f(*v2)
                        glVertex3f(*v3)
                        
                except Exception as e:
                    print(f"[Model Viewer] Error rendering triangle: {str(e)}")
                finally:
                    glEnd()
                    
            finally:
                # Восстанавливаем состояние OpenGL
                glPopAttrib()
                # Завершаем компиляцию display list
                glEndList()
                
            print(f"[Model Viewer] MDL display list {display_list} compilation completed successfully")
            return display_list
            
        except Exception as e:
            print(f"[Model Viewer] Error creating MDL display list: {str(e)}")
            import traceback
            traceback.print_exc()
            if 'display_list' in locals() and display_list != 0:
                try:
                    glDeleteLists(display_list, 1)
                except:
                    pass
            return 0
    
    def _create_generic_display_list(self, model, material_info):
        """Создает display list для обычных моделей (OBJ, etc.)"""
        try:
            # Создаем новый display list
            display_list = glGenLists(1)
            if display_list == 0:
                print("[Model Viewer] Error: Could not create generic display list")
                return 0
                
            print(f"[Model Viewer] Generated generic display list ID: {display_list}")
            
            # Начинаем компиляцию display list
            glNewList(display_list, GL_COMPILE)
            
            try:
                # Рендерим модель используя существующий метод
                self.render_model(model, material_info)
                    
            finally:
                # Завершаем компиляцию display list
                glEndList()
                
            print(f"[Model Viewer] Generic display list {display_list} compilation completed successfully")
            return display_list
            
        except Exception as e:
            print(f"[Model Viewer] Error creating generic display list: {str(e)}")
            import traceback
            traceback.print_exc()
            if 'display_list' in locals() and display_list != 0:
                try:
                    glDeleteLists(display_list, 1)
                except:
                    pass
            return 0