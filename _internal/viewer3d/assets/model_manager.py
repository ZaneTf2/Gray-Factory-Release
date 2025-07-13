import os
import ctypes
import logging
import traceback
import numpy as np
from pathlib import Path
from typing import Dict, Optional
from OpenGL import GL as gl
from .mdl_converter import MDLConverter

logger = logging.getLogger(__name__)

class Model:
    """Представляет 3D модель в памяти OpenGL"""
    def __init__(self, vao: int, vbo: int, ebo: int, vertex_count: int, vertices: np.ndarray, indices: np.ndarray, material_paths: list):
        self.vao = vao
        self.vbo = vbo
        self.ebo = ebo
        self.vertex_count = vertex_count
        self.vertices = vertices
        self.indices = indices
        self.material_paths = material_paths

class ModelManager:
    """Менеджер для загрузки и управления 3D моделями"""
    def __init__(self):
        self.models: Dict[str, Model] = {}
        self.current_model: Optional[Model] = None
        self.temp_dir = Path("temp_models")
        self.temp_dir.mkdir(exist_ok=True)
        self.converter = MDLConverter()
        
    def load_model_from_file(self, model_path: str) -> Optional[Model]:
        """Загружает модель напрямую из файла, используя MDLConverter
        
        Args:
            model_path: Путь к файлу модели на диске
            
        Returns:
            Model: Загруженная модель или None в случае ошибки
        """
        try:
            logger.info(f"Загрузка модели из файла через MDLConverter: {model_path}")
            
            # Проверяем существование файла
            if not os.path.exists(model_path):
                logger.error(f"Файл не найден: {model_path}")
                return None
                
            # Загружаем модель через MDLConverter
            vertices, indices, materials = self.converter.convert_mdl(model_path)
            
            if vertices is None or indices is None:
                logger.error(f"Не удалось сконвертировать модель: {model_path}")
                return None
            
            # Создаем буферы OpenGL
            vao = gl.glGenVertexArrays(1)
            gl.glBindVertexArray(vao)
            
            # VBO для вершин
            vbo = gl.glGenBuffers(1)
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
            gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW)
            
            # Позиции вершин (XYZ)
            gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, False, 32, ctypes.c_void_p(0))
            gl.glEnableVertexAttribArray(0)
            
            # Нормали (XYZ)
            gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, False, 32, ctypes.c_void_p(12))
            gl.glEnableVertexAttribArray(1)
            
            # UV координаты (UV)
            gl.glVertexAttribPointer(2, 2, gl.GL_FLOAT, False, 32, ctypes.c_void_p(24))
            gl.glEnableVertexAttribArray(2)
            
            # EBO для индексов
            ebo = gl.glGenBuffers(1)
            gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo)
            gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, gl.GL_STATIC_DRAW)
            
            # Создаем модель
            model = Model(vao, vbo, ebo, len(indices), vertices, indices, materials)
            self.models[model_path] = model
            return model
            
        except Exception as e:
            logger.error(f"Ошибка при загрузке модели {model_path}: {str(e)}")
            logger.error(traceback.format_exc())
            return None
            
    def set_current_model(self, model_path: str) -> bool:
        """Устанавливает текущую активную модель
        
        Args:
            model_path: Путь к файлу модели
            
        Returns:
            bool: True если модель успешно установлена
        """
        if model_path in self.models:
            self.current_model = self.models[model_path]
            return True
        return False
        
    def draw_current_model(self):
        """Отрисовывает текущую активную модель"""
        if self.current_model:
            gl.glBindVertexArray(self.current_model.vao)
            gl.glDrawElements(gl.GL_TRIANGLES, self.current_model.vertex_count, gl.GL_UNSIGNED_INT, None)
            gl.glBindVertexArray(0)
