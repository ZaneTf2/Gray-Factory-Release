from pathlib import Path
from typing import Dict, Optional, Tuple
import numpy as np
from PIL import Image
from ..events.event_system import EventSystem, Event, EventType
from .vpk_loader import VPKAssetLoader

class TextureManager:
    """Управление текстурами"""
    
    def __init__(self, event_system: EventSystem, asset_loader: VPKAssetLoader):
        self.event_system = event_system
        self.asset_loader = asset_loader
        self.textures: Dict[str, int] = {}  # путь -> id текстуры OpenGL
        self.temp_dir = Path("temp_textures")
        self.temp_dir.mkdir(exist_ok=True)
        
    def load_texture(self, texture_path: str) -> Optional[int]:
        """
        Загрузка текстуры из VPK
        
        Args:
            texture_path: Путь к текстуре в VPK
            
        Returns:
            Optional[int]: ID текстуры в OpenGL или None в случае ошибки
        """
        try:
            # Проверяем, загружена ли уже текстура
            if texture_path in self.textures:
                return self.textures[texture_path]
                
            # Извлекаем текстуру во временную директорию
            extracted_path = self.asset_loader.extract_file(texture_path, str(self.temp_dir))
            if not extracted_path:
                print(f"Не удалось извлечь текстуру: {texture_path}")
                return None
                
            # Загружаем текстуру
            texture_id = self._load_texture_file(extracted_path)
            if texture_id:
                self.textures[texture_path] = texture_id
                
                # Оповещаем о загрузке текстуры
                self.event_system.emit(Event(
                    EventType.TEXTURE_CHANGED,
                    {"texture_path": texture_path}
                ))
                
            return texture_id
            
        except Exception as e:
            print(f"Ошибка при загрузке текстуры {texture_path}: {str(e)}")
            return None
            
    def _load_texture_file(self, file_path: str) -> Optional[int]:
        """
        Загрузка текстуры в OpenGL
        
        Args:
            file_path: Путь к файлу текстуры
            
        Returns:
            Optional[int]: ID текстуры в OpenGL или None в случае ошибки
        """
        from OpenGL.GL import (
            glGenTextures, glBindTexture, glTexImage2D, glTexParameteri,
            GL_TEXTURE_2D, GL_RGBA, GL_UNSIGNED_BYTE,
            GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER, GL_LINEAR,
            GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_REPEAT
        )
        
        try:
            # Загружаем изображение через PIL
            image = Image.open(file_path)
            image = image.convert("RGBA")
            
            # Создаем текстуру в OpenGL
            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            
            # Устанавливаем параметры текстуры
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            
            # Загружаем данные текстуры
            glTexImage2D(
                GL_TEXTURE_2D,
                0,
                GL_RGBA,
                image.width,
                image.height,
                0,
                GL_RGBA,
                GL_UNSIGNED_BYTE,
                image.tobytes()
            )
            
            return texture_id
            
        except Exception as e:
            print(f"Ошибка при создании текстуры из {file_path}: {str(e)}")
            return None
            
    def cleanup(self) -> None:
        """Очистка временных файлов и текстур OpenGL"""
        from OpenGL.GL import glDeleteTextures
        
        # Удаляем текстуры из OpenGL
        for texture_id in self.textures.values():
            glDeleteTextures(1, [texture_id])
        self.textures.clear()
        
        # Удаляем временные файлы
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
