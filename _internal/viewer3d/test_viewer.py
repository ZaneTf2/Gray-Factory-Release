import sys
from pathlib import Path
import logging
from datetime import datetime
import traceback
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QLabel, QSlider, QGroupBox, QFileDialog,
    QMessageBox
)
from PyQt6.QtCore import Qt, QSettings

import os

# Настройка логирования
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f"tf2_viewer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Добавляем родительскую директорию в путь для поиска модулей
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from viewer3d import TF2GLViewer
from viewer3d import Light
from viewer3d.assets.model_loader import ModelLoader
import numpy as np

class MainWindow(QMainWindow):
    # Стандартные цвета команд
    TEAM_COLORS = {
        'RED': (184/255, 56/255, 59/255),  # #B8383B
        'BLU': (88/255, 133/255, 162/255)  # #5885A2
    }

    def __init__(self):
        super().__init__()
        logger.info("Инициализация главного окна TF2 Model Viewer")
        self.setWindowTitle("TF2 Model Viewer")
        self.resize(1200, 800)
        
        # Текущая выбранная команда
        self.current_team = 'RED'
        
        # Создаем главный виджет
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Создаем горизонтальный layout
        layout = QHBoxLayout(main_widget)
        
        # Создаем виджет просмотра
        self.viewer = TF2GLViewer()
        layout.addWidget(self.viewer, stretch=2)
        
        # Создаем панель управления
        control_panel = self._create_control_panel()
        layout.addWidget(control_panel)
        
        # Создаем временную директорию для моделей
        self.temp_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                   "temp_models")
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
            logger.info(f"Создана временная директория: {self.temp_dir}")
        
        # Загружаем настройки
        self.settings = QSettings('GrayFactory', 'TF2ModelViewer')
        self.tf2_path = self.settings.value('tf2_path', '')
        logger.info(f"Загружен путь к TF2: {self.tf2_path}")
        
        # Если путь к TF2 не настроен, запрашиваем его
        if not self.tf2_path or not os.path.exists(self.tf2_path):
            logger.warning("Путь к TF2 не настроен или недействителен")
            self.select_tf2_directory()
        else:
            self.load_vpk_files()
            
        # Обновляем список моделей после загрузки VPK
        self.update_model_list()
            
        # Добавляем путь для извлеченных файлов
        extracted_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                    "extracted")
        if os.path.exists(extracted_path):
            self.viewer.asset_loader.add_search_path(extracted_path)
            logger.info(f"Добавлен путь для поиска: {extracted_path}")
            
    def select_tf2_directory(self):
        """Диалог выбора директории TF2"""
        logger.info("Открытие диалога выбора директории TF2")
        default_paths = [
            "C:/Program Files (x86)/Steam/steamapps/common/Team Fortress 2",
            "C:/Program Files/Steam/steamapps/common/Team Fortress 2"
        ]
        
        # Ищем существующий путь по умолчанию
        initial_path = next((path for path in default_paths if os.path.exists(path)), "C:/")
        logger.debug(f"Начальный путь для диалога: {initial_path}")
        
        # Открываем диалог выбора директории
        tf2_path = QFileDialog.getExistingDirectory(
            self,
            "Выберите директорию Team Fortress 2",
            initial_path,
            QFileDialog.Option.ShowDirsOnly
        )
        
        if tf2_path:
            logger.info(f"Выбрана директория TF2: {tf2_path}")
            self.tf2_path = tf2_path
            self.settings.setValue('tf2_path', tf2_path)
            self.load_vpk_files()
        else:
            logger.warning("Директория TF2 не выбрана")
            QMessageBox.warning(
                self,
                "Внимание",
                "Директория TF2 не выбрана. Некоторые функции могут быть недоступны."
            )
            
    def load_vpk_files(self):
        """Загрузка VPK файлов из директории TF2"""
        logger.info("Начало загрузки VPK файлов")
        tf2_dir = os.path.join(self.tf2_path, "tf")
        logger.debug(f"Директория TF2: {tf2_dir}")
        
        # Проверяем наличие необходимых VPK файлов
        misc_vpk = os.path.join(tf2_dir, "tf2_misc_dir.vpk")
        textures_vpk = os.path.join(tf2_dir, "tf2_textures_dir.vpk")
        
        vpk_files = []
        if os.path.exists(misc_vpk):
            vpk_files.append(("Модели (misc)", misc_vpk))
        if os.path.exists(textures_vpk):
            vpk_files.append(("Текстуры", textures_vpk))
            
        if not vpk_files:
            logger.error(f"VPK файлы не найдены в директории: {tf2_dir}")
            QMessageBox.critical(
                self,
                "Ошибка",
                f"VPK файлы не найдены в директории:\n{tf2_dir}\n\n"
                "Убедитесь, что выбрана правильная директория игры."
            )
            self.select_tf2_directory()
            return
            
        # Загружаем найденные VPK файлы
        for name, path in vpk_files:
            try:
                logger.info(f"Загрузка VPK файла: {path}")
                self.viewer.asset_loader.add_vpk(path)
                logger.info(f"VPK файл успешно загружен ({name}): {path}")
            except Exception as e:
                logger.error(f"Ошибка при загрузке VPK файла {path}: {str(e)}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                QMessageBox.warning(
                    self,
                    "Ошибка загрузки VPK",
                    f"Не удалось загрузить {name} VPK файл:\n{path}\n\nОшибка: {str(e)}"
                )
                
        # Обновляем список моделей после загрузки VPK
        self.update_model_list()

    def _create_control_panel(self) -> QWidget:
        """Создание панели управления"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Группа настройки TF2
        tf2_group = QGroupBox("Team Fortress 2")
        tf2_layout = QVBoxLayout(tf2_group)
        
        change_dir_button = QPushButton("Изменить директорию TF2")
        change_dir_button.clicked.connect(self.select_tf2_directory)
        tf2_layout.addWidget(change_dir_button)
        
        reload_vpk_button = QPushButton("Перезагрузить VPK файлы")
        reload_vpk_button.clicked.connect(self.load_vpk_files)
        tf2_layout.addWidget(reload_vpk_button)
        
        layout.addWidget(tf2_group)
        
        # Группа выбора команды
        team_group = QGroupBox("Команда")
        team_layout = QVBoxLayout(team_group)
        
        self.team_combo = QComboBox()
        self.team_combo.addItems(['RED', 'BLU'])
        self.team_combo.setCurrentText(self.current_team)
        self.team_combo.currentTextChanged.connect(self.on_team_changed)
        team_layout.addWidget(self.team_combo)
        
        layout.addWidget(team_group)
        
        # Группа выбора модели
        model_group = QGroupBox("Модель")
        model_layout = QVBoxLayout(model_group)
        
        self.model_combo = QComboBox()
        self.model_combo.addItems([""])
        model_layout.addWidget(self.model_combo)
        
        self.load_model_button = QPushButton("Загрузить модель")
        self.load_model_button.clicked.connect(self.load_selected_model)
        model_layout.addWidget(self.load_model_button)
        
        layout.addWidget(model_group)
        
        # Группа выбора текстуры
        texture_group = QGroupBox("Текстура")
        texture_layout = QVBoxLayout(texture_group)
        
        texture_combo = QComboBox()
        texture_combo.addItems(["red", "blue"])
        texture_combo.currentTextChanged.connect(self.viewer.set_texture_variant)
        texture_layout.addWidget(texture_combo)
        
        layout.addWidget(texture_group)
        
        # Группа настройки освещения
        light_group = QGroupBox("Освещение")
        light_layout = QVBoxLayout(light_group)
        
        # Интенсивность света
        intensity_layout = QHBoxLayout()
        intensity_layout.addWidget(QLabel("Интенсивность:"))
        intensity_slider = QSlider(Qt.Orientation.Horizontal)
        intensity_slider.setRange(0, 100)
        intensity_slider.setValue(50)
        intensity_slider.valueChanged.connect(
            lambda v: self.viewer.light_manager.set_intensity(v / 100.0)
        )
        intensity_layout.addWidget(intensity_slider)
        light_layout.addLayout(intensity_layout)
        
        # Фоновое освещение
        ambient_layout = QHBoxLayout()
        ambient_layout.addWidget(QLabel("Фоновое:"))
        ambient_slider = QSlider(Qt.Orientation.Horizontal)
        ambient_slider.setRange(0, 100)
        ambient_slider.setValue(20)
        ambient_slider.valueChanged.connect(
            lambda v: self.viewer.light_manager.set_ambient(v / 100.0)
        )
        ambient_layout.addWidget(ambient_slider)
        light_layout.addLayout(ambient_layout)
        
        # Диффузное освещение
        diffuse_layout = QHBoxLayout()
        diffuse_layout.addWidget(QLabel("Диффузное:"))
        diffuse_slider = QSlider(Qt.Orientation.Horizontal)
        diffuse_slider.setRange(0, 100)
        diffuse_slider.setValue(80)
        diffuse_slider.valueChanged.connect(
            lambda v: self.viewer.light_manager.set_diffuse(v / 100.0)
        )
        diffuse_layout.addWidget(diffuse_slider)
        light_layout.addLayout(diffuse_layout)
        
        layout.addWidget(light_group)
        
        # Растягивающийся пробел
        layout.addStretch()
        
        return panel

    def update_model_list(self):
        """Обновление списка доступных моделей"""
        if not hasattr(self, 'model_combo'):
            logger.warning("model_combo не инициализирован")
            return
            
        logger.info("Обновление списка моделей")
        self.model_combo.clear()
        
        # Поиск всех MDL файлов
        try:
            # Ищем только модели в директории bots
            models = self.viewer.asset_loader.find_files("models/bots/**/*.mdl")
            logger.info(f"Найдено {len(models)} моделей ботов")
            
            # Собираем информацию о моделях и их текстурах
            bot_models = []
            
            # Получаем список всех VPK
            vpk_readers = list(self.viewer.asset_loader._vpk_readers.values())
            texture_vpk = next((reader for reader in vpk_readers if "textures" in reader.vpk_path.lower()), None)
            
            for model_path in models:
                logger.debug(f"Обработка модели: {model_path}")
                
                # Используем индекс текстур для быстрой проверки
                model_base = f"materials/models/bots/{os.path.splitext(os.path.basename(model_path))[0]}"
                has_texture = model_base in self.viewer.asset_loader._texture_index
                
                # Добавляем модель в список с понятным именем
                model_name = os.path.basename(model_path)
                display_text = f"{model_name} {'[✓]' if has_texture else '[ ]'}"
                bot_models.append((model_path, display_text))
                logger.debug(f"Добавлена модель: {display_text}")
            
            # Сортируем модели по пути
            bot_models.sort(key=lambda x: x[0])
            
            # Добавляем отсортированные модели в комбобокс
            for model_path, display_text in bot_models:
                self.model_combo.addItem(display_text, model_path)
            
            logger.info(f"В список добавлено {len(bot_models)} моделей ботов")
            
        except Exception as e:
            logger.error(f"Ошибка при обновлении списка моделей: {str(e)}")
            logger.error(f"Traceback:\n{traceback.format_exc()}")
            QMessageBox.warning(
                self,
                "Ошибка",
                f"Не удалось обновить список моделей:\n{str(e)}"
            )

    def load_selected_model(self):
        """Загрузка выбранной модели"""
        if not self.model_combo.currentData():
            logger.warning("Не выбрана модель для загрузки")
            return
            
        # Получаем путь к модели без индикаторов
        model_path = self.model_combo.currentData()
        logger.info(f"Запуск загрузки модели: {model_path}")
        
        try:
            # Находим нужный VPK (с моделями)
            vpk_reader = None
            for reader in self.viewer.asset_loader._vpk_readers.values():
                if "misc" in reader.vpk_path.lower():
                    vpk_reader = reader
                    break
                    
            if not vpk_reader:
                raise RuntimeError("VPK с моделями не найден")
            
            # Создаем структуру временных директорий
            model_dir = os.path.dirname(model_path)
            temp_model_dir = os.path.join(self.temp_dir, model_dir)
            os.makedirs(temp_model_dir, exist_ok=True)
            
            # Формируем пути к файлам
            files_to_extract = {
                'mdl': (model_path, os.path.basename(model_path)),
                'vtx': (os.path.splitext(model_path)[0] + '.dx90.vtx',
                       os.path.basename(os.path.splitext(model_path)[0] + '.dx90.vtx')),
                'vvd': (os.path.splitext(model_path)[0] + '.vvd',
                       os.path.basename(os.path.splitext(model_path)[0] + '.vvd'))
            }
            
            extracted_files = {}
            
            # Извлекаем все необходимые файлы
            for file_type, (vpk_path, filename) in files_to_extract.items():
                temp_file = os.path.join(temp_model_dir, filename)
                try:
                    data = vpk_reader[vpk_path].read()
                    with open(temp_file, 'wb') as f:
                        f.write(data)
                    logger.info(f"{file_type.upper()} файл извлечен в: {temp_file}")
                    extracted_files[file_type] = temp_file
                except KeyError:
                    raise FileNotFoundError(f"{file_type.upper()} файл не найден в VPK: {vpk_path}")
                except Exception as e:
                    raise IOError(f"Ошибка при извлечении {file_type.upper()} файла: {str(e)}")

            # Проверяем извлеченные файлы
            for file_type, file_path in extracted_files.items():
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"Не найден извлеченный {file_type.upper()} файл: {file_path}")
                if os.path.getsize(file_path) == 0:
                    raise ValueError(f"Пустой {file_type.upper()} файл: {file_path}")

            # Загружаем модель используя ModelLoader
            logger.info("Создание загрузчика моделей")
            loader = ModelLoader()
            
            if not loader.load_model(extracted_files['mdl']):
                raise RuntimeError("Ошибка при загрузке модели через ModelLoader")
                
            # Получаем данные модели
            vertices, indices = loader.get_mesh_data()
            materials = loader.get_material_info()
            bones = loader.get_bones()
            
            # Проверяем полученные данные
            if vertices is None or indices is None:
                raise ValueError("Не удалось получить геометрию модели")
                
            if len(vertices) == 0 or len(indices) == 0:
                raise ValueError("Пустая геометрия модели")
                
            logger.info(f"Загружено: {len(vertices)} вершин, {len(indices)} индексов")
            logger.info(f"Материалов: {len(materials)}, костей: {len(bones) if bones else 0}")
            
            # Передаем данные в просмотрщик
            if self.viewer.set_model_data(vertices, indices, materials, bones):
                # Применяем цвет текущей команды
                self.on_team_changed(self.current_team)
                logger.info("Модель успешно загружена")
            else:
                raise RuntimeError("Ошибка при установке данных модели в просмотрщик")
                
        except Exception as e:
            logger.error(f"Ошибка при загрузке модели {model_path}: {str(e)}")
            logger.error("Подробная информация об ошибке:")
            logger.error(traceback.format_exc())
            QMessageBox.warning(
                self,
                "Ошибка загрузки",
                f"Ошибка при загрузке модели {model_path}:\n{str(e)}\n\n"
                "Проверьте лог-файл для получения дополнительной информации."
            )

    def on_team_changed(self, team: str):
        """Обработчик изменения команды"""
        logger.info(f"Смена команды на: {team}")
        self.current_team = team
        
        # Если модель загружена, применяем цвет команды
        if hasattr(self, 'viewer') and self.viewer.current_model:
            color = self.TEAM_COLORS[team]
            logger.info(f"Применение цвета команды: {color}")
            self.viewer.set_model_color(color)
            self.viewer.update()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
