from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt
from PIL import Image

from pathlib import Path
import numpy as np
import os
import trimesh

class ModelViewer(QOpenGLWidget):
    def __init__(self, parent=None):
        super(ModelViewer, self).__init__(parent)
        self.models = []  # List to hold loaded models
        self.textures = {}  # Dictionary to hold textures
        self.display_lists = {}  # Кэш для display lists
        self.rotation = [0, 0]  # Rotation angles for the model
        self.zoom = 120  # Camera distance from the center
        self.camera_target = [0, 0, 0]  # The point camera is looking at
        self.camera_position = [0, 50, self.zoom]  # Initial camera position
        self.last_mouse_position = None  # Track last mouse position for dragging
        self.background_color = (0.15, 0.15, 0.15, 1)  # Default background color
        self.is_shift_pressed = False  # Track if Shift is pressed
        # Добавляем стандартный цвет модели
        self.default_model_color = (0.7, 0.7, 0.7, 1.0)  # Светло-серый
        
    def initializeGL(self):
        """Инициализация OpenGL с улучшенными настройками освещения."""
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
        print("[Model Viewer] OpenGL initialized with enhanced lighting and material settings.")
        
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
        """Отрисовка сцены с использованием display lists (ускоренный рендер)"""
        glClearColor(*self.background_color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        gluLookAt(
            *self.camera_position,
            *self.camera_target,
            0, 1, 0
        )

        glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
        glLightfv(GL_LIGHT1, GL_POSITION, [-0.5, 0.5, 0.2, 0.0])

        for model_path, position, material_info in self.models:
            if model_path in self.display_lists:
                glPushMatrix()
                glTranslatef(*position)
                glCallList(self.display_lists[model_path])
                glPopMatrix()

    def load_texture(self, path):
        """Загрузка текстуры с оптимизацией и поддержкой всех форматов. Проверка RGBA и однократный flip."""
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
            #image = image.transpose(Image.FLIP_TOP_BOTTOM)
            # Помечаем, что flip был произведён
            image.is_flipped = True

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
        """Оптимизированный рендер модели с использованием VBO и дисплейных списков."""
        try:
            # Загружаем материалы
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
            print(f"[Model Viewer] Warning: MDL format detected. This format is not directly supported.")
            return
            
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
    def create_display_list(self, model, material_info):
        """Создание display list для оптимизированного рендеринга."""
        display_list = glGenLists(1)
        glNewList(display_list, GL_COMPILE)
        self.render_model(model, material_info)
        glEndList()
        return display_list

