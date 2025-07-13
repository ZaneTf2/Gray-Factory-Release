from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path

@dataclass
class ModelFiles:
    """Содержит пути к файлам, связанным с моделью Source Engine"""
    mdl_path: str           # Путь к основному файлу модели (.mdl)
    phy_path: Optional[str] # Путь к файлу физики (.phy), если есть
    vtx_path: Optional[str] # Путь к файлу вертексов (.vvd)
    vvd_path: Optional[str] # Путь к файлу данных вертексов (.sw.vtx)
    
    @property
    def base_name(self) -> str:
        """Возвращает базовое имя модели без расширения"""
        return Path(self.mdl_path).stem
    
    def has_all_files(self) -> bool:
        """Проверяет наличие всех необходимых файлов"""
        return all([self.mdl_path, self.vtx_path, self.vvd_path])
        
    def __str__(self) -> str:
        return f"Model: {self.base_name} [MDL: {bool(self.mdl_path)}, PHY: {bool(self.phy_path)}, VTX: {bool(self.vtx_path)}, VVD: {bool(self.vvd_path)}]"

class ModelManager:
    """Управляет извлечением и обработкой моделей Source Engine"""
    
    def __init__(self, vpk_reader, output_dir: str):
        """
        Инициализирует менеджер моделей
        
        Args:
            vpk_reader: Экземпляр VPKReader для доступа к архиву
            output_dir: Директория для сохранения извлеченных файлов
        """
        self.vpk = vpk_reader
        self.output_dir = Path(output_dir)
        self.models: List[ModelFiles] = []
        
    def find_model_files(self, model_pattern: str) -> List[ModelFiles]:
        """
        Ищет все файлы моделей по заданному паттерну
        
        Args:
            model_pattern: Паттерн для поиска (например, "models/bots/**/*.mdl")
            
        Returns:
            List[ModelFiles]: Список найденных моделей с их файлами
        """
        self.models.clear()
        
        # Ищем основные файлы моделей
        for mdl_path in self.vpk.find_files(model_pattern):
            base_path = str(Path(mdl_path).with_suffix(''))
            
            # Ищем связанные файлы
            phy_path = next(self.vpk.find_files(f"{base_path}.phy"), None)
            vtx_path = next(self.vpk.find_files(f"{base_path}.sw.vtx"), None)
            vvd_path = next(self.vpk.find_files(f"{base_path}.vvd"), None)
            
            model = ModelFiles(
                mdl_path=mdl_path,
                phy_path=phy_path,
                vtx_path=vtx_path,
                vvd_path=vvd_path
            )
            
            if model.has_all_files():
                self.models.append(model)
                
        return self.models
    
    def extract_model(self, model: ModelFiles) -> bool:
        """
        Извлекает все файлы модели
        
        Args:
            model: Модель для извлечения
            
        Returns:
            bool: True если извлечение успешно, False если нет
        """
        try:
            # Извлекаем основной файл модели
            self.vpk.extract_file(
                model.mdl_path,
                str(self.output_dir / model.mdl_path)
            )
            
            # Извлекаем связанные файлы
            if model.phy_path:
                self.vpk.extract_file(
                    model.phy_path,
                    str(self.output_dir / model.phy_path)
                )
                
            if model.vtx_path:
                self.vpk.extract_file(
                    model.vtx_path,
                    str(self.output_dir / model.vtx_path)
                )
                
            if model.vvd_path:
                self.vpk.extract_file(
                    model.vvd_path,
                    str(self.output_dir / model.vvd_path)
                )
                
            return True
            
        except Exception as e:
            print(f"Error extracting model {model.base_name}: {e}")
            return False
            
    def extract_all_models(self) -> List[str]:
        """
        Извлекает все найденные модели
        
        Returns:
            List[str]: Список путей к извлеченным моделям
        """
        extracted = []
        
        for model in self.models:
            if self.extract_model(model):
                extracted.append(str(self.output_dir / model.mdl_path))
                
        return extracted
