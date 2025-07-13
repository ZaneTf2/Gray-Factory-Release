import numpy as np
from dataclasses import dataclass
from typing import Tuple
from ..events.event_system import EventSystem, Event, EventType
from OpenGL.GLU import gluLookAt, gluPerspective

@dataclass
class CameraState:
    """Состояние камеры"""
    position: np.ndarray  # Позиция камеры
    target: np.ndarray   # Точка, на которую смотрит камера
    up: np.ndarray       # Вектор "вверх"
    fov: float          # Поле зрения
    aspect: float       # Соотношение сторон
    near: float         # Ближняя плоскость отсечения
    far: float         # Дальняя плоскость отсечения

class Camera:
    """Компонент управления камерой"""
    
    def __init__(self, event_system: EventSystem):
        self.event_system = event_system
        
        # Инициализация состояния камеры по умолчанию
        self.state = CameraState(
            position=np.array([0.0, 0.0, 5.0]),
            target=np.array([0.0, 0.0, 0.0]),
            up=np.array([0.0, 1.0, 0.0]),
            fov=45.0,
            aspect=1.0,
            near=0.1,
            far=1000.0
        )
        
        # Параметры орбитальной камеры
        self.orbit_speed = 0.01
        self.zoom_speed = 0.1
        self.min_zoom = 2.0
        self.max_zoom = 20.0
        
        # Текущие углы поворота
        self.theta = 0.0  # Горизонтальный угол
        self.phi = 0.0    # Вертикальный угол
        
    def orbit(self, delta_x: float, delta_y: float) -> None:
        """
        Вращение камеры вокруг цели
        
        Args:
            delta_x: Изменение по горизонтали
            delta_y: Изменение по вертикали
        """
        self.theta += delta_x * self.orbit_speed
        self.phi += delta_y * self.orbit_speed
        
        # Ограничиваем вертикальный угол
        self.phi = np.clip(self.phi, -np.pi/2 + 0.1, np.pi/2 - 0.1)
        
        # Вычисляем новую позицию камеры
        distance = np.linalg.norm(self.state.position - self.state.target)
        x = distance * np.cos(self.phi) * np.sin(self.theta)
        y = distance * np.sin(self.phi)
        z = distance * np.cos(self.phi) * np.cos(self.theta)
        
        self.state.position = self.state.target + np.array([x, y, z])
        self._update()
        
    def zoom(self, delta: float) -> None:
        """
        Приближение/отдаление камеры
        
        Args:
            delta: Величина приближения (положительная - отдаление)
        """
        direction = self.state.position - self.state.target
        distance = np.linalg.norm(direction)
        
        # Изменяем расстояние с ограничениями
        new_distance = np.clip(
            distance * (1.0 + delta * self.zoom_speed),
            self.min_zoom,
            self.max_zoom
        )
        
        # Обновляем позицию камеры
        self.state.position = self.state.target + direction * (new_distance / distance)
        self._update()
        
    def get_view_matrix(self) -> np.ndarray:
        """Возвращает матрицу вида"""
        return self._look_at(self.state.position, self.state.target, self.state.up)
        
    def get_projection_matrix(self) -> np.ndarray:
        """Возвращает матрицу проекции"""
        return self._perspective(
            self.state.fov,
            self.state.aspect,
            self.state.near,
            self.state.far
        )
        
    def apply(self) -> None:
        """Применяет настройки камеры к текущему контексту OpenGL"""
        # Устанавливаем проекцию
        gluPerspective(
            self.state.fov,
            self.state.aspect,
            self.state.near,
            self.state.far
        )
        
        # Устанавливаем положение и направление камеры
        gluLookAt(
            *self.state.position,  # Позиция камеры
            *self.state.target,    # Точка, на которую смотрит камера
            *self.state.up         # Вектор "вверх"
        )
        
    def _update(self) -> None:
        """Оповещает о изменении состояния камеры"""
        self.event_system.emit(Event(
            EventType.CAMERA_MOVED,
            {"camera": self.state}
        ))
        
    @staticmethod
    def _look_at(eye: np.ndarray, target: np.ndarray, up: np.ndarray) -> np.ndarray:
        """Создает матрицу вида"""
        forward = target - eye
        forward = forward / np.linalg.norm(forward)
        
        right = np.cross(forward, up)
        right = right / np.linalg.norm(right)
        
        new_up = np.cross(right, forward)
        
        view_matrix = np.eye(4)
        view_matrix[:3, 0] = right
        view_matrix[:3, 1] = new_up
        view_matrix[:3, 2] = -forward
        view_matrix[:3, 3] = -np.array([
            np.dot(right, eye),
            np.dot(new_up, eye),
            np.dot(-forward, eye)
        ])
        
        return view_matrix
        
    @staticmethod
    def _perspective(fov: float, aspect: float, near: float, far: float) -> np.ndarray:
        """Создает матрицу перспективной проекции"""
        f = 1.0 / np.tan(np.radians(fov) / 2.0)
        
        projection_matrix = np.zeros((4, 4))
        projection_matrix[0, 0] = f / aspect
        projection_matrix[1, 1] = f
        projection_matrix[2, 2] = (far + near) / (near - far)
        projection_matrix[2, 3] = 2.0 * far * near / (near - far)
        projection_matrix[3, 2] = -1.0
        
        return projection_matrix
