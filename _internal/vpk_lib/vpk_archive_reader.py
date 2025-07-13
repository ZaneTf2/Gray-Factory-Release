import os
import logging
import struct
from typing import Dict, Optional, BinaryIO

logger = logging.getLogger(__name__)

class VPKArchiveReader:
    """Класс для чтения отдельных архивов VPK"""
    
    def __init__(self, archive_path: str):
        self.path = archive_path
        self.file: Optional[BinaryIO] = None
        logger.info(f"Инициализация VPK архива: {archive_path}")
        
    def open(self):
        """Открытие архива"""
        if self.file is None:
            try:
                self.file = open(self.path, 'rb')
                logger.info(f"Архив открыт: {self.path}")
            except Exception as e:
                logger.error(f"Ошибка при открытии архива {self.path}: {str(e)}")
                raise
    
    def close(self):
        """Закрытие архива"""
        if self.file is not None:
            self.file.close()
            self.file = None
            logger.info(f"Архив закрыт: {self.path}")
    
    def read_bytes(self, offset: int, size: int) -> bytes:
        """Чтение данных из архива"""
        try:
            self.open()
            self.file.seek(offset)
            data = self.file.read(size)
            if len(data) != size:
                logger.error(f"Неверный размер прочитанных данных: {len(data)} != {size}")
                raise IOError(f"Неверный размер прочитанных данных: {len(data)} != {size}")
            return data
        except Exception as e:
            logger.error(f"Ошибка при чтении данных из архива {self.path}: {str(e)}")
            raise
            
    def __del__(self):
        """Деструктор"""
        self.close()
