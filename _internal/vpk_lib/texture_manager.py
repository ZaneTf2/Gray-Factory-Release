import os
from typing import Dict, List, Optional
from pathlib import Path
from PIL import Image

from vtf2img_lib.parser import Parser as VTFParser
from .exceptions import VPKError

class TextureManager:
    """Управляет извлечением и конвертацией текстур из VPK"""
    
    def __init__(self, vpk_reader, output_dir: str):
        """
        Инициализирует менеджер текстур
        
        Args:
            vpk_reader: Экземпляр VPKReader для доступа к архиву
            output_dir: Директория для сохранения извлеченных текстур
        """
        self.vpk = vpk_reader
        self.output_dir = Path(output_dir)
        self.texture_cache: Dict[str, str] = {}  # Кэш путей к сконвертированным текстурам
        
    def convert_vtf(self, vtf_path: str, output_path: str) -> Optional[str]:
        """
        Конвертирует VTF файл в PNG
        
        Args:
            vtf_path: Путь к VTF файлу
            output_path: Путь для сохранения PNG
            
        Returns:
            Optional[str]: Путь к сконвертированному файлу или None при ошибке
        """
        try:
            # Убеждаемся что директория существует
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Конвертируем VTF в PNG
            parser = VTFParser(vtf_path)
            image = parser.get_image()
            
            # Сохраняем PNG
            image.save(output_path, 'PNG')
            
            return output_path
            
        except Exception as e:
            print(f"Error converting texture {vtf_path}: {e}")
            return None
            
    def find_model_textures(self, model_pattern: str) -> List[str]:
        """
        Ищет текстуры для заданного паттерна моделей
        
        Args:
            model_pattern: Паттерн моделей (например, "models/bots/**/*.mdl")
            
        Returns:
            List[str]: Список найденных путей к текстурам
        """
        # Преобразуем паттерн моделей в паттерн текстур
        # models/bots/foo.mdl -> materials/models/bots/foo/*.vtf
        texture_pattern = model_pattern.replace('models/', 'materials/models/')
        texture_pattern = str(Path(texture_pattern).parent / '*.vtf')
        
        return list(self.vpk.find_files(texture_pattern))
        
    def extract_and_convert_texture(self, vtf_path: str) -> Optional[str]:
        """
        Извлекает и конвертирует текстуру
        
        Args:
            vtf_path: Путь к текстуре в VPK
            
        Returns:
            Optional[str]: Путь к сконвертированной текстуре или None при ошибке
        """
        # Проверяем кэш
        if vtf_path in self.texture_cache:
            return self.texture_cache[vtf_path]
            
        try:
            # Создаем временный путь для VTF
            temp_vtf = str(self.output_dir / 'temp' / vtf_path)
            os.makedirs(os.path.dirname(temp_vtf), exist_ok=True)
            
            # Извлекаем VTF
            self.vpk.extract_file(vtf_path, temp_vtf)
            
            # Определяем путь для PNG
            png_path = str(self.output_dir / vtf_path).replace('.vtf', '.png')
            
            # Конвертируем
            if self.convert_vtf(temp_vtf, png_path):
                self.texture_cache[vtf_path] = png_path
                return png_path
                
        except Exception as e:
            print(f"Error processing texture {vtf_path}: {e}")
            
        return None
        
    def extract_all_textures(self, texture_paths: List[str]) -> List[str]:
        """
        Извлекает и конвертирует список текстур
        
        Args:
            texture_paths: Список путей к текстурам в VPK
            
        Returns:
            List[str]: Список путей к сконвертированным текстурам
        """
        converted = []
        
        for vtf_path in texture_paths:
            if png_path := self.extract_and_convert_texture(vtf_path):
                converted.append(png_path)
                
        return converted
