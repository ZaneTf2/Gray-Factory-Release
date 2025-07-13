import os
import struct
import logging
from typing import List, Dict, Optional, BinaryIO, Generator, Set
from pathlib import Path
from .exceptions import VPKError, VPKParseError, VPKFileNotFoundError
from .vpk_entry import VPKEntry

logger = logging.getLogger(__name__)

class VPKReader:
    """Класс для чтения VPK архивов Source Engine"""
    
    SIGNATURE = 0x55AA1234
    
    def __init__(self, dir_path: str, search_dirs: list = None):
        """
        Инициализирует чтение VPK архива и опционально директории для поиска
        
        Args:
            dir_path: Путь к dir VPK файлу (например, pak01_dir.vpk)
            search_dirs: Список дополнительных директорий для поиска файлов
        """
        self.dir_path = dir_path
        self.search_dirs = search_dirs or []
        self.entries: Dict[str, VPKEntry] = {}
        self.archives: Dict[int, str] = {}  # index -> path
        self._initialized = False
        
        # Инициализация при создании
        self._initialize()
        self.dir_path = Path(dir_path)
        if not self.dir_path.exists():
            raise FileNotFoundError(f"VPK file not found: {dir_path}")
            
        if not str(self.dir_path).endswith('_dir.vpk'):
            raise VPKError(f"Not a directory VPK file: {dir_path}")
            
        self.base_path = str(self.dir_path).replace('_dir.vpk', '')
        self.entries: Dict[str, VPKEntry] = {}
        self._normalized_paths: Dict[str, str] = {}  # Кэш нормализованных путей
        self._file_handle: Optional[BinaryIO] = None
        self._archive_handles: Dict[int, BinaryIO] = {}  # Кэш открытых архивов
        self.search_dirs = [Path(d) for d in (search_dirs or [])]
        
        # Проверяем наличие архивных файлов
        archive_path = f"{self.base_path}_000.vpk"
        if not Path(archive_path).exists():
            raise VPKError(f"Archive file not found: {archive_path}")
        
        # Читаем структуру архива
        self._read_directory()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def close(self):
        """Закрывает открытые файловые дескрипторы"""
        if self._file_handle:
            self._file_handle.close()
            self._file_handle = None
        
        # Закрываем все кэшированные архивы
        for handle in self._archive_handles.values():
            try:
                handle.close()
            except:
                pass
        self._archive_handles.clear()

    def normalize_path(self, path: str) -> str:
        """
        Нормализует путь для VPK:
        - Приводит к нижнему регистру
        - Заменяет обратные слэши на прямые
        - Убирает повторяющиеся слэши
        - Убирает начальные/конечные слэши
        
        Args:
            path: Исходный путь
        Returns:
            str: Нормализованный путь
        """
        path = path.replace('\\', '/')
        while '//' in path:
            path = path.replace('//', '/')
        path = path.strip('/')
        return path.lower()

    def _initialize(self):
        """Инициализация VPK: чтение заголовка, дерева и поиск архивов"""
        if self._initialized:
            return
            
        try:
            self._read_header()
            self._read_directory_tree()
            self._find_archives()
            self._initialized = True
        except Exception as e:
            logger.error(f"Ошибка при инициализации VPK: {str(e)}")
            raise VPKError(f"Ошибка инициализации: {str(e)}")
            
    def _find_archives(self):
        """Поиск связанных VPK архивов"""
        try:
            vpk_dir = os.path.dirname(self.dir_path)
            vpk_name = os.path.splitext(os.path.basename(self.dir_path))[0]
            
            if vpk_name.endswith('_dir'):
                base_name = vpk_name[:-4]
                logger.info(f"Поиск архивов для {base_name}")
                
                # Поиск архивов по маске base_name_*.vpk
                for file in os.listdir(vpk_dir):
                    if file.startswith(base_name + '_') and file.endswith('.vpk') and '_dir' not in file:
                        try:
                            archive_path = os.path.join(vpk_dir, file)
                            archive_index = int(file[len(base_name) + 1:-4])
                            self.archives[archive_index] = archive_path
                            logger.info(f"Найден архив {archive_index}: {archive_path}")
                        except ValueError:
                            logger.warning(f"Пропущен файл с неверным индексом: {file}")
                            
        except Exception as e:
            logger.error(f"Ошибка при поиске архивов: {str(e)}")
            raise VPKError(f"Ошибка поиска архивов: {str(e)}")
            
    def _read_from_archive(self, archive_index: int, offset: int, size: int) -> bytes:
        """Чтение данных из архива"""
        if archive_index not in self.archives:
            raise VPKError(f"Архив не найден: {archive_index}")
            
        archive_path = self.archives[archive_index]
        try:
            with open(archive_path, 'rb') as f:
                f.seek(offset)
                data = f.read(size)
                if len(data) != size:
                    raise VPKError(f"Неверный размер прочитанных данных: {len(data)} != {size}")
                return data
        except Exception as e:
            logger.error(f"Ошибка при чтении из архива {archive_path}: {str(e)}")
            raise VPKError(f"Ошибка чтения из архива: {str(e)}")
            
    def _read_directory(self):
        """Читает структуру VPK архива"""
        print(f"\nЧтение VPK архива: {self.dir_path}")
        print("--------------------------------")
        with open(self.dir_path, 'rb') as f:
            # Читаем заголовок
            signature = struct.unpack('<I', f.read(4))[0]
            print(f"Сигнатура: {hex(signature)}")
            if signature != self.SIGNATURE:
                raise VPKParseError(f"Неверная сигнатура VPK: {hex(signature)}, ожидалась: {hex(self.SIGNATURE)}")
            version = struct.unpack('<I', f.read(4))[0]
            tree_size = struct.unpack('<I', f.read(4))[0]
            print(f"Версия VPK: {version}")
            print(f"Размер дерева: {tree_size:,} bytes")
            if version == 1:
                pass
            elif version == 2:
                file_data_section_size = struct.unpack('<I', f.read(4))[0]
                archive_md5_section_size = struct.unpack('<I', f.read(4))[0]
                other_md5_section_size = struct.unpack('<I', f.read(4))[0]
                signature_section_size = struct.unpack('<I', f.read(4))[0]
            else:
                raise VPKParseError(f"Unsupported VPK version: {version}")
            print("\nЧтение структуры файлов:")
            print("--------------------------------")
            extension_count = 0
            dir_count = 0
            file_count = 0
            while True:
                extension = self._read_string(f)
                if not extension:
                    break
                extension_count += 1
                while True:
                    directory = self._read_string(f)
                    if not directory:
                        break
                    dir_count += 1
                    if directory.startswith("models/bots"):
                        print(f"\nНайдена директория ботов: {directory}")
                    while True:
                        filename = self._read_string(f)
                        if not filename:
                            break
                        crc = struct.unpack('<I', f.read(4))[0]
                        preload_bytes_size = struct.unpack('<H', f.read(2))[0]
                        archive_index = struct.unpack('<H', f.read(2))[0]
                        entry_offset = struct.unpack('<I', f.read(4))[0]
                        entry_length = struct.unpack('<I', f.read(4))[0]
                        terminator = struct.unpack('<H', f.read(2))[0]
                        if terminator != 0xFFFF:
                            raise VPKParseError(f"Invalid entry terminator: {hex(terminator)}")
                        preload_bytes = f.read(preload_bytes_size) if preload_bytes_size > 0 else b''
                        # Корректное формирование пути
                        if directory != ' ':
                            file_path = f"{directory}/{filename}"
                        else:
                            file_path = filename
                        if extension != ' ':
                            file_path = f"{file_path}.{extension}"
                        file_path = self.normalize_path(file_path)
                        entry = VPKEntry(
                            path=file_path,
                            archive_index=archive_index,
                            entry_offset=entry_offset,
                            entry_length=entry_length,
                            preload_bytes=preload_bytes,
                            preload_data=preload_bytes,
                            crc32=crc
                        )
                        self.entries[file_path] = entry
                        file_count += 1
                        if "models/bots" in file_path:
                            print(f"  Файл: {file_path} (архив: {archive_index}, размер: {entry_length:,} bytes)")
            print("\nСтатистика VPK архива:")
            print(f"- Найдено расширений: {extension_count}")
            print(f"- Найдено директорий: {dir_count}")
            print(f"- Найдено файлов: {file_count}")
            relevant = sum(1 for path in self.entries if "models/bots" in path)
            print(f"- Файлов моделей ботов: {relevant}")
    
    def _read_string(self, f: BinaryIO) -> str:
        """Читает null-terminated строку из файла"""
        result = []
        while True:
            char = f.read(1)
            if char == b'\0' or not char:
                break
            result.append(char.decode('utf-8'))
        return ''.join(result)
    
    def get_file_data(self, path: str) -> bytes:
        """
        Получает данные файла из архива
        
        Args:
            path: Путь к файлу внутри архива
            
        Returns:
            bytes: Данные файла
            
        Raises:
            VPKFileNotFoundError: Если файл не найден в архиве
        """
        # Нормализуем путь
        norm_path = self.normalize_path(path)
        
        # Ищем файл в entries
        found_path = None
        for entry_path in self.entries:
            if self.normalize_path(entry_path) == norm_path:
                found_path = entry_path
                break
                
        if not found_path:
            raise VPKFileNotFoundError(f"File not found in VPK: {path}")
            
        entry = self.entries[found_path]
        
        # Если все данные предзагружены, возвращаем их
        if entry.is_preloaded:
            return entry.preload_bytes
            
        # Иначе читаем данные из архива
        archive_path = f"{self.base_path}_{entry.archive_index:03d}.vpk"
        
        with open(archive_path, 'rb') as f:
            f.seek(entry.entry_offset)
            data = f.read(entry.entry_length)
            
        return entry.preload_bytes + data
    
    def find_files(self, pattern: str) -> Generator[str, None, None]:
        """
        Ищет файлы в архиве по паттерну и в search_dirs
        
        Args:
            pattern: Паттерн для поиска (например, "models/bots/*.mdl")
        """
        import fnmatch
        import logging
        logger = logging.getLogger(__name__)
        
        # Нормализуем паттерн
        pattern = self.normalize_path(pattern)
        logger.info(f"[VPKReader] Поиск файлов по паттерну: {pattern}")
        
        # Создаем множество для уникальных путей
        found_paths = set()
        
        # Ищем в VPK
        for path in self.entries.keys():
            norm_path = self.normalize_path(path)
            if fnmatch.fnmatch(norm_path, pattern):
                if path not in found_paths:  # Проверяем дубликаты
                    found_paths.add(path)
                    logger.info(f"[VPKReader] Найден файл: {path}")
                    yield path
        
        # Ищем в search_dirs
        for search_dir in self.search_dirs:
            for file in search_dir.glob(pattern):
                if file.is_file():
                    rel_path = str(file.relative_to(search_dir)).replace('\\', '/')
                    norm_path = self.normalize_path(rel_path)
                    if norm_path not in found_paths:
                        found_paths.add(norm_path)
                        logger.info(f"[VPKReader] Найден файл в директории: {rel_path}")
                        yield rel_path

    def extract_file(self, file_path: str, output_dir: str) -> str:
        """
        Извлекает файл из VPK
    
        Args:
            file_path: Путь к файлу внутри VPK
            output_dir: Директория для сохранения
    
        Returns:
            str: Путь к извлеченному файлу
    
        Raises:
            VPKError: Если файл не найден или возникла ошибка при извлечении
        """
        import logging
        logger = logging.getLogger(__name__)
    
        logger.info(f"\n=== Начало извлечения файла {file_path} ===")
        try:
            # Нормализуем пути
            norm_file_path = self.normalize_path(file_path)
            abs_output_dir = os.path.abspath(output_dir)
            logger.info(f"Нормализованный путь: {norm_file_path}")
            logger.info(f"Директория назначения: {abs_output_dir}")
            
            # Проверяем наличие файла в VPK
            if norm_file_path not in self.entries:
                logger.info("Поиск файла в других регистрах...")
                # Попробуем поискать файл без учета регистра
                found = False
                for entry_path in self.entries:
                    if entry_path.lower() == norm_file_path.lower():
                        file_path = entry_path
                        found = True
                        logger.info(f"Найден файл с другим регистром: {entry_path}")
                        break
                if not found:
                    logger.error("Файл не найден в VPK")
                    logger.info("Доступные файлы в этой директории:")
                    dir_path = os.path.dirname(norm_file_path)
                    for entry in self.entries:
                        if entry.startswith(dir_path):
                            logger.info(f"- {entry}")
                    raise VPKFileNotFoundError(f"File not found in VPK: {file_path}")
            
            # Создаем директории для сохранения
            full_output_path = os.path.join(abs_output_dir, norm_file_path)
            output_dir = os.path.dirname(full_output_path)
            logger.info(f"Полный путь назначения: {full_output_path}")
            
            try:
                os.makedirs(output_dir, exist_ok=True)
                logger.info(f"Директория создана: {output_dir}")
            except Exception as e:
                logger.error(f"Ошибка при создании директории {output_dir}: {str(e)}")
                raise VPKError(f"Не удалось создать директорию: {str(e)}")
            
            # Проверяем path traversal
            if not os.path.abspath(full_output_path).startswith(os.path.abspath(output_dir)):
                logger.error(f"Обнаружена попытка path traversal: {file_path}")
                raise VPKError(f"Попытка path traversal: {file_path}")
            
            # Получаем метаданные файла
            entry = self.entries[file_path]
            logger.info(f"Метаданные файла:")
            logger.info(f"- Индекс архива: {entry.archive_index}")
            logger.info(f"- Смещение: {entry.entry_offset}")
            logger.info(f"- Размер: {entry.entry_length}")
            logger.info(f"- Размер предзагруженных данных: {len(entry.preload_bytes) if entry.preload_bytes else 0}")
            
            try:
                # Открываем архив с файлом
                if entry.archive_index == 0x7fff:
                    logger.info("Используем основной архив")
                    archive = self._file_handle
                else:
                    archive_path = self.dir_path.parent / f"{self.dir_path.stem}_{entry.archive_index:03d}.vpk"
                    logger.info(f"Открываем архив: {archive_path}")
                    if not archive_path.exists():
                        logger.error(f"Архив не найден: {archive_path}")
                        raise VPKError(f"Архив не найден: {archive_path}")
                    archive = open(archive_path, 'rb')
                
                try:
                    # Извлекаем файл
                    with open(full_output_path, 'wb') as out_file:
                        total_written = 0
                        
                        # Записываем preload данные если есть
                        if entry.preload_bytes:
                            logger.info("Запись предзагруженных данных...")
                            written = out_file.write(entry.preload_bytes)
                            total_written += written
                            logger.info(f"Записано предзагруженных данных: {written} байт")
                        
                        # Записываем основные данные
                        if entry.entry_length > 0:
                            logger.info("Запись основных данных...")
                            archive.seek(entry.entry_offset)
                            data = archive.read(entry.entry_length)
                            if len(data) != entry.entry_length:
                                logger.error(f"Прочитано {len(data)} байт, ожидалось {entry.entry_length}")
                                raise VPKError(f"Неверный размер прочитанных данных")
                                
                            written = out_file.write(data)
                            total_written += written
                            logger.info(f"Записано основных данных: {written} байт")
                    
                    logger.info(f"Всего записано: {total_written} байт")
                    
                    # Проверяем результат
                    if not os.path.exists(full_output_path):
                        logger.error(f"Файл не был создан: {full_output_path}")
                        raise VPKError(f"Файл не был создан: {full_output_path}")
                        
                    actual_size = os.path.getsize(full_output_path)
                    expected_size = len(entry.preload_bytes or b'') + entry.entry_length
                    if actual_size != expected_size:
                        logger.error(f"Неверный размер файла: {actual_size} байт (ожидалось {expected_size})")
                        raise VPKError(
                            f"Неверный размер извлеченного файла: {actual_size} байт "
                            f"(ожидалось {expected_size} байт)"
                        )
                    
                    logger.info(f"Файл успешно извлечен: {full_output_path}")
                    return full_output_path
                
                finally:
                    if entry.archive_index != 0x7fff and archive != self._file_handle:
                        archive.close()
                        
            except Exception as e:
                logger.error(f"Ошибка при извлечении данных: {str(e)}")
                import traceback
                logger.error(f"Traceback:\n{traceback.format_exc()}")
                if os.path.exists(full_output_path):
                    try:
                        os.remove(full_output_path)
                        logger.info(f"Удален неполный файл: {full_output_path}")
                    except:
                        pass
                raise
            
        except Exception as e:
            logger.error(f"Ошибка при извлечении файла {file_path}: {str(e)}")
            import traceback
            logger.error(f"Traceback:\n{traceback.format_exc()}")
            raise VPKError(f"Ошибка при извлечении файла {file_path}: {str(e)}") from e
    
    def extract_files(self, pattern: str, output_dir: str) -> List[str]:
        """
        Извлекает все файлы, соответствующие паттерну
        
        Args:
            pattern: Паттерн для поиска файлов
            output_dir: Директория для извлечения
            
        Returns:
            List[str]: Список извлеченных файлов
        """
        extracted = []
        for path in self.find_files(pattern):
            relative_path = path
            output_path = os.path.join(output_dir, relative_path)
            self.extract_file(path, output_path)
            extracted.append(output_path)
        return extracted
    
    def diagnose_file(self, file_path: str) -> None:
        """Диагностика файла в VPK"""
        print(f"\n=== Диагностика файла: {file_path} ===")
        
        # Проверяем исходный путь
        print(f"Исходный путь: {file_path}")
        norm_path = self.normalize_path(file_path)
        print(f"Нормализованный путь: {norm_path}")
        
        # Проверяем наличие файла
        if norm_path in self.entries:
            print("✓ Файл найден в VPK")
            entry = self.entries[norm_path]
            print(f"Метаданные:")
            print(f"- Архив: {entry.archive_index}")
            print(f"- Смещение: {entry.entry_offset}")
            print(f"- Размер: {entry.entry_length}")
            print(f"- CRC32: {hex(entry.crc32)}")
            
            # Проверяем архивный файл
            archive_path = f"{self.base_path}_{entry.archive_index:03d}.vpk"
            if os.path.exists(archive_path):
                print(f"✓ Архивный файл найден: {archive_path}")
                print(f"  Размер архива: {os.path.getsize(archive_path):,} байт")
            else:
                print(f"× Архивный файл не найден: {archive_path}")
        else:
            print("× Файл не найден в VPK")
            print("\nПохожие файлы:")
            dir_path = os.path.dirname(norm_path)
            base_name = os.path.splitext(os.path.basename(norm_path))[0].lower()
            
            for entry_path in self.entries:
                entry_dir = os.path.dirname(entry_path)
                entry_base = os.path.splitext(os.path.basename(entry_path))[0].lower()
                
                if dir_path == entry_dir or base_name in entry_base:
                    print(f"- {entry_path}")

    def _get_archive_handle(self, archive_index: int) -> BinaryIO:
        """Получает файловый дескриптор для архива, используя кэш"""
        if archive_index == 0x7fff:
            return self._file_handle
            
        if archive_index in self._archive_handles:
            handle = self._archive_handles[archive_index]
            handle.seek(0)  # Сбрасываем позицию на начало
            return handle
            
        archive_path = self.dir_path.parent / f"{self.dir_path.stem}_{archive_index:03d}.vpk"
        if not archive_path.exists():
            raise VPKError(f"Архив не найден: {archive_path}")
            
        handle = open(archive_path, 'rb')
        self._archive_handles[archive_index] = handle
        return handle

    def _read_header(self):
        """Чтение заголовка VPK"""
        with open(self.dir_path, 'rb') as f:
            signature = struct.unpack('<I', f.read(4))[0]
            if signature != self.SIGNATURE:
                raise VPKParseError(f"Неверная сигнатура VPK: {hex(signature)}")
            version = struct.unpack('<I', f.read(4))[0]
            tree_size = struct.unpack('<I', f.read(4))[0]
            self._header = (signature, version, tree_size)
            # Для версии 2 читаем дополнительные поля
            if version == 2:
                self._file_data_section_size = struct.unpack('<I', f.read(4))[0]
                self._archive_md5_section_size = struct.unpack('<I', f.read(4))[0]
                self._other_md5_section_size = struct.unpack('<I', f.read(4))[0]
                self._signature_section_size = struct.unpack('<I', f.read(4))[0]
            else:
                self._file_data_section_size = 0
                self._archive_md5_section_size = 0
                self._other_md5_section_size = 0
                self._signature_section_size = 0

    def _read_directory_tree(self):
        """Чтение дерева файлов VPK"""
        with open(self.dir_path, 'rb') as f:
            # Пропускаем заголовок
            version = self._header[1]
            header_size = 8 if version == 1 else 28
            f.seek(header_size)
            while True:
                extension = self._read_cstring(f)
                if not extension:
                    break
                while True:
                    path = self._read_cstring(f)
                    if not path:
                        break
                    while True:
                        filename = self._read_cstring(f)
                        if not filename:
                            break
                        full_path = os.path.join(path, filename).replace('\\', '/').strip('/')
                        if extension:
                            full_path = f"{full_path}.{extension}"
                        crc32 = struct.unpack('<I', f.read(4))[0]
                        preload_bytes = struct.unpack('<H', f.read(2))[0]
                        archive_index = struct.unpack('<H', f.read(2))[0]
                        entry_offset = struct.unpack('<I', f.read(4))[0]
                        entry_length = struct.unpack('<I', f.read(4))[0]
                        terminator = struct.unpack('<H', f.read(2))[0]
                        preload_data = f.read(preload_bytes) if preload_bytes > 0 else b''
                        entry = VPKEntry(
                            path=full_path,
                            archive_index=archive_index,
                            entry_offset=entry_offset,
                            entry_length=entry_length,
                            preload_bytes=preload_bytes,
                            preload_data=preload_data,
                            crc32=crc32
                        )
                        self.entries[full_path.lower()] = entry
                        if terminator != 0xFFFF:
                            raise VPKParseError(f"Неверный терминатор для {full_path}: {hex(terminator)}")

    def _read_cstring(self, f: BinaryIO) -> str:
        chars = []
        while True:
            c = f.read(1)
            if c == b'\x00' or c == b'':
                break
            chars.append(c)
        return b''.join(chars).decode('utf-8', errors='replace')
