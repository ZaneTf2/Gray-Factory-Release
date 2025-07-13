import os
import sys
import unittest
import logging
from pathlib import Path

# Добавляем родительскую директорию в путь для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from viewer3d.assets.vpk_loader import VPKAssetLoader
from viewer3d.events.event_system import EventSystem

class TestVPKLoading(unittest.TestCase):
    def setUp(self):
        # Настройка логирования
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        
        # Инициализация
        self.event_system = EventSystem()
        self.vpk_loader = VPKAssetLoader(self.event_system)
        
        # Путь к VPK файлам
        tf2_path = "C:/Program Files (x86)/Steam/steamapps/common/Team Fortress 2/tf"
        self.vpk_path = os.path.join(tf2_path, "tf2_misc_dir.vpk")
        
    def test_vpk_loading(self):
        """Тест загрузки VPK архива"""
        self.vpk_loader.add_vpk(self.vpk_path)
        self.assertTrue(len(self.vpk_loader._vpk_readers) > 0)
        
    def test_model_search(self):
        """Тест поиска моделей ботов"""
        self.vpk_loader.add_vpk(self.vpk_path)
        models = list(self.vpk_loader.find_files("models/bots/**/*.mdl"))
        self.logger.info(f"Найдено моделей: {len(models)}")
        self.assertTrue(len(models) > 0)
        
        # Проверяем конкретную модель
        test_model = "models/bots/spy/bot_spy.mdl"
        self.assertTrue(test_model in models)
        
    def test_model_extraction(self):
        """Тест извлечения модели"""
        self.vpk_loader.add_vpk(self.vpk_path)
        test_model = "models/bots/spy/bot_spy.mdl"
        
        # Создаем временную директорию
        temp_dir = Path("./temp_test")
        temp_dir.mkdir(exist_ok=True)
        
        # Извлекаем модель
        extracted_path = self.vpk_loader.extract_file(test_model, str(temp_dir))
        self.assertIsNotNone(extracted_path)
        self.assertTrue(os.path.exists(extracted_path))
        
        # Проверяем размер файла
        self.assertTrue(os.path.getsize(extracted_path) > 0)
        
    def test_texture_loading(self):
        """Тест поиска текстур для модели"""
        self.vpk_loader.add_vpk(self.vpk_path)
        model_dir = "models/bots/spy"
        textures = list(self.vpk_loader.find_files(f"materials/{model_dir}/*.vtf"))
        self.logger.info(f"Найдено текстур: {len(textures)}")
        self.assertTrue(len(textures) > 0)

if __name__ == '__main__':
    unittest.main()
