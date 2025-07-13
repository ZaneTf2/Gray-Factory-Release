import os
import sys
import logging
from pathlib import Path

# Добавляем родительскую директорию в путь для импорта
sys.path.append(str(Path(__file__).parent.parent))

from viewer3d.assets.model_loader import ModelLoader

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('model_import_test.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def test_model_loading(tf2_path: str, model_name: str = "bot_heavy.mdl"):
    """
    Тестирует загрузку модели
    
    Args:
        tf2_path (str): Путь к директории TF2
        model_name (str): Имя файла модели
    """
    try:
        # Формируем путь к модели
        model_path = os.path.join(tf2_path, "tf", "models", "bots", model_name)
        logger.info(f"Testing model loading from: {model_path}")
        
        # Создаем загрузчик
        loader = ModelLoader()
        
        # Загружаем модель
        if not loader.load_model(model_path):
            logger.error("Failed to load model")
            return False
            
        # Получаем данные модели
        vertices, indices = loader.get_mesh_data()
        materials = loader.get_material_info()
        bones = loader.get_bones()
        
        # Проверяем данные
        logger.info(f"Vertex count: {len(vertices)}")
        logger.info(f"Index count: {len(indices)}")
        logger.info(f"Material count: {len(materials)}")
        logger.info(f"Bone count: {len(bones) if bones else 0}")
        
        # Проверяем формат данных
        logger.info("Vertex format:")
        logger.info(f"  Shape: {vertices.shape}")
        logger.info(f"  Type: {vertices.dtype}")
        
        logger.info("Index format:")
        logger.info(f"  Shape: {indices.shape}")
        logger.info(f"  Type: {indices.dtype}")
        
        # Проверяем материалы
        logger.info("\nMaterials:")
        for material in materials:
            logger.info(f"  {material.name} ({material.width}x{material.height})")
            
        # Проверяем кости
        if bones:
            logger.info("\nBones:")
            for bone in bones:
                logger.info(f"  {bone.name} (parent: {bone.parent})")
                
        logger.info("\nModel loaded successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error testing model: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def main():
    # Стандартные пути установки TF2
    tf2_paths = [
        r"C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2",
        r"C:\Program Files\Steam\steamapps\common\Team Fortress 2"
    ]
    
    # Проверяем каждый путь
    tf2_path = None
    for path in tf2_paths:
        if os.path.exists(path):
            tf2_path = path
            break
            
    if not tf2_path:
        logger.error("TF2 directory not found!")
        return
        
    # Тестируем загрузку разных моделей ботов
    test_models = [
        "bot_heavy.mdl",
        "bot_soldier.mdl",
        "bot_medic.mdl"
    ]
    
    for model in test_models:
        logger.info(f"\nTesting {model}...")
        if test_model_loading(tf2_path, model):
            logger.info(f"{model} test completed successfully")
        else:
            logger.error(f"{model} test failed")

if __name__ == "__main__":
    main()