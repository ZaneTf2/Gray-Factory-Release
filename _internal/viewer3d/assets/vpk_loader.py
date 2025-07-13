import os
import logging
import traceback
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from ..events.event_system import EventSystem, Event, EventType
import vpk

logger = logging.getLogger(__name__)

class VPKAssetLoader:
    """Загрузчик ресурсов из VPK архивов"""
    
    def __init__(self, event_system: EventSystem):
        self.event_system = event_system
        self._vpk_readers: Dict[str, vpk.VPK] = {}
        self._search_paths: List[Path] = []
        self._model_cache = {}
        self._bot_models_index = []  # Кэш для моделей ботов
        self._texture_index = {}     # Кэш для текстур
        self._temp_dir = Path(os.path.dirname(os.path.dirname(__file__))) / "temp"
        self._temp_dir.mkdir(exist_ok=True)
        logger.info("VPKAssetLoader инициализирован")
        logger.info(f"Временная директория: {self._temp_dir}")
        
    def add_vpk(self, vpk_path: str) -> None:
        """
        Добавление VPK архива
        
        Args:
            vpk_path: Путь к VPK архиву
        """
        try:
            logger.info(f"Добавление VPK архива: {vpk_path}")
            reader = vpk.open(vpk_path)
            self._vpk_readers[vpk_path] = reader
            
            # Индексация содержимого
            if "misc" in vpk_path.lower():
                # Индексируем модели ботов
                logger.info("Индексация моделей ботов...")
                for path in reader:
                    if path.startswith('models/bots/') and path.endswith('.mdl'):
                        self._bot_models_index.append(path)
                logger.info(f"Проиндексировано {len(self._bot_models_index)} моделей ботов")
                
            elif "textures" in vpk_path.lower():
                # Индексируем текстуры ботов
                logger.info("Индексация текстур ботов...")
                for path in reader:
                    if path.startswith('materials/models/bots/') and path.endswith('.vtf'):
                        base_name = os.path.splitext(path)[0]
                        if base_name.endswith('_red') or base_name.endswith('_blue'):
                            model_name = base_name[:-4]  # убираем _red/_blue
                            if model_name not in self._texture_index:
                                self._texture_index[model_name] = []
                            self._texture_index[model_name].append(path)
                logger.info(f"Проиндексировано текстур для {len(self._texture_index)} моделей")
            
        except Exception as e:
            logger.error(f"Ошибка при загрузке VPK {vpk_path}: {str(e)}")
            logger.error(f"Traceback:\n{traceback.format_exc()}")
            
    def get_file_data(self, file_path: str) -> Optional[bytes]:
        """
        Получение данных файла из VPK
        
        Args:
            file_path: Путь к файлу внутри VPK
            
        Returns:
            bytes: Данные файла или None если файл не найден
        """
        # Нормализуем путь к файлу
        file_path = file_path.replace('\\', '/')
        if file_path.startswith('/'):
            file_path = file_path[1:]
            
        try:
            # Ищем файл во всех VPK
            for reader in self._vpk_readers.values():
                try:
                    entry = reader[file_path]
                    logger.info(f"Файл {file_path} найден в VPK")
                    return entry.read()
                except KeyError:
                    continue
                    
            logger.warning(f"Файл {file_path} не найден ни в одном из VPK")
            return None
            
        except Exception as e:
            logger.error(f"Ошибка при чтении файла {file_path}: {str(e)}")
            logger.error(f"Traceback:\n{traceback.format_exc()}")
            return None
            
    def find_files(self, pattern: str) -> List[str]:
        """
        Поиск файлов в VPK по шаблону
        
        Args:
            pattern: Шаблон для поиска (напр. 'models/bots/**/*.mdl')
            
        Returns:
            List[str]: Список найденных файлов
        """
        pattern = pattern.replace('\\', '/')
        if pattern.startswith('/'):
            pattern = pattern[1:]
            
        # Используем индекс для моделей ботов
        if pattern == "models/bots/**/*.mdl":
            return sorted(self._bot_models_index)
            
        # Для остальных паттернов - обычный поиск
        parts = pattern.split('/')
        start_path = '/'.join(p for p in parts if not '*' in p)
        ext = parts[-1].split('.')[-1] if '.' in parts[-1] else None
        
        logger.debug(f"Поиск файлов по шаблону: {pattern}")
        logger.debug(f"Начальный путь: {start_path}")
        logger.debug(f"Расширение: {ext}")
        
        results = set()
        for vpk_path, reader in self._vpk_readers.items():
            try:
                # Используем генератор файлов VPK
                for filepath in reader:
                    # Нормализуем путь
                    filepath = filepath.replace('\\', '/')
                    
                    # Проверяем соответствие шаблону
                    if ext and not filepath.endswith(f".{ext}"):
                        continue
                        
                    if start_path and not filepath.startswith(start_path):
                        continue
                        
                    results.add(filepath)
                    logger.debug(f"Найден файл: {filepath}")
                    
            except Exception as e:
                logger.error(f"Ошибка при поиске в VPK {vpk_path}: {str(e)}")
                continue
                
        if not results:
            logger.warning(f"Файлы по шаблону {pattern} не найдены")
            
        return sorted(list(results))

            
    def extract_file(self, vpk_path: str, file_path: str, output_dir: Path) -> Optional[Path]:
        """
        Извлекает файл из VPK
        
        Args:
            vpk_path: Путь к VPK архиву
            file_path: Путь к файлу внутри VPK
            output_dir: Директория для извлечения
            
        Returns:
            Path: Путь к извлечённому файлу или None в случае ошибки
        """
        try:
            if vpk_path not in self._vpk_readers:
                logger.error(f"VPK {vpk_path} не найден")
                return None
                
            reader = self._vpk_readers[vpk_path]
            file_path = file_path.replace('\\', '/')
            
            try:
                entry = reader[file_path]
            except KeyError:
                logger.error(f"Файл {file_path} не найден в VPK {vpk_path}")
                return None
                
            # Создаём директории если нужно
            out_path = output_dir / file_path
            out_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Извлекаем файл
            entry.save(str(out_path))
            logger.info(f"Файл {file_path} успешно извлечён в {out_path}")
            
            return out_path
            
        except Exception as e:
            logger.error(f"Ошибка при извлечении {file_path} из VPK {vpk_path}: {str(e)}")
            logger.error(f"Traceback:\n{traceback.format_exc()}")
            return None
