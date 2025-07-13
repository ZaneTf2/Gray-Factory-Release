import numpy as np
from dataclasses import dataclass
from typing import Tuple
from ..events.event_system import EventSystem, Event, EventType
from OpenGL.GL import *

@dataclass
class Light:
    """Параметры источника света"""
    position: np.ndarray    # Позиция источника света
    direction: np.ndarray   # Направление света (для направленного света)
    color: np.ndarray      # Цвет света (RGB)
    intensity: float       # Интенсивность света
    ambient: float        # Интенсивность фонового освещения
    diffuse: float       # Интенсивность рассеянного света
    specular: float      # Интенсивность бликов
    constant: float      # Постоянное затухание
    linear: float        # Линейное затухание
    quadratic: float     # Квадратичное затухание

class LightManager:
    """Управление источниками света в сцене"""
    
    def __init__(self, event_system: EventSystem):
        self.event_system = event_system
        
        # Создаем основной источник света по умолчанию
        self.main_light = Light(
            position=np.array([5.0, 5.0, 5.0]),
            direction=np.array([-1.0, -1.0, -1.0]),
            color=np.array([1.0, 1.0, 1.0]),
            intensity=1.0,
            ambient=0.2,
            diffuse=0.8,
            specular=0.5,
            constant=1.0,
            linear=0.09,
            quadratic=0.032
        )
        
        # Нормализуем направление света
        self.main_light.direction = self.main_light.direction / np.linalg.norm(self.main_light.direction)
        
    def set_position(self, x: float, y: float, z: float) -> None:
        """Установка позиции источника света"""
        self.main_light.position = np.array([x, y, z])
        self._notify_change()
        
    def set_direction(self, x: float, y: float, z: float) -> None:
        """Установка направления света"""
        direction = np.array([x, y, z])
        self.main_light.direction = direction / np.linalg.norm(direction)
        self._notify_change()
        
    def set_color(self, r: float, g: float, b: float) -> None:
        """Установка цвета света"""
        self.main_light.color = np.array([r, g, b])
        self._notify_change()
        
    def set_intensity(self, intensity: float) -> None:
        """Установка интенсивности света"""
        self.main_light.intensity = np.clip(intensity, 0.0, 1.0)
        self._notify_change()
        
    def set_ambient(self, ambient: float) -> None:
        """Установка интенсивности фонового освещения"""
        self.main_light.ambient = np.clip(ambient, 0.0, 1.0)
        self._notify_change()
        
    def set_diffuse(self, diffuse: float) -> None:
        """Установка интенсивности рассеянного света"""
        self.main_light.diffuse = np.clip(diffuse, 0.0, 1.0)
        self._notify_change()
        
    def set_specular(self, specular: float) -> None:
        """Установка интенсивности бликов"""
        self.main_light.specular = np.clip(specular, 0.0, 1.0)
        self._notify_change()
        
    def set_attenuation(self, constant: float, linear: float, quadratic: float) -> None:
        """Установка параметров затухания света"""
        self.main_light.constant = max(constant, 0.0)
        self.main_light.linear = max(linear, 0.0)
        self.main_light.quadratic = max(quadratic, 0.0)
        self._notify_change()
        
    def _update_material(self) -> None:
        """Обновление параметров материала"""
        # Настройка материала по умолчанию
        mat_ambient = [0.2, 0.2, 0.2, 1.0]
        mat_diffuse = [0.8, 0.8, 0.8, 1.0]
        mat_specular = [1.0, 1.0, 1.0, 1.0]
        mat_shininess = [50.0]
        
        glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
        
    def get_light_data(self) -> Light:
        """Получение текущих параметров освещения"""
        return self.main_light
        
    def _notify_change(self) -> None:
        """Оповещение об изменении параметров освещения"""
        self.event_system.emit(Event(
            EventType.LIGHT_CHANGED,
            {"light": self.main_light}
        ))
        
    def apply(self) -> None:
        """Применяет настройки освещения к текущему контексту OpenGL"""
        # Устанавливаем позицию источника света
        light_pos = list(self.main_light.position) + [1.0]  # w=1.0 для позиционного света
        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
        
        # Устанавливаем цвет и интенсивность света
        color = self.main_light.color * self.main_light.intensity
        
        # Настройка компонентов освещения
        ambient = color * self.main_light.ambient
        diffuse = color * self.main_light.diffuse
        specular = np.ones(3) * self.main_light.specular  # Белые блики
        
        glLightfv(GL_LIGHT0, GL_AMBIENT, list(ambient) + [1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, list(diffuse) + [1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, list(specular) + [1.0])
        
        # Настройка затухания света
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, self.main_light.constant)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, self.main_light.linear)
        glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, self.main_light.quadratic)
