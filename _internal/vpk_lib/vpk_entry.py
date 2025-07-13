from dataclasses import dataclass
from typing import Optional

@dataclass
class VPKEntry:
    """Представляет файл внутри VPK архива"""
    path: str                # Полный путь к файлу в архиве
    archive_index: int       # Индекс архива (для многотомных VPK)
    entry_offset: int        # Смещение в архиве
    entry_length: int        # Длина данных
    preload_bytes: int       # Размер предзагруженных данных
    preload_data: bytes     # Предзагруженные данные
    crc32: int              # CRC32 файла
    
    @property
    def is_preloaded(self) -> bool:
        """Проверка, находятся ли все данные в предзагруженной секции"""
        return self.entry_length == 0 and self.preload_bytes > 0
        
    @property
    def total_size(self) -> int:
        """Общий размер файла"""
        return self.preload_bytes + self.entry_length

    def __repr__(self) -> str:
        status = "preloaded" if self.is_preloaded else f"in archive {self.archive_index}"
        return f"VPKEntry('{self.path}', {status}, size={self.total_size} bytes)"
