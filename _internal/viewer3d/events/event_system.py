from typing import Callable, Dict, List, Any
from dataclasses import dataclass
from enum import Enum, auto

class EventType(Enum):
    """Типы событий в системе"""
    MODEL_LOADED = auto()
    TEXTURE_CHANGED = auto()
    CAMERA_MOVED = auto()
    LIGHT_CHANGED = auto()

@dataclass
class Event:
    """Базовый класс события"""
    type: EventType
    data: Dict[str, Any]

class EventSystem:
    """Система событий для коммуникации между компонентами"""
    
    def __init__(self):
        self._listeners: Dict[EventType, List[Callable[[Event], None]]] = {}
        
    def subscribe(self, event_type: EventType, callback: Callable[[Event], None]) -> None:
        """Подписка на событие"""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)
        
    def unsubscribe(self, event_type: EventType, callback: Callable[[Event], None]) -> None:
        """Отписка от события"""
        if event_type in self._listeners:
            self._listeners[event_type].remove(callback)
            
    def emit(self, event: Event) -> None:
        """Отправка события всем подписчикам"""
        if event.type in self._listeners:
            for callback in self._listeners[event.type]:
                callback(event)

# Создаем глобальный экземпляр системы событий
event_system = EventSystem()
