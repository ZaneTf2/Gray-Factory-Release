import os
import logging
import traceback
from typing import Optional
import ctypes
import numpy as np
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QWheelEvent, QSurfaceFormat
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

from ..events.event_system import EventSystem, Event
from ..components.camera import Camera
from ..components.light import LightManager
from ..assets.vpk_loader import VPKAssetLoader
from ..assets.model_manager import ModelManager
from ..assets.texture_manager import TextureManager

logger = logging.getLogger(__name__)

class TF2GLViewer(QOpenGLWidget):
    """Виджет для отображения 3D моделей из Team Fortress 2"""
    
    # Сигналы
    modelLoaded = pyqtSignal(str)  # Сигнал о загрузке модели
    textureChanged = pyqtSignal(str)  # Сигнал о смене текстуры
    
    def __init__(self, parent=None):
        # Устанавливаем формат OpenGL до инициализации
        format = QSurfaceFormat()
        format.setDepthBufferSize(24)
        format.setStencilBufferSize(8)
        format.setVersion(3, 3)  # Используем OpenGL 3.3
        format.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
        QSurfaceFormat.setDefaultFormat(format)
        
        super().__init__(parent)
        
        # Инициализация систем
        self.event_system = EventSystem()
        self.camera = Camera(self.event_system)
        self.light_manager = LightManager(self.event_system)
        
        # Цвет модели по умолчанию (белый)
        self.current_model_color = (1.0, 1.0, 1.0)
        
        # Ресурсы OpenGL
        self.vao = None
        self.vbo = None
        self.ibo = None
        self.current_texture = None
        
        # Данные модели
        self.current_model = None
        self.vertex_count = 0
        self.index_count = 0
        self.materials = None
        self.bones = None
        
        # Инициализация загрузчиков ресурсов
        self.asset_loader = VPKAssetLoader(self.event_system)
        self.model_manager = ModelManager()
        self.texture_manager = TextureManager(self.event_system, self.asset_loader)
        
    def initializeGL(self):
        """Инициализация OpenGL"""
        try:
            logger.debug("Инициализация OpenGL контекста...")
            
            # Проверка поддержки OpenGL 3.3
            gl_version = glGetString(GL_VERSION).decode('utf-8')
            logger.info(f"OpenGL версия: {gl_version}")
            
            if not gl_version.startswith("3.3"):
                logger.warning(f"Требуется OpenGL 3.3+, текущая версия: {gl_version}")
                
            # Основные настройки OpenGL
            glClearColor(0.2, 0.2, 0.2, 1.0)
            glEnable(GL_DEPTH_TEST)
            glEnable(GL_CULL_FACE)
            glCullFace(GL_BACK)
            
            # Инициализация шейдеров
            if not self.init_shaders():
                raise RuntimeError("Ошибка инициализации шейдеров")
                
            logger.debug("OpenGL контекст инициализирован успешно")
            
        except Exception as e:
            logger.error(f"Ошибка при инициализации OpenGL: {str(e)}")
            logger.error(traceback.format_exc())
            raise
        
    def init_shaders(self):
        """Инициализация шейдеров"""
        try:
            # Vertex shader
            vertex_shader_src = """
            #version 330 core
            layout (location = 0) in vec3 position;
            layout (location = 1) in vec3 normal;
            layout (location = 2) in vec2 texCoord;
            uniform mat4 model;
            uniform mat4 view;
            uniform mat4 projection;
            out vec3 FragPos;
            out vec3 Normal;
            out vec2 TexCoord;
            void main() {
                FragPos = vec3(model * vec4(position, 1.0));
                Normal = mat3(transpose(inverse(model))) * normal;
                TexCoord = texCoord;
                gl_Position = projection * view * model * vec4(position, 1.0);
            }
            """
            fragment_shader_src = """
            #version 330 core
            in vec3 FragPos;
            in vec3 Normal;
            in vec2 TexCoord;
            out vec4 FragColor;
            uniform vec3 modelColor;
            void main() {
                FragColor = vec4(modelColor, 1.0);
            }
            """
            # Компиляция вершинного шейдера
            vertex_shader = glCreateShader(GL_VERTEX_SHADER)
            glShaderSource(vertex_shader, vertex_shader_src)
            glCompileShader(vertex_shader)
            success = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS)
            if not success:
                info_log = glGetShaderInfoLog(vertex_shader).decode()
                logger.error(f"Ошибка компиляции вершинного шейдера:\n{info_log}")
                return False
            # Компиляция фрагментного шейдера
            fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
            glShaderSource(fragment_shader, fragment_shader_src)
            glCompileShader(fragment_shader)
            success = glGetShaderiv(fragment_shader, GL_COMPILE_STATUS)
            if not success:
                info_log = glGetShaderInfoLog(fragment_shader).decode()
                logger.error(f"Ошибка компиляции фрагментного шейдера:\n{info_log}")
                return False
            # Линковка программы
            shader_program = glCreateProgram()
            glAttachShader(shader_program, vertex_shader)
            glAttachShader(shader_program, fragment_shader)
            glLinkProgram(shader_program)
            success = glGetProgramiv(shader_program, GL_LINK_STATUS)
            if not success:
                info_log = glGetProgramInfoLog(shader_program).decode()
                logger.error(f"Ошибка линковки шейдерной программы:\n{info_log}")
                return False
            # Удаляем шейдеры после линковки
            glDeleteShader(vertex_shader)
            glDeleteShader(fragment_shader)
            self.shader_program = shader_program
            logger.info("Шейдеры успешно скомпилированы и залинкованы.")
            return True
        except Exception as e:
            logger.error(f"Ошибка при инициализации шейдеров: {str(e)}")
            logger.error(traceback.format_exc())
            return False
        
    def cleanup_gl_resources(self):
        """Очистка ресурсов OpenGL"""
        self.makeCurrent()
        
        if self.vao:
            glDeleteVertexArrays(1, [self.vao])
            self.vao = None
            
        if self.vbo:
            glDeleteBuffers(1, [self.vbo])
            self.vbo = None
            
        if self.ibo:
            glDeleteBuffers(1, [self.ibo])
            self.ibo = None
            
        if self.current_texture:
            glDeleteTextures([self.current_texture])
            self.current_texture = None
            
        self.doneCurrent()
        
    def closeEvent(self, event):
        """Очистка при закрытии виджета"""
        self.cleanup_gl_resources()
        super().closeEvent(event)
        
    def resizeGL(self, width: int, height: int):
        """Обработка изменения размера окна"""
        glViewport(0, 0, width, height)
        aspect = width / height if height > 0 else 1.0
        self.camera.state.aspect = aspect
        
    def paintGL(self):
        """Отрисовка сцены"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Если нет модели, не рендерим
        if not self.current_model:
            return
            
        # Устанавливаем матрицы камеры
        self.camera.apply()
        
        # Настраиваем освещение
        self.light_manager.apply()
        
        # Биндим VAO для рендеринга
        glBindVertexArray(self.vao)
        
        # Если есть текстуры, используем их
        if self.materials and hasattr(self, 'current_texture'):
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.current_texture)
        else:
            # Иначе используем цвет команды
            glDisable(GL_TEXTURE_2D)
            glColor3f(*self.current_model_color)
        
        # Рендерим модель
        glDrawElements(GL_TRIANGLES, self.index_count, GL_UNSIGNED_INT, None)
        
        # Сбрасываем состояние
        glBindVertexArray(0)
        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)
        
    def mousePressEvent(self, event: QMouseEvent):
        """Обработка нажатия кнопки мыши"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._mouse_pressed = True
            self._last_pos = event.pos()
            
    def mouseReleaseEvent(self, event: QMouseEvent):
        """Обработка отпускания кнопки мыши"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._mouse_pressed = False
            
    def mouseMoveEvent(self, event: QMouseEvent):
        """Обработка движения мыши"""
        if self._mouse_pressed and self._last_pos:
            dx = event.pos().x() - self._last_pos.x()
            dy = event.pos().y() - self._last_pos.y()
            self.camera.orbit(dx, dy)
            self.update()
            self._last_pos = event.pos()
            
    def wheelEvent(self, event: QWheelEvent):
        """Обработка прокрутки колеса мыши"""
        delta = event.angleDelta().y() / 120.0
        self.camera.zoom(-delta)
        self.update()
        
    def load_model(self, model_path: str) -> bool:
        """Загрузка модели из VPK"""
        try:
            logger.info(f"=== Загрузка модели: {model_path} ===")
            
            # 1. Извлекаем модель из VPK
            temp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp")
            os.makedirs(temp_dir, exist_ok=True)
            
            extracted_path = self.asset_loader.extract_file(model_path, temp_dir)
            if not extracted_path:
                logger.error(f"Не удалось извлечь модель: {model_path}")
                return False
                
            logger.info(f"Модель извлечена в: {extracted_path}")
            
            # 2. Загружаем модель
            logger.info("Начинаем загрузку модели в OpenGL")
            self.current_model = self.model_manager.load_model(extracted_path)
            
            if not self.current_model:
                logger.error("Не удалось загрузить модель в OpenGL")
                return False
            
            # 3. Обновляем отображение
            self.update()
            self.modelLoaded.emit(model_path)
            logger.info("Модель успешно загружена")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при загрузке модели: {str(e)}")
            logger.error(traceback.format_exc())
            return False
        
    def load_extracted_model(self, model_path: str) -> bool:
        """Загружает уже извлеченную модель из файловой системы
        
        Args:
            model_path: Путь к извлеченной модели на диске
            
        Returns:
            bool: True если загрузка успешна, False в случае ошибки
        """
        try:
            logger.info(f"Загрузка извлеченной модели: {model_path}")
            
            if not os.path.exists(model_path):
                logger.error(f"Файл модели не найден: {model_path}")
                return False
                
            # Загружаем модель через ModelManager
            self.current_model = self.model_manager.load_model_from_file(model_path)
            
            if self.current_model is None:
                logger.error("ModelManager вернул None")
                return False
                
            logger.info("Модель успешно загружена")
            self.update()  # Обновляем отрисовку
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при загрузке модели: {str(e)}")
            logger.error(traceback.format_exc())
            return False
        
    def set_texture_variant(self, variant: str) -> None:
        """
        Установка варианта текстуры (red/blue)
        
        Args:
            variant: Вариант текстуры ('red' или 'blue')
        """
        model = self.model_manager.get_current_model()
        if model and "diffuse" in model.textures:
            current_texture = model.textures["diffuse"]
            new_texture = current_texture.replace("_red", f"_{variant}").replace("_blue", f"_{variant}")
            if new_texture != current_texture:
                model.textures["diffuse"] = new_texture
                self.update()
                
    def set_model_color(self, color) -> None:
        """Установка цвета модели"""
        logger.info(f"Установка цвета модели: {color}")
        self.current_model_color = color
        self.update()  # Запрос перерисовки
        
    def set_model_data(self, vertices: np.ndarray, indices: np.ndarray, 
                      materials: list, bones: Optional[list] = None) -> bool:
        """
        Устанавливает данные модели для отображения
        
        Args:
            vertices (np.ndarray): Вершины модели [x,y,z, nx,ny,nz, u,v]
            indices (np.ndarray): Индексы для рендеринга треугольников
            materials (list): Список материалов модели
            bones (Optional[list]): Список костей для анимации
            
        Returns:
            bool: True если данные успешно установлены
        """
        try:
            logger.info("Установка данных модели")
            
            # Очищаем старые ресурсы
            self.cleanup()
            
            # Конвертируем данные в нужный формат если нужно
            if not vertices.flags['C_CONTIGUOUS']:
                vertices = np.ascontiguousarray(vertices, dtype=np.float32)
            if not indices.flags['C_CONTIGUOUS']:
                indices = np.ascontiguousarray(indices, dtype=np.uint32)
            
            # Подготавливаем OpenGL буферы
            self.makeCurrent()
            
            # Создаем VAO
            self.vao = glGenVertexArrays(1)
            glBindVertexArray(self.vao)
            
            # VBO для вершин
            self.vbo = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
            glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
            
            # Позиции (x,y,z)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, None)
            glEnableVertexAttribArray(0)
            
            # Нормали (nx,ny,nz)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
            glEnableVertexAttribArray(1)
            
            # UV координаты (u,v)
            glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))
            glEnableVertexAttribArray(2)
            
            # IBO для индексов
            self.ibo = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ibo)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
            
            # Сохраняем данные
            self.vertex_count = len(vertices)
            self.index_count = len(indices)
            self.materials = materials
            self.bones = bones
            
            # Сбрасываем биндинги
            glBindVertexArray(0)
            glBindBuffer(GL_ARRAY_BUFFER, 0)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
            
            logger.info(f"Данные модели установлены: {self.vertex_count} вершин, {self.index_count} индексов")
            
            # Обновляем отображение
            self.current_model = True
            self.update()
            
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при установке данных модели: {str(e)}")
            logger.error(traceback.format_exc())
            return False
        
    def _on_model_loaded(self, event: Event):
        """Обработчик события загрузки модели"""
        self.modelLoaded.emit(event.data["model_path"])
        self.update()
        
    def _on_texture_changed(self, event: Event):
        """Обработчик события изменения текстуры"""
        self.textureChanged.emit(event.data["texture_path"])
        self.update()
        
    def cleanup(self):
        """Освобождаем ресурсы OpenGL"""
        self.makeCurrent()
        
        if self.vao:
            glDeleteVertexArrays(1, [self.vao])
            self.vao = None
            
        if self.vbo:
            glDeleteBuffers(1, [self.vbo])
            self.vbo = None
            
        if self.ibo:
            glDeleteBuffers(1, [self.ibo])
            self.ibo = None
            
        if self.current_texture:
            glDeleteTextures([self.current_texture])
            self.current_texture = None
            
        logger.info("OpenGL ресурсы освобождены")
        
    def __del__(self):
        """Деструктор"""
        self.cleanup()
