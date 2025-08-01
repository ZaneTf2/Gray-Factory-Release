# === Стандартные библиотеки Python ===
import shutil
import sys
import os
import random
import json

# === PyQt6 и связанные библиотеки ===
from PyQt6 import QtCore, QtGui, QtWidgets

# === Работа с изображениями ===
from PIL import Image, ImageQt

# === Работа с файлами и диалогами ===
from tkinter import Tk, filedialog, messagebox
from tkinter import filedialog as fd 
from pathlib import Path

# === Работа c мышью ===
import keyboard

# === Импорт ресурсов и библиотек приложения ===
from resources import resources
from Pathes import SystemPath
_systemPath = SystemPath()

import weapons_libary
import atribute_libary
import default_mercenary as default_stat
from Icons_Archive import icons as Icons_Archive
from TemplateLibary import Template, find_robot_by_name
from colorpicker import ColorPicker

# === Импорт конкретных структур из библиотек ===
from atribute_libary import Atribute
from weapons_libary import Weapon_Libary

# === Работа с 3D сценой ===
from viewer import ModelViewer

# === Импорт интерфейсов и окон приложения ===
from typing import Dict, List, Any, Optional
from pop_file_parser.parser import Mission
from pop_file_parser.valve_parser import ValveFormat

# === Работа с парсингом игровых файлов ===
from tf2_items_parser import TF2ItemsParser
from vtf2img_lib import parser as vtf2img_parser
import vpk

class windowColor(object):
    global SquadSettingsGlobal
    def __init__(self):
        self.setupUi()
        
    def selectColor(self):
        # get current color wit getColor() method
        r,g,b = self.colorpicker.getRGB()
        h,s,v = self.colorpicker.getHSV()

        hsv = self.colorpicker.getHSV(360, 1)  # hue in degrees, saturation & value from 0 to 1
        rgb = self.colorpicker.getRGB(100)     # rgb with white = (100,100,100)
        hex = self.colorpicker.getHex(True)    # output with hashtag in string

        squad = SquadSettingsGlobal
        squad.SquadList[squad.curLocalSquad]["Color"]["rgb"] = ((r,g,b)) 
        squad.ColorUpdate(squad.SquadList[squad.curLocalSquad])
        self.GroupBox.close()
        #self.selected_color_frame.setStyleSheet(f"background-color: rgb({r},{g},{b})")

    def onColorChange(self):
        self.colorpicker.getHex(True)
        
    def setupUi(self):
        GroupBox = QtWidgets.QMainWindow()
        self.GroupBox = GroupBox
        GroupBox.setWindowTitle("Pick Color")
        GroupBox.setObjectName("ColorPick")
        GroupBox.resize(400, 200)
        
        GroupBox.setStyleSheet("QLabel{color: rgb(255, 255, 255);}")
        
        self.centralwidget = QtWidgets.QWidget(GroupBox)
        self.centralwidget.setStyleSheet("background-color: #202020;")
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.right_panel = QtWidgets.QFrame(self.centralwidget)
        self.right_panel.setStyleSheet("QFrame{    background-color: #303030;    border-radius: 10px;}")
        self.right_panel.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.right_panel.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.right_panel.setObjectName("right_panel")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.right_panel)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.right_panel)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("TF2 Secondary")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        
        self.verticalLayout.addWidget(self.label_2)
        self.colorpicker_area = QtWidgets.QFrame(self.right_panel)
        self.colorpicker_area.setMaximumSize(QtCore.QSize(16777215, 220))
        self.colorpicker_area.setStyleSheet("background-color: #222;")
        self.colorpicker_area.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.colorpicker_area.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.colorpicker_area.setObjectName("colorpicker_area")
        
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.colorpicker_area)
        
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        
        self.colorpicker_frame = QtWidgets.QFrame(self.colorpicker_area)
        self.colorpicker_frame.setMinimumSize(QtCore.QSize(360, 200))
        self.colorpicker_frame.setMaximumSize(QtCore.QSize(360, 200))
        self.colorpicker_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.colorpicker_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.colorpicker_frame.setObjectName("colorpicker_frame")
        
        squad = SquadSettingsGlobal
        self.colorpicker = ColorPicker(self.colorpicker_frame, rgb=squad.SquadList[squad.curLocalSquad]["Color"]["rgb"])

        # the colorpicker handle is a bit dark and blends in with the bg, let's change it:
        self.colorpicker.ui.hue_selector.setStyleSheet("background-color: #aaa")
        
        self.horizontalLayout_2.addWidget(self.colorpicker_frame)
        self.verticalLayout.addWidget(self.colorpicker_area)
        self.pushButton = QtWidgets.QPushButton(self.right_panel)
        font = QtGui.QFont()
        font.setFamily("TF2")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton{font: 9pt \"TF2 Secondary\";background-color: none;    color: #fff;    border: 4px solid #aaa;    border-radius: 10px;}QPushButton:hover{    background-color: #aaa;    border: 4px solid #aaa;    color: #000;}QPushButton:pressed{    background-color: #666;    color: #000;    border: 4px solid #666;}")
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        
        #self.picked_color_lbl = QtWidgets.QLabel(self.right_panel)
        #self.picked_color_lbl.setStyleSheet("")
        #self.picked_color_lbl.setObjectName("picked_color_lbl")
        #self.verticalLayout.addWidget(self.picked_color_lbl)
        
        #self.selected_color_frame = QtWidgets.QFrame(self.right_panel)
        #self.selected_color_frame.setMinimumSize(QtCore.QSize(0, 100))
        #self.selected_color_frame.setMaximumSize(QtCore.QSize(16777215, 16777215))
        #self.selected_color_frame.setStyleSheet("background-color: rgb(0, 85, 255);")
        #self.selected_color_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        #self.selected_color_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        #self.selected_color_frame.setObjectName("selected_color_frame")
        #self.verticalLayout.addWidget(self.selected_color_frame)
        
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addWidget(self.right_panel, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        GroupBox.setCentralWidget(self.centralwidget)
        self.actiontest = QtWidgets.QWidgetAction(GroupBox)
        self.actiontest.setObjectName("actiontest")
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(GroupBox)
        global Addition_interface
        Addition_interface = GroupBox
        
        GroupBox.show()
        
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_2.setText(_translate("MainWindow", "Pick a Color here"))
        self.pushButton.setText(_translate("MainWindow", "Select Color"))
        # self.picked_color_lbl.setText(_translate("MainWindow", "  Picked Color:"))
        self.actiontest.setText(_translate("MainWindow", "test"))
        
        # connect custom Button to display currently selected color
        self.pushButton.clicked.connect(lambda: self.selectColor())
        # using ColorPicker's colorChanged signal:
        self.colorpicker.colorChanged.connect(lambda: self.onColorChange())

class Ui_MainWindow(object):
    global General_Information_Robot
    global WaveManagerGlobal
    global InitSettingsGlobal
    global generalGlobal

    def __init__(self):
        super().__init__()
        self.GenerateWindow()
        
        self.GeneralInterface(self.Main)
        
        self.GeneralMissionSettings()
        self.GeneralWaveSettings()
        self.WaveSettingsRuntime()
        
        self.SquadControll = SquadSettings()
        self.SquadSettingsRuntime()
        self.SquadInWaveRuntime()
        
        self.ModelViewRuntime()
        
        self.MercenarySettingsRuntime()
        self.MercenaryAttributesRuntimeSettings()
        self.MercenaryWeaponsRuntime()
        self.MercenaryCosmeticsRuntime()
        self.MercenaryAttributesRuntime()
        
        self.BindHotKeys()
        
        self.retranslateUi(self.Main)
        
        WaveManagerGlobal.addWave("Wave 1")
        WaveManagerGlobal.setWave("Wave 1")
        
        QtCore.QMetaObject.connectSlotsByName(self.Main)
        self.Main.show()
        
    def GenerateWindow(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.Main = QtWidgets.QMainWindow()
        
    def GeneralInterface(self, MainWindow):    
        self.Main.setObjectName("MainWindow")
        self.Main.resize(1858, 1050)
        self.Main.setMinimumSize(QtCore.QSize(1858, 1050))
        self.Main.setBaseSize(QtCore.QSize(1858, 1050))
        self.Main.setAutoFillBackground(False)
        self.Main.setStyleSheet("color:white; font: 11pt \"TF2\";")

        self.Main.setWindowIcon(QtGui.QIcon(_systemPath.get("icon_gray_factory.png", 'icon')))
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")  
        self.MainWindow = MainWindow
        
        self.Background = QtWidgets.QLabel(parent=self.centralwidget)
        self.Background.setEnabled(True)
        self.Background.setGeometry(QtCore.QRect(0, 0, 1860, 1058))
        self.Background.setMaximumSize(QtCore.QSize(1860, 1058))
        self.Background.setAcceptDrops(False)
        self.Background.setAutoFillBackground(False)
        self.Background.setPixmap(ImageQt.toqpixmap(Image.open(_systemPath.get('Background',"Backgrounds"))))
        self.Background.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        self.Background.setScaledContents(True)
        self.Background.setObjectName("Background")           
    
    def GeneralMissionSettings(self):
        self.startUpMoney_text = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.startUpMoney_text.setGeometry(QtCore.QRect(50, 10, 80, 23))
        self.startUpMoney_text.setStyleSheet("background-color: rgb(48, 48, 48);\n"
                                            "border-radius: 5px;\n"
                                            "color: rgb(0, 255, 17);\n"
                                            "font: 11pt \"TF2\";")
        self.startUpMoney_text.setObjectName("startUpMoney_text")
        self.startUpMoney_text.setValidator(QtGui.QIntValidator())

        InitSettingsGlobal.addButton(name="startUpMoney_text", param= self.startUpMoney_text)
        
        self.Image_StartUpCredit = QtWidgets.QLabel(parent=self.centralwidget)
        self.Image_StartUpCredit.setGeometry(QtCore.QRect(8, 6, 40, 30))
        self.Image_StartUpCredit.setStyleSheet(f"border-image: url({ _systemPath.get('Smallcredits.png') })")
        
        InitSettingsGlobal.addButton(name = "Image_StartUpCredit", param = self.Image_StartUpCredit)
        
        self.fixedRespawn_text = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.fixedRespawn_text.setGeometry(QtCore.QRect(182, 10, 80, 23))
        self.fixedRespawn_text.setStyleSheet("background-color: rgb(48, 48, 48);border-radius: 5px;font: 11pt \"TF2\";")
        self.fixedRespawn_text.setObjectName("fixedRespawn_text")
        self.fixedRespawn_text.setText("5")
        generalGlobal.buttonAdd(name = "fixedRespawn_text", param = self.fixedRespawn_text)
        
    def WaveSettingsRuntime(self):
        self.WaveSettings_discription = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.WaveSettings_discription.setGeometry(QtCore.QRect(110, 602, 201, 20))
        self.WaveSettings_discription.setStyleSheet("background-color: rgb(58, 58, 58); border-radius: 5px;")
        self.WaveSettings_discription.setObjectName("WaveSettings_discription")
        
        WaveManagerGlobal.AddButton(name = "WaveSettings_discription", param = self.WaveSettings_discription)
        
        self.WaveSettings_sound = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.WaveSettings_sound.setGeometry(QtCore.QRect(73, 627, 200, 20))
        self.WaveSettings_sound.setStyleSheet("background-color: rgb(58, 58, 58);border-radius: 5px;")
        self.WaveSettings_sound.setObjectName("WaveSettings_sound")
        
        WaveManagerGlobal.AddButton(name = "WaveSettings_sound", param = self.WaveSettings_sound)
                
        self.mapName_text = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.mapName_text.setGeometry(QtCore.QRect(1240, 8, 181, 23))
        self.mapName_text.setStyleSheet("background-color: rgb(48, 48, 48);border-radius: 5px;font: 11pt \"TF2\";")
        self.mapName_text.setObjectName("mapName_text")
        
        self.mapName_text.setText("coal_town")
        
        generalGlobal.buttonAdd("mapName_text", self.mapName_text)
        
        self.MissionName_text = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.MissionName_text.setGeometry(QtCore.QRect(550, 8, 160, 23))
        self.MissionName_text.setStyleSheet("background-color: rgb(48, 48, 48);border-radius: 5px;font: 11pt \"TF2\";")
        self.MissionName_text.setObjectName("MissionName_text")
        self.MissionName_text.setText("normal")
        
        generalGlobal.buttonAdd("MissionName_text", self.MissionName_text)
              
        self.WaveSelect_text = QtWidgets.QLabel(parent=self.centralwidget)
        self.WaveSelect_text.setGeometry(QtCore.QRect(840, 10, 181, 41))
        self.WaveSelect_text.setStyleSheet("font: 16pt \"TF2 Build\";")
        self.WaveSelect_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.WaveSelect_text.setObjectName("WaveSelect_text")
        
        WaveManagerGlobal.AddComponent(name = "WaveSelect_text", param = self.WaveSelect_text)
        self.CountingForWave_PreviousWave = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.CountingForWave_PreviousWave.setGeometry(QtCore.QRect(552, 918, 91, 17))
        self.CountingForWave_PreviousWave.setStyleSheet("background-color: rgb(58, 58, 58);border-radius: 5px;color: rgb(255, 153, 0);")
        self.CountingForWave_PreviousWave.setObjectName("CountingForWave_PreviousWave")
        
        WaveManagerGlobal.AddButton(name = "CountingForWave_PreviousWave", param = self.CountingForWave_PreviousWave)
        
        self.CountingForWave_AllRobots = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.CountingForWave_AllRobots.setGeometry(QtCore.QRect(560, 945, 81, 17))
        self.CountingForWave_AllRobots.setStyleSheet("background-color: rgb(58, 58, 58);border-radius: 5px;color: rgb(196, 255, 29);")
        self.CountingForWave_AllRobots.setObjectName("CountingForWave_AllRobots")
        
        WaveManagerGlobal.AddButton(name = "CountingForWave_AllRobots", param = self.CountingForWave_AllRobots)
        
        self.CountingForWave_ForNextWave = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.CountingForWave_ForNextWave.setGeometry(QtCore.QRect(543, 974, 91, 17))
        self.CountingForWave_ForNextWave.setStyleSheet("background-color: rgb(58, 58, 58);border-radius: 5px;color: rgb(29, 255, 51);")
        self.CountingForWave_ForNextWave.setObjectName("CountingForWave_ForNextWave")
        
        WaveManagerGlobal.AddButton(name = "CountingForWave_ForNextWave", param = self.CountingForWave_ForNextWave)
        
        self.CountingForWave_CountingRobots = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.CountingForWave_CountingRobots.setGeometry(QtCore.QRect(791, 966, 91, 17))
        self.CountingForWave_CountingRobots.setStyleSheet("background-color: rgb(58, 58, 58);border-radius: 5px;")
        self.CountingForWave_CountingRobots.setObjectName("CountingForWave_CountingRobots")
        self.CountingForWave_CountingGiantRobots = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.CountingForWave_CountingGiantRobots.setGeometry(QtCore.QRect(790, 941, 81, 17))
        self.CountingForWave_CountingGiantRobots.setStyleSheet("background-color: rgb(58, 58, 58);border-radius: 5px;")
        self.CountingForWave_CountingGiantRobots.setObjectName("CountingForWave_CountingGiantRobots")
        
        WaveManagerGlobal.AddButton(name = "CountingForWave_CountingGiantRobots", param = self.CountingForWave_CountingGiantRobots)
        
        self.CountingForWave_CountAllRobots = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.CountingForWave_CountAllRobots.setGeometry(QtCore.QRect(742, 916, 91, 17))
        self.CountingForWave_CountAllRobots.setStyleSheet("background-color: rgb(58, 58, 58);border-radius: 5px;")
        self.CountingForWave_CountAllRobots.setObjectName("CountingForWave_CountAllRobots")
        
        WaveManagerGlobal.AddButton(name = "CountingForWave_CountAllRobots", param = self.CountingForWave_CountAllRobots)
        
        self.load_mission_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.load_mission_button.setGeometry(QtCore.QRect(760, 72, 91, 26))
        self.load_mission_button.setMinimumSize(QtCore.QSize(70, 26))
        self.load_mission_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.load_mission_button.setStyleSheet("QPushButton{background-color: rgb(48, 48, 48);font: 9pt \"TF2 Build\";border-bottom-left-radius: 7px;border-bottom-right-radius: 7px;}QPushButton:hover{background-color: rgb(64, 64, 64);}")
        self.load_mission_button.setCheckable(True)
        self.load_mission_button.setObjectName("load_mission_button")
        self.load_mission_button.clicked.connect(lambda: SaveManagerGlobal.Load())
                
        self.clearAllMission = QtWidgets.QPushButton(parent=self.centralwidget)
        self.clearAllMission.setGeometry(QtCore.QRect(720, 0, 113, 30))
        self.clearAllMission.setMinimumSize(QtCore.QSize(70, 26))
        self.clearAllMission.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.clearAllMission.setStyleSheet("QPushButton{background-color: rgb(64, 64, 64);font: 9pt \"TF2 Build\";border-bottom-left-radius: 7px;border-bottom-right-radius: 7px;}QPushButton:hover{background-color: rgb(70, 70, 70);}")
        self.clearAllMission.setCheckable(True)
        self.clearAllMission.setObjectName("clearAllMission")
        self.clearAllMission.clicked.connect(lambda: WaveManagerGlobal.clearAll())
        
        self.clear_cur_mission = QtWidgets.QPushButton(parent=self.centralwidget)
        self.clear_cur_mission.setGeometry(QtCore.QRect(1028, 0, 113, 30))
        self.clear_cur_mission.setMinimumSize(QtCore.QSize(70, 26))
        self.clear_cur_mission.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.clear_cur_mission.setStyleSheet("QPushButton{background-color: rgb(64, 64, 64);font: 9pt \"TF2 Build\";border-bottom-left-radius: 7px;border-bottom-right-radius: 7px;}QPushButton:hover{background-color: rgb(70, 70, 70);}")
        self.clear_cur_mission.setCheckable(True)
        self.clear_cur_mission.setObjectName("clearAllMission")
        self.clear_cur_mission.clicked.connect(lambda: WaveManagerGlobal.removeCurrentWave())

        self.exportProjectButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.exportProjectButton.setGeometry(QtCore.QRect(860, 72, 131, 26))
        self.exportProjectButton.setMinimumSize(QtCore.QSize(70, 26))
        self.exportProjectButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.exportProjectButton.setStyleSheet("QPushButton{background-color: rgb(48, 48, 48);font: 9pt \"TF2 Build\";border-bottom-left-radius: 7px;border-bottom-right-radius: 7px;}QPushButton:hover{background-color: rgb(64, 64, 64);}")
        self.exportProjectButton.setCheckable(True)
        self.exportProjectButton.setObjectName("exportProjectButton")
        
        generalGlobal.bindExportButton(self.exportProjectButton)

        self.generateMissionRandom = QtWidgets.QPushButton(parent=self.centralwidget)
        self.generateMissionRandom.setGeometry(QtCore.QRect(1100, 72, 131, 26))
        self.generateMissionRandom.setMinimumSize(QtCore.QSize(70, 26))
        self.generateMissionRandom.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.generateMissionRandom.setStyleSheet("QPushButton{background-color: rgb(48, 48, 48);font: 9pt \"TF2 Build\";border-bottom-left-radius: 7px;border-bottom-right-radius: 7px;}QPushButton:hover{background-color: rgb(64, 64, 64);}")
        self.generateMissionRandom.setCheckable(True)
        self.generateMissionRandom.setObjectName("generateMissionRandom")
        
        generator_window = MissionGeneratorWindow()
        self.generateMissionRandom.clicked.connect(lambda: generator_window.show())
        
        self.pushButton_9 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_9.setGeometry(QtCore.QRect(1000, 72, 91, 26))
        self.pushButton_9.setMinimumSize(QtCore.QSize(70, 26))
        self.pushButton_9.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.pushButton_9.setStyleSheet("QPushButton{background-color: rgb(48, 48, 48);font: 9pt \"TF2 Build\";border-bottom-left-radius: 7px;border-bottom-right-radius: 7px;}QPushButton:hover{background-color: rgb(64, 64, 64);}")
        self.pushButton_9.setCheckable(True)
        self.pushButton_9.setObjectName("pushButton_9")
        
        global SaveManagerGlobal
        self.pushButton_9.clicked.connect(lambda: SaveManagerGlobal.Save())
        
        self.Main.setCentralWidget(self.centralwidget)
        
        global _AddButtonInWaveList
        _AddButtonInWaveList = AddButtonInWaveList(self.horizontalLayout_4, self.horizontalLayout_3, self.scrollAreaWidgetContents_7, self.verticalLayout_9)        
        
    def GeneralWaveSettings(self):
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(parent=self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(560, 40, 261, 31))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.Wave_list_scrollbar_1 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.Wave_list_scrollbar_1.setContentsMargins(5, 0, 0, 0)
        self.Wave_list_scrollbar_1.setObjectName("Wave_list_scrollbar_1")
        
        WaveManagerGlobal.AddComponent(name = "horizontalLayoutWidget_3", param = self.horizontalLayoutWidget_3)
        WaveManagerGlobal.AddComponent(name = "Wave_list_scrollbar_1", param = self.Wave_list_scrollbar_1)             

        self.InWave_List = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.InWave_List.setGeometry(QtCore.QRect(10, 115, 870, 78))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.InWave_List.sizePolicy().hasHeightForWidth())
        self.InWave_List.setSizePolicy(sizePolicy)
        
        font = QtGui.QFont()
        font.setFamily("TF2")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setKerning(True)
        
        self.InWave_List.setFont(font)
        self.InWave_List.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.InWave_List.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.InWave_List.setAcceptDrops(False)
        self.InWave_List.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.InWave_List.setAutoFillBackground(True)
        self.InWave_List.setStyleSheet("QWidget{background-color: rgba(255, 255, 255, 0);border:0;}:handle, QWidget:horizontal  {    border-radius: 1px;    background-color: rgb(86, 86, 86);    height: 10px;}:handle, QWidget:verical  {    border-radius: 5px;    background-color: rgb(86, 86, 86);}:sub-line, QWidget:vertical{    background-color: rgba(51, 51, 51, 0);}:add-line, QWidget:horizontal{    background-color: rgba(255, 255, 255, 0);}QWidget::add-page:horizontal, QWidget::sub-page:horizontal {    background-color: rgb(51, 51, 51, 0);}QWidget::add-page:vertical, QWidget::sub-page:vertical {    background-color: rgb(51, 51, 51, 0);}")
        self.InWave_List.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.InWave_List.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.InWave_List.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.InWave_List.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.InWave_List.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.InWave_List.setWidgetResizable(True)
        self.InWave_List.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.InWave_List.setObjectName("InWave_List")
        
        self.scrollAreaWidgetContents_7 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_7.setGeometry(QtCore.QRect(0, 0, 882, 95))
        self.scrollAreaWidgetContents_7.setObjectName("scrollAreaWidgetContents_7")
        
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_7)
        self.verticalLayout_9.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.InWave_List.setWidget(self.scrollAreaWidgetContents_7)   
             
        self.WaveList_scrollbar_2 = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.WaveList_scrollbar_2.setGeometry(QtCore.QRect(1035, 40, 251, 31))
        self.WaveList_scrollbar_2.setStyleSheet("QWidget{background-color: rgba(0, 0, 0, 0);border:0;}:handle, QWidget:vertical  {    border-radius: 5px;    background-color: rgb(86, 86, 86);    width: 10px;    min-height: 30px;    max-width: 50px;}:handle, QWidget:horizontal  {    border-radius: 5px;    background-color: rgb(86, 86, 86);    width: 7px;    min-width: 10px;    max-width: 10px;}:sub-line, QWidget:vertical{    background-color: rgba(51, 51, 51, 255);}:add-line, QWidget:vertical{    background-color: rgba(0, 0, 0, 0);}QWidget::add-page:horizontal, QWidget::sub-page:horizontal {    background: none;}QWidget::add-page:vertical, QWidget::sub-page:vertical {    background: none;}")
        self.WaveList_scrollbar_2.setWidgetResizable(True)
        self.WaveList_scrollbar_2.setObjectName("WaveList_scrollbar_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 251, 31))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(parent=self.scrollAreaWidgetContents_2)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(0, 0, 251, 31))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.Wave_lits_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.Wave_lits_2.setContentsMargins(5, 0, 0, 0)
        self.Wave_lits_2.setObjectName("Wave_lits_2")
        #spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        #self.Wave_lits_2.addItem(spacerItem2)
        self.WaveList_scrollbar_2.setWidget(self.scrollAreaWidgetContents_2)
        
        WaveManagerGlobal.AddComponent(name = "horizontalLayoutWidget_4", param = self.horizontalLayoutWidget_4)
        WaveManagerGlobal.AddComponent(name = "Wave_lits_2", param = self.Wave_lits_2)

        self.scrollArea_2 = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.scrollArea_2.setGeometry(QtCore.QRect(10, 650, 301, 381))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_2.sizePolicy().hasHeightForWidth())
        self.scrollArea_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("TF2")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setKerning(True)
        self.scrollArea_2.setFont(font)
        self.scrollArea_2.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.scrollArea_2.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.scrollArea_2.setAcceptDrops(False)
        self.scrollArea_2.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.scrollArea_2.setAutoFillBackground(True)
        self.scrollArea_2.setStyleSheet("QWidget{    background-color: rgba(0, 0, 0, 0);    border:0;}:handle, QWidget:vertical  {    border-radius: 10px;    background-color: rgb(86, 86, 86);    width: 10px;    min-height: 30px;    max-width: 50px;}:handle, QWidget:horizontal  {    border-radius: 5px;    background-color: rgb(86, 86, 86);    width: 5px;    min-width: 10px;    max-width: 10px;}:sub-line, QWidget:vertical{    background-color: rgba(51, 51, 51, 255);}:add-line, QWidget:vertical{    background-color: rgba(255, 255, 255, 0);}QWidget::add-page:horizontal, QWidget::sub-page:horizontal {    background-color: rgb(51, 51, 51);}QWidget::add-page:vertical, QWidget::sub-page:vertical {    background-color: rgb(51, 51, 51);}")
        self.scrollArea_2.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.scrollArea_2.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.scrollArea_2.setLineWidth(0)
        self.scrollArea_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 291, 606))
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_4)
        self.verticalLayout_6.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.StartWaveInput = QtWidgets.QGroupBox(parent=self.scrollAreaWidgetContents_4)
        self.StartWaveInput.setMinimumSize(QtCore.QSize(0, 140))
        self.StartWaveInput.setMaximumSize(QtCore.QSize(16777215, 210))
        self.StartWaveInput.setStyleSheet("font: 10pt \"TF2 Build\";border:0;")
        self.StartWaveInput.setObjectName("StartWaveInput")

        self.textEdit = QtWidgets.QTextEdit(parent=self.StartWaveInput)
        self.textEdit.setGeometry(QtCore.QRect(9, 20, 261, 120))
        self.textEdit.setMinimumSize(QtCore.QSize(0, 120))
        self.textEdit.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CursorShape.IBeamCursor))
        self.textEdit.setStyleSheet("background-color: rgb(56, 56, 56);border-radius: 10px; font: 9pt \'TF2\';")
        self.textEdit.setTabStopDistance(15)
        self.textEdit.setObjectName("textEdit")
           
        WaveManagerGlobal.AddButton(name = "StartWaveOutput", param = self.textEdit)   
             
        self.verticalLayout_3.addWidget(self.StartWaveInput)
        self.InitWaveOutPut = QtWidgets.QGroupBox(parent=self.scrollAreaWidgetContents_4)
        self.InitWaveOutPut.setMinimumSize(QtCore.QSize(0, 140))
        self.InitWaveOutPut.setStyleSheet("font: 10pt \"TF2 Build\"; border:0;")
        self.InitWaveOutPut.setObjectName("InitWaveOutPut")
        self.textEdit_3 = QtWidgets.QTextEdit(parent=self.InitWaveOutPut)
        self.textEdit_3.setGeometry(QtCore.QRect(9, 20, 261, 122))
        self.textEdit_3.setMinimumSize(QtCore.QSize(0, 120))
        self.textEdit_3.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CursorShape.IBeamCursor))
        self.textEdit_3.setStyleSheet("background-color: rgb(56, 56, 56);border-radius: 10px; font: 9pt \'TF2\';")
        self.textEdit_3.setObjectName("textEdit_3")
        self.textEdit_3.setTabStopDistance(15)

        WaveManagerGlobal.AddButton(name = "InitWaveOutput", param = self.textEdit_3)

        self.verticalLayout_3.addWidget(self.InitWaveOutPut)
        self.DoneOutPut = QtWidgets.QGroupBox(parent=self.scrollAreaWidgetContents_4)
        self.DoneOutPut.setMinimumSize(QtCore.QSize(0, 140))
        self.DoneOutPut.setMaximumSize(QtCore.QSize(16777215, 210))
        self.DoneOutPut.setStyleSheet("font: 10pt \"TF2 Build\";border:0;")
        self.DoneOutPut.setObjectName("DoneOutPut")
        self.textEdit_4 = QtWidgets.QTextEdit(parent=self.DoneOutPut)
        self.textEdit_4.setGeometry(QtCore.QRect(9, 20, 261, 122))
        self.textEdit_4.setMinimumSize(QtCore.QSize(0, 120))
        self.textEdit_4.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CursorShape.IBeamCursor))
        self.textEdit_4.setStyleSheet("background-color: rgb(56, 56, 56);border-radius: 10px; font: 9pt \'TF2\';")
        self.textEdit_4.setObjectName("textEdit_4")
        self.textEdit_4.setTabStopDistance(15)

        WaveManagerGlobal.AddButton(name = "DoneOutput", param = self.textEdit_4)

        self.verticalLayout_3.addWidget(self.DoneOutPut)
        self.DoneOutPut_2 = QtWidgets.QGroupBox(parent=self.scrollAreaWidgetContents_4)
        self.DoneOutPut_2.setMinimumSize(QtCore.QSize(0, 140))
        self.DoneOutPut_2.setMaximumSize(QtCore.QSize(16777215, 210))
        self.DoneOutPut_2.setStyleSheet("font: 10pt \"TF2 Build\";border:0;")
        self.DoneOutPut_2.setObjectName("DoneOutPut_2")
        self.textEdit_5 = QtWidgets.QTextEdit(parent=self.DoneOutPut_2)
        self.textEdit_5.setGeometry(QtCore.QRect(9, 20, 261, 122))
        self.textEdit_5.setMinimumSize(QtCore.QSize(0, 120))
        self.textEdit_5.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CursorShape.IBeamCursor))
        self.textEdit_5.setStyleSheet("background-color: rgb(56, 56, 56);border-radius: 10px; font: 9pt \'TF2\';")
        self.textEdit_5.setObjectName("textEdit_5")
        self.textEdit_5.setTabStopDistance(15)

        WaveManagerGlobal.AddButton(name = "Custom", param = self.textEdit_5)
        
    def ModelViewRuntime(self):
        global ModelViewRuntime
        ModelViewRuntime = None
        self.AnchorForModel = QtWidgets.QLabel(parent=self.centralwidget)
        self.AnchorForModel.setGeometry(QtCore.QRect(1420, 180, 410, 800))
        self.AnchorForModel.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        # Create central widget and layout
        ModelViewRuntime = ModelViewer()
        central_widget = self.AnchorForModel
        layout = QtWidgets.QVBoxLayout(central_widget)

        # Add the 3D viewer
        layout.addWidget(ModelViewRuntime)
        
    def SquadSettingsRuntime(self):
        self.Squad_Name = QtWidgets.QComboBox(parent=self.centralwidget)
        self.Squad_Name.setGeometry(QtCore.QRect(80, 340, 200, 17))
        self.Squad_Name.setStyleSheet("background-color: rgb(58, 58, 58); border-radius: 5px;")
        self.Squad_Name.setObjectName("Squad_Name")
        self.Squad_Name.setEditable(True)
        
        self.SquadControll.AdditionButton(name = "Squad Name", param = self.Squad_Name)

        self.totalSquad_text = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.totalSquad_text.setGeometry(QtCore.QRect(186, 406, 151, 17))
        self.totalSquad_text.setStyleSheet("background-color: rgb(58, 58, 58);border-radius: 5px;")
        self.totalSquad_text.setObjectName("totalSquad_text")
        
        self.SquadControll.AdditionButton(name = "totalSquad_text", param = self.totalSquad_text)
        
        self.CreditForSquad_text = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.CreditForSquad_text.setGeometry(QtCore.QRect(169, 496, 165, 20))
        self.CreditForSquad_text.setStyleSheet("background-color: rgb(58, 58, 58);border-radius: 5px;color: rgb(29, 255, 51);")
        self.CreditForSquad_text.setObjectName("CreditForSquad_text")
        
        self.SquadControll.AdditionButton(name = "CreditForSquad_text", param = self.CreditForSquad_text)
        
        self.CreditSquadOneRobot_text = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.CreditSquadOneRobot_text.setGeometry(QtCore.QRect(170, 527, 165, 20))
        self.CreditSquadOneRobot_text.setStyleSheet("background-color: rgb(58, 58, 58);\n"
                    "border-radius: 5px;\n"
                    "color: rgb(196, 255, 29);")
        self.CreditSquadOneRobot_text.setObjectName("CreditSquadOneRobot_text")
        
        self.SquadControll.AdditionButton(name = "CreditSquadOneRobot_text", param = self.CreditSquadOneRobot_text)
        
        self.maxAlive_squad_text = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.maxAlive_squad_text.setGeometry(QtCore.QRect(186, 430, 151, 17))
        self.maxAlive_squad_text.setStyleSheet("background-color: rgb(58, 58, 58); border-radius: 5px;")
        self.maxAlive_squad_text.setObjectName("maxAlive_squad_text")
        
        self.SquadControll.AdditionButton(name = "maxAlive_squad_text", param = self.maxAlive_squad_text)
        
        self.SquadSpawnCount_text = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.SquadSpawnCount_text.setGeometry(QtCore.QRect(186, 456, 151, 17))
        self.SquadSpawnCount_text.setStyleSheet("background-color: rgb(58, 58, 58); border-radius: 5px;")
        self.SquadSpawnCount_text.setObjectName("SquadSpawnCount_text")
        
        self.SquadControll.AdditionButton(name = "SquadSpawnCount_text", param = self.SquadSpawnCount_text)        
        
        self.WaitForAll_spawn_text = QtWidgets.QComboBox(parent=self.centralwidget)
        self.WaitForAll_spawn_text.setGeometry(QtCore.QRect(621, 341, 110, 16))
        self.WaitForAll_spawn_text.setStyleSheet("background-color: rgb(58, 58, 58);border-radius: 5px;")
        self.WaitForAll_spawn_text.setObjectName("WaitForAll_spawn_text")
        self.WaitForAll_spawn_text.addItem("")
        self.WaitForAll_spawn_text.setEditable(True)
        
        self.SquadControll.AdditionButton(name = "WaitForAll_spawn_text", param = self.WaitForAll_spawn_text)
        
        self.WaitForAll_dead_text = QtWidgets.QComboBox(parent=self.centralwidget)
        self.WaitForAll_dead_text.setGeometry(QtCore.QRect(775, 341, 100, 16))
        self.WaitForAll_dead_text.setStyleSheet("background-color: rgb(58, 58, 58);border-radius: 5px;")
        self.WaitForAll_dead_text.setObjectName("WaitForAll_dead_text")
        self.WaitForAll_dead_text.addItem("")
        self.WaitForAll_dead_text.setEditable(True)
        self.SquadControll.AdditionButton(name = "WaitForAll_dead_text", param = self.WaitForAll_dead_text)
        
        self.waitSpawn_Before_text = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.waitSpawn_Before_text.setGeometry(QtCore.QRect(630, 370, 171, 16))
        self.waitSpawn_Before_text.setStyleSheet("background-color: rgb(58, 58, 58); border-radius: 5px;")
        self.waitSpawn_Before_text.setObjectName("waitSpawn_Before_text")
        
        self.SquadControll.AdditionButton(name = "waitSpawn_Before_text", param = self.waitSpawn_Before_text)
        
        self.waitSpawn_Between_text = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.waitSpawn_Between_text.setGeometry(QtCore.QRect(643, 394, 161, 16))
        self.waitSpawn_Between_text.setStyleSheet("background-color: rgb(58, 58, 58);border-radius: 5px;")
        self.waitSpawn_Between_text.setObjectName("waitSpawn_Between_text")
        
        self.SquadControll.AdditionButton(name = "waitSpawn_Between_text", param = self.waitSpawn_Between_text)
        self.Image_SquadCreditForOneRobot = QtWidgets.QLabel(parent=self.centralwidget)
        self.Image_SquadCreditForOneRobot.setGeometry(QtCore.QRect(38, 524, 30, 25))
        self.Image_SquadCreditForOneRobot.setStyleSheet(f"border-image: url({  _systemPath.get('Smallcredits.png') });")
        self.Image_SquadCreditForOneRobot.setText("")
        self.Image_SquadCreditForOneRobot.setObjectName("Image_SquadCreditForOneRobot")
        
        self.Image_SquadCreditForSquad = QtWidgets.QLabel(parent=self.centralwidget)
        self.Image_SquadCreditForSquad.setGeometry(QtCore.QRect(29, 493, 45, 29))
        self.Image_SquadCreditForSquad.setStyleSheet(f"border-image: url({ _systemPath.get('Mediumcredits.png') });")
        self.Image_SquadCreditForSquad.setText("")
        self.Image_SquadCreditForSquad.setObjectName("Image_SquadCreditForSquad")
        
        self.selecteble_button_SquadSupport = QtWidgets.QPushButton(parent=self.centralwidget)
        self.selecteble_button_SquadSupport.setGeometry(QtCore.QRect(450, 430, 25, 25))
        self.selecteble_button_SquadSupport.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.selecteble_button_SquadSupport.setStyleSheet("background-color: rgb(89, 89, 89);border-radius: 7px;")
        self.selecteble_button_SquadSupport.setText("")
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"{_systemPath.get('None.png')}"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon.addPixmap(QtGui.QPixmap(f"{_systemPath.get('59508.png')}"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.selecteble_button_SquadSupport.setIcon(icon)
        self.selecteble_button_SquadSupport.setShortcut("")
        self.selecteble_button_SquadSupport.setCheckable(True)
        self.selecteble_button_SquadSupport.setChecked(False)
        self.selecteble_button_SquadSupport.setAutoRepeat(False)
        self.selecteble_button_SquadSupport.setAutoDefault(False)
        self.selecteble_button_SquadSupport.setObjectName("selecteble_button_SquadSupport")

        self.SquadControll.AdditionButton(name = "selecteble_button_SquadSupport", param = self.selecteble_button_SquadSupport)
        
        self.selecteble_button_RandomChoice = QtWidgets.QPushButton(parent=self.centralwidget)
        self.selecteble_button_RandomChoice.setGeometry(QtCore.QRect(555, 430, 25, 25))
        self.selecteble_button_RandomChoice.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.selecteble_button_RandomChoice.setStyleSheet("background-color: rgb(89, 89, 89);border-radius: 7px;")
        self.selecteble_button_RandomChoice.setText("")
        self.selecteble_button_RandomChoice.setIcon(icon)
        self.selecteble_button_RandomChoice.setShortcut("")
        self.selecteble_button_RandomChoice.setCheckable(True)
        self.selecteble_button_RandomChoice.setChecked(False)
        self.selecteble_button_RandomChoice.setAutoRepeat(False)
        self.selecteble_button_RandomChoice.setAutoDefault(False)
        self.selecteble_button_RandomChoice.setObjectName("selecteble_button_RandomChoice")
        
        self.SquadControll.AdditionButton(name = "selecteble_button_RandomChoice", param = self.selecteble_button_RandomChoice)
       
        self.colorSquad = QtWidgets.QPushButton(parent=self.centralwidget)
        self.colorSquad.setGeometry(QtCore.QRect(410, 340, 17, 17))
        self.colorSquad.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.colorSquad.setStyleSheet("background-color: rgb(89, 89, 89);border-radius: 3px;")
        self.colorSquad.setText("")
        self.colorSquad.setShortcut("")
        self.colorSquad.setObjectName("selecteble_button_RandomChoice")
        self.SquadControll.AdditionButton(name = "colorSquad", param = self.colorSquad)
        
        self.selecteble_button_RandomSpawn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.selecteble_button_RandomSpawn.setGeometry(QtCore.QRect(655, 430, 25, 25))
        self.selecteble_button_RandomSpawn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.selecteble_button_RandomSpawn.setStyleSheet("background-color: rgb(89, 89, 89);border-radius: 7px;")
        self.selecteble_button_RandomSpawn.setText("")
        self.selecteble_button_RandomSpawn.setIcon(icon)
        self.selecteble_button_RandomSpawn.setShortcut("")
        self.selecteble_button_RandomSpawn.setCheckable(True)
        self.selecteble_button_RandomSpawn.setChecked(False)
        self.selecteble_button_RandomSpawn.setAutoRepeat(False)
        self.selecteble_button_RandomSpawn.setAutoDefault(False)
        self.selecteble_button_RandomSpawn.setObjectName("selecteble_button_RandomSpawn")

        self.SquadControll.AdditionButton(name = "selecteble_button_RandomSpawn", param = self.selecteble_button_RandomSpawn)

        self.Image_SquadCreditForOneRobot = QtWidgets.QLabel(parent=self.centralwidget)
        self.Image_SquadCreditForOneRobot.setGeometry(QtCore.QRect(38, 524, 30, 25))
        self.Image_SquadCreditForOneRobot.setStyleSheet(f"border-image: url({  _systemPath.get('Smallcredits.png') });")
        self.Image_SquadCreditForOneRobot.setText("")
        self.Image_SquadCreditForOneRobot.setObjectName("Image_SquadCreditForOneRobot")
        
        self.Image_SquadCreditForSquad = QtWidgets.QLabel(parent=self.centralwidget)
        self.Image_SquadCreditForSquad.setGeometry(QtCore.QRect(29, 493, 45, 29))
        self.Image_SquadCreditForSquad.setStyleSheet(f"border-image: url({ _systemPath.get('Mediumcredits.png') });")
        self.Image_SquadCreditForSquad.setText("")
        self.Image_SquadCreditForSquad.setObjectName("Image_SquadCreditForSquad")
        
        self.selecteble_button_SquadSupport = QtWidgets.QPushButton(parent=self.centralwidget)
        self.selecteble_button_SquadSupport.setGeometry(QtCore.QRect(450, 430, 25, 25))
        self.selecteble_button_SquadSupport.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.selecteble_button_SquadSupport.setStyleSheet("background-color: rgb(89, 89, 89); border-radius: 7px;")
        self.selecteble_button_SquadSupport.setText("")
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"{_systemPath.get('None.png')}"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon.addPixmap(QtGui.QPixmap(f"{_systemPath.get('59508.png')}"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.selecteble_button_SquadSupport.setIcon(icon)
        self.selecteble_button_SquadSupport.setShortcut("")
        self.selecteble_button_SquadSupport.setCheckable(True)
        self.selecteble_button_SquadSupport.setChecked(False)
        self.selecteble_button_SquadSupport.setAutoRepeat(False)
        self.selecteble_button_SquadSupport.setAutoDefault(False)
        self.selecteble_button_SquadSupport.setObjectName("selecteble_button_SquadSupport")

        self.SquadControll.AdditionButton(name = "selecteble_button_SquadSupport", param = self.selecteble_button_SquadSupport)
        
        self.selecteble_button_RandomChoice = QtWidgets.QPushButton(parent=self.centralwidget)
        self.selecteble_button_RandomChoice.setGeometry(QtCore.QRect(555, 430, 25, 25))
        self.selecteble_button_RandomChoice.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.selecteble_button_RandomChoice.setStyleSheet("background-color: rgb(89, 89, 89);border-radius: 7px;")
        self.selecteble_button_RandomChoice.setText("")
        self.selecteble_button_RandomChoice.setIcon(icon)
        self.selecteble_button_RandomChoice.setShortcut("")
        self.selecteble_button_RandomChoice.setCheckable(True)
        self.selecteble_button_RandomChoice.setChecked(False)
        self.selecteble_button_RandomChoice.setAutoRepeat(False)
        self.selecteble_button_RandomChoice.setAutoDefault(False)
        self.selecteble_button_RandomChoice.setObjectName("selecteble_button_RandomChoice")
        
        self.SquadControll.AdditionButton(name = "selecteble_button_RandomChoice", param = self.selecteble_button_RandomChoice)
       
       
        self.colorSquad = QtWidgets.QPushButton(parent=self.centralwidget)
        self.colorSquad.setGeometry(QtCore.QRect(410, 340, 17, 17))
        self.colorSquad.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.colorSquad.setStyleSheet("background-color: rgb(89, 89, 89);border-radius: 3px;")
        self.colorSquad.setText("")
        self.colorSquad.setShortcut("")
        self.colorSquad.setObjectName("selecteble_button_RandomChoice")
        self.SquadControll.AdditionButton(name = "colorSquad", param = self.colorSquad)
        
        self.selecteble_button_RandomSpawn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.selecteble_button_RandomSpawn.setGeometry(QtCore.QRect(655, 430, 25, 25))
        self.selecteble_button_RandomSpawn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.selecteble_button_RandomSpawn.setStyleSheet("background-color: rgb(89, 89, 89);border-radius: 7px;")
        self.selecteble_button_RandomSpawn.setText("")
        self.selecteble_button_RandomSpawn.setIcon(icon)
        self.selecteble_button_RandomSpawn.setShortcut("")
        self.selecteble_button_RandomSpawn.setCheckable(True)
        self.selecteble_button_RandomSpawn.setChecked(False)
        self.selecteble_button_RandomSpawn.setAutoRepeat(False)
        self.selecteble_button_RandomSpawn.setAutoDefault(False)
        self.selecteble_button_RandomSpawn.setObjectName("selecteble_button_RandomSpawn")

        self.SquadControll.AdditionButton(name = "selecteble_button_RandomSpawn", param = self.selecteble_button_RandomSpawn)

        self.comboBox_SpawnPosition = QtWidgets.QComboBox(parent=self.centralwidget)
        self.comboBox_SpawnPosition.setGeometry(QtCore.QRect(82, 365, 251, 19))
        self.comboBox_SpawnPosition.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.comboBox_SpawnPosition.setStyleSheet("background-color: rgb(58, 58, 58);border-radius: 5px;font: 12pt \"TF2\";padding: 1px 18px 1px 3px;")
        self.comboBox_SpawnPosition.setEditable(True)
        self.comboBox_SpawnPosition.setMinimumContentsLength(10)
        self.comboBox_SpawnPosition.setIconSize(QtCore.QSize(16, 16))
        self.comboBox_SpawnPosition.setObjectName("comboBox_SpawnPosition")
        self.comboBox_SpawnPosition.addItem("spawnbot")
        self.comboBox_SpawnPosition.addItem("spawnbot_mission_sniper")
        self.comboBox_SpawnPosition.addItem("spawnbot_mission_spy")
        
        self.SquadControll.AdditionButton(name = "comboBox_SpawnPosition", param = self.comboBox_SpawnPosition)

    def MercenarySettingsRuntime(self):
        self.Stats_Health = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.Stats_Health.setGeometry(QtCore.QRect(1010, 535, 95, 20))
        self.Stats_Health.setStyleSheet("background-color: rgb(58, 58, 58);border-radius: 5px;font: 14pt \"TF2\";")
        self.Stats_Health.setObjectName("Stats_Health")
        
        General_Information_Robot["Stats_Healt Text"] = self.Stats_Health
        
        self.Stats_Scale = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.Stats_Scale.setGeometry(QtCore.QRect(1185, 535, 95, 20))
        self.Stats_Scale.setStyleSheet("background-color: rgb(58, 58, 58);border-radius: 5px;font: 14pt \"TF2\";")
        self.Stats_Scale.setText("1x")
        self.Stats_Scale.setObjectName("Stats_Scale")
        
        General_Information_Robot["Stats_Scale Text"] = self.Stats_Scale
        
        self.Stats_MaxVisionRange = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.Stats_MaxVisionRange.setGeometry(QtCore.QRect(1120, 708, 231, 20))
        self.Stats_MaxVisionRange.setStyleSheet("background-color: rgb(58, 58, 58);border-radius: 5px;font: 14pt \"TF2\";")
        self.Stats_MaxVisionRange.setText("1500")
        self.Stats_MaxVisionRange.setObjectName("Stats_MaxVisionRange")
        
        General_Information_Robot["Stats_MaxVisionRange Text"] = self.Stats_MaxVisionRange
        
        self.Stats_AutoJump_min = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.Stats_AutoJump_min.setGeometry(QtCore.QRect(1090, 683, 41, 20))
        self.Stats_AutoJump_min.setStyleSheet("background-color: rgb(58, 58, 58);border-radius: 5px;font: 14pt \"TF2\";")
        self.Stats_AutoJump_min.setText("-1")
        self.Stats_AutoJump_min.setObjectName("Stats_AutoJump_min")
        
        General_Information_Robot["Stats_AutoJump_min Text"] = self.Stats_AutoJump_min
        
        self.Stats_AutoJump_max = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.Stats_AutoJump_max.setGeometry(QtCore.QRect(1185, 683, 41, 20))
        self.Stats_AutoJump_max.setStyleSheet("background-color: rgb(58, 58, 58);border-radius: 5px;font: 14pt \"TF2\";")
        self.Stats_AutoJump_max.setText("-1")
        self.Stats_AutoJump_max.setObjectName("Stats_AutoJump_max")
        
        General_Information_Robot["Stats_AutoJump_max Text"] = self.Stats_AutoJump_max
             
        self.comboBox_Stats_Tag = QtWidgets.QComboBox(parent=self.centralwidget)
        self.comboBox_Stats_Tag.setGeometry(QtCore.QRect(1165, 572, 180, 20))
        self.comboBox_Stats_Tag.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.comboBox_Stats_Tag.setAcceptDrops(False)
        self.comboBox_Stats_Tag.setStyleSheet("background-color: rgb(58, 58, 58);border-radius: 5px;font: 12pt \"TF2\";")
        self.comboBox_Stats_Tag.setEditable(True)
        self.comboBox_Stats_Tag.setCurrentText("")
        self.comboBox_Stats_Tag.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.InsertAtBottom)
        self.comboBox_Stats_Tag.setDuplicatesEnabled(False)
        self.comboBox_Stats_Tag.setObjectName("comboBox_Stats_Tag")
        
        General_Information_Robot["comboBox_Stats_Tag ComboBox"] = self.comboBox_Stats_Tag
        
        self.Stats_WeaponRestriction_comboBox = QtWidgets.QComboBox(parent=self.centralwidget)
        self.Stats_WeaponRestriction_comboBox.setGeometry(QtCore.QRect(1150, 660, 200, 19))
        self.Stats_WeaponRestriction_comboBox.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Stats_WeaponRestriction_comboBox.setStyleSheet("background-color: rgb(58, 58, 58);border-radius: 5px;font: 14pt \"TF2\";color: rgb(217, 210, 41);")
        self.Stats_WeaponRestriction_comboBox.setEditable(True)
        self.Stats_WeaponRestriction_comboBox.setObjectName("Stats_WeaponRestriction_comboBox")
        self.Stats_WeaponRestriction_comboBox.addItem("")
        self.Stats_WeaponRestriction_comboBox.addItem("")
        self.Stats_WeaponRestriction_comboBox.addItem("")
        self.Stats_WeaponRestriction_comboBox.addItem("")
        General_Information_Robot["Stats_WeaponRestriction_comboBox Text"] = self.Stats_WeaponRestriction_comboBox
        
        self.Stats_Behaivior_comboBox = QtWidgets.QComboBox(parent=self.centralwidget)
        self.Stats_Behaivior_comboBox.setGeometry(QtCore.QRect(1030, 637, 200, 17))
        self.Stats_Behaivior_comboBox.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Stats_Behaivior_comboBox.setStyleSheet("background-color: rgb(58, 58, 58);border-radius: 5px;font: 14pt \"TF2\";")
        self.Stats_Behaivior_comboBox.setEditable(True)
        self.Stats_Behaivior_comboBox.setObjectName("Stats_Behaivior_comboBox")
        self.Stats_Behaivior_comboBox.addItem("")
        self.Stats_Behaivior_comboBox.addItem("")
        self.Stats_Behaivior_comboBox.addItem("")
        self.Stats_Behaivior_comboBox.addItem("")
        
        General_Information_Robot["Stats_Behaivior_comboBox Text"] = self.Stats_Behaivior_comboBox
        
        self.Stats_Icon_comboBox = QtWidgets.QComboBox(parent=self.centralwidget)
        self.Stats_Icon_comboBox.setGeometry(QtCore.QRect(985, 607, 370, 20))
        self.Stats_Icon_comboBox.setMinimumSize(QtCore.QSize(1, 0))
        self.Stats_Icon_comboBox.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Stats_Icon_comboBox.setStyleSheet("background-color: rgb(58, 58, 58);border-radius: 5px;font: 14pt \"TF2\";")
        self.Stats_Icon_comboBox.setEditable(True)
        self.Stats_Icon_comboBox.setObjectName("Stats_Icon_comboBox")
        
        General_Information_Robot["Stats_Icon_comboBox Text"] = self.Stats_Icon_comboBox

        self.Stats_ClassMercenary = QtWidgets.QComboBox(parent=self.centralwidget)
        self.Stats_ClassMercenary.setGeometry(QtCore.QRect(926, 462, 195, 20))
        self.Stats_ClassMercenary.setMinimumSize(QtCore.QSize(1, 0))
        self.Stats_ClassMercenary.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Stats_ClassMercenary.setStyleSheet("background-color: rgb(48, 48, 48);border-radius: 5px;font: 14pt \"TF2\";")
        self.Stats_ClassMercenary.setEditable(True)
        self.Stats_ClassMercenary.setObjectName("Stats_ClassMercenary")
        self.Stats_ClassMercenary.setEditable(False)
        
        General_Information_Robot["Stats_ClassMercenary"] = self.Stats_ClassMercenary

        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(f"{_systemPath.get('Plus')}"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        
        self.Button_ShowAdditionSettings = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Button_ShowAdditionSettings.setGeometry(QtCore.QRect(270, 11, 20, 20))
        self.Button_ShowAdditionSettings.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_ShowAdditionSettings.setStyleSheet("background-color: rgb(65, 65, 65);border-radius: 5px;")
        self.Button_ShowAdditionSettings.setText("")
        self.Button_ShowAdditionSettings.setIcon(icon2)
        self.Button_ShowAdditionSettings.setObjectName("Button_ShowAdditionSettings")
        
        self.DeleteMercenary = QtWidgets.QPushButton(parent=self.centralwidget)
        self.DeleteMercenary.setGeometry(QtCore.QRect(730, 598, 154, 25))
        self.DeleteMercenary.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.DeleteMercenary.setStyleSheet("background-color: rgba(148, 148, 148, 0);border-left:   3px solid;border-right:  3px solid;border-top:    3px solid;border-bottom: 3px solid;border-color: rgb(183, 45, 43);border-radius: 5px;color:rgb(183, 45, 43);font: 9pt \"TF2 Build\";")
        
        self.DeleteMercenary.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(f"{_systemPath.get('trash', 'Interface')}"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.DeleteMercenary.setIcon(icon2)
        self.DeleteMercenary.setIconSize(QtCore.QSize(10,13))
        self.DeleteMercenary.setText("Delete Bot")
        self.DeleteMercenary.clicked.connect(lambda: self.SquadControll.DeleteMercenary())
        
        self.Stats_Skill_comboBox = QtWidgets.QComboBox(parent=self.centralwidget)
        self.Stats_Skill_comboBox.setGeometry(QtCore.QRect(981, 573, 125, 20))
        self.Stats_Skill_comboBox.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Stats_Skill_comboBox.setStyleSheet("background-color: rgb(58, 58, 58);border-radius: 5px;font: 12pt \"TF2\";")
        self.Stats_Skill_comboBox.setEditable(False)
        self.Stats_Skill_comboBox.setObjectName("Stats_Skill_comboBox")
        self.Stats_Skill_comboBox.addItem("Easy")
        self.Stats_Skill_comboBox.addItem("Normal")
        self.Stats_Skill_comboBox.addItem("Hard")
        self.Stats_Skill_comboBox.addItem("Expert")

        General_Information_Robot["Stats_Skill_comboBox ComboBox"] = self.Stats_Skill_comboBox
            
    def MercenaryAttributesRuntimeSettings(self):
        AtributeStat = AtributeUI()

        self.Stats_Attributes = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Stats_Attributes.setGeometry(QtCore.QRect(930, 740, 200, 20))
        self.Stats_Attributes.setMinimumSize(QtCore.QSize(1, 0))
        self.Stats_Attributes.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Stats_Attributes.setStyleSheet("background-color: rgb(70, 70, 70);border-radius: 5px;font: 12pt \"TF2 Build\";")
        self.Stats_Attributes.setObjectName("Stats_Attributes")
        self.Stats_Attributes.setText("Attributes")
        self.Stats_Attributes.clicked.connect(lambda: AtributeStat.Show())
        
        self.Stats_Template = QtWidgets.QComboBox(parent=self.centralwidget)
        self.Stats_Template.setGeometry(QtCore.QRect(1164, 462, 195, 20))
        self.Stats_Template.setMinimumSize(QtCore.QSize(1, 0))
        self.Stats_Template.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Stats_Template.setStyleSheet("background-color: rgb(48, 48, 48);border-radius: 5px;font: 14pt \"TF2\";")
        self.Stats_Template.setEditable(True)
        self.Stats_Template.setObjectName("Stats_Template")
        self.Stats_Template.setEditable(False)
        General_Information_Robot["Stats_Template"] = self.Stats_Template

        self.Icon_withName = QtWidgets.QLabel(parent=self.centralwidget)
        self.Icon_withName.setGeometry(QtCore.QRect(1440, 120, 31, 31))
        self.Icon_withName.setStyleSheet(f"border-image: url({_systemPath.get('Scout')});")
        self.Icon_withName.setObjectName("Icon_withName")
        
        General_Information_Robot["Icon_withName Icon"] = self.Icon_withName
        
        self.NameRobot_text = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.NameRobot_text.setGeometry(QtCore.QRect(1480, 120, 300, 32))
        self.NameRobot_text.setStyleSheet("background-color: rgba(255, 255, 255, 0);border:0;font: 16pt \"TF2\";")
        self.NameRobot_text.setObjectName("NameRobot_text")
        self.NameRobot_text.setText("Scout")

        General_Information_Robot['Name_Text'] = self.NameRobot_text          
    
    def MercenaryWeaponsRuntime(self):
        _weaponsAtributeMenu = WeaponsAtributeMenu()

        self.FirsGun = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.FirsGun.setGeometry(QtCore.QRect(918, 120, 131, 81))
        self.FirsGun.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.FirsGun.setStyleSheet("border:0;")
        self.FirsGun.setObjectName("Primary")
        self.FirsGun.mousePressEvent = (lambda x: open_weapon(type="Primary"))
        self.FirsGun.mouseDoubleClickEvent = (lambda x: open_weapon(type="Primary"))
        self.FirsGun.setMouseTracking(True)
                
        self.ButtonAddFirstGun = QtWidgets.QPushButton(parent=self.FirsGun)
        self.ButtonAddFirstGun.setGeometry(QtCore.QRect(0, 0, 131, 81))
        self.ButtonAddFirstGun.setStyleSheet("background-color: rgb(47, 47, 47);border-radius: 10px;")
        self.ButtonAddFirstGun.setIconSize(QtCore.QSize(90, 90))
        self.ButtonAddFirstGun.setObjectName("ButtonAddFirstGun")
        self.ButtonAddFirstGun.setMouseTracking(False)
        
        General_Information_Robot["ButtonAddFirstGun"] = self.ButtonAddFirstGun
        
        ico = QtGui.QIcon()
        ico.addPixmap(QtGui.QPixmap(f"{_systemPath.get('Plus')}"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)           
        self.CustomFirstAtribbutes = QtWidgets.QPushButton(parent=self.FirsGun)
        self.CustomFirstAtribbutes.setGeometry(QtCore.QRect(105,5, 20, 20))
        self.CustomFirstAtribbutes.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.CustomFirstAtribbutes.setStyleSheet("background-color: rgb(65, 65, 65);border-radius: 5px;")
        self.CustomFirstAtribbutes.setIcon(ico)
        self.CustomFirstAtribbutes.setObjectName("CustomFirstAtribbutes")

        global Mercenary_now        
        self.CustomFirstAtribbutes.mousePressEvent = (lambda x: _weaponsAtributeMenu.Open(Mercenary_now.stat["Primary Weapon"]) if Mercenary_now else None)
        self.CustomFirstAtribbutes.mouseDoubleClickEvent = (lambda x: _weaponsAtributeMenu.Open(Mercenary_now.stat["Primary Weapon"] if Mercenary_now else None))
            
            #   Primary Weapon
            #   Secondary Weapons
            #   Melee
        
        self.label_7 = QtWidgets.QLabel(parent=self.FirsGun)
        self.label_7.setEnabled(False)
        self.label_7.setGeometry(QtCore.QRect(0, 60, 131, 21))
        self.label_7.setStyleSheet("color: rgb(217, 210, 41); font: 7pt \"TF2 Build\";")
        self.label_7.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_7.setObjectName("label_7")
        
        self.frame = QtWidgets.QFrame(parent=self.FirsGun)
        self.frame.setEnabled(False)
        self.frame.setGeometry(QtCore.QRect(34, 8, 61, 51))
        self.frame.setStyleSheet(f"border-image: url({_systemPath.get('Plus')});")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        
        General_Information_Robot["Primary label_7"] = self.label_7
        General_Information_Robot["FirsGun  frame"] = self.frame
        
        self.PremoryGun = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.PremoryGun.setGeometry(QtCore.QRect(1077, 119, 131, 81))
        self.PremoryGun.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.PremoryGun.setStyleSheet("border:0;")
        self.PremoryGun.setObjectName("PremoryGun")
        self.PremoryGun.mousePressEvent = (lambda x: open_weapon(type="Secondary"))
        self.PremoryGun.mouseDoubleClickEvent = (lambda x: open_weapon(type="Secondary"))
        
        General_Information_Robot["PremoryGun"] = self.PremoryGun
        self.PremoryGun.setMouseTracking(True)        
        
        self.ButtonAddPremoryGun = QtWidgets.QPushButton(parent=self.PremoryGun)
        self.ButtonAddPremoryGun.setGeometry(QtCore.QRect(0, 0, 131, 81))
        self.ButtonAddPremoryGun.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.ButtonAddPremoryGun.setMouseTracking(True)
        self.ButtonAddPremoryGun.setStyleSheet("background-color: rgb(47, 47, 47);border-radius: 10px;")
        self.ButtonAddPremoryGun.setText("")
        self.ButtonAddPremoryGun.setIconSize(QtCore.QSize(90, 90))
        self.ButtonAddPremoryGun.setObjectName("ButtonAddPremoryGun")
        
        ico = QtGui.QIcon()
        ico.addPixmap(QtGui.QPixmap(f"{_systemPath.get('Plus')}"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)           
        self.CustomSecondaryAtribbutes = QtWidgets.QPushButton(parent=self.ButtonAddPremoryGun)
        self.CustomSecondaryAtribbutes.setGeometry(QtCore.QRect(105,5, 20, 20))
        self.CustomSecondaryAtribbutes.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.CustomSecondaryAtribbutes.setStyleSheet("background-color: rgb(65, 65, 65);border-radius: 5px;")
        self.CustomSecondaryAtribbutes.setIcon(ico)
        self.CustomSecondaryAtribbutes.setObjectName("CustomSecondaryAtribbutes")
        self.CustomSecondaryAtribbutes.mousePressEvent = (lambda x: _weaponsAtributeMenu.Open(Mercenary_now.stat["Secondary Weapons"]))
        self.CustomSecondaryAtribbutes.mouseDoubleClickEvent = (lambda x: _weaponsAtributeMenu.Open(Mercenary_now.stat["Secondary Weapons"]))
           
        self.MeelGun = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.MeelGun.setGeometry(QtCore.QRect(1235, 119, 131, 81))
        self.MeelGun.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.MeelGun.setStyleSheet("border:0;")
        self.MeelGun.setTitle("")
        self.MeelGun.setObjectName("MeelGun")
        
        self.MeelGun.mousePressEvent = (lambda x: open_weapon(type="Melee"))
        
        General_Information_Robot["MeelGun"] = self.MeelGun
        
        self.ButtonAddMelee = QtWidgets.QPushButton(parent=self.MeelGun)
        self.ButtonAddMelee.setGeometry(QtCore.QRect(0, 0, 131, 81))
        self.ButtonAddMelee.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.ButtonAddMelee.setMouseTracking(True)
        self.ButtonAddMelee.setStyleSheet("background-color: rgb(47, 47, 47);border-radius: 10px;")
        self.ButtonAddMelee.setText("")
        self.ButtonAddMelee.setIconSize(QtCore.QSize(90, 90))
        self.ButtonAddMelee.setObjectName("ButtonAddMelee")
               
        ico = QtGui.QIcon()
        ico.addPixmap(QtGui.QPixmap(f"{_systemPath.get('Plus')}"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)           
        self.CustomMeleeAtribbutes = QtWidgets.QPushButton(parent=self.ButtonAddMelee)
        self.CustomMeleeAtribbutes.setGeometry(QtCore.QRect(105,5, 20, 20))
        self.CustomMeleeAtribbutes.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.CustomMeleeAtribbutes.setStyleSheet("background-color: rgb(65, 65, 65);border-radius: 5px;")
        self.CustomMeleeAtribbutes.setIcon(ico)
        self.CustomMeleeAtribbutes.setObjectName("CustomMeleeAtribbutes")

        self.CustomMeleeAtribbutes.mousePressEvent = (lambda x: _weaponsAtributeMenu.Open(Mercenary_now.stat["Melee"]))
        self.CustomMeleeAtribbutes.mouseDoubleClickEvent = (lambda x: _weaponsAtributeMenu.Open(Mercenary_now.stat["Melee"]))

        self.label_13 = QtWidgets.QLabel(parent=self.PremoryGun)
        self.label_13.setEnabled(False)
        self.label_13.setGeometry(QtCore.QRect(0, 60, 131, 21))
        self.label_13.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.label_13.setAccessibleDescription("")
        self.label_13.setStyleSheet("color: rgb(217, 210, 41);font: 7pt \"TF2 Build\";")
        self.label_13.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.frame_3 = QtWidgets.QFrame(parent=self.PremoryGun)
        self.frame_3.setEnabled(False)
        self.frame_3.setGeometry(QtCore.QRect(34, 8, 61, 51))
        self.frame_3.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.frame_3.setAccessibleDescription("")
        self.frame_3.setStyleSheet(f"border-image: url({_systemPath.get('Plus')});")
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        
        General_Information_Robot["ButtonAddPremoryGun label_13"] = self.label_13
        General_Information_Robot["ButtonAddPremoryGun frame_3"]  = self.frame_3
                
        self.label_14 = QtWidgets.QLabel(parent=self.MeelGun)
        self.label_14.setEnabled(False)
        self.label_14.setGeometry(QtCore.QRect(0, 60, 131, 21))
        self.label_14.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.label_14.setAccessibleDescription("")
        self.label_14.setStyleSheet("color: rgb(217, 210, 41);font: 7pt \"TF2 Build\";")
        self.label_14.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.frame_4 = QtWidgets.QFrame(parent=self.MeelGun)
        self.frame_4.setEnabled(False)
        self.frame_4.setGeometry(QtCore.QRect(34, 8, 61, 51))
        self.frame_4.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.frame_4.setAccessibleDescription("")
        self.frame_4.setStyleSheet(f"border-image: url({_systemPath.get('Plus')});\n")
        self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_4.setObjectName("frame_4")
        
        General_Information_Robot["ButtonAddMelee label_14"] = self.label_14
        General_Information_Robot["ButtonAddMelee frame_4"]  = self.frame_4
    
    def MercenaryCosmeticsRuntime(self):
        self.verticalLayout_3.addWidget(self.DoneOutPut_2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_4)
        
        self.Cosmitis_list = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.Cosmitis_list.setGeometry(QtCore.QRect(920, 220, 431, 220))
        

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Cosmitis_list.sizePolicy().hasHeightForWidth())
        
        self.Cosmitis_list.setSizePolicy(sizePolicy)     
        font = QtGui.QFont()
        font.setFamily("TF2")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setKerning(True)
                   
        self.Cosmitis_list.setFont(font)
        
        self.Cosmitis_list.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.Cosmitis_list.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.Cosmitis_list.setAcceptDrops(False)
        self.Cosmitis_list.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.Cosmitis_list.setAutoFillBackground(True)
        self.Cosmitis_list.setStyleSheet("QWidget{    background-color: rgba(0, 0, 0, 0);    border:0;}:handle, QWidget:vertical  {    border-radius: 10px;    background-color: rgb(86, 86, 86);    width: 10px;    min-height: 30px;    max-width: 50px;}:handle, QWidget:horizontal  {    border-radius: 5px;    background-color: rgb(86, 86, 86);    width: 5px;    min-width: 10px;    max-width: 10px;}:sub-line, QWidget:vertical{    background-color: rgba(51, 51, 51, 255);}:add-line, QWidget:vertical{    background-color: rgba(255, 255, 255, 0);}QWidget::add-page:horizontal, QWidget::sub-page:horizontal {    background-color: rgb(51, 51, 51);}QWidget::add-page:vertical, QWidget::sub-page:vertical {    background-color: rgb(51, 51, 51);}")
        self.Cosmitis_list.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.Cosmitis_list.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.Cosmitis_list.setLineWidth(0)
        self.Cosmitis_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.Cosmitis_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.Cosmitis_list.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.Cosmitis_list.setWidgetResizable(True)
        self.Cosmitis_list.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.Cosmitis_list.setObjectName("Cosmitis_list")
        
        self.scrollAreaWidgetContents_6 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_6.setGeometry(QtCore.QRect(0, 0, 421, 252))
        self.scrollAreaWidgetContents_6.setObjectName("scrollAreaWidgetContents_6")
        
        
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_6)
        self.verticalLayout_8.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        #self.gridLayout.setSpacing(10)
        
        global cosmetic_list_class
        cosmetic_list_class = cosmetic_list(
            grid=self.gridLayout, 
            scrollAreaWidgetContents_6=self.scrollAreaWidgetContents_6,
            Cosmitis_list = self.Cosmitis_list, 
            verticalLayout_8 = self.verticalLayout_8)
        self.verticalLayout_8.addLayout(self.gridLayout)
    
    def MercenaryAttributesRuntime(self):
        self.scrollAreaWidgetContents_13 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_13.setGeometry(QtCore.QRect(0, 0, 861, 61))
        self.scrollAreaWidgetContents_13.setObjectName("scrollAreaWidgetContents_13")
        
        self.horizontalLayoutWidget_7 = QtWidgets.QWidget(parent=self.scrollAreaWidgetContents_13)
        self.horizontalLayoutWidget_7.setGeometry(QtCore.QRect(0, 0, 861, 61))
        self.horizontalLayoutWidget_7.setObjectName("horizontalLayoutWidget_7")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_7)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        
        self.Item_3 = QtWidgets.QGroupBox(parent=self.horizontalLayoutWidget_7)
        self.Item_3.setMinimumSize(QtCore.QSize(41, 59))
        self.Item_3.setMaximumSize(QtCore.QSize(41, 59))
        self.Item_3.setStyleSheet("border:0;")
        self.Item_3.setTitle("")
        self.Item_3.setObjectName("Item_3")
        
        self.Text_3 = QtWidgets.QLabel(parent=self.Item_3)
        self.Text_3.setGeometry(QtCore.QRect(0, 40, 41, 16))
        self.Text_3.setStyleSheet("font: 9pt \"TF2\";")
        self.Text_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Text_3.setObjectName("Text_3")
        
        self.Button_3 = QtWidgets.QPushButton(parent=self.Item_3)
        self.Button_3.setGeometry(QtCore.QRect(0, 0, 41, 41))
        self.Button_3.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_3.setMouseTracking(True)
        self.Button_3.setStyleSheet(f"border-image: url({_systemPath.get('Plus')});background-color: rgba(0, 0, 0, 100);border-radius: 5px;")
        self.Button_3.setText("")
        self.Button_3.setIconSize(QtCore.QSize(62, 62))
        self.Button_3.setObjectName("Button_3")
        
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_9.addWidget(self.Item_3)
        self.horizontalLayout_9.addItem(spacerItem6)
        
        self.InWave_List_2.setWidget(self.scrollAreaWidgetContents_13)
        self.scrollArea_3 = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.scrollArea_3.setGeometry(QtCore.QRect(930, 840, 411, 141))
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_3.sizePolicy().hasHeightForWidth())
        self.scrollArea_3.setSizePolicy(sizePolicy)
        self.scrollArea_3.setMinimumSize(QtCore.QSize(411, 141))
        
        font = QtGui.QFont()
        font.setFamily("TF2")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setKerning(True)
        
        self.scrollArea_3.setFont(font)
        self.scrollArea_3.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.scrollArea_3.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.scrollArea_3.setAcceptDrops(False)
        self.scrollArea_3.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.scrollArea_3.setAutoFillBackground(True)
        self.scrollArea_3.setStyleSheet("QWidget{background-color: rgba(50, 50, 50, 255);border-radius : 10px;}:handle, QWidget:vertical  {    border-radius: 5px;    background-color: rgb(86, 86, 86);    width: 10px;    min-height: 30px;    max-width: 50px;}:handle, QWidget:horizontal  {    border-radius: 5px;    background-color: rgb(86, 86, 86);    width: 7px;    min-width: 10px;    max-width: 10px;}:sub-line, QWidget:vertical{    background-color: rgba(51, 51, 51, 255);}:add-line, QWidget:vertical{    background-color: rgba(255, 255, 255, 0);}QWidget::add-page:horizontal, QWidget::sub-page:horizontal {    background: none;}QWidget::add-page:vertical, QWidget::sub-page:vertical {    background: none;}")
        self.scrollArea_3.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.scrollArea_3.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.scrollArea_3.setLineWidth(0)
        self.scrollArea_3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea_3.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea_3.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.scrollArea_3.setObjectName("scrollArea_3")
        
        self.scrollAreaWidgetContents_5 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_5.setGeometry(QtCore.QRect(0, 0, 401, 142))
        self.scrollAreaWidgetContents_5.setObjectName("scrollAreaWidgetContents_5")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_5)
        self.verticalLayout_7.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        
        global Atribute_global  
        Atribute_global = Atributes(scrollAreaWidgetContents_5=self.scrollAreaWidgetContents_5 ,verticalLayout_4=self.verticalLayout_4, horizontalLayout_2 = self.horizontalLayout_2)
        
        #spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        #self.verticalLayout_4.addItem(spacerItem7)
        
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout_7.addLayout(self.horizontalLayout_2)
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_5) 
               
        self.CusomParametrs_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.CusomParametrs_button.setGeometry(QtCore.QRect(1330, 530, 20, 20))
        self.CusomParametrs_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.CusomParametrs_button.setStyleSheet("background-color: rgb(65, 65, 65);border-radius: 5px;")
        ico = QtGui.QIcon()
        ico.addPixmap(QtGui.QPixmap(f"{_systemPath.get('Plus')}"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.CusomParametrs_button.setIcon(ico)
        self.CusomParametrs_button.setObjectName("CusomParametrs_button")
        
        global CustomAtributeGlobal
        self.CusomParametrs_button.clicked.connect(lambda x: CustomAtributeGlobal.Show())
    
    def SquadInWaveRuntime(self):
        self.InWave_List_2 = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.InWave_List_2.setGeometry(QtCore.QRect(20, 223, 861, 61))
        self.InWave_List_2.setStyleSheet("background-color: rgba(255, 255, 255, 0);border:0;")
        self.InWave_List_2.setWidgetResizable(True)
        self.InWave_List_2.setObjectName("InWave_List_2")

    def BindHotKeys(self): # Привязка горячих клавиш
        keyboard.add_hotkey('Ctrl+S', lambda : self.pushButton_9.click()) # Сохранить Save
        keyboard.add_hotkey('Ctrl+E', lambda : self.exportProjectButton.click()) # Экспортировать Export
        keyboard.add_hotkey('Ctrl+L', lambda : self.load_mission_button.click()) # Загрузить Load
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.Main.setWindowTitle(_translate("MainWindow", "Gray Factory"))
                        
        self.Stats_WeaponRestriction_comboBox.setItemText(0, _translate("MainWindow", "All"))
        self.Stats_WeaponRestriction_comboBox.setItemText(1, _translate("MainWindow", "Primary Only"))
        self.Stats_WeaponRestriction_comboBox.setItemText(2, _translate("MainWindow", "Secondary Only"))
        self.Stats_WeaponRestriction_comboBox.setItemText(3, _translate("MainWindow", "Melee Only"))
        self.Stats_Behaivior_comboBox.setItemText(0, _translate("MainWindow", "None"))
        self.Stats_Behaivior_comboBox.setItemText(1, _translate("MainWindow", "Push"))
        self.Stats_Behaivior_comboBox.setItemText(2, _translate("MainWindow", "Iddler"))
        self.Stats_Behaivior_comboBox.setItemText(3, _translate("MainWindow", "Mobber"))
        self.CountingForWave_CountingRobots.setText(_translate("MainWindow", "0"))
        self.CountingForWave_CountingGiantRobots.setText(_translate("MainWindow", "0"))
        self.CountingForWave_CountAllRobots.setText(_translate("MainWindow", "10"))
        self.StartWaveInput.setTitle(_translate("MainWindow", "StartWaveOutput{}"))
        self.InitWaveOutPut.setTitle(_translate("MainWindow", "InitWaveOutput{}"))
        self.DoneOutPut.setTitle(_translate("MainWindow", "DoneOutput{}"))
        self.DoneOutPut_2.setTitle(_translate("MainWindow", "Custom"))
        self.Text_3.setText(_translate("MainWindow", "Add"))
        self.load_mission_button.setText(_translate("MainWindow", "Load"))
        self.exportProjectButton.setText(_translate("MainWindow", "Export"))
        self.pushButton_9.setText(_translate("MainWindow", "Save"))
        self.generateMissionRandom.setText("Generate")
        self.clearAllMission.setText("Delete All")
        self.clear_cur_mission.setText("Delete")

class AddButtonInWaveList(object):
    def __init__(self,horizontalLayout_4, scrollbar, horizontalLayoutWidget_6, verticalLayout_9):
        self.area = scrollbar
        self.horizontalLayoutWidget_6 = horizontalLayoutWidget_6
        self.verticalLayout_9 = verticalLayout_9
        self.horizontalLayout_4 = horizontalLayout_4
        self.spacer = None
        self.AllButtons = []
        self.AllMercenary = []
        
    def clear(self):
        if len(self.AllButtons) != 0:
            for item in self.AllButtons:
                try:
                    item.delete()
                except:
                    item.deleteLater()
            self.AllButtons.clear()
            self.AllButtons = []
            self.AllMercenary.clear()
            self.AllMercenary = []
            
        _AddButtonInWaveList.AddButton("Add", command=lambda: Adding_New_Mercenary_To_Wave())
    
    def DeleteGlobalButton(self):
        buttonMercenaryActive.deleteLater()

    def AddButton(self, exemplar_mercenary, title : str = "Add", count : int = 1, command = None, iconName : str = None):
        if exemplar_mercenary in self.AllMercenary and exemplar_mercenary != "Add":
            print(f"[ERROR] Mercenary {exemplar_mercenary} already exists in the list.")
            return False
        else:
            self.AllMercenary.append(exemplar_mercenary)
            
        if self.spacer:
            self.horizontalLayout_4.removeItem(self.spacer)
         
        for i in range(count):
            self.Item = QtWidgets.QGroupBox(parent=self.horizontalLayoutWidget_6)
            self.Item.setMinimumSize(QtCore.QSize(41, 59))
            self.Item.setMaximumSize(QtCore.QSize(41, 59))
            self.Item.setStyleSheet("border:0;")
            self.Item.setObjectName("Item")
            self.Text = QtWidgets.QLabel(parent=self.Item)
            self.Text.setGeometry(QtCore.QRect(0, 40, 41, 16))
            self.Text.setStyleSheet("font: 9pt \"TF2\";")
            self.Text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.Text.setText(title)
            self.Button = QtWidgets.QPushButton(parent=self.Item)
            self.Button.setGeometry(QtCore.QRect(0, 0, 41, 41))
            self.Button.setCheckable(True)
            if(iconName != None):
                icon = _systemPath.get(iconName, "Leaderboard")
            else: 
                icon = _systemPath.get("Plus", "Interface")
            self.Button.setStyleSheet(f"border-image: url({icon});\n"
                                        "background-color: rgba(0, 0, 0, 100);\n"
                                        "border-radius: 5px;")
            self.Button.setIconSize(QtCore.QSize(62, 62))
            self.Button.setObjectName("Button")

            if(command != None):
                self.Button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.Button.setMouseTracking(True)
                self.Button.clicked.connect( lambda x : command () )

            self.AllButtons.append(self.Item)
            self.horizontalLayout_4.addWidget(self.Item)

        #spacer
        spacer = QtWidgets.QSpacerItem(379, 17, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.spacer = spacer
        self.horizontalLayout_4.addItem(self.spacer)
        #print(f"[DEBUG : Items in List <Robots in Wave> ] Adding button : name = {title} | count = {count} | command = {command}")
        global started_click
        if started_click == False:
            #self.Button.click()
            started_click = True
            self.area.addLayout(self.horizontalLayout_4)
            self.verticalLayout_9.addLayout(self.area)
        
        return {"Text" : self.Text, "Button" : self.Button}

class Ui_GroupBox(QtWidgets.QMainWindow):
    global Global_Components
    def __init__(self):
        self.stat = None
        
    def setupUi(self, stat = None):
        self.stat = stat
        self.Box = QtWidgets.QMainWindow()
        self.Box.setObjectName("self")
        self.Box.resize(600, 500)
        self.Box.setMinimumSize(QtCore.QSize(400, 300))
        self.Box.setStyleSheet("background-color: rgb(39, 39, 39);")
        self.Box.setWindowTitle("Chose")
        Global_Components["UI_Box_Group_Main"] = self.Box
        
        # Central widget and layout
        central_widget = QtWidgets.QWidget(self.Box)
        
        self.Box.resizeEvent = lambda event: print("") # Placeholder for resize event handling
        
        self.Box.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)

        # Search bar layout
        search_layout = QtWidgets.QHBoxLayout()
        Seach_lineedit = QtWidgets.QLineEdit()
        Seach_lineedit.setPlaceholderText("Search...")
        Seach_lineedit.setMinimumHeight(24)
        Seach_lineedit.setStyleSheet(
            "font: 11pt \"TF2\";border:0;border-radius: 7px;background-color: rgb(61, 61, 61);color: rgb(255, 255, 255);"
        )
        Seach_lineedit.setObjectName("Seach_lineedit")
        Seach_lineedit.editingFinished.connect(lambda: self.Search(Seach_lineedit.text()))
        search_layout.addWidget(Seach_lineedit)

        Seach_icon = QtWidgets.QLabel()
        Seach_icon.setFixedSize(20, 20)
        Seach_icon.setStyleSheet(
            f"border-image: url({_systemPath.get('search', 'Interface')});background-color: rgba(255, 255, 255,0);"
        )
        search_layout.addWidget(Seach_icon)
        search_layout.setStretch(0, 1)
        search_layout.setStretch(1, 0)
        main_layout.addLayout(search_layout)

        # Scalable scroll area for items
        Cosmitis_list = QtWidgets.QScrollArea()
        Cosmitis_list.setWidgetResizable(True)
        Cosmitis_list.setStyleSheet(
            "QWidget{background-color: rgba(0, 0, 0, 0);border:0;}"
            ":handle, QWidget:vertical  {border-radius: 10px;background-color: rgb(86, 86, 86);width: 10px;min-height: 30px;max-width: 50px;}"
            ":handle, QWidget:horizontal  {border-radius: 5px;background-color: rgb(86, 86, 86);width: 5px;min-width: 10px;max-width: 10px;}"
            ":sub-line, QWidget:vertical{background-color: rgba(51, 51, 51, 255);}"
            ":add-line, QWidget:vertical{background-color: rgba(255, 255, 255, 0);}"
            "QWidget::add-page:horizontal, QWidget::sub-page:horizontal {background-color: rgb(51, 51, 51);}"
            "QWidget::add-page:vertical, QWidget::sub-page:vertical {background-color: rgb(51, 51, 51);}"
        )
        Cosmitis_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        Cosmitis_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        Cosmitis_list.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        Cosmitis_list.setObjectName("Cosmitis_list")

        # Contents for scroll area
        scrollAreaWidgetContents_6 = QtWidgets.QWidget()
        scrollAreaWidgetContents_6.setObjectName("scrollAreaWidgetContents_6")
        verticalLayout_8 = QtWidgets.QVBoxLayout(scrollAreaWidgetContents_6)
        verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        verticalLayout_8.setSpacing(0)
        verticalLayout_8.setObjectName("verticalLayout_8")
        gridLayout = QtWidgets.QGridLayout()
        gridLayout.setObjectName("gridLayout")

        Global_Components["scrollAreaWidgetContents_6"] = scrollAreaWidgetContents_6
        Global_Components["gridLayout"] = gridLayout

        verticalLayout_8.addLayout(gridLayout)
        verticalLayout_8.addStretch(1)
        Cosmitis_list.setWidget(scrollAreaWidgetContents_6)
        main_layout.addWidget(Cosmitis_list)

        # Cancel button
        pushButton = QtWidgets.QPushButton("Cancel")
        pushButton.setMinimumHeight(32)
        pushButton.setStyleSheet(
            "border-radius: 7px;border:0;background-color: rgb(176, 57, 57);color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";"
        )
        pushButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        pushButton.clicked.connect(lambda: self.exit_select())
        main_layout.addWidget(pushButton)

        QtCore.QMetaObject.connectSlotsByName(self.Box)
        self.Box.show()
        global Addition_interface
        Addition_interface = self.Box

    def Search(self, searchText):
        if self.stat is not None:
            global TileGlobal
            TileGlobal.SearchDelete(key = searchText, stat=self.stat)

    def exit_select(self):
        self.Box.close()

class Tile():
    global Global_Components
    global Mercenary_now
    
    def __init__(self):
        self.countButton = 0
        self.line = 0
        self.spacer = None
        global TileGlobal
        TileGlobal = self
        self.buttons = []
        self.firstStat = {}
        self._setup_grid_signals()

    def _setup_grid_signals(self):
        # Подключаем обработчик изменения размера родительского виджета
        parent_widget: QtWidgets.QWidget = Global_Components.get("UI_Box_Group_Main")

        if parent_widget is not None:
            parent_widget.resizeEvent = lambda event: self._on_parent_resize(event)

    def _on_parent_resize(self, event):
        self._relayout_buttons()
        event.accept()

    def _relayout_buttons(self):
        parent_widget = Global_Components["scrollAreaWidgetContents_6"]
        grid_layout = Global_Components["gridLayout"]
        button_width = 130
        spacing = 10  # spacing между элементами
        grid_layout.setHorizontalSpacing(spacing)
        grid_layout.setVerticalSpacing(spacing)
        container_width = parent_widget.width()
        columns = max(1, container_width // (button_width + spacing))

        # Удаляем все элементы из сетки (кроме spacer)
        for i in reversed(range(grid_layout.count())):
            item = grid_layout.itemAt(i)
            widget = item.widget()
            if widget is not None and widget in self.buttons:
                grid_layout.removeWidget(widget)
        # Добавляем обратно с новыми координатами
        for idx, btn in enumerate(self.buttons):
            row = idx // columns
            col = idx % columns
            grid_layout.addWidget(btn, row, col, 1, 1)
        # Spacer для заполнения пространства
        if self.spacer is not None:
            grid_layout.removeItem(self.spacer)
        self.spacer = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding
        )

        grid_layout.addItem(self.spacer, (len(self.buttons) // columns) + 1, 0, 1, columns)
        
    def Clear(self):
        if len(self.buttons) > 0:
            for item in self.buttons:
                item.deleteLater()
            self.buttons.clear()

    def SearchDelete(self, key : str = None , stat : dict = {}):
        _stat = stat.keys()
        find = {}
        
        for index in _stat:
            item = parser.get_item_by_key(index)
            if "name" in item:
                item_name = item["name"].title()
                if key is not None and key.title() in item_name:
                    find[index] = item
                    
        def filtered_items():
            criteria = {
                'used_by_classes': Mercenary_now.stat['Class Name'].lower(),
                'equip_region' : "hat",	
            }
            return parser.filter_items(criteria)   
               
        if len(find) > 0 and len(key) > 0:
            self.Clear()
            self.AddButton(items = find)
            
        elif len(key) >= 0 or len(find) <= 0 :
            items = parser.get_items_by_name(key)

            if items:
                self.firstStat = {}
                for item in items:
                    if item[0] not in self.firstStat:
                        self.firstStat[item[0]] = item[1]
                        
                if len(self.firstStat) > 0:
                    self.Clear()
                    self.AddButton(self.firstStat)
            else:
                self.Clear()
                self.AddButton(filtered_items())
        else:
            self.Clear()
            self.AddButton(filtered_items())

    def AddButton(self, items : dict = [], index = None):
        self.countButton = 0
        self.line = 0
        self.now = 0
        if index != None:
            self.curIndex = index
        else:
            index = self.curIndex
            
        # Очищаем старые кнопки
        for btn in self.buttons:
            try:
                btn.deleteLater()
                btn.setParent(None)
            except Exception as e:
                print(f"Error deleting button: {e}")
        self.buttons.clear()

        for item in items:
            stat = items[item]
            self.CreateButton(stat = stat, index = item, slot = index)

        # Перераскладываем кнопки после добавления
        self._relayout_buttons()

    def CreateButton(self, stat, index = None, slot = "Primary"):
        Item = QtWidgets.QGroupBox(parent=Global_Components["scrollAreaWidgetContents_6"])
        Item.setMinimumSize(QtCore.QSize(130, 80))
        Item.setMaximumSize(QtCore.QSize(130, 80))
        Item.setStyleSheet("border:0;")
        Item.setObjectName("Item")

        ButtonAddCosmetic = QtWidgets.QPushButton(parent=Item)
        ButtonAddCosmetic.setGeometry(QtCore.QRect(0, 0, 131, 81))
        ButtonAddCosmetic.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
       
        color_rgb_item = "rgb(217, 210, 41)"
        if "hwn" in stat.get("name","").lower() or "halloween" in stat.get("name","").lower():
            color_rgb_item = "rgb(56, 243, 171)"
            styleSheet = ("background-color: rgb(47, 47, 47);"
                          "border-left:   1px solid;"
                          "border-right:  1px solid;"
                          "border-top:    1px solid;"
                          "border-bottom: 1px solid;"
                          f"border-color:  {color_rgb_item};"
                          "border-radius: 10px;"
                          "color:rgb(183, 45, 43);")
        elif stat.get("Rome"):
            color_rgb_item = "rgb(200, 120, 35)"
            styleSheet = ("background-color: rgb(47, 47, 47);"
                          "border-left:   1px solid;"
                          "border-right:  1px solid;"
                          "border-top:    1px solid;"
                          "border-bottom: 1px solid;"
                          f"border-color:  {color_rgb_item};"
                          "border-radius: 10px;"
                          "color:rgb(183, 45, 43);")
            
        styleSheetName = f"color: {color_rgb_item};font: 7pt \"TF2 Build\";"
        styleSheet = (
            "background-color: rgb(47, 47, 47);"
            "border-radius: 10px;")        
        
        ButtonAddCosmetic.setStyleSheet(styleSheet)
        ButtonAddCosmetic.setIconSize(QtCore.QSize(90, 90))
        ButtonAddCosmetic.setObjectName("ButtonAddCosmetic")
        ButtonAddCosmetic.setMouseTracking(True)

        Name = QtWidgets.QLabel(parent=Item)
        Name.setGeometry(QtCore.QRect(0, 60, 131, 21))
        Name.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        Name.setStyleSheet(styleSheetName)
        Name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        Name.setObjectName("Name")
        Name.setMouseTracking(False)

        Icon = QtWidgets.QFrame(parent=Item)
        Icon.setGeometry(QtCore.QRect(34, 8, 64, 64))
        Icon.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        Icon.setMouseTracking(False)
        Icon.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        Icon.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        Icon.setObjectName("Icon")
                
        if stat is None:
            item_icon = _systemPath.get("Plus")
            Name.setText("Add")
        else: 
            item_icon = get_icon_from_game(index)
                
            if item_icon is None:
                item = stat.get("Icon", "")
                item_icon = _systemPath.get(item, "weapon")  
                         
            Name.setText(stat.get("name", "Unknown"))
            Icon.setStyleSheet(f'border-image: url({item_icon}); width: 64px; height: 64px; min-width: 32px; min-height: 32px; max-width: 128px; max-height: 128px;')
            stat["index_item"] = index
            
        stat["ready_icon"] = item_icon
        
        if "Id" in stat:
            atributet = Button_Weapon_Atribute(stat, slot)
        else:
            atributet = Button_Cosmetic_Atribute(stat)
        
        ButtonAddCosmetic.clicked.connect(lambda x: atributet.get())
        
        Icon.mousePressEvent = (lambda x: atributet.get())
        Name.mousePressEvent = (lambda x: atributet.get())

        self.buttons.append(Item)


class SaveManager(object):
    def __init__(self):
        super().__init__()

    def Save(self):
        global WaveManagerGlobal
        global InitSettingsGlobal
        
        global project_file
        global generalGlobal
        global path_project_file
        
        missionName = f'{generalGlobal.buttonsGlobal["mapName_text"].text()}_{generalGlobal.buttonsGlobal["MissionName_text"].text()}'
        try:
            if project_file == None:
                Tk().withdraw()
                name = fd.asksaveasfile(title="Save Project", filetypes = [('Json Project', '*.json')], initialfile= missionName)
                Tk().destroy()
                
                if name != None and len(name.name) > 0:
                    name = name.name
                    path_project_file = name
                else:
                    return
            else:
                name = project_file
        except:return
        
        waveList = {}
        for key, value in WaveManagerGlobal.waveList.items():
            # Пропускаем все объекты, которые являются классами (например, QPushButton)
            # или содержат параметр 'button' с объектом QPushButton
            if isinstance(value, type) or (hasattr(value, "__class__") and "PyQt" in str(type(value))):
                continue
            # Удаляем параметр 'button', если он есть и это QPushButton
            if isinstance(value, dict) and "button" in value:
                btn = value["button"]
                # Проверяем, что это действительно QPushButton
                if "QPushButton" in str(type(btn)):
                    value = value.copy()
                    value.pop("button")
            waveList[key] = value
            
        waveList[next(iter(waveList))]["GlobalSettings"] = InitSettingsGlobal.Get()
        
        for _squad in waveList:
            squad =     waveList[_squad]["Squad"]
            primary =   dict
            secondary = dict
            melee =     dict
            
            if len(squad) > 0:
                for squadItem in squad:
                    squadItem = squad[squadItem]["InSquad"]
                    allInSquad = []
                    
                    for _item in squadItem:
                        item = squadItem[squadItem.index(_item)]
                        
                        if isinstance(item, Mercenary):
                            if isinstance(item.stat["Primary Weapon"], WeaponData):
                                primary =   item.stat["Primary Weapon"].get()
                            else:
                                primary =   item.stat["Primary Weapon"]
                                
                            if isinstance(item.stat["Secondary Weapons"], WeaponData):
                                secondary =   item.stat["Secondary Weapons"].get()
                            else:
                                secondary =   item.stat["Secondary Weapons"]
                                
                            if isinstance(item.stat["Melee"], WeaponData):
                                melee =   item.stat["Melee"].get()
                            else:
                                melee =   item.stat["Melee"]
                                
                            item.stat["Primary Weapon"] = primary
                            item.stat["Secondary Weapons"] = secondary
                            item.stat["Melee"] = melee
                        if isinstance(item, Mercenary):
                            allInSquad.append(item.stat)
                        else:
                            allInSquad.append(item)

                    squadItem.clear()
                    squadItem.extend(allInSquad)
                    
        if len(name) > 1:
            out_file = open(f'{name.replace(".json", "")}.json', "w")
            def convert_paths(obj):
                if isinstance(obj, dict):
                    return {k: convert_paths(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [convert_paths(i) for i in obj]
                elif hasattr(obj, "as_posix"):
                    return str(obj)
                else:
                    return obj
            exit_file = convert_paths(waveList)

            json.dump(exit_file, out_file)

            out_file.close()
            project_file = name
            
        self.Load(True)
        
    def Load(self, oldSave : bool = False):
        global project_file
        global path_project_file
        if oldSave:
            name = path_project_file
        else:
            Tk().withdraw()
            name = fd.askopenfilename(title="Select Project", filetypes = [('Json Project', '*.json')])
            name.replace(".json", "")
            Tk().destroy()
            
            path_project_file = name.replace(".json", "")
            if len(name) <= 0:
                return
        try:
            f = open(f'{name.replace(".json", "")}.json')
            data = json.load(f)
            global WaveManagerGlobal
            WaveManagerGlobal.clearAll()
            global SquadSettingsGlobal
            SquadSettingsGlobal.ClearSettingsSquad()
            SquadSettingsGlobal.clearSquad()
            global InitSettingsGlobal
            
            InitSettingsGlobal.SetFromSave(data[next(iter(data))]["GlobalSettings"])
            
            for item in data:
                waveItem = {}
                waveItem[item] = data[item]
                WaveManagerGlobal.SetFromSave(waveItem)
                
            project_file = name
            
            WaveManagerGlobal.setWave(next(iter(WaveManagerGlobal.waveList)))
            f.close()
            
        except Exception as e:
            Tk().withdraw()
            from tkinter import messagebox
            print(f"[ERROR] Failed to load project: {e}")
            messagebox.showerror('Gray Factory', 'Error: File cannot be uploaded! \n' + str(e))
            Tk().destroy()


class InitialSettings(object):
    def __init__(self):
        self.money = 400
        self.restartTime = 0
        self.GlobalButtons = {}
        global generalGlobal
        
    def SetFromSave(self, info : dict):
        if "Map Name" in info:
            generalGlobal.buttonsGlobal["mapName_text"].setText(info["Map Name"])
            generalGlobal.buttonsGlobal["MissionName_text"].setText(info["Mission Name"])
            
        self.money = info["money"]
        self.restartTime = info["restartTime"]
        self.setMoney()
        
    def Get(self):
        _get = {
            "Map Name" : generalGlobal.buttonsGlobal["mapName_text"].text(),
            "Mission Name" : generalGlobal.buttonsGlobal["MissionName_text"].text(), 
            "money" : self.money,
            "restartTime" : self.restartTime,
        }
        return _get
    
    def returnConfiguration(self):
        return self.money, self.restartTime
    
    def addButton(self, name, param):
        self.GlobalButtons[name] = param
        for item in self.GlobalButtons:
            try:self.GlobalButtons[item].editingFinished.connect(lambda : (self.save(), self.setMoney()))
            except:pass

    def setMoney(self):
        self.GlobalButtons["startUpMoney_text"].setText(f"{self.money}")
        if   self.money < 999: image  = 'Smallcredits'
        elif self.money >= 1000 and self.money < 2999: image  = 'Mediumcredits'
        elif self.money >= 3000: image  = 'Largecredits'
        else: image  = 'Smallcredits'
        self.GlobalButtons["Image_StartUpCredit"].setStyleSheet(f"border-image: url({ _systemPath.get(image)})")
    
    def save(self):
        self.money = int(self.GlobalButtons["startUpMoney_text"].text())
        try: 
            self.restartTime = self.GlobalButtons["fixedRespawn_text"].text()
        except Exception as e: 
            print("[ERROR] Failed to save restart time:", e)
        global WaveManagerGlobal
        WaveManagerGlobal.CountingWave()


class WaveManager(object):
    global SquadSettingsGlobal
    def __init__(self):
        self.waveCurrent = None
        self.waveList = {}
        
        self.waveCount = 0
        self.allWave = []
        self.globalButtons = {}
        self.components = {}
        self.addWaveButton = None
        self.spacerItem = None
        self.allButtonsInGlobal = []
    
    def removeCurrentWave(self):
        """Удаляет текущую волну или очищает её, если это единственная волна."""
        if not self.waveCurrent:
            return  # Если текущая волна не установлена, ничего не делаем

        if len(self.allWave) == 1:
            # Если это единственная волна, только очищаем её содержимое
            wave = self.waveList[self.waveCurrent]
            wave["Squad"].clear()  # Очищаем отряды в волне
            wave["Money"] = 0
            wave["Support"].clear()
            wave["Settings"] = {
                "Description": "",
                "Sound": "",
                "StartWaveOutput": "Target  wave_start_relay\nAction  Trigger",
                "InitWaveOutput": "",
                "DoneOutput": "Target  wave_finished_relay\nAction  Trigger",
                "Custom": ""
            }
            # Также очищаем интерфейс
            SquadSettingsGlobal.clearSquad()
            self.components["WaveSelect_text"].setText(self.waveCurrent)
            self.setWave(self.waveCurrent)
            self.CountingWave()
            return

        # Найти индекс текущей волны
        current_index = next(
            (i for i, wave in enumerate(self.allWave) if wave["Name"] == self.waveCurrent), None
        )

        if current_index is not None:
            # Удалить текущую волну из списков
            wave_to_remove = self.waveList.pop(self.waveCurrent, None)
            if wave_to_remove:
                self.allWave.pop(current_index)

            # Удалить кнопку из интерфейса
            button_to_remove = next(
                (btn for btn in self.allButtonsInGlobal if btn.text() == self.waveCurrent), None
            )
            if button_to_remove:
                self.allButtonsInGlobal.remove(button_to_remove)
                button_to_remove.deleteLater()

            # Переход к предыдущей волне или создание новой
            if current_index > 0:
                new_wave = self.allWave[current_index - 1]["Name"]
            elif self.allWave:  # Если удалённая волна была первой, выбираем новую первую волну
                new_wave = self.allWave[0]["Name"]
            #else:  # Если волн больше не осталось, создаём новую волну
            #    new_wave = self.addWave()["Name"]

            self.waveCurrent = new_wave
            if new_wave:
                self.setWave(new_wave)
            else:
                self.components["WaveSelect_text"].clear()  # Очистить текст выбора волны


    def clearAll(self):
        for item in self.allButtonsInGlobal:
            item.deleteLater()
        self.allButtonsInGlobal.clear()
        self.allButtonsInGlobal = []
        
        self.allWave.clear()
        self.allWave = []
        
        self.waveCount = 0
        self.waveCurrent = None
        
        self.waveList.clear()
        self.waveList = {}
        
        self.spacerItem = None
        
        global _AddButtonInWaveList
        _AddButtonInWaveList.clear()
        
        SquadSettingsGlobal.ClearSettingsSquad()
        
    def SetFromSave(self, list : dict):
        _Squads = {}
        
        for wave in list:
            wave = list[wave]
            self.waveCount += 1
            
            for squad in wave["Squad"] or wave["Squads"]:
                createSquad = SquadSettingsGlobal.SetSquadFromSettings(wave["Squad"][squad])
                _Squads[createSquad["Name"]] = createSquad
                Wave = {
                    "Name": wave.get("Name"),
                    "Wave Queue": self.waveCount,
                    "Squad": _Squads,
                    "Support": [],
                    "Money": wave.get("Money"),
                    "Settings": {
                        "Description":      wave.get("Settings", {}).get("Description"),
                        "Sound":            wave.get("Settings", {}).get("Sound"),
                        "StartWaveOutput":  wave.get("Settings", {}).get("StartWaveOutput"),
                        "InitWaveOutput":   wave.get("Settings", {}).get("InitWaveOutput"),
                        "DoneOutput":       wave.get("Settings", {}).get("DoneOutput"),
                        "Custom":           wave.get("Settings", {}).get("Custom"),
                    }
                }
            
            self.waveList[Wave["Name"]] = Wave
            self.allWave.append(Wave)
            
            global _AddButtonInWaveList
            _AddButtonInWaveList.clear()
            self.AddButtonToGlobal(Wave["Name"])
            
        self.setSettings()
                
    def AddButton(self, name, param):
        self.globalButtons[name] = param
        if type(self.globalButtons[name]) is QtWidgets.QPushButton:
            self.globalButtons[name].clicked.connect(lambda: (self.saveSettings(), self.CountingWave()) )
        elif type(self.globalButtons[name]) is QtWidgets.QLineEdit:
            self.globalButtons[name].editingFinished.connect(lambda: (self.saveSettings(), self.CountingWave()) )
        elif type(self.globalButtons[name]) is QtWidgets.QTextEdit:
            self.globalButtons[name].textChanged.connect(lambda: (self.saveSettings(), self.CountingWave()) )

    def AddComponent(self, name, param):
        self.components[name] = param
        
    def CountingWave(self):
        endValue = 0
        if len(self.waveList) > 0:
            item = self.waveList[self.waveCurrent]
            for inSquad in item["Squad"]:
                endValue += self.waveList[self.waveCurrent]['Squad'][inSquad]["Credits For Squad"]
            item["Money"] = endValue
            
            self.globalButtons["CountingForWave_AllRobots"].setText(f"{endValue}$")
            self.countPerviosWave(endValue)
        
    def countPerviosWave(self, nowMoney):
        if len(self.allWave) > -1:
            lastMoney = 0
            if len(self.allWave) > 1 and len(self.allWave[len(self.allWave)-2]) != 1 and self.waveCurrent != "Wave 1":
                startMoney = InitSettingsGlobal.GlobalButtons["startUpMoney_text"].text().replace("$", "")
                lastMoney = self.allWave[len(self.allWave)-2]["Money"] + int(startMoney)
                self.nextWaveCount(lastMoney = lastMoney, curMoney=nowMoney)
            elif self.waveCurrent == "Wave 1":
                startMoney = InitSettingsGlobal.GlobalButtons["startUpMoney_text"].text().replace("$", "")
                if len(startMoney) > 0:
                    lastMoney = int(startMoney)
                    self.nextWaveCount(lastMoney = lastMoney, curMoney=nowMoney)
            else:
                self.nextWaveCount(curMoney=nowMoney)
                
            self.globalButtons["CountingForWave_PreviousWave"].setText(f"{lastMoney}$")
            
    def nextWaveCount(self, lastMoney = 0, curMoney = 0):
        nowValue = curMoney + lastMoney
        self.globalButtons["CountingForWave_ForNextWave"].setText(f"{nowValue}$")
        
    def saveSettings(self):
        if len(self.waveList) > -1 and self.waveCurrent != None:
            self.waveList[self.waveCurrent]["Settings"] = {
                "Description" : self.globalButtons["WaveSettings_discription"].text(),
                "Sound" : self.globalButtons["WaveSettings_sound"].text(),
                
                "StartWaveOutput" : self.globalButtons["StartWaveOutput"].toPlainText(),
                "InitWaveOutput" : self.globalButtons["InitWaveOutput"].toPlainText(),
                "DoneOutput" : self.globalButtons["DoneOutput"].toPlainText(),
                "Custom" : self.globalButtons["Custom"].toPlainText(),
            }

    def setSettings(self):
        if len(self.waveList) > -1 and self.waveCurrent != None:
            self.CountingWave()
            settings = self.waveList[self.waveCurrent]["Settings"]
            self.globalButtons["WaveSettings_discription"].setText(settings["Description"])
            self.globalButtons["WaveSettings_sound"].setText(settings["Sound"])

            self.globalButtons["StartWaveOutput"].setPlainText(settings["StartWaveOutput"])
            self.globalButtons["InitWaveOutput"].setPlainText(settings["InitWaveOutput"])
            self.globalButtons["DoneOutput"].setPlainText(settings["DoneOutput"])
            self.globalButtons["Custom"].setPlainText(settings["Custom"])
        
    def setWave(self, waveName, button = None): #Open Wave
        global InitSettingsGlobal
        InitSettingsGlobal.setMoney()
        if waveName in self.waveList:
            self.waveCurrent = waveName
            global CurrentWave
            CurrentWave = self.waveList[self.waveCurrent]
            self.components["WaveSelect_text"].setText(str(self.waveCurrent))
            
            for item in self.allButtonsInGlobal:
                self.Set_style_for_button(item, False)

            if button is not None:
                self.Set_style_for_button(button, True)
            else:
                # Безопасно получаем кнопку, если она есть
                wave_button = self.waveList[self.waveCurrent].get("button")
                if wave_button is not None:
                    self.Set_style_for_button(wave_button, True)

            global _AddButtonInWaveList
            _AddButtonInWaveList.clear()
            
            SquadSettingsGlobal.clearSquad()
            
            list_squad = self.waveList[self.waveCurrent]["Squad"]

            for squad_name, squad_data in list(list_squad.items()):  # Проходим по элементам словаря
                #if squad_data["Wave"] is not self.waveList[self.waveCurrent]["Name"]:
                #    continue
                if len(squad_data.get("InSquad", [])) <= 0:
                    continue 
                for item in squad_data.get("InSquad", []):  # Получаем список из "InSquad", если он есть
                    Adding_New_Mercenary_To_Wave(item)

            self.setSettings()
            self.CountingWave()
            
    def addWave(self, nameWave : str = None):
        if len(self.waveList) == 6: # max count wave
            return
        self.saveSettings()
        if nameWave != None:
            if nameWave in self.waveList:
                return
        else:
            name = "Wave 1"
            count = 1
            while True:
                name = f"Wave {count}"
                try:
                    self.waveList[name]
                    count += 1
                except: break
            nameWave = name
            
        self.waveCount += 1
        Wave = {
            "Name" : nameWave,
            "Wave Queue" : self.waveCount,
            "Squad" : {},
            "Support" : [],
            "Money" : 0,
            "Settings" : {
                "Description":"",
                "Sound":"",
                "StartWaveOutput" : "Target  wave_start_relay\nAction  Trigger",
                "InitWaveOutput" :  "",
                "DoneOutput" :      "Target  wave_finished_relay\nAction  Trigger",
                "Custom" :          "",
            }
        }
        self.allWave.append(Wave)
        self.waveList[Wave["Name"]] = Wave
        self.waveCurrent = Wave["Name"]
        
        global CurrentWave
        CurrentWave = self.waveList[self.waveCurrent]
        
        global _AddButtonInWaveList
        _AddButtonInWaveList.clear()
        
        Wave["button"] = self.AddButtonToGlobal(Wave["Name"])
        self.setSettings()
        
        return self.waveList[Wave["Name"]]["Squad"]
    
    def add_wave_by_generate(self, 
                                nameWave : str = None,
                                path : str = "path_1"
                            ):
        Wave = {
            "Name" : nameWave,
            "Wave Queue" : self.waveCount,
            "Squad" : {},
            "Support" : [],
            "Money" : 0,
            "Settings" : 
            {
                "Description":"",
                "Sound":"",
                "StartWaveOutput" : "Target  wave_start_relay\nAction  Trigger",
                "InitWaveOutput" :  f"Target {path}\nAction  Trigger",
                "DoneOutput" :      "Target  wave_finished_relay\nAction  Trigger",
                "Custom" :          "",
            }
        }
        self.allWave.append(Wave)
        self.waveList[Wave["Name"]] = Wave
        self.waveCurrent = Wave["Name"]
        
        global CurrentWave
        CurrentWave = self.waveList[self.waveCurrent]
        
        global _AddButtonInWaveList
        _AddButtonInWaveList.clear()
        Wave["button"] = self.AddButtonToGlobal(Wave["Name"])
        self.setSettings()
        
        return self.waveList[Wave["Name"]]["Squad"]
    
    def Set_style_for_button(self, button : QtWidgets.QPushButton, active : bool):
        color = "0, 158, 26" if active else "48, 48, 48"
        
        if active:
            hover = ""
        else:
            hover = "QPushButton:hover{background-color: rgb(64, 64, 64);}"
            
        button.setStyleSheet("QPushButton{"
                                   f"background-color: rgb({color});\n"
                                   "font: 9pt \"TF2 Build\";\n"
                                   "border-bottom-left-radius: 7px;\n"
                                   "border-bottom-right-radius: 7px;\n"
                                   "}"
                                   f"{hover}")
        
    def AddButtonToGlobal(self, WaveName):
        if len(self.waveList) < 4:
            layer = self.components["horizontalLayoutWidget_3"]
            scrollBar = self.components["Wave_list_scrollbar_1"]
        else:
            layer = self.components["horizontalLayoutWidget_4"]
            scrollBar = self.components["Wave_lits_2"]

        pushButton_5 = QtWidgets.QPushButton( parent = layer )
        pushButton_5.setMinimumSize(QtCore.QSize(70, 26))
        pushButton_5.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        pushButton_5.setStyleSheet("QPushButton{\n"
                                   "background-color: rgb(48, 48, 48);\n"
                                   "font: 9pt \"TF2 Build\";\n"
                                   "border-bottom-left-radius: 7px;\n"
                                   "border-bottom-right-radius: 7px;\n"
                                   "}\n")
        
        pushButton_5.setObjectName(WaveName)
        pushButton_5.setText(WaveName)
        pushButton_5.setCheckable(True)
        pushButton_5.clicked.connect(lambda x : self.setWave(waveName=WaveName,button=pushButton_5) )
        self.allButtonsInGlobal.append(pushButton_5)
        scrollBar.addWidget(pushButton_5)
        
        self.setWave(waveName=WaveName,button=pushButton_5)
        
        self.EndList(layer, scrollBar)
        return pushButton_5
    
    def EndList(self, layer, scrollBar):
        if self.addWaveButton != None:
            self.addWaveButton.deleteLater()
        AddWave = QtWidgets.QPushButton( parent = layer)
        AddWave.setMinimumSize(QtCore.QSize(70, 26))
        AddWave.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        AddWave.setStyleSheet("QPushButton{\n"
                                "background-color: rgb(48, 48, 48);\n"
                                "font: 9pt \"TF2 Build\";\n"
                                "border-bottom-left-radius: 7px;\n"
                                "border-bottom-right-radius: 7px;\n"
                                "}\n"
                                "QPushButton:hover{\n"
                                "background-color: rgb(64, 64, 64);\n"
                                "}\n"
                                "QPushButton:checked{\n"
                                "background-color: rgb(0, 158, 26);\n"
                                "}")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(f"{_systemPath.get('Plus')}"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        AddWave.setIcon(icon2)
        AddWave.setObjectName("AddWave")
        AddWave.clicked.connect(lambda : self.addWave())
        self.addWaveButton = AddWave
        scrollBar.addWidget(AddWave)
        
        #if self.spacerItem != None:
        #    scrollBar.removeItem(self.spacerItem)
        #self.spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        #scrollBar.addItem(self.spacerItem)

class SquadSettings(object):
    global CurrentWave

    def __init__(self):
        self.SquadList = {}
        self.OperatingButtons = {}
        global SquadSettingsGlobal
        SquadSettingsGlobal = self
        self.curLocalSquad = None
        global Mercenary_now
        self.count_all_created_squad = 0

    def AddingToSquad(self, mercenary, Squad):
        if Squad not in self.SquadList:
            self.SquadList[Squad] = {
                "Name": Squad,
                "InSquad": [],
            }
        if mercenary not in self.SquadList[Squad]["InSquad"]:
            self.SquadList[Squad]["InSquad"].append(mercenary)

    def ClearSettingsSquad(self):
        self.SquadList.clear()
        self.curLocalSquad = None
        for key in ["WaitForAll_spawn_text", "WaitForAll_dead_text", "Squad Name"]:
            if key in self.OperatingButtons:
                self.OperatingButtons[key].clear()
                self.OperatingButtons[key].addItem("")

    def SetSquadFromSettings(self, squad: dict):
        Squad = {
            "Name": squad.get("Name"),
            "InSquad": [],
            "SpawnPostion": squad.get("SpawnPostion"),
            "Total Squad": squad.get("Total Squad"),
            "Max Alive Squads": squad.get("Max Alive Squads"),
            "Squad Spawn": squad.get("Squad Spawn"),
            "Credits For Squad": squad.get("Credits For Squad"),
            "Credist for one robot": squad.get("Credist for one robot"),
            "Wait For All Spawn": squad.get("Wait For All Spawn"),
            "Wait For All Dead": squad.get("Wait For All Dead"),
            "Wait Spawn Before": squad.get("Wait Spawn Before"),
            "Wait Spawn Between": squad.get("Wait Spawn Between"),
            "Squad Is Support": squad.get("Squad Is Support"),
            "Random Choice": squad.get("Random Choice"),
            "Random Spawn": squad.get("Random Spawn"),
            "Color": {
                "Id": squad.get("Color", {}).get("Id"),
                "rgb": squad.get("Color", {}).get("rgb"),
            },
            "Wave": squad.get("Wave"),
        }
        self.SquadList[Squad["Name"]] = Squad

        # Создание наемников для отряда, избегая циклов
        for mercenary in squad["InSquad"]:
            if mercenary.get("Squad") == squad["Name"]:
                m = Create_Mercenary_From_Save(mercenary, squad["Name"])
                if m not in Squad["InSquad"]:
                    Squad["InSquad"].append(m)

        for key in ["WaitForAll_spawn_text", "WaitForAll_dead_text", "Squad Name"]:
            if key in self.OperatingButtons:
                self.OperatingButtons[key].addItem(Squad["Name"])

        self.curLocalSquad = Squad["Name"]
        return Squad

    def AdditionButton(self, name: str, param):
        self.OperatingButtons[name] = param
        for item in self.OperatingButtons.values():
            try:
                item.disconnect()
                if isinstance(item, QtWidgets.QComboBox):
                    item.activated.connect(lambda: (self.SaveSquad(), WaveManagerGlobal.CountingWave()))
                elif isinstance(item, QtWidgets.QPushButton):
                    item.clicked.connect(lambda: (self.SaveSquad(), WaveManagerGlobal.CountingWave()))
                else:
                    item.editingFinished.connect(lambda: (self.SaveSquad(), WaveManagerGlobal.CountingWave()))
            except Exception as e:
                print(f"[Debug] Ошибка при подключении событий: {e}")

    def DeleteMercenary(self):
        squad_name = self.curLocalSquad
        if squad_name not in self.SquadList:
            print(f"[Debug] Squad '{squad_name}' not found in SquadList.")
            return
        _squad = self.SquadList[squad_name]["InSquad"]
        if Mercenary_now in _squad:
            _squad.remove(Mercenary_now)
            if len(_squad) == 0:
                self.SquadList.pop(squad_name, None)
                if "Squad" in CurrentWave and squad_name in CurrentWave["Squad"]:
                    CurrentWave["Squad"].pop(squad_name, None)
                self.curLocalSquad = None if not self.SquadList else next(iter(self.SquadList))
            if self.curLocalSquad is not None and self.curLocalSquad in self.SquadList:
                self.OpenSquad(self.curLocalSquad)
            elif self.SquadList:
                next_squad = next(iter(self.SquadList), None)
                if next_squad:
                    self.OpenSquad(next_squad)
            _AddButtonInWaveList.DeleteGlobalButton()
            WaveManagerGlobal.setWave(CurrentWave["Name"])

    def CreateSquad(self, nameSquad: str = None, total_squad=10, max_active=1, squad_spawn=1,
                    credit_for_squad=400, wait_before_spawn=0, wait_between_spawn=0,
                    wait_all_spawn="", wait_all_dead="", where_spawn=0, support=False,
                    random_choice=False, random_spawn=False):

        name = nameSquad or f"Squad {self.count_all_created_squad + 1}"
        self.count_all_created_squad += 1
        import random

        Squad = {
            "Name": name,
            "InSquad": [],
            "SpawnPostion": where_spawn,
            "Total Squad": total_squad,
            "Max Alive Squads": max_active,
            "Squad Spawn": squad_spawn,
            "Credits For Squad": credit_for_squad,
            "Credist for one robot": credit_for_squad // total_squad if total_squad else 1,
            "Wait For All Spawn": wait_all_spawn,
            "Wait For All Dead": wait_all_dead,
            "Wait Spawn Before": wait_before_spawn,
            "Wait Spawn Between": wait_between_spawn,
            "Squad Is Support": support,
            "Random Choice": random_choice,
            "Random Spawn": random_spawn,
            "Color": {"Id": "#ffffff", "rgb": (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))},
            "Wave": CurrentWave["Name"]
        }

        self.SquadList[name] = Squad
        self.curLocalSquad = name

        for key in ["WaitForAll_spawn_text", "WaitForAll_dead_text", "Squad Name"]:
            if key in self.OperatingButtons:
                self.OperatingButtons[key].addItem(name)

        CurrentWave.setdefault("Squad", {})[Squad["Name"]] = Squad
        WaveManagerGlobal.CountingWave()
        return Squad["Name"]

    def ColorUpdate(self, Settings):
        try:
            self.OperatingButtons["colorSquad"].setStyleSheet(
                f'background-color: rgb({Settings["Color"]["rgb"][0]}, {Settings["Color"]["rgb"][1]}, {Settings["Color"]["rgb"][2]});border-radius: 3px;'
            )
        except KeyError as e:
            print(f"[Debug] Ошибка обновления цвета: {e}")

    def OpenSquad(self, nameSquad: str):
        if self.curLocalSquad and self.curLocalSquad != nameSquad and self.curLocalSquad in self.SquadList:
            self.ColorUpdate(self.SquadList[self.curLocalSquad])

        if nameSquad in self.SquadList:
            self.curLocalSquad = nameSquad
            Settings = self.SquadList[nameSquad]
            self.OperatingButtons["colorSquad"].disconnect()
            self.ColorUpdate(self.SquadList[nameSquad])
            self.OperatingButtons["colorSquad"].clicked.connect(self.openSelectColor)

            squadbox = self.OperatingButtons["Squad Name"]
            squadbox.disconnect()
            squadbox.setCurrentText(Settings["Name"])
            squadbox.editTextChanged.connect(lambda: (self.SaveSquad(), self.OpenSquad(squadbox.currentText())))

            if type(Settings["SpawnPostion"]) is str:
                if self.OperatingButtons["comboBox_SpawnPosition"].findText(str(Settings["SpawnPostion"])) == -1:
                    self.OperatingButtons["comboBox_SpawnPosition"].addItem(str(Settings["SpawnPostion"]))
                self.OperatingButtons["comboBox_SpawnPosition"].setCurrentIndex(self.OperatingButtons["comboBox_SpawnPosition"].findText(str(Settings["SpawnPostion"])))
            elif type(Settings["SpawnPostion"]) is int:
                self.OperatingButtons["comboBox_SpawnPosition"].setCurrentIndex(Settings["SpawnPostion"])

            self.OperatingButtons["totalSquad_text"].setText(str(Settings["Total Squad"]))
            self.OperatingButtons["CreditForSquad_text"].setText(str(Settings["Credits For Squad"]))
            self.OperatingButtons["CreditSquadOneRobot_text"].setText(str(Settings["Credist for one robot"]))
            self.OperatingButtons["maxAlive_squad_text"].setText(str(Settings["Max Alive Squads"]))
            self.OperatingButtons["SquadSpawnCount_text"].setText(str(Settings["Squad Spawn"]))

            self.OperatingButtons["WaitForAll_spawn_text"].setCurrentText(str(Settings["Wait For All Spawn"]))
            self.OperatingButtons["WaitForAll_dead_text"].setCurrentText(str(Settings["Wait For All Dead"]))

            self.OperatingButtons["waitSpawn_Before_text"].setText(str(Settings["Wait Spawn Before"]))
            self.OperatingButtons["waitSpawn_Between_text"].setText(str(Settings["Wait Spawn Between"]))

            self.OperatingButtons["selecteble_button_RandomSpawn"].setChecked(bool(Settings["Random Spawn"]))
            self.OperatingButtons["selecteble_button_RandomChoice"].setChecked(bool(Settings["Random Choice"]))
            self.OperatingButtons["selecteble_button_SquadSupport"].setChecked(bool(Settings["Squad Is Support"]))

    def RemoveMySquad(self, mersenary, squadName: str):
        print(f"Removing {mersenary} from squad {squadName}")
        if squadName in self.SquadList and mersenary in self.SquadList[squadName]["InSquad"]:
            self.SquadList[squadName]["InSquad"].remove(mersenary)

    def clearSquad(self):
        to_remove = [item for item, squad in self.SquadList.items() if len(squad["InSquad"]) == 0]
        for item in to_remove:
            self.SquadList.pop(item, None)
            if "Squad" in CurrentWave and item in CurrentWave["Squad"]:
                CurrentWave["Squad"].pop(item, None)
                
        #for key in ["WaitForAll_spawn_text", "WaitForAll_dead_text", "Squad Name"]:
        #    if key in self.OperatingButtons:
        #        current_text = self.OperatingButtons[key].currentText()
        #        idx = self.OperatingButtons[key].findText(current_text)
        #        if idx != -1:
        #            self.OperatingButtons[key].removeItem(idx)
        #self.OperatingButtons[key].addItem("")
        #if "totalSquad_text" in self.OperatingButtons:
        #    self.OperatingButtons["totalSquad_text"].clear()
        #    for squad in self.SquadList.values():
        #        self.OperatingButtons["totalSquad_text"].insert(str(squad["Total Squad"]))
        
        WaveManagerGlobal.CountingWave()
        
    def SaveSquad(self, isGenerate=False):
        
        if not self.curLocalSquad or self.curLocalSquad not in self.SquadList or self.curLocalSquad == "" or len(self.curLocalSquad) < 1:
            return
        
        total_squad_text = self.OperatingButtons["totalSquad_text"].text()
        max_alive_squad_text = self.OperatingButtons["maxAlive_squad_text"].text()
        squad_spawn_text = self.OperatingButtons["SquadSpawnCount_text"].text()
        credit_for_squad_text = self.OperatingButtons["CreditForSquad_text"].text()

        total_squad = int(total_squad_text) if total_squad_text.isdigit() and int(total_squad_text) > 0 else 10
        credit_for_squad = int(credit_for_squad_text) if credit_for_squad_text.isdigit() and int(credit_for_squad_text) > 0 else 1

        Squad = {
            "Name": str(self.OperatingButtons["Squad Name"].currentText()),
            "SpawnPostion": self.OperatingButtons["comboBox_SpawnPosition"].currentText() if not isGenerate else self.SquadList[self.curLocalSquad]["SpawnPostion"],
            "Total Squad": total_squad,
            "Max Alive Squads": int(max_alive_squad_text) if max_alive_squad_text.isdigit() and int(max_alive_squad_text) > 0 else 1,
            "Squad Spawn": int(squad_spawn_text) if squad_spawn_text.isdigit() and int(squad_spawn_text) > 0 else 1,
            "Credits For Squad": credit_for_squad,
            "Credist for one robot": credit_for_squad // total_squad if total_squad else 1,
            "Wait For All Spawn": str(self.OperatingButtons["WaitForAll_spawn_text"].currentText()),
            "Wait For All Dead": str(self.OperatingButtons["WaitForAll_dead_text"].currentText()),
            "Wait Spawn Before": str(self.OperatingButtons["waitSpawn_Before_text"].text()),
            "Wait Spawn Between": str(self.OperatingButtons["waitSpawn_Between_text"].text()),
            "Squad Is Support": self.OperatingButtons["selecteble_button_SquadSupport"].isChecked(),
            "Random Choice": self.OperatingButtons["selecteble_button_RandomChoice"].isChecked(),
            "Random Spawn": self.OperatingButtons["selecteble_button_RandomSpawn"].isChecked(),
        }
        
        global Mercenary_now
        if Mercenary_now != None:
            Mercenary_now.ChangeMySquad(Squad["Name"])
            
        self.SquadList[self.curLocalSquad].update(Squad)
        self.OpenSquad(self.curLocalSquad)
        self.clearSquad()

    def openSelectColor(self):
        windowColor()  

class Mercenary(object):
    global SquadSettingsGlobal
    global General_Information_Robot
    
    def __init__(self, Squad, components : list = None):
        super().__init__()
        self.SquadName = Squad
        
        toClass = "Scout" # Кто по дефолту
        
        data = {
            "Name": default_stat.Mercenary[toClass].get("Name"),
            "Template": "",
            "Class": default_stat.Mercenary[toClass].get("Class"),
            "Class Name": default_stat.Mercenary[toClass].get("Class Name"),
            "Icon": default_stat.Mercenary[toClass].get("Icon"),
            "Health": default_stat.Mercenary[toClass].get("Health"),
            "Scale": default_stat.Mercenary[toClass].get("Scale"),
            "MaxVision": default_stat.Mercenary[toClass].get("MaxVision"),
            "AutoJump Min": default_stat.Mercenary[toClass].get("AutoJump Min"),
            "AutoJump Max": default_stat.Mercenary[toClass].get("AutoJump Max"),
            "Tag": default_stat.Mercenary[toClass].get("Tag"),
            "Skill": default_stat.Mercenary[toClass].get("Skill"),
            "Weapon Restriction": default_stat.Mercenary[toClass].get("Weapon Restriction"),
            "Behavior": default_stat.Mercenary[toClass].get("Behavior"),
            
            "Cosmetics": [],
            
            "Primary Weapon": WeaponData(toClass, "Primary"),
            "Secondary Weapons": WeaponData(toClass, "Secondary"),
            "Melee": WeaponData(toClass, "Melee"),
            
            "CharacterAttributes": {},
            
            "Tag_Attributes": dict(default_stat.Mercenary[toClass].get("Tag_Attributes", [])),
            "Attributes": default_stat.Mercenary[toClass].get("Attributes", []),
            "Custom Parametrs": default_stat.Mercenary[toClass].get("Custom Parametrs"),
            
            "Squad": self.SquadName,
            "power": 1,
            "model": default_stat.Mercenary[toClass].get("Model")
        }

        self.stat = data.copy()
        
        SquadSettingsGlobal.AddingToSquad(self, Squad)
        
        try:
            self.ui_components = components
            self.ui_components["Text"].setText(self.stat["Name"])
            squad_color = SquadSettingsGlobal.SquadList[self.SquadName]["Color"]["rgb"]
            self.ui_components["Button"].setStyleSheet(f"border-image: url({_systemPath.get(self.stat['Icon'])});\n"
                                                        f"background-color: rgba({squad_color[0]}, {squad_color[1]}, {squad_color[2]}, 255);\n"
                                                        "border-radius: 5px;")
        except:
            pass
        
    def Set_Stat(self, list : dict):
        self.stat = {
            "Name" : list["Name"],
            "Template" : list["Template"],
            "Class" : list["Class"],
            "Class Name" : list["Class Name"],
            "Icon" : list["Icon"],
            "Health" : list["Health"],
            "Scale" : list["Scale"],
            "MaxVision" : list["MaxVision"],
            "AutoJump Min" : list["AutoJump Min"],
            "AutoJump Max" : list["AutoJump Max"],
            "Tag" : list["Tag"],
            "Skill" : list["Skill"],
            "Weapon Restriction" : list["Weapon Restriction"],
            "Behavior" : list["Behavior"],
            
            "Cosmetics" : list["Cosmetics"],
            
            "Primary Weapon" : list["Primary Weapon"],
            "Secondary Weapons" : list["Secondary Weapons"],
            "Melee" : list["Melee"],
            
            "CharacterAttributes" : list["CharacterAttributes"],
            "Tag_Attributes" : list["Tag_Attributes"],
            "Attributes" : list["Attributes"] if "Attributes" in list else [],
            "Custom Parametrs" : list["Custom Parametrs"],
            
            "Squad" : list["Squad"], 
            "power" : 1,
            "model" : default_stat.Mercenary[list["Class Name"]]["Model"]
        }
       
        
    def Set_Stat_from_Save(self, list : dict):
        Primary = WeaponData()
        Primary.Set_Settings_From_Save(list["Primary Weapon"])
        
        Secondary = WeaponData()
        Secondary.Set_Settings_From_Save(list["Secondary Weapons"])
        
        Melee = WeaponData()
        Melee.Set_Settings_From_Save(list["Melee"])
        
        self.SquadName = list["Squad"]
        
        self.stat = {
            "Name":                list.get("Name"),
            "Template":            list.get("Template"),
            "Class":               list.get("Class"),
            "Class Name":          list.get("Class Name"),
            "Icon":                list.get("Icon"),
            "Health":              list.get("Health"),
            "Scale":               list.get("Scale"),
            "MaxVision":           list.get("MaxVision"),
            "AutoJump Min":        list.get("AutoJump Min"),
            "AutoJump Max":        list.get("AutoJump Max"),
            "Tag":                 list.get("Tag"),
            "Skill":               list.get("Skill"),
            "Weapon Restriction":  list.get("Weapon Restriction"),
            "Behavior":            list.get("Behavior"),
            "Cosmetics":           list.get("Cosmetics"),
            "Primary Weapon":      Primary,
            "Secondary Weapons":   Secondary,
            "Melee":               Melee,
            "CharacterAttributes": list.get("CharacterAttributes", {}),
            "Tag_Attributes":      list.get("Tag_Attributes", []),
            "Attributes":          list.get("Attributes", []),
            "Custom Parametrs":    list.get("Custom Parametrs"),
            "Squad":               list.get("Squad"),
            "power":               list.get("power"),
            "model":               default_stat.Mercenary[list.get("Class")]["Model"] if list.get("Class") in default_stat.Mercenary else None
        }
        
    def process_item_attributes(self, _template):
        atrWeapon = {}

        if "ItemAttributes" not in _template:
            return atrWeapon

        now_atr = None
        for item, atr in _template["ItemAttributes"].items():
            if item == "ItemName" and atr not in atrWeapon:
                atrWeapon[atr] = {"Attributes": {}}
                now_atr = atr
                findType = False

                # Функция для поиска типа оружия
                def find_weapon_type(weapon_class, weapon_type):
                    nonlocal findType
                    for weapon in weapons_libary.Weapon_Libary[weapon_class][weapon_type]:
                        weapon_data = weapons_libary.Weapon_Libary[weapon_class][weapon_type][weapon]
                        if weapon_data["Id"].lower() == atr.lower() or weapon_data["name"].lower() == atr.lower():
                            atrWeapon[atr]["Type"] = weapon_type
                            findType = True
                            return

                # Поиск в Primary, Secondary, Melee
                for weapon_type in ["Primary", "Secondary", "Melee"]:
                    if not findType:
                        find_weapon_type(_template["Class"].title(), weapon_type)

            elif now_atr:
                lib = atribute_libary.Atribute
                if item in lib:
                    atrWeapon[now_atr]["Attributes"][item] = lib[item]
                    atrWeapon[now_atr]["Attributes"][item]["Value"] = atr

        return atrWeapon
    
    def change_to_template(self, templateNameOrg : str, cosmetics : list = [], tags : list = []):
        templateName = f'T_TFBot_{templateNameOrg.replace("T_TFBot_", "")}'
        
        if len(templateName) <= 0 or templateName not in Template:
            return
        
        _template = Template[templateName]
        self.stat = {}
        
        if "name" not in _template:
            _template["name"] = _template["Class"]
        
        if "Scale" not in _template:
            _template["Scale"] = 1
            
        if "MaxVision" not in _template:
            _template["MaxVision"] = -1
        if "AutoJumpMin" not in _template:
            _template["AutoJumpMin"] = -1
        if "AutoJumpMax" not in _template:
            _template["AutoJumpMax"] = -1
        if "WeaponRestrictions" not in _template:
            _template["WeaponRestrictions"] = "None"
        if "Behavior" not in _template:
            _template["Behavior"] = 0
            
        if _template["Skill"] == "Easy":
            skill = 0
        elif _template["Skill"] == "Normal":
            skill = 1
        elif _template["Skill"] == "Hard":
            skill = 2
        elif _template["Skill"] == "Expert":
            skill = 3
        else: skill = 0
        
        if "WeaponRestrictions" not in _template:
            WeaponRestrictions = 0
        elif _template["WeaponRestrictions"] == "PrimaryOnly":
            WeaponRestrictions = 1
        elif _template["WeaponRestrictions"] == "SecondaryOnly":
            WeaponRestrictions = 2
        elif _template["WeaponRestrictions"] == "MeleeOnly":
            WeaponRestrictions = 3
        else:
            WeaponRestrictions = 0
        
        if   _template["Class"] == "Scout":         className = 0
        elif _template["Class"] == "Soldier":       className = 1
        elif _template["Class"] == "Pyro":          className = 2
        elif _template["Class"] == "Demoman":       className = 3
        elif _template["Class"] == "Heavy":         className = 4
        elif _template["Class"] == "Engineer":      className = 5
        elif _template["Class"] == "Medic":         className = 6
        elif _template["Class"] == "Sniper":        className = 7
        elif _template["Class"] == "Spy":           className = 8
        else:className = 0
        
        atrbutes = {}
        for Atribute in _template["CharacterAttributes"]:
            if Atribute.lower() in atribute_libary.Atribute:
                atr = atribute_libary.Atribute[Atribute]
                atr["Value"] = _template["CharacterAttributes"][Atribute]
                atrbutes[atr["Name"]] = atr

        if "ItemAttributes" in _template and "ItemName" in _template["ItemAttributes"]:
            weapon_data = weapons_libary.find_weapon_info(_template["ItemAttributes"]["ItemName"].title())
        else:
            weapon_data = None
            
        get_weapon_atr = self.process_item_attributes(_template)
        Attributes_primary = {}
        Attributes_secondary = {}
        Attributes_melee = {}
        
        if weapon_data is not None:
            if weapon_data["Type"] == "Primary":
                Attributes_primary = get_weapon_atr
            elif weapon_data["Type"] == "Secondary":
                Attributes_secondary = get_weapon_atr
            elif weapon_data["Type"] == "Melee":
                Attributes_melee = get_weapon_atr

        Primary =   WeaponData(Class=_template["Class"].title(), WeaponType="Primary",      weaponName=next(iter(weapons_libary.Weapon_Libary[_template["Class"].title()]["Primary"])), attrubutes =   Attributes_primary)
        Secondary = WeaponData(Class=_template["Class"].title(), WeaponType="Secondary",    weaponName=next(iter(weapons_libary.Weapon_Libary[_template["Class"].title()]["Secondary"])), attrubutes = Attributes_secondary)
        Melee =     WeaponData(Class=_template["Class"].title(), WeaponType="Melee",        weaponName=next(iter(weapons_libary.Weapon_Libary[_template["Class"].title()]["Melee"])), attrubutes =     Attributes_melee)

        cosmeticslist = []
        if "Items" in _template:
            for item in _template["Items"]:
                if item == "None" or item == None or item == "NoItem":
                    continue
                item_title = item.title()
                
                weapon_find = weapons_libary.find_weapon_info(item_title)
                index_name = parser.get_item_by_name(item_title)
                
                if weapon_find != None:
                    weapon_data = WeaponData(
                        Class=weapon_find["Class"],
                        WeaponType=weapon_find["Type"],
                        weaponName=weapon_find["name"],
                        attrubutes=self.process_item_attributes(_template)
                    )
                    if weapon_find["Type"] == "Primary":
                        Primary = weapon_data
                    elif weapon_find["Type"] == "Secondary":
                        Secondary = weapon_data
                    elif weapon_find["Type"] == "Melee":
                        Melee = weapon_data
                
                elif index_name != None:
                    cosmeticslist.append(index_name[0])

        cosmeticslist += cosmetics
        
        TagList = []
        if "Tag" in _template:
            TagList = _template["Tag"]
            if len(tags) > 0:
                TagList += tags
        else:
            TagList = tags
            
        ico = "None"
        if "ClassIcon" in _template:
            ico = _template["ClassIcon"]

        self.stat = {
            "Name" : str(_template["name"]).title(),
            "Template" : templateNameOrg.title(),
            "Class" : className,
            "Class Name" : _template["Class"].title(),
            "Icon" : ico,
            "Health" : int(_template["Health"]),
            "Scale" : _template["Scale"],
            "MaxVision" : int(_template["MaxVision"]),
            "AutoJump Min" : int(_template["AutoJumpMin"]),
            "AutoJump Max" : int(_template["AutoJumpMax"]),
            "Tag" : TagList,
            "Skill" : skill,
            "Weapon Restriction" : WeaponRestrictions,
            "Behavior" : _template["Behavior"],
            
            "Cosmetics" :  cosmeticslist,
            
            "Primary Weapon" :      Primary,
            "Secondary Weapons" :   Secondary,
            "Melee" :               Melee,
            
            "CharacterAttributes" : atrbutes,
            "Tag_Attributes" : _template.get("Attributes", []),
            "Attributes" : _template.get("Attributes", []),
            "Custom Parametrs" : """""",

            "Squad" : self.SquadName,
            "power" : 2 *  (int(_template["Health"]) / 1000),
            "model" : default_stat.Mercenary[_template["Class"].title()]["Model"]
        }  
        self.open()
        
    def change_class(self, toClass : str = "Scout", isGenerated = False):
        if len(toClass) <= 0 or toClass not in default_stat.Mercenary:
            return
                
        if toClass == "Tank":
            Primary =   WeaponData(Class="Scout", WeaponType="Primary",             weaponName=next(iter(weapons_libary.Weapon_Libary["Scout"]["Primary"])))
            Secondary = WeaponData(Class="Scout", WeaponType="Secondary",           weaponName=next(iter(weapons_libary.Weapon_Libary["Scout"]["Secondary"])))
            Melee =     WeaponData(Class="Scout", WeaponType="Melee",               weaponName=next(iter(weapons_libary.Weapon_Libary["Scout"]["Melee"])))
        else:
            Primary =   WeaponData(Class=toClass.title(), WeaponType="Primary",     weaponName=next(iter(weapons_libary.Weapon_Libary[toClass.title()]["Primary"])))
            Secondary = WeaponData(Class=toClass.title(), WeaponType="Secondary",   weaponName=next(iter(weapons_libary.Weapon_Libary[toClass.title()]["Secondary"])))
            Melee =     WeaponData(Class=toClass.title(), WeaponType="Melee",       weaponName=next(iter(weapons_libary.Weapon_Libary[toClass.title()]["Melee"])))
        
        self.stat = {
            "Name" : default_stat.Mercenary[toClass].get("Name"),
            "Template" : "",
            "Class" : default_stat.Mercenary[toClass].get("Class"),
            "Class Name" : default_stat.Mercenary[toClass].get("Class Name"),
            "Icon" : default_stat.Mercenary[toClass].get("Icon"),
            "Health" : default_stat.Mercenary[toClass].get("Health"),
            "Scale" : default_stat.Mercenary[toClass].get("Scale"),
            "MaxVision" : default_stat.Mercenary[toClass].get("MaxVision"),
            "AutoJump Min" : default_stat.Mercenary[toClass].get("AutoJump Min"),
            "AutoJump Max" : default_stat.Mercenary[toClass].get("AutoJump Max"),
            "Tag" : default_stat.Mercenary[toClass].get("Tag"),
            "Skill" : default_stat.Mercenary[toClass].get("Skill"),
            "Weapon Restriction" : default_stat.Mercenary[toClass].get("Weapon Restriction"),
            "Behavior" : default_stat.Mercenary[toClass].get("Behavior"),
            
            "Cosmetics" : default_stat.Mercenary[toClass].get("Cosmetics"),
            
            "Primary Weapon" :  Primary,
            "Secondary Weapons" : Secondary,
            "Melee" : Melee,
            
            "CharacterAttributes" : {},
            "Tag_Attributes" : default_stat.Mercenary[toClass].get("Tag_Attributes", []),
            "Attributes" : default_stat.Mercenary[toClass].get("Attributes", []),
            "Custom Parametrs" : default_stat.Mercenary[toClass].get("Custom Parametrs"),

            "Squad" : self.SquadName, 
            "model" : default_stat.Mercenary[toClass].get("Model"),
        }
        if isGenerated == False:
            self.open()
        
    def update_squad_icon(self):
        try:
            squad_color = SquadSettingsGlobal.SquadList[self.SquadName]["Color"]["rgb"]
            self.ui_components["Button"].setStyleSheet(f"border-image: url({_systemPath.get(General_Information_Robot['Stats_Icon_comboBox Text'].currentText(), path='Leaderboard')});\n"
                                                    f"background-color: rgba({squad_color[0]}, {squad_color[1]}, {squad_color[2]}, 255);\n"
                                                    "border-radius: 5px;")
        except:
            pass
        
    def update_icons(self):
        icon_name = General_Information_Robot['Stats_Icon_comboBox Text'].currentText()
        self.stat["Icon"] = icon_name
        try:
            self.ui_components["Button"].setStyleSheet(f"border-image: url({_systemPath.get(icon_name,'Leaderboard')});\n"
                                                        "background-color: rgb(58, 109, 57);\n"
                                                        "border-radius: 5px;")
            
            self.ui_components["Text"].setText(self.stat["Name"])
            General_Information_Robot["Icon_withName Icon"].setStyleSheet(f"border-image: url({_systemPath.get(icon_name,'Leaderboard')});")
            self.update_weapon_icon(info=self.stat["Primary Weapon"],gunIndex=0)
            self.update_weapon_icon(info=self.stat["Secondary Weapons"],gunIndex=1)
            self.update_weapon_icon(info=self.stat["Melee"],gunIndex=2)
            
        except:
            pass
        
    def ChangeMySquad(self, squad : str):
        self.stat["Squad"] = squad
        self.SquadName = squad
        self.update_icons()
            
    def setNewButtons(self, component):
        self.ui_components = component
        self.update_squad_icon()
        
    def open(self, isGenerate = False):
        SquadSettingsGlobal.OpenSquad(self.stat["Squad"])
        try:
            global buttonMercenaryActive
            buttonMercenaryActive = self.ui_components["Button"]
        except:
            pass
        
        general_icon = General_Information_Robot["Stats_Icon_comboBox Text"]
        general_icon.clear()

        for item in Icons_Archive:
            icon1 = QtGui.QIcon()
            icon1.addPixmap(QtGui.QPixmap(f"{_systemPath.get(item)}" ), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            general_icon.addItem(icon1, item.replace("Leaderboard_", "").replace("leaderboard_", "").replace("class_", ""))
            
        classIcons = General_Information_Robot["Stats_ClassMercenary"]
        classIcons.disconnect()
        classIcons.clear()
        
        for item in default_stat.Mercenary:
            icon1 = QtGui.QIcon()
            icon1.addPixmap(QtGui.QPixmap(f"{_systemPath.get(default_stat.Mercenary[item]['Icon'])}" ), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            classIcons.addItem(icon1, item.replace("Leaderboard_", "").replace("leaderboard_", "").replace("class_", ""))
        
        classTemaplte = General_Information_Robot["Stats_Template"]
        classTemaplte.clear()
        try: 
            classTemaplte.disconnect()
        except:
            pass
        for item in Template:
            icon1 = QtGui.QIcon()
            if "ClassIcon" in Template[item]:
                iconType = Template[item]['ClassIcon']
                icon1.addPixmap(QtGui.QPixmap(f"{_systemPath.get(iconType)}" ), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                classTemaplte.addItem(icon1, item.replace("Leaderboard_", "").replace("leaderboard_", "").replace("class_", "").replace("T_TFBot_", ""))
            else:
                classTemaplte.addItem(item.replace("T_TFBot_", ""))
        
        for item in range(general_icon.count()):
            if general_icon.itemText(item) in self.stat["Icon"]:
                general_icon.setCurrentIndex(item)
                
        self.update_icons()
                
        General_Information_Robot['Name_Text'].setText(self.stat["Name"])
        
        General_Information_Robot["Stats_Healt Text"].setText( str(self.stat["Health"]) )        
        General_Information_Robot["Stats_Scale Text"].setText( str(self.stat["Scale"]) )
        
        General_Information_Robot["Stats_MaxVisionRange Text"].setText( str(self.stat["MaxVision"]) )
        
        General_Information_Robot["Stats_AutoJump_min Text"].setText( str(self.stat["AutoJump Min"]) )
        General_Information_Robot["Stats_AutoJump_max Text"].setText( str(self.stat["AutoJump Max"]) )
        
        General_Information_Robot["Stats_Skill_comboBox ComboBox"].setCurrentIndex(self.stat["Skill"])
        
        General_Information_Robot["Stats_Behaivior_comboBox Text"].setCurrentIndex(self.stat["Behavior"])
        
        for item in General_Information_Robot:
            try:
                General_Information_Robot[item].disconnect()
                if type(General_Information_Robot[item]) == QtWidgets.QComboBox:
                    General_Information_Robot[item].activated.connect(lambda : (self.save()))
                    pass
                else:
                    General_Information_Robot[item].editingFinished.connect(lambda : (self.save()))
                #print(f"[DEBUG <Open Stats Robot>]  Success <Add connect (self.save()) for> : {item} GOOD")
            except:
                #print(f"[DEBUG <Open Stats Robot>]  ERROR <Can`t disconect or add connect for> : {item} ERROR")
                pass
        General_Information_Robot["comboBox_Stats_Tag ComboBox"].clear()
        
        for item in self.stat["Tag"]:
            General_Information_Robot["comboBox_Stats_Tag ComboBox"].addItem(item)        
        try:
            General_Information_Robot["Stats_WeaponRestriction_comboBox Text"].setCurrentIndex(self.stat["Weapon Restriction"])
        except:pass
        classIcons.setCurrentIndex(self.stat["Class"])
        
        classIcons.currentIndexChanged.connect(lambda x: (self.change_class(classIcons.currentText().title())))
        
        if len(str(self.stat["Template"])) > 0:
            classTemaplte.setCurrentIndex(classTemaplte.findText(self.stat["Template"]))
        classTemaplte.currentIndexChanged.connect(lambda x: self.change_to_template(classTemaplte.currentText()))
        
        self.rebuild_cosmetics()
        
        global Atribute_global
        Atribute_global.Open_General(self.stat['CharacterAttributes'])
        
        global CustomAtributeGlobal
        CustomAtributeGlobal.SetText(str(self.stat["Custom Parametrs"]))
        
        if isGenerate == False:
            global ModelViewRuntime
            if ModelViewRuntime:
                if self.stat["model"] is not None and len(self.stat["model"]) > 0:
                    ModelViewRuntime.create_new_model(
                        model_path=self.stat["model"]["obj"], 
                        texture_path=self.stat["model"]["texture"],
                        mtl_path=self.stat["model"]["mtl"],
                    )
                else:
                    ModelViewRuntime.remove_model() 

        self.update_icons()
                
    def rebuild_cosmetics(self):
        global cosmetic_list_class
        cosmetic_list_class.clear()
        cosmetic_list_class.AddCosmeticsFromList(self.stat["Cosmetics"])
        
    def save(self):
        self.stat["Class"] = General_Information_Robot["Stats_ClassMercenary"].currentIndex()
        self.stat["Name"] = General_Information_Robot["Name_Text"].text()
        self.stat["Health"] = General_Information_Robot["Stats_Healt Text"].text()
        self.stat["Scale"] = General_Information_Robot["Stats_Scale Text"].text()
        self.stat["MaxVision"] = General_Information_Robot["Stats_MaxVisionRange Text"].text()
        self.stat["AutoJump Min"] = General_Information_Robot["Stats_AutoJump_min Text"].text()
        self.stat["AutoJump Max"] = General_Information_Robot["Stats_AutoJump_max Text"].text()
        self.stat["Skill"] = General_Information_Robot["Stats_Skill_comboBox ComboBox"].currentIndex()
        
        global Atribute_global
        self.stat['CharacterAttributes'] = Atribute_global.activeStats
        
        global CustomAtributeGlobal
        self.stat["Custom Parametrs"] = str(CustomAtributeGlobal.Get())
        
        # save tag
        tag_combobox = General_Information_Robot["comboBox_Stats_Tag ComboBox"]
        if tag_combobox.currentIndex() != -1:
            sd = []
            for item in range(tag_combobox.count()):
                text = tag_combobox.itemText(item)
                sd.append(text)
            self.stat["Tag"] = sd
            
        self.stat["Weapon Restriction"] = General_Information_Robot["Stats_WeaponRestriction_comboBox Text"].currentIndex()
        self.stat["Behavior"] = General_Information_Robot["Stats_Behaivior_comboBox Text"].currentIndex()
        
        self.update_squad_icon()
        self.update_icons()
    
    def change_first_weapon_def(self, stat_weapon = None, gunIndex = str):
        if stat_weapon != None:
            data = WeaponData(Class=self.stat["Class Name"], WeaponType = gunIndex, weaponName = stat_weapon["name"])
            print(f"[DEBUG <Mercenary.change_first_weapon_def>]  Change weapon {gunIndex} to {stat_weapon['name']}")
            info = data
            if gunIndex == "Primary":
                self.stat["Primary Weapon"] = data
            elif gunIndex == "Secondary":
                self.stat["Secondary Weapons"] = data
            elif gunIndex == "Melee":
                self.stat["Melee"] = data
            self.save()
        else:
            info = self.stat["Primary Weapon"]
            
        self.update_weapon_icon(info, gunIndex)

    def update_weapon_icon(self, info, gunIndex: int):
        name = f'""{info.get("Custom Name")}""' if len(info.get("Custom Name")) > 0 else info.get("Name")
        quality = colorQuality[info.get('Quality')]
        
        icon = _systemPath.get(info.get('Icon'), 'weapon')
        
        if icon is None:
            icon = info.get('Icon')
            
            if icon is None:
                item = parser.get_item_by_name(info.get('Name'))

                if item:
                    icon = get_icon_from_game(item[0])                    
            
        if gunIndex == 0:
            General_Information_Robot["Primary label_7"].setText(name)
            General_Information_Robot["Primary label_7"].setStyleSheet(f"color: rgb({quality});font: 7pt \"TF2 Build\";")
            General_Information_Robot["FirsGun  frame"].setStyleSheet(f"border-image: url({icon});")
        elif gunIndex == 1:
            General_Information_Robot["ButtonAddPremoryGun label_13"].setText(name)
            General_Information_Robot["ButtonAddPremoryGun label_13"].setStyleSheet(f"color: rgb({quality});font: 7pt \"TF2 Build\";")
            General_Information_Robot["ButtonAddPremoryGun frame_3"].setStyleSheet(f"border-image: url({icon});")
        elif gunIndex == 2:
            General_Information_Robot["ButtonAddMelee label_14"].setText(name)
            General_Information_Robot["ButtonAddMelee label_14"].setStyleSheet(f"color: rgb({quality});font: 7pt \"TF2 Build\";")
            General_Information_Robot["ButtonAddMelee frame_4"].setStyleSheet(f"border-image: url({icon});")


class CustomAtributes(object):
    def __init__(self):
        self.Text = None
        self.window = None
        self.editor = None  # Инициализируем как None

    def Show(self):
        from PyQt6.QtWidgets import QVBoxLayout, QDialog
        from PyQt6.QtCore import Qt
        import custom_editor
        global Mercenary_now
        if Mercenary_now is None:
            return

        # Закрываем старое окно если оно есть
        if self.window is not None:
            try:
                self.window.close()
            except Exception:
                pass

        # Создаём окно диалога
        dialog = QDialog()
        dialog.setWindowTitle("Custom Attributes Editor")
        dialog.resize(700, 500)
        # Делаем окно полнофункциональным (можно разворачивать/сворачивать)
        dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowType.WindowMinMaxButtonsHint | Qt.WindowType.Window)

        # Создаём layout для диалога
        layout = QVBoxLayout()

        # Создаём редактор
        editor = custom_editor.PopEditorWindow(dialog)
        layout.addWidget(editor)

        # Добавляем панель кнопок из custom_editor
        btn_panel = custom_editor.EditorButtonPanel(dialog, on_save=self.Save, on_cancel=self.Close)
        layout.addWidget(btn_panel)

        # Устанавливаем layout для диалога
        dialog.setLayout(layout)

        # Сохраняем ссылки на объекты
        self.window = dialog
        self.editor = editor

        # Устанавливаем текст если он был задан ранее
        if self.Text is not None:
            self.editor.editor.setText(str(self.Text))
        # Иначе берём из текущего Mercenary
        else:
            self.SetText(Mercenary_now.stat["Custom Parametrs"])

        # Показываем окно
        dialog.show()

    def Save(self):
        if self.editor is not None:
            self.Text = self.editor.editor.text()
            global Mercenary_now
            Mercenary_now.stat["Custom Parametrs"] = self.Text
            Mercenary_now.save()
            self.Close()

    def Close(self):
        if self.window is not None:
            self.window.close()
            self.window = None
            self.editor = None

    def Get(self):
        if self.editor is not None:
            return self.editor.editor.text()
        return self.Text

    def SetText(self, text):
        self.Text = str(text)
        # Если окно открыто, обновляем текст в редакторе
        if self.editor is not None:
            self.editor.editor.setText(str(text))


class Atributes:
    global Mercenary_now
    def __init__(self, stat = None, scrollAreaWidgetContents_5 = None, verticalLayout_4 = None, horizontalLayout_2 = None):
        
        self.atribut = atribute_libary.Atribute
        
        self.stat = stat
        self.scrollAreaWidgetContents_5 = scrollAreaWidgetContents_5
        self.verticalLayout_4 = verticalLayout_4
        self.horizontalLayout_2 = horizontalLayout_2
        self.spacer_2 = None
        self.ListButton = []
        self.AllButtonTile = []
        self.activeStats = {}
        self.AddDefault()

    def AddButtonToGeneral(self, stat = None, button = None):

        if button is not None:
            self.DeleteFromList(button)
        #self.exit_select() #close window
        
        if stat["Name"].title() in self.activeStats:
            return
        
        if self.spacer_2 is not None:
            self.verticalLayout_4.removeItem(self.spacer_2)

        Item_Atribute = QtWidgets.QGroupBox(parent=self.scrollAreaWidgetContents_5)
        Item_Atribute.setMinimumSize(QtCore.QSize(300, 30))
        Item_Atribute.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        Item_Atribute.setStyleSheet("border:0;")
        Item_Atribute.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        Item_Atribute.setFlat(False)
        Item_Atribute.setCheckable(False)
        Item_Atribute.setObjectName("Item_Atribute")

        # Layout для содержимого
        h_layout = QtWidgets.QHBoxLayout(Item_Atribute)
        h_layout.setContentsMargins(5, 2, 5, 2)
        h_layout.setSpacing(8)

        DeleteCosmeticButton_2 = QtWidgets.QPushButton()
        DeleteCosmeticButton_2.setFixedSize(24, 24)
        DeleteCosmeticButton_2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        DeleteCosmeticButton_2.setStyleSheet("background-color: rgba(0, 0, 0,0); font: 21pt 'TF2'; color: rgb(185, 45, 43);")
        DeleteCosmeticButton_2.setObjectName("DeleteCosmeticButton")
        DeleteCosmeticButton_2.setText("-")
        h_layout.addWidget(DeleteCosmeticButton_2)

        ButtunAddAtributes_2 = QtWidgets.QPushButton()
        ButtunAddAtributes_2.setMinimumSize(QtCore.QSize(120, 30))
        ButtunAddAtributes_2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        ButtunAddAtributes_2.setAccessibleDescription("")
        ButtunAddAtributes_2.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        ButtunAddAtributes_2.setAutoFillBackground(False)
        ButtunAddAtributes_2.setStyleSheet("background-color: rgb(65,65,65);border-radius: 5px;font: 12pt 'TF2';")
        ButtunAddAtributes_2.setCheckable(False)
        ButtunAddAtributes_2.setChecked(False)
        ButtunAddAtributes_2.setObjectName("ButtunAddAtributes_2")
        h_layout.addWidget(ButtunAddAtributes_2, stretch=2)

        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setMinimumSize(QtCore.QSize(60, 24))
        self.lineEdit.setMaximumWidth(80)
        self.lineEdit.setStyleSheet("background-color: rgb(80, 80, 80); border:0; border-radius: 5px; font: 12pt 'TF2';")
        self.lineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        h_layout.addWidget(self.lineEdit)

        icon3 = QtGui.QIcon()

        if stat is not None:
            if "Value" not in stat:
                stat['Value'] = 0
            if stat["Effect"] == "Positive":
                ico = "Pictogram_plus"
                color = "0,202,40"
            elif stat["Effect"] == "Nigative":
                ico = "Pictogram_minus"
                color = "183,45,43"
            else:
                ico = "Pictogram_neutral"
                color = "100,100,100"
            icon3.addPixmap(QtGui.QPixmap(f"{_systemPath.get(ico)}"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            ButtunAddAtributes_2.setStyleSheet(f"background-color: rgb(65,65,65);border-radius: 5px;font: 12pt 'TF2'; color: rgb({color})")
            ButtunAddAtributes_2.setText(stat["Name"].title())
            self.lineEdit.setText(f"{stat['Value']}")
            self.lineEdit.editingFinished.connect(lambda: self.editValue(stat['Name'].title(), self.lineEdit.text()))
            
            self.ListButton.append(Item_Atribute)
            
            DeleteCosmeticButton_2.clicked.connect(lambda: self.remove(Item_Atribute, stat))
            
            self.activeStats[stat['Name'].title()] = stat
        else:
            ButtunAddAtributes_2.setText("None")
        ButtunAddAtributes_2.setIcon(icon3)

        self.verticalLayout_4.addWidget(Item_Atribute)
        self.spacer_2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_4.addItem(self.spacer_2)
        Mercenary_now.save()
    
    def BaseInterface(self):
        if Mercenary_now is None:
            return
        self.spacer = None
        GroupBox = QtWidgets.QMainWindow()
        GroupBox.setObjectName("GroupBox")
        GroupBox.resize(453, 460)
        GroupBox.setMinimumSize(QtCore.QSize(372, 360))
        # Убираем максимальный размер чтобы окно могло растягиваться
        GroupBox.setAutoFillBackground(False)
        GroupBox.setStyleSheet("background-color: rgb(48, 48, 48);")

        self.GroupBox = GroupBox
        
        # Создаем центральный виджет для QMainWindow
        centralWidget = QtWidgets.QWidget(GroupBox)
        GroupBox.setCentralWidget(centralWidget)
        mainLayout = QtWidgets.QVBoxLayout(centralWidget)
        
        # Создаем виджеты с относительным позиционированием
        searchLayout = QtWidgets.QHBoxLayout()
        Seach_lineedit = QtWidgets.QLineEdit()
        Seach_lineedit.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        Seach_lineedit.setStyleSheet("font: 11pt \"TF2\";border:0;border-radius: 7px;background-color: rgb(61, 61, 61);color: rgb(255, 255, 255);")
        Seach_lineedit.setObjectName("Seach_lineedit")
        
        Seach_icon = QtWidgets.QFrame()
        Seach_icon.setFixedSize(16, 16)
        Seach_icon.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        Seach_icon.setStyleSheet(f"border-image: url({_systemPath.get('search','Interface')});background-color: rgba(255, 255, 255,0);")
        Seach_icon.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        Seach_icon.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        Seach_icon.setObjectName("Seach_icon")
        
        searchLayout.addWidget(Seach_lineedit)
        searchLayout.addWidget(Seach_icon)
        mainLayout.addLayout(searchLayout)
        
        List = QtWidgets.QScrollArea()
        List.setEnabled(True)
        List.setWidgetResizable(True)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        List.setSizePolicy(sizePolicy)
        
        font = QtGui.QFont()
        font.setFamily("TF2")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setKerning(True)
        List.setFont(font)
        List.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        List.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        List.setAcceptDrops(False)
        List.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        List.setAutoFillBackground(False)
        List.setStyleSheet("QWidget{    background-color: rgb(48, 48, 48);}:handle, QWidget:vertical  {    border-radius: 5px;    background-color: rgb(56, 56, 56);    width: 10px;    min-height: 30px;}:handle, QWidget:horizontal  {    border-radius: 5px;    background-color: rgb(56, 56, 56);    width: 10px;    min-width: 10px;}:groove, QWidget:vertical {    background-color: rgb(72, 72, 72);    border-radius:  4px;}:sub-line, QWidget:vertical{    background-color: rgba(255, 255, 255, 0);}:add-line, QWidget:vertical{    background-color: rgba(255, 255, 255, 0);}QWidget::add-page:horizontal, QWidget::sub-page:horizontal {    background: none;}QWidget::add-page:vertical, QWidget::sub-page:vertical {    background: none;}")
        List.setFrameShape(QtWidgets.QFrame.Shape.Box)
        List.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        List.setLineWidth(1)
        List.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        List.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        List.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        List.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        List.setObjectName("List")
        
        self.scrollAreaWidgetContents_6 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_6.setObjectName("scrollAreaWidgetContents_6")
        verticalLayout_8 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_6)
        verticalLayout_8.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        verticalLayout_8.setObjectName("verticalLayout_8")
        List.setWidget(self.scrollAreaWidgetContents_6)
        
        verticalLayout = QtWidgets.QVBoxLayout()
        verticalLayout.setObjectName("verticalLayout")

        self.verticalLayout = verticalLayout
        self.FillTileAtribute()
        verticalLayout_8.addLayout(verticalLayout)
        
        mainLayout.addWidget(List)
        
        Cancel = QtWidgets.QPushButton()
        Cancel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        Cancel.setStyleSheet("""
                             border-radius: 5px; 
                             height: 20px;
                             background-color: rgb(176, 57, 57);
                             color: rgb(255, 255, 255);
                             font: 9pt \"TF2 Build\";"""
                            )
        Cancel.setObjectName("Cancel")
        Cancel.setText("Cancel")
        Cancel.clicked.connect(lambda : self.exit_select())
        mainLayout.addWidget(Cancel)
        
        Seach_lineedit.editingFinished.connect(lambda: self.Search(Seach_lineedit.text()))
        
        QtCore.QMetaObject.connectSlotsByName(GroupBox)
        GroupBox.show()
        
        global Addition_interface
        Addition_interface = GroupBox
    
    def AddDefault(self):
        ButtunAddAtributes = QtWidgets.QPushButton(parent=self.scrollAreaWidgetContents_5)
        ButtunAddAtributes.setMinimumSize(QtCore.QSize(300, 30))
        ButtunAddAtributes.setBaseSize(QtCore.QSize(0, 25))
        ButtunAddAtributes.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        ButtunAddAtributes.setStyleSheet("background-color: rgb(65, 65, 65);\n"
                                           "border-radius: 5px;\n"
                                           "font: 12pt \"TF2\";")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"{_systemPath.get('Plus')}"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        ButtunAddAtributes.setIcon(icon)
        ButtunAddAtributes.setCheckable(False)
        ButtunAddAtributes.setChecked(False)
        ButtunAddAtributes.setObjectName("ButtunAddAtributes")
        
        ButtunAddAtributes.clicked.connect(lambda : self.BaseInterface())

        self.Default = ButtunAddAtributes
        self.verticalLayout_4.addWidget(ButtunAddAtributes)
        
    def AddButton(self, stat=None, indexPosition = -1):
        if stat["Name"].title() in self.activeStats:
            return
        Item = QtWidgets.QGroupBox(parent=self.scrollAreaWidgetContents_6)
        Item.setMinimumSize(QtCore.QSize(130, 50))
        Item.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        Item.setStyleSheet("border:0;")
        Item.setObjectName("Item")

        # Layout для содержимого
        h_layout = QtWidgets.QHBoxLayout(Item)
        h_layout.setContentsMargins(8, 4, 8, 4)
        h_layout.setSpacing(10)

        Icon = QtWidgets.QFrame(parent=Item)
        Icon.setFixedSize(32, 32)
        Icon.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        Icon.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        Icon.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        Icon.setObjectName("Icon")
        h_layout.addWidget(Icon)

        ButtonAddCosmetic = QtWidgets.QPushButton(parent=Item)
        ButtonAddCosmetic.setMinimumHeight(40)
        ButtonAddCosmetic.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        ButtonAddCosmetic.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        ButtonAddCosmetic.setStyleSheet("background-color: rgb(56, 56, 56); border-radius: 10px; font: 12pt 'TF2 Build';")
        ButtonAddCosmetic.setIconSize(QtCore.QSize(90, 90))
        ButtonAddCosmetic.setObjectName("ButtonAddCosmetic")
        h_layout.addWidget(ButtonAddCosmetic, stretch=2)
        
        if indexPosition == -1:
            self.verticalLayout.addWidget(Item)
        else:
            self.verticalLayout.insertWidget(indexPosition, Item)

        if stat is not None:
            if stat["Effect"] == "Positive":
                ico = "Pictogram_plus"
                color = "0,202,40"
            elif stat["Effect"] == "Nigative":
                ico = "Pictogram_minus"
                color = "183,45,43"
            else:
                ico = "Pictogram_neutral"
                color = "100,100,100"
            Icon.setStyleSheet(f"border-image: url({_systemPath.get(ico)}); background-color: rgba(255, 255, 255, 0);")
            ButtonAddCosmetic.setStyleSheet(f"background-color: rgb(56, 56, 56); border-radius: 10px; font: 12pt 'TF2 Build'; color: rgb({color});")
            ButtonAddCosmetic.setText(stat["Name"])
            event = lambda x: self.AddButtonToGeneral(stat, Item)
            ButtonAddCosmetic.mousePressEvent = event 
            Icon.mousePressEvent = event
        else:
            Icon.setStyleSheet(f"border-image: url({_systemPath.get('Plus')}); background-color: rgba(255, 255, 255, 0);")
            
        self.AllButtonTile.append(Item)
        
        if self.spacer is not None:
            self.verticalLayout.removeItem(self.spacer)
            
        self.spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(self.spacer)

    def editValue(self, objName, value : float):
        self.activeStats[objName]["Value"] = value
        Mercenary_now.save()
        
    def remove(self, button, stat):           
        self.ListButton.remove(button)
        try:
            self.activeStats.pop(stat["Name"].title())
            self.verticalLayout_4.removeWidget(button)
        except Exception as e:
            print(f"[ERROR] <Atributes> Can`t remove {stat['Name']} from activeStats: {e}")
            
        button.deleteLater()
        self.ReturnButtonAttribute(stat)
            
    def ReturnButtonAttribute(self, stat):
        self.AddButton(stat, 0)

    def Clear(self):
        if len(self.ListButton) > 0:
            for item in self.ListButton:
                self.verticalLayout_4.removeWidget(item)
                item.deleteLater()
            self.ListButton.clear()
            
    def ClearTile(self):
        if len(self.AllButtonTile) > 0:
            for item in self.AllButtonTile:
                try: item.deleteLater()
                except:pass
            self.AllButtonTile.clear()
            
    def FillTileAtribute(self, key = ""):
        if len(key) > 0:
            self.ClearTile()
        
        for item in self.atribut:
            if len(key) > 0:
                if key.lower() in self.atribut[item]["Name"].lower():
                    self.AddButton(self.atribut[item])
            else: 
                self.AddButton(self.atribut[item])
    
    def Search(self, searchText):
        self.FillTileAtribute(key = searchText)

    def DeleteFromList(self, button):
        try:
            button.deleteLater()
        except Exception as e:
            print(f"[ERROR] <Atributes> Could not delete button {button}: {e}")

    def Open_General(self, stat):
        self.Clear()
        self.activeStats={}
        for item in stat:
            self.AddButtonToGeneral(stat[item])        

    def exit_select(self):
        self.GroupBox.close()

class AtributeUI(QtWidgets.QMainWindow):
    global Mercenary_now
    def __init__(self):
        super().__init__()
        self.buttonList : QtWidgets.QPushButton = []
        self.current_attribute = []
        self.setupUi()

    def Show(self):
        if Mercenary_now is None:
            return
        stat = Mercenary_now.stat["Attributes"]
        for item in self.buttonList:
            item.setChecked(False)
            if item.text() in stat:
                item.setChecked(True)
                
        _tag = Mercenary_now.stat["Tag"]
        for item in self.buttonList:
            if item.text().lower() in _tag:
                item.setChecked(True)
                
        self.current_attribute = list(Mercenary_now.stat["Attributes"])
        self.show()

    def Close(self):
        self.current_attribute.clear()
        self.close()
        
    def SaveStat(self):
        Mercenary_now.stat["Attributes"] = self.current_attribute
        Mercenary_now.save()

        self.close()

    def AddRemoveAtribute(self, nameAtr, active):
        if active and nameAtr not in self.current_attribute:
            self.current_attribute.append(nameAtr)
            
        elif active == False and nameAtr in self.current_attribute:
            indx = self.current_attribute.index(nameAtr)
            self.current_attribute.pop(indx)
        
    def setupUi(self):
        self.setObjectName("AtributeUI")
        self.resize(450, 430)
        self.setMinimumSize(QtCore.QSize(450, 430))
        self.setMaximumSize(QtCore.QSize(450, 430))
        self.setAutoFillBackground(False)
        self.setStyleSheet("background-color: rgb(35, 35, 35);")
        
        self.AtributeUI = QtWidgets.QGroupBox(parent=self)
        self.AtributeUI.setGeometry(QtCore.QRect(0, 0, 446, 422))
        self.AtributeUI.setStyleSheet("background-color: rgba(255, 255, 255, 0);border:0;")
        self.AtributeUI.setTitle("")
        self.AtributeUI.setObjectName("AtributeUI")
        self.leftside_atributesLibary_7 = QtWidgets.QFrame(parent=self.AtributeUI)
        self.leftside_atributesLibary_7.setGeometry(QtCore.QRect(10, 6, 429, 370))
        self.leftside_atributesLibary_7.setStyleSheet("background-color: rgb(47, 47, 47);border-radius: 5px;")
        self.leftside_atributesLibary_7.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.leftside_atributesLibary_7.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.leftside_atributesLibary_7.setObjectName("leftside_atributesLibary_7")
        self.pushButton = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_7)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 198, 30))
        self.pushButton.setStyleSheet("QPushButton{background-color: rgb(72, 72, 72);border-radius:5px;color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";border-bottom-left-radius: 7px;border-bottom-right-radius: 7px;}QPushButton:hover{background-color: rgb(80, 80, 80);}QPushButton:checked{background-color: rgb(110, 110, 110);}")
        self.pushButton.setText("SpawnWithFullCharge")
        self.pushButton.setCheckable(True)
        self.pushButton.clicked.connect(lambda x: self.AddRemoveAtribute(self.pushButton.text(), self.pushButton.isChecked()))
        self.buttonList.append(self.pushButton)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"{resources()}/resources/Icons/Leaderboard/leaderboard_class_medic_uber.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(20, 20))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.pushButton.setCheckable(True)
        self.pushButton.setChecked(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_7)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 50, 198, 30))
        self.pushButton_2.setStyleSheet("QPushButton{background-color: rgb(72, 72, 72);border-radius:5px;color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";border-bottom-left-radius: 7px;border-bottom-right-radius: 7px;}QPushButton:hover{background-color: rgb(80, 80, 80);}QPushButton:checked{background-color: rgb(110, 110, 110);}")
        self.pushButton_2.setText("HoldFireUntilFullReload")
        self.pushButton_2.setCheckable(True)
        self.pushButton_2.clicked.connect(lambda x: self.AddRemoveAtribute(self.pushButton_2.text(), self.pushButton_2.isChecked()))
        self.buttonList.append(self.pushButton_2)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(f"{resources()}/resources/Icons/weapon/Backpack_Panic_Attack.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.pushButton_2.setCheckable(True)
        self.pushButton_2.setChecked(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_7)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 90, 198, 30))
        self.pushButton_3.setStyleSheet("QPushButton{background-color: rgb(72, 72, 72);border-radius:5px;color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";border-bottom-left-radius: 7px;border-bottom-right-radius: 7px;}QPushButton:hover{background-color: rgb(80, 80, 80);}QPushButton:checked{background-color: rgb(110, 110, 110);}")
        self.pushButton_3.setText("SuppressFire")
        self.buttonList.append(self.pushButton_3)
        self.pushButton_3.setCheckable(True)
        self.pushButton_3.clicked.connect(lambda x: self.AddRemoveAtribute(self.pushButton_3.text(), self.pushButton_3.isChecked()))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(f"{resources()}/resources/Icons/Leaderboard/leaderboard_class_soldier_rocketrain.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        
        self.pushButton_3.setIcon(icon2)
        self.pushButton_3.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_3.setCheckable(True)
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.pushButton_3.setChecked(False)
        self.pushButton_3.setObjectName("pushButton_3")
        
        self.botGiant = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_7)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_systemPath.get("leaderboard_class_demo_bomber", "Leaderboard")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.botGiant.setIcon(icon3)
        self.botGiant.setGeometry(QtCore.QRect(10, 130, 198, 30))
        self.botGiant.setStyleSheet("QPushButton{background-color: rgb(72, 72, 72);border-radius:5px;color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";border-bottom-left-radius: 7px;border-bottom-right-radius: 7px;}QPushButton:hover{background-color: rgb(80, 80, 80);}QPushButton:checked{background-color: rgb(110, 110, 110);}")
        self.botGiant.setText("Bot_Giant")
        self.botGiant.setCheckable(True)
        self.botGiant.clicked.connect(lambda x: self.AddRemoveAtribute(self.botGiant.text(), self.botGiant.isChecked()))
        self.botGiant.setIconSize(QtCore.QSize(20, 20))
        self.botGiant.setCheckable(True)
        self.botGiant.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.botGiant.setChecked(False)
        self.buttonList.append(self.botGiant)
        
        self.pushButton_5 = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_7)
        self.pushButton_5.setGeometry(QtCore.QRect(10, 170, 198, 30))
        self.pushButton_5.setStyleSheet("QPushButton{background-color: rgb(72, 72, 72);border-radius:5px;color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";border-bottom-left-radius: 7px;border-bottom-right-radius: 7px;}QPushButton:hover{background-color: rgb(80, 80, 80);}QPushButton:checked{background-color: rgb(110, 110, 110);}")
        self.pushButton_5.setText("MiniBoss")
        self.buttonList.append(self.pushButton_5)
        self.pushButton_5.setCheckable(True)
        self.pushButton_5.clicked.connect(lambda x: self.AddRemoveAtribute(self.pushButton_5.text(), self.pushButton_5.isChecked()))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(f"{resources()}/resources/Icons/Leaderboard/leaderboard_class_soldier_sergeant_crits.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_5.setIcon(icon4)
        self.pushButton_5.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_5.setCheckable(True)
        self.pushButton_5.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.pushButton_5.setChecked(False)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_7)
        self.pushButton_6.setGeometry(QtCore.QRect(10, 210, 198, 30))
        self.pushButton_6.setStyleSheet("QPushButton{background-color: rgb(72, 72, 72);border-radius:5px;color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";border-bottom-left-radius: 7px;border-bottom-right-radius: 7px;}QPushButton:hover{background-color: rgb(80, 80, 80);}QPushButton:checked{background-color: rgb(110, 110, 110);}")
        self.pushButton_6.setText("TeleportToHint")
        self.buttonList.append(self.pushButton_6)
        self.pushButton_6.setCheckable(True)
        self.pushButton_6.clicked.connect(lambda x: self.AddRemoveAtribute(self.pushButton_6.text(), self.pushButton_6.isChecked()))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(f"{resources()}/resources/Icons/Leaderboard/leaderboard_class_spy.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_6.setIcon(icon5)
        self.pushButton_6.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_6.setCheckable(True)
        self.pushButton_6.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.pushButton_6.setChecked(False)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_7)
        self.pushButton_7.setGeometry(QtCore.QRect(10, 250, 198, 30))
        self.pushButton_7.setStyleSheet("QPushButton{background-color: rgb(72, 72, 72);border-radius:5px;color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";border-bottom-left-radius: 7px;border-bottom-right-radius: 7px;}QPushButton:hover{background-color: rgb(80, 80, 80);}QPushButton:checked{background-color: rgb(110, 110, 110);}")
        self.pushButton_7.setText("IgnoreFlag")
        self.buttonList.append(self.pushButton_7)
        self.pushButton_7.setCheckable(True)
        self.pushButton_7.clicked.connect(lambda x: self.AddRemoveAtribute(self.pushButton_7.text(), self.pushButton_7.isChecked()))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(f"{resources()}/resources/Icons/bomb_icon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_7.setIcon(icon6)
        self.pushButton_7.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_7.setCheckable(True)
        self.pushButton_7.setChecked(False)
        self.pushButton_7.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_7)
        self.pushButton_8.setGeometry(QtCore.QRect(10, 330, 198, 30))
        self.pushButton_8.setStyleSheet("QPushButton{background-color: rgb(72, 72, 72);border-radius:5px;color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";border-bottom-left-radius: 7px;border-bottom-right-radius: 7px;}QPushButton:hover{background-color: rgb(80, 80, 80);}QPushButton:checked{background-color: rgb(110, 110, 110);}")
        self.pushButton_8.setText("VaccinatorBlast")
        self.buttonList.append(self.pushButton_8)
        self.pushButton_8.setCheckable(True)
        self.pushButton_8.clicked.connect(lambda x: self.AddRemoveAtribute(self.pushButton_8.text(), self.pushButton_8.isChecked()))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(f"{resources()}/resources/Icons/Leaderboard/leaderboard_class_medic_blast.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_8.setIcon(icon7)
        self.pushButton_8.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_8.setCheckable(True)
        self.pushButton_8.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.pushButton_8.setChecked(False)
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_7)
        self.pushButton_9.setGeometry(QtCore.QRect(10, 290, 198, 30))
        self.pushButton_9.setStyleSheet("QPushButton{background-color: rgb(72, 72, 72);border-radius:5px;color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";border-bottom-left-radius: 7px;border-bottom-right-radius: 7px;}QPushButton:hover{background-color: rgb(80, 80, 80);}QPushButton:checked{background-color: rgb(110, 110, 110);}")
        self.pushButton_9.setText("AirChargeOnly")
        self.buttonList.append(self.pushButton_9)
        self.pushButton_9.setCheckable(True)
        self.pushButton_9.clicked.connect(lambda x: self.AddRemoveAtribute(self.pushButton_9.text(), self.pushButton_9.isChecked()))
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(f"{resources()}/resources/Icons/Leaderboard/leaderboard_class_demoknight.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_9.setIcon(icon8)
        self.pushButton_9.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_9.setCheckable(True)
        self.pushButton_9.setChecked(False)
        self.pushButton_9.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_10 = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_7)
        self.pushButton_10.setGeometry(QtCore.QRect(220, 10, 198, 30))
        self.pushButton_10.setStyleSheet("QPushButton{background-color: rgb(72, 72, 72);border-radius:5px;color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";border-bottom-left-radius: 7px;border-bottom-right-radius: 7px;}QPushButton:hover{background-color: rgb(80, 80, 80);}QPushButton:checked{background-color: rgb(110, 110, 110);}")
        self.pushButton_10.setText("AlwaysCrit")
        self.buttonList.append(self.pushButton_10)
        self.pushButton_10.setCheckable(True)
        self.pushButton_10.clicked.connect(lambda x: self.AddRemoveAtribute(self.pushButton_10.text(), self.pushButton_10.isChecked()))
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(f"{resources()}/resources/Icons/crit_shit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_10.setIcon(icon9)
        self.pushButton_10.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_10.setCheckable(True)
        self.pushButton_10.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.pushButton_10.setChecked(False)
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_11 = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_7)
        self.pushButton_11.setGeometry(QtCore.QRect(220, 130, 198, 30))
        self.pushButton_11.setStyleSheet("QPushButton{background-color: rgb(72, 72, 72);border-radius:5px;color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";border-bottom-left-radius: 7px;border-bottom-right-radius: 7px;}QPushButton:hover{background-color: rgb(80, 80, 80);}QPushButton:checked{background-color: rgb(110, 110, 110);}")
        self.pushButton_11.setText("RetainBuildings")
        self.buttonList.append(self.pushButton_11)
        self.pushButton_11.setCheckable(True)
        self.pushButton_11.clicked.connect(lambda x: self.AddRemoveAtribute(self.pushButton_11.text(), self.pushButton_11.isChecked()))
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(f"{resources()}/resources/Icons/Leaderboard/leaderboard_class_engineer.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_11.setIcon(icon10)
        self.pushButton_11.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_11.setCheckable(True)
        self.pushButton_11.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.pushButton_11.setChecked(False)
        self.pushButton_11.setObjectName("pushButton_11")
        self.pushButton_12 = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_7)
        self.pushButton_12.setGeometry(QtCore.QRect(220, 210, 198, 30))
        self.pushButton_12.setStyleSheet("QPushButton{background-color: rgb(72, 72, 72);border-radius:5px;color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";border-bottom-left-radius: 7px;border-bottom-right-radius: 7px;}QPushButton:hover{background-color: rgb(80, 80, 80);}QPushButton:checked{background-color: rgb(110, 110, 110);}")
        self.pushButton_12.setText("AlwaysFireWeapon")
        self.buttonList.append(self.pushButton_12)
        self.pushButton_12.setCheckable(True)
        self.pushButton_12.clicked.connect(lambda x: self.AddRemoveAtribute(self.pushButton_12.text(), self.pushButton_12.isChecked()))
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(f"{resources()}/resources/Icons/Leaderboard/leaderboard_class_pyro.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_12.setIcon(icon11)
        self.pushButton_12.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_12.setCheckable(True)
        self.pushButton_12.setChecked(False)
        self.pushButton_12.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.pushButton_12.setObjectName("pushButton_12")
        self.pushButton_13 = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_7)
        self.pushButton_13.setGeometry(QtCore.QRect(220, 170, 198, 30))
        self.pushButton_13.setStyleSheet("QPushButton{background-color: rgb(72, 72, 72);border-radius:5px;color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";border-bottom-left-radius: 7px;border-bottom-right-radius: 7px;}QPushButton:hover{background-color: rgb(80, 80, 80);}QPushButton:checked{background-color: rgb(110, 110, 110);}")
        self.pushButton_13.setText("UseBossHealthBar")
        self.buttonList.append(self.pushButton_13)
        self.pushButton_13.setCheckable(True)
        self.pushButton_13.clicked.connect(lambda x: self.AddRemoveAtribute(self.pushButton_13.text(), self.pushButton_13.isChecked()))
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(f"{resources()}/resources/Icons/Leaderboard/leaderboard_class_heavy_chief.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_13.setIcon(icon12)
        self.pushButton_13.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_13.setCheckable(True)
        self.pushButton_13.setChecked(False)
        self.pushButton_13.setObjectName("pushButton_13")
        self.pushButton_13.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.pushButton_14 = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_7)
        self.pushButton_14.setGeometry(QtCore.QRect(220, 290, 198, 30))
        self.pushButton_14.setStyleSheet("QPushButton{background-color: rgb(72, 72, 72);border-radius:5px;color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";border-bottom-left-radius: 7px;border-bottom-right-radius: 7px;}QPushButton:hover{background-color: rgb(80, 80, 80);}QPushButton:checked{background-color: rgb(110, 110, 110);}")
        self.pushButton_14.setText("VaccinatorBullets")
        self.pushButton_14.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.buttonList.append(self.pushButton_14)
        self.pushButton_14.setCheckable(True)
        self.pushButton_14.clicked.connect(lambda x: self.AddRemoveAtribute(self.pushButton_14.text(), self.pushButton_14.isChecked()))
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(f"{resources()}/resources/Icons/Leaderboard/leaderboard_class_medic_bullet.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_14.setIcon(icon13)
        self.pushButton_14.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_14.setCheckable(True)
        self.pushButton_14.setChecked(False)
        self.pushButton_14.setObjectName("pushButton_14")
        self.pushButton_15 = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_7)
        self.pushButton_15.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.pushButton_15.setGeometry(QtCore.QRect(220, 330, 198, 30))
        self.pushButton_15.setStyleSheet("QPushButton{background-color: rgb(72, 72, 72);border-radius:5px;color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";border-bottom-left-radius: 7px;border-bottom-right-radius: 7px;}QPushButton:hover{background-color: rgb(80, 80, 80);}QPushButton:checked{background-color: rgb(110, 110, 110);}")
        self.pushButton_15.setText("VaccinatorFire")
        self.buttonList.append(self.pushButton_15)
        self.pushButton_15.setCheckable(True)
        self.pushButton_15.clicked.connect(lambda x: self.AddRemoveAtribute(self.pushButton_15.text(), self.pushButton_15.isChecked()))
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(f"{resources()}/resources/Icons/Leaderboard/leaderboard_class_medic_fire.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_15.setIcon(icon14)
        self.pushButton_15.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_15.setCheckable(True)
        self.pushButton_15.setChecked(False)
        self.pushButton_15.setObjectName("pushButton_15")
        self.pushButton_16 = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_7)
        self.pushButton_16.setGeometry(QtCore.QRect(220, 250, 198, 30))
        self.pushButton_16.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.pushButton_16.setStyleSheet("QPushButton{background-color: rgb(72, 72, 72);border-radius:5px;color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";border-bottom-left-radius: 7px;border-bottom-right-radius: 7px;}QPushButton:hover{background-color: rgb(80, 80, 80);}QPushButton:checked{background-color: rgb(110, 110, 110);}")
        self.pushButton_16.setText("AutoJump")
        self.buttonList.append(self.pushButton_16)
        self.pushButton_16.setCheckable(True)
        self.pushButton_16.clicked.connect(lambda x: self.AddRemoveAtribute(self.pushButton_16.text(), self.pushButton_16.isChecked()))
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(f"{resources()}/resources/Icons/Leaderboard/leaderboard_class_scout.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_16.setIcon(icon15)
        self.pushButton_16.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_16.setCheckable(True)
        self.pushButton_16.setChecked(False)
        self.pushButton_16.setObjectName("pushButton_16")
        self.pushButton_17 = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_7)
        self.pushButton_17.setGeometry(QtCore.QRect(220, 90, 198, 30))
        self.pushButton_17.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.pushButton_17.setStyleSheet("QPushButton{background-color: rgb(72, 72, 72);border-radius:5px;color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";border-bottom-left-radius: 7px;border-bottom-right-radius: 7px;}QPushButton:hover{background-color: rgb(80, 80, 80);}QPushButton:checked{background-color: rgb(110, 110, 110);}")
        self.pushButton_17.setText("DisableDodge")
        self.buttonList.append(self.pushButton_17)
        self.pushButton_17.setCheckable(True)
        self.pushButton_17.clicked.connect(lambda x: self.AddRemoveAtribute(self.pushButton_17.text(), self.pushButton_17.isChecked()))
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(f"{resources()}/resources/Icons/Leaderboard/leaderboard_class_heavy_grapple.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_17.setIcon(icon16)
        self.pushButton_17.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_17.setCheckable(True)
        self.pushButton_17.setChecked(False)
        self.pushButton_17.setObjectName("pushButton_17")
        self.pushButton_18 = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_7)
        self.pushButton_18.setGeometry(QtCore.QRect(220, 50, 198, 30))
        self.pushButton_18.setStyleSheet("QPushButton{background-color: rgb(72, 72, 72);border-radius:5px;color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";border-bottom-left-radius: 7px;border-bottom-right-radius: 7px;}QPushButton:hover{background-color: rgb(80, 80, 80);}QPushButton:checked{background-color: rgb(110, 110, 110);}")
        self.pushButton_18.setText("RemoveOnDeath")
        self.buttonList.append(self.pushButton_18)
        self.pushButton_18.setCheckable(True)
        self.pushButton_18.clicked.connect(lambda x: self.AddRemoveAtribute(self.pushButton_18.text(), self.pushButton_18.isChecked()))
        self.pushButton_18.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap(f"{resources()}/resources/Icons/Leaderboard/leaderboard_class_soldier_dumpster.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_18.setIcon(icon17)
        self.pushButton_18.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_18.setCheckable(True)
        self.pushButton_18.setChecked(False)
        self.pushButton_18.setObjectName("pushButton_18")
        self.Save = QtWidgets.QPushButton(parent=self.AtributeUI)
        self.Save.setGeometry(QtCore.QRect(10, 390, 200, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Save.sizePolicy().hasHeightForWidth())
        self.Save.setSizePolicy(sizePolicy)
        self.Save.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Save.setMouseTracking(True)
        self.Save.setStyleSheet("border-radius: 7px;border:0;background-color: rgb(0, 158, 26);color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";")
        self.Save.setObjectName("Save")
        self.Save.clicked.connect(lambda: self.SaveStat())
        self.Cancel = QtWidgets.QPushButton(parent=self.AtributeUI)
        self.Cancel.setGeometry(QtCore.QRect(240, 390, 200, 31))
        self.Cancel.clicked.connect(lambda : self.Close())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Cancel.sizePolicy().hasHeightForWidth())
        self.Cancel.setSizePolicy(sizePolicy)
        self.Cancel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Cancel.setMouseTracking(True)
        self.Cancel.setStyleSheet("border-radius: 7px;border:0;background-color: rgb(176, 57, 57);color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";")
        self.Cancel.setObjectName("Cancel")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.Save.setText(_translate("AtributeUI", "Save"))
        self.Cancel.setText(_translate("AtributeUI", "Cancel"))


class cosmetic_list:
    global Mercenary_now
    
    def __init__(self, grid, scrollAreaWidgetContents_6, Cosmitis_list, verticalLayout_8):
        self.grid = grid
        self.scrollAreaWidgetContents_6 = scrollAreaWidgetContents_6
        self.Cosmitis_list = Cosmitis_list
        self.verticalLayout_8 = verticalLayout_8
        self.now = 0
        self.countButton = 0
        self.spacer = None
        self.allButtons = []

        # Make the scroll area and its contents scalable
        self.Cosmitis_list.setWidgetResizable(True)
        self.scrollAreaWidgetContents_6.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents_6.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        )
        self.grid.setSpacing(8)
        self.scrollAreaWidgetContents_6.setUpdatesEnabled(False)

    def clear(self):
        if len(self.allButtons) > 0:
            for item in self.allButtons:
                item.deleteLater()
            self.now = 0
            self.countButton = 0
            self.spacer = None
            self.allButtons = []
        self.AddButton()
    
    def AddCosmeticsFromList(self, list_items):
        if isinstance(list_items, list):
            for item in list_items:
                if not item:  # Проверка на пустое значение
                    continue
                try:
                    # Убеждаемся что item это строка или число
                    item_key = str(item) if isinstance(item, (str, int)) else None
                    if not item_key:
                        print(f"Warning: Invalid item key format: {item}")
                        continue
                    
                    stat = parser.get_item_by_key(item_key)

                    if stat:
                        if "ready_icon" not in stat:
                            index = parser.get_item_by_name(stat.get("name"))
                            stat["ready_icon"] = get_icon_from_game(index[0])
                        
                        self.AddButton(stat)
                    else:
                        print(f"Warning: Could not find cosmetic item with key {item_key}")
                except Exception as e:
                    print(f"Error processing cosmetic item {item}: {str(e)}")
                    continue
        else:
            if "ready_icon" not in list_items:
                index = parser.get_item_by_name(list_items.get("name"))
                list_items["ready_icon"] = get_icon_from_game(index[0])
                
            self.AddButton(list_items)
            
    def AddButton(self, stat = None):
        if self.spacer is not None:
            self.grid.removeItem(self.spacer)

        self.scrollAreaWidgetContents_6.setUpdatesEnabled(False)
        
        Item_2 = QtWidgets.QGroupBox(parent=self.scrollAreaWidgetContents_6)
        # Set minimal possible size based on style (icon 61x51, button 131x81)
        Item_2.setMinimumSize(QtCore.QSize(131, 81))
        Item_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        Item_2.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        )
        Item_2.setStyleSheet("border:0;")
        Item_2.setObjectName("Item_2")

        ButtonAddCosmetic = QtWidgets.QPushButton(parent=Item_2)
        ButtonAddCosmetic.setGeometry(QtCore.QRect(0, 0, 131, 81))
        ButtonAddCosmetic.setMinimumSize(QtCore.QSize(131, 81))
        ButtonAddCosmetic.setMaximumSize(QtCore.QSize(16777215, 16777215))
        ButtonAddCosmetic.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        )
        ButtonAddCosmetic.setStyleSheet("background-color: rgb(47, 47, 47);border-radius: 10px;")
        ButtonAddCosmetic.setIconSize(QtCore.QSize(90, 90))
        ButtonAddCosmetic.setObjectName("ButtonAddCosmetic")

        label_15 = QtWidgets.QLabel(parent=Item_2)
        label_15.setGeometry(QtCore.QRect(0, 60, 131, 21))
        label_15.setMinimumSize(QtCore.QSize(131, 21))
        label_15.setMaximumSize(QtCore.QSize(16777215, 16777215))
        label_15.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        )
        label_15.setStyleSheet("color: rgb(217, 210, 41); font: 7pt \"TF2 Build\";")
        label_15.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label_15.setObjectName("label_15")

        frame_5 = QtWidgets.QFrame(parent=Item_2)
        frame_5.setGeometry(QtCore.QRect(34, 8, 61, 51))
        frame_5.setMinimumSize(QtCore.QSize(61, 51))
        frame_5.setMaximumSize(QtCore.QSize(16777215, 16777215))
        frame_5.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        )
        frame_5.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        frame_5.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        frame_5.setObjectName("frame_5")

        if stat is None or 'name' not in stat:
            frame_5.setStyleSheet(f"border-image: url({_systemPath.get('Plus')});\n")
            label_15.setText("Add")
            
            Item_2.mousePressEvent = (lambda x: open_addition_panel(self.filtered_items()))
            
            frame_5.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            label_15.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            ButtonAddCosmetic.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        else:
            name_item = stat.get("name", "Unknow")
            label_15.setText(name_item)
            frame_5.setStyleSheet(f"border-image: url({stat['ready_icon']});\n")

            DeleteCosmeticButton = QtWidgets.QPushButton(parent=Item_2)
            DeleteCosmeticButton.setGeometry(QtCore.QRect(106, 4, 20, 20))
            DeleteCosmeticButton.setMinimumSize(QtCore.QSize(20, 20))
            DeleteCosmeticButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
            DeleteCosmeticButton.setSizePolicy(
                QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
            )
            DeleteCosmeticButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            DeleteCosmeticButton.setStyleSheet("background-color: rgba(0, 0, 0,0);\n"
                                               "font: 30pt \"TF2\";\n"
                                               "color: rgb(185, 45, 43);")
            DeleteCosmeticButton.setObjectName("DeleteCosmeticButton")
            DeleteCosmeticButton.setText("-")
            DeleteCosmeticButton.clicked.connect(lambda hui: self.DeleteCosmetic(stat, Item_2))
            
        # Оптимизированная логика размещения элементов в сетке
        row_capacity = 3
        row = self.now // row_capacity
        col = self.now % row_capacity
        self.countButton = row
        self.line = col
        self.now += 1

        self.grid.addWidget(Item_2, self.countButton, self.line)
        self.allButtons.append(Item_2)
        self.Cosmitis_list.setWidget(self.scrollAreaWidgetContents_6)
        
        self.scrollAreaWidgetContents_6.setUpdatesEnabled(True)
        
        self.spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.grid.addItem(self.spacer, self.countButton + 1, 0)
    
    def filtered_items(self):
        criteria = {
            'used_by_classes': Mercenary_now.stat['Class Name'].lower(),
            'equip_region' : "hat",
                              #"whole_hat",
                              #"face", 
                              #"glasses", 
                              #"lenses", 
                              #"pants", 
                              #"beard", 
                              #"shirt", 
                              #"medal", 
                              #"arms", 
                              #"back", 
                              #"feet", 
                              #"necklace", 
                              #"grenades",
                              #"arm_tattoos", 
                              #"flair", 
                              #"head_skin", 
                              #"ears", 
                              #"left_shoulder", 
                              #"belt_misc", 
                              #"disconnected_floating_item", 
                              #"zombie_body", 
                              #"sleeves", 
                              #"right_shoulder"],	
        }
        return parser.filter_items(criteria)
        
    def DeleteCosmetic(self, stat, Item_2):
        self.allButtons.remove(Item_2)
        Item_2.deleteLater()
        if stat["name"] in Mercenary_now.stat["Cosmetics"]:
            Mercenary_now.stat["Cosmetics"].remove(stat["name"])

class WeaponData(object):
    def __init__(self, Class = None, WeaponType = None, weaponName = None, attrubutes = {}):
        if Class == None:
            return

        if weaponName != None:
            weapon = weapons_libary.Weapon_Libary[Class][WeaponType].get(weaponName, None)

            if weapon is None:
                weapon_find = parser.get_item_by_name(weaponName)

                if weapon_find:
                    weapon_find = weapon_find[1]  # Assuming the first item is the correct one
                    if 'base_item_name' in weapon_find:
                        weapon_ID = str(weapon_find['base_item_name'])
                    elif 'item_class' in weapon_find:
                        weapon_ID = str(weapon_find['item_class'])
                    else:
                        weapon_ID = str(weapon_find.get("name", "Unknown Weapon"))
                    weapon = {
                        "Id": weapon_ID.upper(),
                        "name": weapon_find.get("name", "Unknown Weapon"),
                        "Icon": weapon_find.get("image_inventory", ""),
                    }
        else:
            weapon = weapons_libary.Weapon_Libary[Class][WeaponType][next(iter(weapons_libary.Weapon_Libary[Class][WeaponType]))]
        
        if weapon["Icon"] is None or weapon["Icon"] == "" or weapon["Icon"] == "None":
            index = parser.get_item_by_name(weapon["Id"])

            if index is not None:
                weapon["Icon"] = get_icon_from_game(index[0])
            else:
                index = parser.get_item_by_name(weapon["name"])
                if index:
                    weapon["Icon"] = get_icon_from_game(index[0])
                
        self.stat = {
            "Name" :        weapon["name"],
            "Icon" :        weapon["Icon"],
            "Class" :       Class,
            "Type" :        WeaponType,
            "ID" :          weapon["Id"],
            
            "Custom Name" : "",
            "Description" : "",
            "Custom" : "",
            "Quality" :     "Unique",
            "Attributes" :    attrubutes,
        }

    def Set_Settings_From_Save(self, list : dict):
        self.stat = {
            "Name" :        list["Name"],
            "Icon" :        list["Icon"],
            "Class" :       list["Class"],
            "Type" :        list["Type"],
            "ID" :          list["ID"],
            
            "Custom Name" : list["Custom Name"],
            "Description" : list["Description"],
            "Custom" :      list["Custom"],
            "Quality" :     list["Quality"],
            "Attributes" :  list["Attributes"],
        }
        
    def get(self, index : str = None) -> dict:
        if index == None:
            return self.stat
        else:
            return self.stat[index]

class WeaponsAtributeMenu(QtWidgets.QMainWindow):
    global Mercenary_now
    def __init__(self):
        super().__init__()
        self.stat = None
        self.weapon = None
        self.qualityWeapon = "Unique"
        self.buttonsQuality = {}
        
        global Addition_interface
        Addition_interface = self
                
        self.setupUi()

    def setupUi(self):
        self.resize(1100, 600)
        self.setMinimumSize(QtCore.QSize(1100, 600))
        self.setMaximumSize(QtCore.QSize(900, 500))
        self.setAutoFillBackground(False)
        self.setStyleSheet("background-color: rgb(35, 35, 35);")
        
        self.Cancel = QtWidgets.QPushButton(parent=self)
        self.Cancel.setGeometry(QtCore.QRect(890, 550, 200, 31))
        self.Cancel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Cancel.clicked.connect(lambda: self.CloseMenu())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Cancel.sizePolicy().hasHeightForWidth())
        
        self.Cancel.setSizePolicy(sizePolicy)
        self.Cancel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Cancel.setMouseTracking(True)
        self.Cancel.setStyleSheet("border-radius: 7px;border:0;background-color: rgb(176, 57, 57);color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";")
        self.Cancel.setObjectName("Cancel")
        
        self.Save = QtWidgets.QPushButton(parent=self)
        self.Save.setGeometry(QtCore.QRect(680, 550, 200, 31))
        self.Save.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Save.clicked.connect(lambda: self.SaveStat())
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Save.sizePolicy().hasHeightForWidth())
        
        self.Save.setSizePolicy(sizePolicy)
        self.Save.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Save.setMouseTracking(True)
        self.Save.setStyleSheet("border-radius: 7px;border:0;background-color: rgb(0, 158, 26);color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";")
        self.Save.setObjectName("Save")
        
        self.groupBox = QtWidgets.QGroupBox(parent=self)
        self.groupBox.setGeometry(QtCore.QRect(14, 30, 288, 503))
        self.groupBox.setStyleSheet("border:0;color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";background-color: rgba(255, 255, 255, 0);")
        self.groupBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        
        self.leftside_atributesLibary = QtWidgets.QFrame(parent=self.groupBox)
        self.leftside_atributesLibary.setGeometry(QtCore.QRect(15, 19, 271, 480))
        self.leftside_atributesLibary.setStyleSheet("background-color: rgb(47, 47, 47);border-radius: 15px;")
        self.leftside_atributesLibary.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.leftside_atributesLibary.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.leftside_atributesLibary.setObjectName("leftside_atributesLibary")
        
        self.frame = QtWidgets.QFrame(parent=self)
        self.frame.setGeometry(QtCore.QRect(910, 47, 140, 100))
        self.frame.setStyleSheet("background-color: rgb(47, 47, 47);border-radius: 15px;")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        
        self.nameWeapon = QtWidgets.QLabel(parent=self.frame)
        self.nameWeapon.setGeometry(QtCore.QRect(5, 65, 132, 35))
        self.nameWeapon.setStyleSheet("color: rgb(217, 210, 41);font: 9pt \"TF2 Build\";")
        self.nameWeapon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.nameWeapon.setObjectName("nameWeapon")
        
        self.ico_weapon = QtWidgets.QFrame(parent=self.frame)
        self.ico_weapon.setGeometry(QtCore.QRect(32, 0, 74, 70))
        self.ico_weapon.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.ico_weapon.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.ico_weapon.setObjectName("ico_weapon")
        
        self.strange = QtWidgets.QFrame(parent=self.frame)
        self.strange.setGeometry(QtCore.QRect(100, 3, 30, 27))
        self.strange.setStyleSheet(f"border-image: url({_systemPath.get('stattrack', 'weapon')});border-radius: 15px;border-color: rgba(255, 255, 255, 0);")
        self.strange.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.strange.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.strange.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.strange.setObjectName("strange")
        self.strange.hide()
        
        self.groupBox_2 = QtWidgets.QGroupBox(parent=self)
        self.groupBox_2.setGeometry(QtCore.QRect(300, 30, 288, 503))
        self.groupBox_2.setStyleSheet("border:0;color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";background-color: rgba(255, 255, 255, 0);")
        self.groupBox_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.groupBox_2.setObjectName("groupBox_2")
        
        self.leftside_atributesLibary_3 = QtWidgets.QFrame(parent=self.groupBox_2)
        self.leftside_atributesLibary_3.setGeometry(QtCore.QRect(15, 19, 271, 480))
        self.leftside_atributesLibary_3.setStyleSheet("background-color: rgb(47, 47, 47);border-radius: 15px;")
        self.leftside_atributesLibary_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.leftside_atributesLibary_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.leftside_atributesLibary_3.setObjectName("leftside_atributesLibary_3")
        
        self.groupBox_3 = QtWidgets.QGroupBox(parent=self)
        self.groupBox_3.setGeometry(QtCore.QRect(586, 30, 288, 503))
        self.groupBox_3.setStyleSheet("border:0;color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";background-color: rgba(255, 255, 255, 0);")
        self.groupBox_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.groupBox_3.setObjectName("groupBox_3")
        
        self.leftside_atributesLibary_4 = QtWidgets.QFrame(parent=self.groupBox_3)
        self.leftside_atributesLibary_4.setGeometry(QtCore.QRect(15, 19, 271, 480))
        self.leftside_atributesLibary_4.setStyleSheet("background-color: rgb(47, 47, 47);border-radius: 15px;")
        self.leftside_atributesLibary_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.leftside_atributesLibary_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.leftside_atributesLibary_4.setObjectName("leftside_atributesLibary_4")
        
        self.lineEdit_3 = QtWidgets.QTextEdit(parent=self.leftside_atributesLibary_4)
        self.lineEdit_3.setGeometry(QtCore.QRect(12, 15, 247, 452))
        self.lineEdit_3.setStyleSheet("font: 11pt \"Consolas\";background-color: rgb(64, 64, 64);border-radius:10px;")
        self.lineEdit_3.setText("Custom")
        self.lineEdit_3.setPlaceholderText("""Custom parameters and blocks.
"override projectile type" 7
""")
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.lineEdit_3.setObjectName("lineEdit_3")
        
        self.groupBox_4 = QtWidgets.QGroupBox(parent=self)
        self.groupBox_4.setGeometry(QtCore.QRect(877, 157, 212, 51))
        self.groupBox_4.setStyleSheet("border:0;color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";background-color: rgba(255, 255, 255, 0);")
        self.groupBox_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.groupBox_4.setObjectName("groupBox_4")
        
        self.leftside_atributesLibary_5 = QtWidgets.QFrame(parent=self.groupBox_4)
        self.leftside_atributesLibary_5.setGeometry(QtCore.QRect(10, 18, 190, 30))
        self.leftside_atributesLibary_5.setStyleSheet("background-color: rgb(47, 47, 47);border-radius: 5px;")
        self.leftside_atributesLibary_5.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.leftside_atributesLibary_5.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.leftside_atributesLibary_5.setObjectName("leftside_atributesLibary_5")
        
        self.customName = QtWidgets.QLineEdit(parent=self.leftside_atributesLibary_5)
        self.customName.setGeometry(QtCore.QRect(8, 6, 175, 19))
        self.customName.setStyleSheet("font: 9pt \"TF2\";")
        self.customName.setObjectName("lineEdit")
        self.customName.editingFinished.connect(lambda: self.ChangeName())
        
        self.groupBox_5 = QtWidgets.QGroupBox(parent=self)
        self.groupBox_5.setGeometry(QtCore.QRect(880, 220, 212, 191))
        self.groupBox_5.setStyleSheet("border:0;color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";background-color: rgba(255, 255, 255, 0);")
        self.groupBox_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.groupBox_5.setObjectName("groupBox_5")
        
        self.leftside_atributesLibary_6 = QtWidgets.QFrame(parent=self.groupBox_5)
        self.leftside_atributesLibary_6.setGeometry(QtCore.QRect(10, 18, 190, 170))
        self.leftside_atributesLibary_6.setStyleSheet("background-color: rgb(47, 47, 47);border-radius: 5px;")
        self.leftside_atributesLibary_6.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.leftside_atributesLibary_6.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.leftside_atributesLibary_6.setObjectName("leftside_atributesLibary_6")
        
                
        self.normal_quality = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_6)
        self.normal_quality.setGeometry(QtCore.QRect(10, 10, 82, 20))
        self.normal_quality.setStyleSheet(
                                "QPushButton{\n"
                                f"background-color: rgb(70, 70, 70);color: rgb({colorQuality['Normal']});"
                                "font: 9pt \"TF2\";"
                                "border-bottom-left-radius: 7px;"
                                "border-bottom-right-radius: 7px;}"
                                "QPushButton:hover{"
                                "background-color: rgb(65, 65, 65);"
                                "}"
                                "QPushButton:checked{background-color: rgb(60, 100, 75);}")
        self.normal_quality.setCheckable(True)
        self.normal_quality.setObjectName("Normal")
        self.normal_quality.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.buttonsQuality["Normal"] = self.normal_quality
        self.normal_quality.clicked.connect(lambda x: self.setQualityWeapon("Normal"))        
        
        
        self.Unique_quality = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_6)
        self.Unique_quality.setGeometry(QtCore.QRect(100, 10, 82, 20))
        self.Unique_quality.setStyleSheet(
                                "QPushButton{\n"
                                f"background-color: rgb(70, 70, 70);color: rgb({colorQuality['Unique']});"
                                "font: 9pt \"TF2\";"
                                "border-bottom-left-radius: 7px;"
                                "border-bottom-right-radius: 7px;}"
                                "QPushButton:hover{"
                                "background-color: rgb(65, 65, 65);"
                                "}"
                                "QPushButton:checked{background-color: rgb(60, 100, 75);}")
        self.Unique_quality.setCheckable(True)
        self.Unique_quality.setObjectName("Unique")
        self.Unique_quality.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.buttonsQuality["Unique"] = self.Unique_quality
        self.Unique_quality.clicked.connect(lambda x: self.setQualityWeapon("Unique"))
        
        self.Genuine_quality = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_6)
        self.Genuine_quality.setGeometry(QtCore.QRect(100, 36, 82, 20))
        self.Genuine_quality.setObjectName("Genuine")
        self.Genuine_quality.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.buttonsQuality["Genuine"] = self.Genuine_quality
        self.Genuine_quality.clicked.connect(lambda x: self.setQualityWeapon("Genuine"))
        self.Genuine_quality.setStyleSheet(
                                "QPushButton{\n"
                                f"background-color: rgb(70, 70, 70);color: rgb({colorQuality['Genuine']});"
                                "font: 9pt \"TF2\";"
                                "border-bottom-left-radius: 7px;"
                                "border-bottom-right-radius: 7px;}"
                                "QPushButton:hover{"
                                "background-color: rgb(65, 65, 65);"
                                "}"
                                "QPushButton:checked{background-color: rgb(60, 100, 75);}")
        self.Genuine_quality.setCheckable(True)
        
        
        self.Vintage_quality = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_6)
        self.Vintage_quality.setGeometry(QtCore.QRect(10, 36, 82, 20))
        self.Vintage_quality.setObjectName("Vintage")
        self.Vintage_quality.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.buttonsQuality["Vintage"] = self.Vintage_quality
        self.Vintage_quality.clicked.connect(lambda x: self.setQualityWeapon("Vintage"))
        self.Vintage_quality.setStyleSheet(
                                "QPushButton{\n"
                                f"background-color: rgb(70, 70, 70);color: rgb({colorQuality['Vintage']});"
                                "font: 9pt \"TF2\";"
                                "border-bottom-left-radius: 7px;"
                                "border-bottom-right-radius: 7px;}"
                                "QPushButton:hover{"
                                "background-color: rgb(65, 65, 65);"
                                "}"
                                "QPushButton:checked{background-color: rgb(60, 100, 75);}")
        self.Vintage_quality.setCheckable(True)
        
        self.Unusual_quality = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_6)
        self.Unusual_quality.setGeometry(QtCore.QRect(100, 62, 82, 20))
        self.Unusual_quality.setObjectName("Unusual")
        self.Unusual_quality.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.buttonsQuality["Unusual"] = self.Unusual_quality
        self.Unusual_quality.clicked.connect(lambda x: self.setQualityWeapon("Unusual"))
        self.Unusual_quality.setStyleSheet(
                                "QPushButton{\n"
                                f"background-color: rgb(70, 70, 70);color: rgb({colorQuality['Unusual']});"
                                "font: 9pt \"TF2\";"
                                "border-bottom-left-radius: 7px;"
                                "border-bottom-right-radius: 7px;}"
                                "QPushButton:hover{"
                                "background-color: rgb(65, 65, 65);"
                                "}"
                                "QPushButton:checked{background-color: rgb(60, 100, 75);}")
        self.Unusual_quality.setCheckable(True)
        
        self.Strange_quality = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_6)
        self.Strange_quality.setGeometry(QtCore.QRect(10, 62, 82, 20))
        self.Strange_quality.setObjectName("Strange")
        self.Strange_quality.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.buttonsQuality["Strange"] = self.Strange_quality
        self.Strange_quality.clicked.connect(lambda x: self.setQualityWeapon("Strange"))
        self.Strange_quality.setStyleSheet(
                                "QPushButton{\n"
                                f"background-color: rgb(70, 70, 70);color: rgb({colorQuality['Strange']});"
                                "font: 9pt \"TF2\";"
                                "border-bottom-left-radius: 7px;"
                                "border-bottom-right-radius: 7px;}"
                                "QPushButton:hover{"
                                "background-color: rgb(65, 65, 65);"
                                "}"
                                "QPushButton:checked{background-color: rgb(60, 100, 75);}")
        self.Strange_quality.setCheckable(True)
        
        self.Collector_quality = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_6)
        self.Collector_quality.setGeometry(QtCore.QRect(100, 89, 82, 20))
        self.Collector_quality.setObjectName("Collector")
        self.Collector_quality.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.buttonsQuality["Collector"] = self.Collector_quality
        self.Collector_quality.clicked.connect(lambda x: self.setQualityWeapon("Collector"))
        self.Collector_quality.setStyleSheet(
                                "QPushButton{\n"
                                f"background-color: rgb(70, 70, 70);color: rgb({colorQuality['Collector']});"
                                "font: 9pt \"TF2\";"
                                "border-bottom-left-radius: 7px;"
                                "border-bottom-right-radius: 7px;}"
                                "QPushButton:hover{"
                                "background-color: rgb(65, 65, 65);"
                                "}"
                                "QPushButton:checked{background-color: rgb(60, 100, 75);}")
        self.Collector_quality.setCheckable(True)
        
        self.Haunted_quality = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_6)
        self.Haunted_quality.setGeometry(QtCore.QRect(10, 89, 82, 20))
        self.Haunted_quality.setObjectName("Haunted")
        self.Haunted_quality.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.buttonsQuality["Haunted"] = self.Haunted_quality
        self.Haunted_quality.clicked.connect(lambda x: self.setQualityWeapon("Haunted"))
        self.Haunted_quality.setStyleSheet(
                                "QPushButton{\n"
                                f"background-color: rgb(70, 70, 70);color: rgb({colorQuality['Haunted']});"
                                "font: 9pt \"TF2\";"
                                "border-bottom-left-radius: 7px;"
                                "border-bottom-right-radius: 7px;}"
                                "QPushButton:hover{"
                                "background-color: rgb(65, 65, 65);"
                                "}"
                                "QPushButton:checked{background-color: rgb(60, 100, 75);}")
        self.Haunted_quality.setCheckable(True)
        
        self.Decorated_quality = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_6)
        self.Decorated_quality.setGeometry(QtCore.QRect(100, 115, 82, 20))
        self.Decorated_quality.setObjectName("Decorated")
        self.Decorated_quality.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.buttonsQuality["Decorated"] = self.Decorated_quality
        self.Decorated_quality.clicked.connect(lambda x: self.setQualityWeapon("Decorated"))
        self.Decorated_quality.setStyleSheet(
                                "QPushButton{\n"
                                f"background-color: rgb(70, 70, 70);color: rgb({colorQuality['Decorated']});"
                                "font: 9pt \"TF2\";"
                                "border-bottom-left-radius: 7px;"
                                "border-bottom-right-radius: 7px;}"
                                "QPushButton:hover{"
                                "background-color: rgb(65, 65, 65);"
                                "}"
                                "QPushButton:checked{background-color: rgb(60, 100, 75);}")
        self.Decorated_quality.setCheckable(True)
        
        self.Community_quality = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_6)
        self.Community_quality.setGeometry(QtCore.QRect(10, 115, 82, 20))
        self.Community_quality.setObjectName("Community")
        self.Community_quality.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.buttonsQuality["Community"] = self.Community_quality
        self.Community_quality.clicked.connect(lambda x: self.setQualityWeapon("Community"))
        self.Community_quality.setStyleSheet(
                                "QPushButton{\n"
                                f"background-color: rgb(70, 70, 70);color: rgb({colorQuality['Community']});"
                                "font: 9pt \"TF2\";"
                                "border-bottom-left-radius: 7px;"
                                "border-bottom-right-radius: 7px;}"
                                "QPushButton:hover{"
                                "background-color: rgb(65, 65, 65);"
                                "}"
                                "QPushButton:checked{background-color: rgb(60, 100, 75);}")
        self.Community_quality.setCheckable(True)
        
        self.Valve_quality = QtWidgets.QPushButton(parent=self.leftside_atributesLibary_6)
        self.Valve_quality.setGeometry(QtCore.QRect(60, 140, 82, 20))
        self.Valve_quality.setObjectName("Valve")
        self.Valve_quality.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Valve_quality.clicked.connect(lambda x: self.setQualityWeapon("Valve"))
        self.buttonsQuality["Valve"] = self.Valve_quality
        self.Valve_quality.setStyleSheet(
                                "QPushButton{\n"
                                f"background-color: rgb(70, 70, 70);color: rgb({colorQuality['Valve']});"
                                "font: 9pt \"TF2\";"
                                "border-bottom-left-radius: 7px;"
                                "border-bottom-right-radius: 7px;}"
                                "QPushButton:hover{"
                                "background-color: rgb(65, 65, 65);"
                                "}"
                                "QPushButton:checked{background-color: rgb(60, 100, 75);}")
        self.Valve_quality.setCheckable(True)
                
        self.groupBox_6 = QtWidgets.QGroupBox(parent=self)
        self.groupBox_6.setGeometry(QtCore.QRect(880, 429, 212, 93))
        self.groupBox_6.setStyleSheet("border:0;color: rgb(255, 255, 255);font: 9pt \"TF2 Build\";background-color: rgba(255, 255, 255, 0);")
        self.groupBox_6.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.groupBox_6.setObjectName("groupBox_6")
        
        self.leftside_atributesLibary_7 = QtWidgets.QFrame(parent=self.groupBox_6)
        self.leftside_atributesLibary_7.setGeometry(QtCore.QRect(10, 18, 190, 68))
        self.leftside_atributesLibary_7.setStyleSheet("background-color: rgb(47, 47, 47);border-radius: 5px;")
        self.leftside_atributesLibary_7.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.leftside_atributesLibary_7.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.leftside_atributesLibary_7.setObjectName("leftside_atributesLibary_7")

        self.lineEdit_2 = QtWidgets.QTextEdit(parent=self.leftside_atributesLibary_7)
        self.lineEdit_2.setGeometry(QtCore.QRect(8, 6, 175, 58))
        self.lineEdit_2.setMinimumSize(QtCore.QSize(0, 58))
        self.lineEdit_2.setStyleSheet("font: 11pt \"TF2\";")
        self.lineEdit_2.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CursorShape.IBeamCursor))
        self.lineEdit_2.setTabStopDistance(15)
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.AtributesInterface()

    def initAtr(self):
        self.atribut = atribute_libary.Atribute
        
        self.ListButtonAccepted = []
        self.spacer_2 = None
        self.ListButton = []
        self.AllButtonTile = []
        self.activeStats = {}

    def AtributesInterface(self):
        self.initAtr()
        self.spacer = None

        List = QtWidgets.QScrollArea(parent=self.groupBox)
        List.setEnabled(True)
        List.setGeometry(QtCore.QRect(10, 50, 275, 440))
                
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(List.sizePolicy().hasHeightForWidth())
        List.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("TF2")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setKerning(True)
        List.setFont(font)
        List.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        List.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        List.setAcceptDrops(False)
        List.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        List.setAutoFillBackground(False)
        List.setStyleSheet("QWidget{background-color: rgb(48, 48, 48);}:handle,QWidget:vertical{border-radius: 5px;    background-color: rgb(56, 56, 56);    width: 5px;    min-height: 10px;}:handle, QWidget:horizontal  {    border-radius: 5px;    background-color: rgb(56, 56, 56);    width: 5px;    min-width: 5px;}:groove, QWidget:vertical {    background-color: rgb(72, 72, 72);    border-radius:  4px;}:sub-line, QWidget:vertical{    background-color: rgba(255, 255, 255, 0);}:add-line, QWidget:vertical{    background-color: rgba(255, 255, 255, 0);}QWidget::add-page:horizontal, QWidget::sub-page:horizontal {background: none;}QWidget::add-page:vertical, QWidget::sub-page:vertical {background: none;}")
        List.setFrameShape(QtWidgets.QFrame.Shape.Box)
        List.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        List.setLineWidth(1)
        List.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        List.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        List.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        List.setWidgetResizable(True)
        List.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        List.setObjectName("List")
        self.scrollAreaWidgetContents_6 = QtWidgets.QWidget(parent=List)
        self.scrollAreaWidgetContents_6.setGeometry(QtCore.QRect(0, 0, 30, 400))
        self.scrollAreaWidgetContents_6.setObjectName("scrollAreaWidgetContents_6")
        verticalLayout_8 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_6)
        verticalLayout_8.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        verticalLayout_8.setObjectName("verticalLayout_8")
        List.setWidget(self.scrollAreaWidgetContents_6)
        
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.FillTileAtribute()
        verticalLayout_8.addLayout(self.verticalLayout)
                
        Seach_lineedit = QtWidgets.QLineEdit(parent=self.groupBox)
        Seach_lineedit.setGeometry(QtCore.QRect(20, 25, 258, 20))
        Seach_lineedit.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        Seach_lineedit.setStyleSheet("font: 11pt \"TF2\";border:0;border-radius: 7px;background-color: rgb(61, 61, 61);color: rgb(255, 255, 255);")
        Seach_lineedit.setObjectName("Seach_lineedit")
        Seach_lineedit.editingFinished.connect(lambda: self.Search(Seach_lineedit.text()))
   
        Seach_icon = QtWidgets.QFrame(parent=Seach_lineedit)
        Seach_icon.setGeometry(QtCore.QRect(234, 3, 16, 16))
        Seach_icon.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        Seach_icon.setStyleSheet(f"border-image: url({_systemPath.get('search','Interface')});background-color: rgba(255, 255, 255,0);")
        Seach_icon.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        Seach_icon.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        Seach_icon.setObjectName("Seach_icon")
        
        self.AcceptedInterface()

    def AcceptedInterface(self):       
        List = QtWidgets.QScrollArea(parent=self.groupBox_2)
        List.setEnabled(True)
        List.setGeometry(QtCore.QRect(20, 30, 260, 450))
        self.acceptedList = List
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(List.sizePolicy().hasHeightForWidth())
        List.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("TF2")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setKerning(True)
        List.setFont(font)
        List.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        List.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        List.setAcceptDrops(False)
        List.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        List.setAutoFillBackground(False)
        List.setStyleSheet("QWidget{background-color: rgb(48, 48, 48);}:handle,QWidget:vertical{border-radius: 5px;    background-color: rgb(56, 56, 56);    width: 5px;    min-height: 10px;}:handle, QWidget:horizontal  {    border-radius: 5px;    background-color: rgb(56, 56, 56);    width: 5px;    min-width: 5px;}:groove, QWidget:vertical {    background-color: rgb(72, 72, 72);    border-radius:  4px;}:sub-line, QWidget:vertical{    background-color: rgba(255, 255, 255, 0);}:add-line, QWidget:vertical{    background-color: rgba(255, 255, 255, 0);}QWidget::add-page:horizontal, QWidget::sub-page:horizontal {background: none;}QWidget::add-page:vertical, QWidget::sub-page:vertical {background: none;}")
        List.setFrameShape(QtWidgets.QFrame.Shape.Box)
        List.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        List.setLineWidth(1)
        List.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        List.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        List.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        List.setWidgetResizable(True)
        List.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        List.setObjectName("List")
        self.scrollad = QtWidgets.QWidget()
        self.scrollad.setGeometry(QtCore.QRect(0, 0, 200, 450))
        verticalbs = QtWidgets.QVBoxLayout(self.scrollad)
        verticalbs.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        verticalbs.setObjectName("verticalbs")
        List.setWidget(self.scrollad)
        
        boxlay = QtWidgets.QVBoxLayout()
        boxlay.setObjectName("verticalLayout")

        self.verticalLayout1 = boxlay
        verticalbs.addLayout(boxlay)

    def editValue(self, objName, value : float):
        self.activeStats[objName]["Value"] = value

    def remove(self, button, stat):
        self.ListButtonAccepted.remove(button)
        try:
            self.activeStats.pop(stat["Name"].title())
        except KeyError as e:
            print(f"KeyError: {e} - {stat['Name'].title()} not found in activeStats.")

        self.verticalLayout1.removeWidget(button)
        button.deleteLater()
        
        self.ReturnButtonAttribute(stat)

    def Clear(self):
        self.activeStats.clear()
        if self.ListButtonAccepted is not None and len(self.ListButtonAccepted) > 0:
            for item in self.ListButtonAccepted:
                self.verticalLayout1.removeWidget(item)
                item.deleteLater()
        self.ListButtonAccepted.clear()
        self.ListButtonAccepted = []

    def ClearTile(self):
        if len(self.AllButtonTile) > 0:
            for item in self.AllButtonTile:
                try:
                    item.deleteLater()
                except Exception as e:
                    print(f"Error deleting item: {e}")
            self.AllButtonTile.clear()

    def FillTileAtribute(self, key = ""):
        self.ClearTile()
        for item in self.atribut:
            if len(key) > 0:
                if key.lower() in self.atribut[item]["Name"].lower():
                    self.AddButton(self.atribut[item])
            else:
                self.AddButton(self.atribut[item])

    def Search(self, searchText):
        self.FillTileAtribute(key = searchText)

    def AddButton(self, stat = None, indexPosition = -1):
        if stat["Name"].title() in self.activeStats:
            return
        
        Item = QtWidgets.QGroupBox(parent=self)
        Item.setMinimumSize(QtCore.QSize(260, 50))
        Item.setMaximumSize(QtCore.QSize(260, 50))
        Item.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        Item.setStyleSheet("border:0;")
        Item.setObjectName("Item")
        ButtonAddCosmetic = QtWidgets.QPushButton(parent=Item)
        ButtonAddCosmetic.setGeometry(QtCore.QRect(0, 0, 260, 50))
        ButtonAddCosmetic.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        ButtonAddCosmetic.setStyleSheet("background-color: rgb(56, 56, 56); border-radius: 10px;")
        ButtonAddCosmetic.setIconSize(QtCore.QSize(90, 90))
        ButtonAddCosmetic.setObjectName("ButtonAddCosmetic")
        Name = QtWidgets.QLabel(parent=ButtonAddCosmetic)
        Name.setGeometry(QtCore.QRect(55, 14, 251, 21))
        Name.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        Name.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        Name.setObjectName("Name")

        Icon = QtWidgets.QFrame(parent=Item)
        Icon.setGeometry(QtCore.QRect(13, 12, 24, 24))
        Icon.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))        
        Icon.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        Icon.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        Icon.setObjectName("Icon")
        
        if indexPosition == -1:
            self.verticalLayout.addWidget(Item)
        else:
            self.verticalLayout.insertWidget(indexPosition, Item, 10, QtCore.Qt.AlignmentFlag.AlignTop|QtCore.Qt.AlignmentFlag.AlignLeft)

        if stat != None:
            if stat["Effect"] == "Positive":
                ico = "Pictogram_plus"
                color = "0,202,40"
                
            elif stat["Effect"] == "Nigative":
                ico = "Pictogram_minus"
                color = "183,45,43"
            else:
                ico = "Pictogram_neutral"
                color = "100,100,100"
                
            Icon.setStyleSheet(f"border-image: url({_systemPath.get(ico, 'Interface')}); background-color: rgba(255, 255, 255, 0);")
            Name.setStyleSheet(f"color: rgb({color}); font: 12pt \"TF2 Build\";")
            Name.setText(stat["Name"])
            
            event = lambda x: (self.AddButtonToGeneral(stat, Item))
            ButtonAddCosmetic.mousePressEvent = event
            Name.mousePressEvent = event
            Icon.mousePressEvent = event
        else:
            Icon.setStyleSheet(f"border-image: url({_systemPath.get('Plus','Interface')}); background-color: rgba(255, 255, 255, 0);")
        
        self.AllButtonTile.append(Item)
        
        if self.spacer != None:
            self.verticalLayout.removeItem(self.spacer)
        self.spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(self.spacer)
        
    def ReturnButtonAttribute(self, stat):
        self.AddButton(stat, 0)

    def DeleteButtonAttribute(self, button):
        try:
            button.deleteLater()
        except Exception as e:
            print(f"Error deleting button: {e}")
            
    def AddButtonToGeneral(self, stat = None, button = None):
        if button is not None:
            self.DeleteButtonAttribute(button)
            
        ButtunAddAtributes_2 = QtWidgets.QPushButton(parent=self.acceptedList)
        ButtunAddAtributes_2.setGeometry(QtCore.QRect(0, 0, 240, 30))
        ButtunAddAtributes_2.setMinimumSize(QtCore.QSize(240, 30))
        ButtunAddAtributes_2.setBaseSize(QtCore.QSize(0, 25))
        ButtunAddAtributes_2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        ButtunAddAtributes_2.setAccessibleDescription("")
        ButtunAddAtributes_2.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        ButtunAddAtributes_2.setAutoFillBackground(False)
        ButtunAddAtributes_2.setStyleSheet(f"background-color: rgb(65,65,65);border-radius: 5px;font: 12pt \"TF2\";")
        
        ButtunAddAtributes_2.setCheckable(False)
        ButtunAddAtributes_2.setChecked(False)
        ButtunAddAtributes_2.setObjectName("ButtunAddAtributes_2")

        self.lineEdit = QtWidgets.QLineEdit(parent=ButtunAddAtributes_2)
        self.lineEdit.textChanged.connect(lambda text: self.lineEdit.setText(text.replace(',', '.')))
        
        self.lineEdit.setGeometry(QtCore.QRect(195, 5, 40, 20))
        self.lineEdit.setStyleSheet("background-color: rgb(80, 80, 80);\n"
                                    "border:0;\n"
                                    "color:white;"
                                    "border-radius: 5px;\n"
                                    "font: 12pt \"TF2\";")
        self.lineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")

        DeleteCosmeticButton_2 = QtWidgets.QPushButton(parent=ButtunAddAtributes_2)
        DeleteCosmeticButton_2.setGeometry(QtCore.QRect(7, 6, 20, 20))
        DeleteCosmeticButton_2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        DeleteCosmeticButton_2.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                                            "font: 30pt \"TF2\";\n"
                                            "color: rgb(185, 45, 43);")
        DeleteCosmeticButton_2.setObjectName("DeleteCosmeticButton")
        DeleteCosmeticButton_2.setText("-")
        
        icon3 = QtGui.QIcon()
        if stat != None:
            if stat["Effect"] == "Positive":
                ico = "Pictogram_plus"
                color = "0,202,40"
            elif stat["Effect"] == "Nigative":
                ico = "Pictogram_minus"
                color = "183,45,43"
            else:
                ico = "Pictogram_neutral"
                color = "100,100,100"
                    
            icon3.addPixmap(QtGui.QPixmap(f"{_systemPath.get(ico)}"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            ButtunAddAtributes_2.setStyleSheet(f"background-color: rgb(65,65,65);border-radius: 5px;font: 12pt \"TF2\"; color: rgb({color})")
            ButtunAddAtributes_2.setText(stat["Name"].title())
            
            if "Value" in stat:
                self.lineEdit.setText(f"{stat['Value']}")
            else:
                stat['Value'] = 0
                self.lineEdit.setText(f"{stat['Value']}")
            
            self.lineEdit.textChanged.connect(lambda: self.editValue(str(stat['Name']).title(), self.lineEdit.text().replace(",", ".")))
          
            self.ListButtonAccepted.append(ButtunAddAtributes_2)
            
            DeleteCosmeticButton_2.clicked.connect(lambda x: self.remove(ButtunAddAtributes_2, stat))
            
            self.activeStats[stat['Name'].title()] = stat
            
        else:
            ButtunAddAtributes_2.setText("None")
            
        ButtunAddAtributes_2.setIcon(icon3)
        
        self.verticalLayout1.addWidget(ButtunAddAtributes_2)
        if self.spacer_2 != None:
            self.verticalLayout1.removeItem(self.spacer_2)
        self.spacer_2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
            
        self.verticalLayout1.addItem(self.spacer_2)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.Cancel.setText(_translate("GroupBox", "Cancel"))
        self.Save.setText(_translate("GroupBox", "Save"))
        self.groupBox.setTitle(_translate("GroupBox", "CharacterAttributes"))
        self.nameWeapon.setText(_translate("GroupBox", "Scattergun"))
        self.groupBox_2.setTitle(_translate("GroupBox", "Accepted"))
        
        self.groupBox_3.setTitle(_translate("GroupBox", "Custom"))
        
        self.groupBox_4.setTitle(_translate("GroupBox", "Name"))
        self.groupBox_5.setTitle(_translate("GroupBox", "quality"))
        self.normal_quality.setText(_translate("GroupBox", "Normal"))
        self.Unique_quality.setText(_translate("GroupBox", "Unique"))
        self.Genuine_quality.setText(_translate("GroupBox", "Genuine"))
        self.Vintage_quality.setText(_translate("GroupBox", "Vintage"))
        self.Unusual_quality.setText(_translate("GroupBox", "Unusual"))
        self.Strange_quality.setText(_translate("GroupBox", "Strange"))
        self.Collector_quality.setText(_translate("GroupBox", "Collector\'s"))
        self.Haunted_quality.setText(_translate("GroupBox", "Haunted"))
        self.Decorated_quality.setText(_translate("GroupBox", "Decorated"))
        self.Community_quality.setText(_translate("GroupBox", "Community"))
        self.Valve_quality.setText(_translate("GroupBox", "Valve"))
        self.groupBox_6.setTitle(_translate("GroupBox", "Description"))
        self.lineEdit_2.setText(_translate("GroupBox", "Description"))

    def setQualityWeapon(self, quality : str):
        self.qualityWeapon = quality
        for item in self.buttonsQuality:
            if item != quality:
                self.buttonsQuality[item].setChecked(False)
            else:
                self.buttonsQuality[item].setChecked(True)
                self.nameWeapon.setStyleSheet(f"color: rgb({colorQuality[quality]});font: 9pt \"TF2 Build\";")
                
                if quality == "Strange": # Проверка на Strange
                    self.strange.show()
                else: 
                    self.strange.hide()

    def Open(self, stat : WeaponData):
        if Mercenary_now == None:
            return
        
        self.activeStats.clear()
        self.Clear()
        
        self.stat = stat.get().copy() # Получаем копию данных оружия
        self.weapon = stat.get() # Сохраняем ссылку на оружие для дальнейшего сохранения изменений
        
        self.ico_weapon.setStyleSheet(f"border-image: url({_systemPath.get(stat.get('Icon'), 'weapon')});")
                
        if len(stat.get('Custom Name')) > 0:
            self.nameWeapon.setText(f'''"{stat.get("Custom Name")}"''')
            self.customName.setText(stat.get("Custom Name"))
        else:
            self.nameWeapon.setText(f'{stat.get("Name")}')
            self.customName.setText("")
        
        self.setQualityWeapon(stat.get("Quality"))
                
        self.lineEdit_2.setText(f"{stat.get('Description')}")
        self.lineEdit_3.setText(f"{stat.get('Custom')}")
        
        atr = self.stat["Attributes"]

        if "Effect" in atr: 
            for item in atr:
                self.AddButtonToGeneral(item)
        else:
            if isinstance(atr, dict):
                for item in atr.values():
                    if "Attributes" in item:
                        for attr in item["Attributes"]:
                            self.AddButtonToGeneral(item["Attributes"][attr])
                    else:
                        self.AddButtonToGeneral(item)
            elif isinstance(atr, list):
                for item in atr:
                    self.AddButtonToGeneral(item)
        self.show()

    def CloseMenu(self):
        self.Clear()
        self.clearFocus()
        self.activeStats.clear()
        self.close()
    
    def ChangeName(self):
        self.nameWeapon.setStyleSheet(f"color: rgb({colorQuality[self.qualityWeapon]});font: 9pt \"TF2 Build\";")
        self.nameWeapon.setText( f'"{self.customName.text()}"' )
        
    def SaveStat(self, exitAfterSave = True):
        if self.weapon != None:
            self.weapon.update({"Custom Name": self.customName.text()})
                
            self.weapon.update({"Description": self.lineEdit_2.toPlainText()})
            self.weapon.update({"Custom": self.lineEdit_3.toPlainText()})
            self.weapon.update({"Quality": self.qualityWeapon.title()})

            self.weapon.update({"Attributes": self.activeStats.copy()})
            Mercenary_now.update_icons()
            if exitAfterSave:
                self.CloseMenu()

class Robot:
    def __init__(self, 
                 robot_type, 
                 size= 1.0, 
                 squad=None, 
                 speed=0, 
                 skill="Normal", 
                 path=None,
                 progress_factor = 1, 
                 max_cosmetics = 8, 
                 max_attributes = 4,
                 can_be_giant = True
        ):
        self.robot_type = robot_type
        self.progress_factor = progress_factor
        robot_default_health = {
            "Scout": 125, 
            "Soldier": 200,
            "Pyro": 175,
            "Demoman": 175,
            "Heavy": 300,
            "Engineer": 125,
            "Medic": 150,
            "Sniper": 125,
            "Spy": 125,
        }
        
        self.squad = squad
        self.speed = speed
        self.skill = skill
        self.path = path
        self.power = 0
        self.weapontype = 0
        self.can_be_giant = can_be_giant
        
        self.size = self.calculate_size(size)
        
        self.giant = self.size > 1.25
        if random.random() < 0.15 and self.size > 1.25 and self.can_be_giant:
            self.health = self.calculate_health(robot_default_health.get(robot_type, 100) * 10)
        else:
            self.health = self.calculate_health(robot_default_health.get(robot_type, 100))
            
        if self.robot_type not in ["Mini Sentry Buster", "Sentry Buster"]:
            self.cosmetics = self.assign_cosmetics(max_cosmetics)
            self.weapons = self.assign_weapons()
            self.weapontype = self.weapons["Type"]
            self.character_attributes = self.assign_attributes(max_attributes)
        else:
            self.cosmetics = []
            self.weapons = {}
            self.character_attributes = []
                    
        self.max_vision_range = self.assign_max_vision_range() 
        self.robot_attributes = self.assign_robot_attributes()

        self.power += self.calculate_power()  # Перемещено в конец
        
    def calculate_health(self, basic_heal = 100):
        heal = max(basic_heal, int(basic_heal * self.size * max(1, self.progress_factor)))        
        return heal
    
    def calculate_size(self, basic_size = 1):
        return float(basic_size + (round(random.uniform(0, 1) / 2 if self.can_be_giant else random.uniform(0, 0.25) , 1) ) )
    
    def assign_max_vision_range(self):
        base_vision = 600
        vision_bonus = self.power * 100 * self.progress_factor
        return int(base_vision + vision_bonus)

    def assign_robot_attributes(self):
        attributes = {}
        power_adjustment = 0.0

        # Общие параметры
        if self.health > 1250 and self.size > 1.25:
            attributes["Bot_Giant"] = 0.25
            attributes["MiniBoss"] = 0.25
            power_adjustment += 0.5
            
        if self.health > 4000:
            attributes["UseBossHealthBar"] = 1
            power_adjustment += 1.25

        # Специфические параметры
        if random.random() < 0.15 and self.robot_type in ["Spy", "Engineer"]:
            attributes["TeleportToHint"] = 0.1
            power_adjustment += 0.1
            
        if random.random() < 0.15 and self.robot_type == "Engineer":
            attributes["RetainBuildings"] = 0.25
            power_adjustment += 0.25

        # Параметры, применимые ко всем типам
        optional_attributes = {
            "SpawnWithFullCharge": 0.25,
            "HoldFireUntilFullReload": 0.25,
            #"SuppressFire": 0.1,
            #"IgnoreFlag": -0.25,
            "VaccinatorBlast": 0.5,
            "VaccinatorBullets": 0.5,
            "VaccinatorFire": 0.5,            
            "AlwaysCrit": 0.5,
            "AlwaysFireWeapon": 0.35,
            "DisableDodge": 0.38,
        }

        # Автоматическое добавление
        for attr, value in optional_attributes.items():
            if random.random() < 0.15:  # 15% шанс добавить атрибут
                attributes[attr] = value * self.progress_factor if self.giant else value
                power_adjustment += value

        # Специальная логика для AutoJump и AirChargeOnly
        if self.robot_type == "Demoman" and random.random() < 0.15:  # 15% шанс добавить
            attributes["AirChargeOnly"] = 0
            attributes["AutoJump"] = 0
            power_adjustment += 0.17  # Комбинированное влияние

        self.power += power_adjustment
        return attributes

    def assign_cosmetics(self, max_cosmetics):
        if self.robot_type == "Tank":
            return []

        available_cosmetics = [
            cosmetic for cosmetic in Cosmetic.values()
            if "Class" in cosmetic and (
                isinstance(cosmetic["Class"], str) and self.robot_type == cosmetic["Class"]
                or isinstance(cosmetic["Class"], list) and self.robot_type in cosmetic["Class"]
            )
        ]
        return random.sample(available_cosmetics, min(len(available_cosmetics), random.randint(1, max_cosmetics)))

    def assign_weapons(self):
        if self.robot_type == "Tank":
            return {
                "Type": "None",
                "Name": "No Weapon",
                "ItemAttributes": {}
            }

        banned_to_type_weapon = [
            "The Buff Banner", 
            "Gunboats", 
            "The Battalion's Backup", 
            "The Concheror",
            "The Mantreads",
            "Festive Buff Banner",
            "The B.A.S.E. Jumper",
            "Thermal Thruster",
            "The Bootlegger",
            "Ali Baba's Wee Booties",
            "The Chargin' Targe",
            "The Tide Turner",
            "The Razorback",
            "Darwin's Danger Shield",
            "Cozy Camper",
        ]
        banned_to_types_weapon = ["Clock", "PDA"]  
        
        weapon_types = list(Weapon_Libary[self.robot_type].keys())  # Например, "Primary", "Secondary", "Melee"
        weapon_type = random.choice(weapon_types)  # Выбор категории оружия
        weapon_name = random.choice(list(Weapon_Libary[self.robot_type][weapon_type].values()))  # Случайное оружие из выбранной категории
                    
        item_attributes = self.assign_item_attributes()  # Генерация атрибутов оружия

        type_weapon = {"All" : 0, "Primary": 1, "Secondary" : 2, "Melee" : 3}
        
        if weapon_type in banned_to_types_weapon or weapon_name in banned_to_type_weapon:
            type = type_weapon.get(0)
        else:
            type = type_weapon.get(weapon_type, 0)
        # Возвращаем данные с упрощённой структурой
        return {
            "Type": type,
            "Name": weapon_name,
            "ItemAttributes": item_attributes
        }

    def assign_item_attributes(self):
        possible_attributes = list(Atribute.keys())
        selected_attributes = random.sample(possible_attributes, int(random.randint(1, 3) * self.progress_factor))  # От 1 до 3 атрибутов
        item_attributes = []  # Список для хранения атрибутов

        for attr in selected_attributes:
            if "Mod" in attr or "Mode" in attr:
                item_attributes.append({"Name": attr, "Value": 1, "Effect": "Neutral"})
            else:
                effect_type = Atribute[attr].get("Effect", "Neutral")
                if effect_type == "Positive":
                    value = 0.15
                    self.power += value
                elif effect_type == "Negative":
                    value = -0.15
                    self.power += value
                else:
                    value = 1

                item_attributes.append({"Name": attr, "Value": round((value * self.progress_factor) if self.giant else value, 2), "Effect": effect_type})

        return item_attributes


    def assign_attributes(self, max_attributes):
        attributes = {}  # Инициализируем список
        possible_attributes = list(Atribute.keys())
        selected_attributes = random.sample(possible_attributes, int(random.randint(1, max_attributes)))  # От 1 до 3 атрибутов

        for attr in selected_attributes:
            if "Mod" in attr or "Mode" in attr:
                attributes.append({"Name": attr, "Value": 1, "Effect": "Neutral"})
            else:
                effect_type = Atribute[attr].get("Effect", "Neutral")
                if effect_type == "Positive":
                    value = round(random.uniform(0.1, 1), 2)
                    self.power += value
                elif effect_type == "Negative":
                    value = -round(random.uniform(0.1, 1), 2)
                    self.power += value
                else:
                    value = 1

                attributes[attr] = {"Name": attr, "Value": round((value * self.progress_factor) if self.giant else value, 2) , "Effect": effect_type}

        return attributes
    
    def calculate_power(self):
        power = 0
    
        base_power = {
            "Scout": 0.1, "Soldier": 0.25, "Pyro": 0.2, "Demoman": 0.2,
            "Heavy": 0.45, "Engineer": 0.35, "Medic": 0.15, "Sniper": 0.12,
            "Spy": 0.12, "Tank": 4.0, "Sentry Buster": 0.5, "Mini Sentry Buster": 0.3
        }
        power += base_power.get(self.robot_type, 0.1)
        
        # Атрибуты оружия
        if "ItemAttributes" in self.weapons:
            
            for attr in self.weapons["ItemAttributes"]:
                if attr["Effect"] == "Positive":
                    power += attr["Value"]
                elif attr["Effect"] == "Nigative":
                    power -= attr["Value"] / 2
        else:
            print("No item attributes found in weapons.")

        for attr, value in self.character_attributes.items():
            if value["Effect"] == "Positive":
                power += value["Value"]
            elif value["Effect"] == "Nigative":
                power -= value["Value"]
        
        for item in range(len(self.cosmetics)):
            power += 0.1
            
        return power

class Mission_Support:
    def __init__(self, waves, difficulty, progression_factor=1.1, default_robot_params = None, useTemplateBots = True, money_for_wave = 5000):
        self.waves = waves
        self.difficulty = difficulty
        self.progression_factor = progression_factor
        self.useTemplateBots = useTemplateBots 
        self.money_for_wave = money_for_wave
        self.default_robot_params = default_robot_params or {
            "Scout":    {"size": 1.0, "speed": 1,  "skill": 1, "health": 125},
            "Soldier":  {"size": 1.0, "speed": 1,  "skill": 1, "health": 200},
            "Pyro":     {"size": 1.0, "speed": 1,  "skill": 1, "health": 175},
            "Demoman":  {"size": 1.0, "speed": 1,  "skill": 1, "health": 175},
            "Heavy":    {"size": 1.0, "speed": 1,  "skill": 1, "health": 300},
            "Engineer": {"size": 1.0, "speed": 1,  "skill": 1, "health": 125},
            "Medic":    {"size": 1.0, "speed": 1,  "skill": 1, "health": 150},
            "Sniper":   {"size": 1.0, "speed": 1,  "skill": 1, "health": 125},
            "Spy":      {"size": 1.0, "speed": 1,  "skill": 1, "health": 125},
            "Tank":     {"size": 1.0, "speed": 75, "skill": 1, "health": 20000},
        }
        self.used_templates = []
        self.squads = []

    def choose_template_robot(self, robot_type, is_chief, giant_health_range, existing_chief, wave_number):
        # Restrict Chiefs and Majors to higher difficulties and later waves
        if self.difficulty < 3 or wave_number < self.waves - 2:
            is_chief = False

        templates = [
            template for template in Template.values()
            if template.get("Class") == robot_type and
            (
                "Chief" in template.get("Name", "") or
                "Major" in template.get("Name", "") or
                "Sergeant" in template.get("Name", "") or
                "Captain" in template.get("Name", "") or
                "Sir" in template.get("Name", "")
                if is_chief else
                "Chief" not in template.get("Name", "") and
                "Major" not in template.get("Name", "") and
                "Sergeant" not in template.get("Name", "") and
                "Captain" not in template.get("Name", "") and
                "Sir" not in template.get("Name", "")
            ) and
            template.get("Name") not in self.used_templates
        ]
        if not templates or (is_chief and existing_chief):
            return None

        if giant_health_range:
            templates = sorted(templates, key=lambda t: abs(t.get("Health", 0) - giant_health_range))

        chance = 0.2 if is_chief else 0.1  # Reduced chance for Chief, Major, and Sergeant robots
        
        chosen_template = random.choices(templates, weights=[chance for _ in templates], k=1)[0]
        self.used_templates.append(chosen_template.get("Name"))
        if is_chief:
            chosen_template["Power"] = 10 # Chief robots have fixed Power of 5
        else:
            chosen_template["Power"] = 3
        # Выводим только имя блока
        return chosen_template
    def process_weapon(self, robot, weapon_type):
        
        type_weapon = {0: "Primary", 1: "Primary", 2 : "Secondary", 3: "Melee"}
        
        if robot.weapons["Type"] == weapon_type:
            atr = robot.weapons.get("ItemAttributes", {})
            if not isinstance(atr, list):
                atr = []
                print(f"[ERROR] Unexpected structure for robot.weapons['ItemAttributes']")
            
            weapon = WeaponData(
                Class =  robot.robot_type,
                WeaponType = type_weapon.get(weapon_type, "Primary"),
                weaponName = robot.weapons["Name"]["Name"],
                attrubutes = atr
            )
        else:
            weapon = WeaponData(robot.robot_type, type_weapon.get(weapon_type, "Primary"))

        return weapon
    
    def calculate_robot_count(self, wave_number, difficulty, progression_factor):
        """
        Рассчитывает количество роботов в волне с учетом нелинейного роста,
        сложности и прогрессии волн, с динамическим минимумом.
        """
        # Нелинейный базовый расчет количества роботов
        base_count = max(4, 1 + int(wave_number ** 1.3 * progression_factor) + difficulty)
        
        # Динамический минимум в зависимости от номера волны
        wave_min = max(4, int(3 + wave_number * 0.55))  # Минимум растет с каждой волны

        # Максимальный лимит растет быстрее для поздних волн
        max_limit = 12 + int(wave_number ** 1.05)  # Более агрессивный рост верхнего предела
        
        # Рассчитываем минимальное и максимальное количество роботов
        min_count = max(wave_min, int(base_count * 1.15))  # Минимум на 10-15% больше базового
        max_count = min(int(base_count * 1.2), max_limit)

        # Гарантируем, что min_count <= max_count
        if min_count > max_count:
            min_count, max_count = max_count, min_count

        return random.randint(min_count, max_count)

    def calculate_squad_attributes(self, robot : Robot, wave_number : int, difficulty : int, progressive : float, chosen_template = None ):
        """
        Рассчитывает атрибуты total_count, max_active и spawn_count для сквада, с учётом состава сквада.
        difficulty: от 1 (Easy) до 5 (Nightmare).
        progressive: Множитель для прогрессии сложности.
        """
        # Проверяем, что progressive имеет значение
        if progressive is None:
            progressive = 1.1  # Устанавливаем значение по умолчанию

        is_giant = robot.size > 1.25 or "Giant" in getattr(robot, "template_name", "") or robot.robot_type == "Tank" or chosen_template is not None
        is_super_giant = any(keyword in getattr(robot, "template_name", "") for keyword in ["Chief", "Major", "Sergeant", "Captain", "Prince", "Sir"])

        if is_super_giant:
            total_count, max_active, spawn_count = 1, 1, 1
        elif is_giant:
            base_count = int(wave_number * progressive * 2 + difficulty * 3)
            lower_bound = max(2, base_count - 3)
            upper_bound = base_count + 3

            if lower_bound >= upper_bound:
                total_count = lower_bound  # Если диапазон некорректен, берём нижнюю границу
            else:
                total_count = random.randint(lower_bound, upper_bound)

            max_active = random.randint(2, min(5, total_count))
            spawn_count = random.randint(2, 4)  # Генерируем значение для баланса
        else:
            robot_power = max(1, robot.power)  # Предотвращаем деление на 0
            base_total_count = int((wave_number * progressive * 4) + (difficulty * 4))
            max_total_count = base_total_count + 10
            min_total_count = max(5, base_total_count - 10)

            # Убедимся, что диапазон корректен
            if min_total_count > max_total_count:
                min_total_count = max_total_count

            total_count = random.randint(min_total_count, max_total_count)
            max_active = random.randint(
                max(3, total_count // (10 * robot_power)),
                max(6, total_count // (8 * robot_power))
            )
            spawn_count = random.randint(2, 6)

        # Увеличение сложности для Nightmare уровня
        if difficulty == 5:  # Nightmare
            total_count = int(total_count * 1.5)
            max_active = int(max_active * 1.25)
            spawn_count = max(2, spawn_count + 2)

        # Уточняем, чтобы max_active был >= spawn_count
        max_active = max(max_active, spawn_count)

        return total_count, max_active, spawn_count

    def generate_wave(self, wave_number, moneyForWave, path_selected, settings_robot):
        """
        Генерирует волну роботов с учетом сложности, факторов прогрессии и выбранного пути.
        """
        
        squad_in = []
        WaveManagerGlobal.add_wave_by_generate(f"Wave {wave_number}", path_selected["init_settings"])
        WaveManagerGlobal.setWave(f"Wave {wave_number}")
        standard_health = 3000 + ((wave_number * self.progression_factor) * 200)
        allSquadCount = self.calculate_robot_count(wave_number, self.difficulty, self.progression_factor)
        class_count = {}
        tank_count =  0
        chief_count = 0
        giant_count = 0
        existing_chief = False

        for _ in range(allSquadCount):
            exit_check1 = False
            exit_check2 = False
            exit_check3 = False
            while True:
                robot_type = random.choice(list(self.default_robot_params.keys()))
                
                if robot_type not in settings_robot["banned_classes"]:
                    exit_check3 = True
                    
                if robot_type == "Tank":
                    if (wave_number <= settings_robot["start_spawn_tank_wave"] if settings_robot["start_spawn_tank_wave"] >= 0 else True) and self.difficulty <= 3:
                        #print(f"Танк не добавлены в волну {wave_number}, так как уровень сложности недостаточен.")
                        pass
                    elif tank_count >= (settings_robot["max_tanks"] - 1) if settings_robot["max_tanks"] >= 0 else True:
                        #print(f"Танк не добавлены в волну {wave_number}, так как их количество достигло максимального значения.")
                        pass
                    else:
                        tank_count += 1
                        exit_check1 = True
                else:
                    exit_check1 = True
                
                class_count.setdefault(robot_type, 0)
                if class_count and ((class_count[robot_type] >= settings_robot["max_type_same_class"]) if settings_robot["max_type_same_class"] >= 0 else True):
                    #print(f"Робот с классом : {robot_type} уже достиг максимального количества в {class_count[robot_type]}.")
                    pass
                else:
                    class_count[robot_type] += 1
                    exit_check2 = True
                    
                if exit_check1 and exit_check2 and exit_check3:
                    break
                
            if self.useTemplateBots != False:
                while True:
                    if (
                        random.random() < 0.5 and 
                        (wave_number >= settings_robot["teplate_start_at_wave"] if settings_robot["teplate_start_at_wave"] >= 0 else True 
                            or self.difficulty >= 3) and
                        (giant_count < settings_robot["max_giant"] - 1 if settings_robot["max_giant"] >= 0 else True)
                    ):
                        is_chief = (
                            (wave_number >= settings_robot["chief_begin_at_wave"] if settings_robot["chief_begin_at_wave"] >= 0 else True) and 
                            self.difficulty >= 4 and (random.random() < 0.22 if wave_number < 3 else random.random() < 0.33) and 
                            (chief_count - 1 < settings_robot["max_chief"] if settings_robot["max_chief"] >= 0 else True)
                        )
                        chosen_template = self.choose_template_robot(robot_type, is_chief, standard_health, existing_chief, wave_number)

                        if chosen_template:
                            isFinded = find_robot_by_name(chosen_template["Name"])
                            if isFinded:
                                if is_chief:
                                    existing_chief = True
                                    chief_count += 1
                                    #print(f"Осторожно! Добавлен Шеф! {chosen_template['Name']}")
                                else:
                                    giant_count += 1
                                    #print(f"Добавлен гигант : {isFinded}")
                                                        
                                class_count[robot_type] += 1
                                break
                    else:
                        chosen_template = None
                        break
            else:
                chosen_template = None

            params = self.default_robot_params[robot_type]
            robot = Robot(
                robot_type, 
                size = params["size"], 
                speed = params["speed"],
                skill = params["skill"], 
                max_cosmetics   = settings_robot["max_cosmetics"], 
                max_attributes  = settings_robot["max_attributes"],
                can_be_giant = giant_count < settings_robot["max_giant"] - 1 if settings_robot["max_giant"] >= 0 else True,
                progress_factor= self.progression_factor
            )
            if robot.giant:
                giant_count += 1
                
            target_squad = None
            if robot_type != "Tank" and chosen_template is None and len(SquadSettingsGlobal.SquadList) > 0:
                if squad_in:
                    target_squad = SquadSettingsGlobal.SquadList[random.choice(list(SquadSettingsGlobal.SquadList))]

                    # Проверка на наличие танка в скваде
                    if any(robot.stat["Class"] == "Tank" for robot in target_squad["InSquad"]):
                        target_squad = None
                    elif len(target_squad["InSquad"]) < 4:
                            target_squad["total_count"], target_squad["max_active"], target_squad["spawn_count"] = self.calculate_squad_attributes(
                                robot = robot, wave_number = wave_number, difficulty = self.difficulty, progressive = self.progression_factor, chosen_template= chosen_template
                            )
                    else:
                        target_squad = None
                    
            if target_squad == None:
                
                isSupport = (random.random() < 0.1 if chosen_template else random.random() < 0.35) if robot_type != "Tank" else False
                
                squad_struct = {
                    "name": f"Squad {len(self.squads) + 1}",
                    "robots": [robot],
                    "wait_between_spawns": round(random.uniform(1, 5), 1),
                    "wait_before_starting": round(random.uniform(1, 10), 1),
                    "Squad Is Support" : isSupport
                }
                if squad_in:
                    available_squads = [
                        squad["name"] for squad in squad_in if not squad.get("Squad Is Support", False)
                    ]  # Исключаем сквады с "Squad Is Support"
                    if available_squads:  # Проверяем, остались ли доступные сквады
                        if random.random() < 0.5:
                            squad_struct["wait_all_dead"] = random.choice(available_squads)
                            squad_struct["wait_all_spawn"] = None
                        else:
                            squad_struct["wait_all_spawn"] = random.choice(available_squads)
                            squad_struct["wait_all_dead"] = None
                    else:  # Если нет доступных сквадов
                        squad_struct["wait_all_dead"] = None
                        squad_struct["wait_all_spawn"] = None
                else:
                    squad_struct["wait_all_dead"] = None
                    squad_struct["wait_all_spawn"] = None
                    
                squad_struct["total_count"], squad_struct["max_active"], squad_struct["spawn_count"] = self.calculate_squad_attributes(
                    robot = robot, wave_number = wave_number, difficulty = self.difficulty, progressive = self.progression_factor, chosen_template= chosen_template
                )

                SquadSettingsGlobal.CreateSquad(
                    nameSquad=squad_struct["name"],
                    wait_before_spawn=squad_struct["wait_before_starting"],
                    wait_between_spawn=squad_struct["wait_between_spawns"],
                    wait_all_dead= "" if squad_struct["wait_all_dead"] in [None, "None"] else squad_struct["wait_all_dead"],
                    wait_all_spawn= "" if squad_struct["wait_all_spawn"] in [None, "None"] else squad_struct["wait_all_spawn"],
                    total_squad=squad_struct["total_count"] if robot_type != "Tank" else 1,
                    max_active=squad_struct["max_active"] if robot_type != "Tank" else 1,
                    squad_spawn=squad_struct["spawn_count"] if robot_type != "Tank" else 1,
                    credit_for_squad=int(moneyForWave / allSquadCount if allSquadCount != 0 else 0),
                    where_spawn=random.choice(path_selected["tank_paths"]) if robot.robot_type == "Tank" else random.choice(path_selected["where_spawn"]),
                    support = isSupport,
                    random_choice = random.random() < 0.15 and isSupport,
                    random_spawn = random.random() < 0.35 and isSupport,
                )
                if robot_type == "Tank":
                    self.create_tank(robot.health)
                else:
                    self.create_mercenary(robot, path_selected, squad_struct["name"], chosen_template)
                    
                    SquadSettingsGlobal.SaveSquad(True)
                    
                self.squads.append(squad_struct)
                squad_in.append(squad_struct)
            else:
                squad_struct = target_squad

                if robot_type == "Tank":
                    self.create_tank(robot.health)
                else:
                    self.create_mercenary(robot, path_selected, squad_struct["Name"], chosen_template)
                    
                SquadSettingsGlobal.SaveSquad(True)
                        
        return self.squads, []
    
    def recalculate_squad_attributes(self, wave_number, difficulty):
        """
        Пересчитывает параметры total_count, max_active и spawn_count для всех сквадов
        в SquadSettingsGlobal.SquadList, основываясь на power, health и типах роботов.
        """
        for squad_name, squad in SquadSettingsGlobal.SquadList.items():
            robots = squad["InSquad"]

            if not robots:
                #print(f"Skipping empty squad: {squad_name}")
                continue

            try:
                # Подсчёт общей мощности и здоровья
                total_power = sum(float(robot.stat["power"]) for robot in robots)
                total_health = sum(float(robot.stat["Health"]) for robot in robots)
                robot_count = len(robots)

                avg_power = total_power / robot_count if robot_count > 0 else 0
                avg_health = total_health / robot_count if robot_count > 0 else 0

                # Определение типа роботов
                has_giant = any(
                    float(robot.stat["Scale"]) > 1.25 or "Giant" in robot.stat["Name"]
                    for robot in robots
                )
                has_super_giant = any(
                    keyword in robot.stat["Name"]
                    for keyword in ["Chief", "Major", "Sergeant", "Captain", "Tank"]
                    for robot in robots
                )

                if has_super_giant:
                    # Ограничения для сверхсильных гигантов
                    total_count = 1
                    max_active = 1
                    spawn_count = 1
                elif has_giant:
                    # Параметры для обычных гигантов
                    base_count = max(1, wave_number // 2 + difficulty * 2)
                    total_count = max(1, min(6, int(base_count / avg_power)))
                    max_active = max(1, total_count // 2)
                    spawn_count = min(max_active, 1)  # Ограничиваем чётностью
                else:
                    # Параметры для стандартных роботов
                    max_total_count = min(30, wave_number * 5 + difficulty * 4)
                    min_total_count = max(10, max_total_count // 3)

                    total_count = random.randint(min_total_count, max_total_count)
                    max_active = random.randint(
                        max(3, total_count // 10), max(6, total_count // 8)
                    )
                    spawn_count = random.randint(2, max(4, total_count // max_active))

                    # Корреляция с avg_health и avg_power
                    if avg_power > 1:
                        total_count = max(2, int(total_count / avg_power))
                    if avg_health > 1000:
                        total_count = max(1, int(total_count / (avg_health / 1000)))

                    # Проверка чётности spawn_count
                    if spawn_count % 2 != 0:
                        spawn_count += 1

                # Корректируем параметры для баланса
                max_active = max(max_active, spawn_count)

                # Обновляем параметры сквада
                squad["Total Squad"] = total_count
                squad["Max Alive Squads"] = max_active
                squad["Squad Spawn"] = spawn_count

                #print(
                #    f"Updated squad '{squad_name}': total_count={total_count}, "
                #    f"max_active={max_active}, spawn_count={spawn_count}, "
                #    f"avg_power={avg_power}, avg_health={avg_health}"
                #)
            except Exception as e:
                print(f"Error processing squad '{squad_name}': {e}")     
        
    def create_mercenary(self, robot, robot_path, squadName, chosen_template = None):
        robot_type_to_index = {
            "Scout": 0,
            "Soldier": 1,
            "Pyro": 2,
            "Demoman": 3,
            "Heavy": 4,
            "Engineer": 5,
            "Medic": 6,
            "Sniper": 7,
            "Spy": 8,
        }
        robot_tag = [tag for tag in robot_path["robot_tag"]] if robot_path["robot_tag"] != None else []
        
        create_stat = {
            "Name": f"Giant {robot.robot_type.title()}" if (robot.size > 1.25 and robot.health > 700) else robot.robot_type,
            "Template": "" if chosen_template is None else chosen_template["Name"],
            "Class": robot_type_to_index.get(robot.robot_type, 0),
            "Class Name" : robot.robot_type,
            "Icon" :       Icons_Archive[f"leaderboard_class_{'demo' if robot.robot_type.lower() == 'demoman' else robot.robot_type.lower()}"],
            "Skill": robot.skill,
            "Health": robot.health,
            "Scale": robot.size,
            "MaxVision": robot.max_vision_range,
            "AutoJump Min": 0,
            "AutoJump Max": 0,
            "Tag": robot_tag or [],
            "Behavior": 0,
            "Cosmetics": [{'Name': item["Name"], 'Icon': item["Icon"]} for item in robot.cosmetics],
            "Primary Weapon": self.process_weapon(robot, weapon_type=1),
            "Secondary Weapons": self.process_weapon(robot, weapon_type=2),
            "Melee": self.process_weapon(robot, weapon_type=3),
            "CharacterAttributes": robot.character_attributes,
            "Tag_Attributes": robot.robot_attributes,
            "Custom Parametrs": """""",
            "Squad": squadName,
            "Weapon Restriction" :  robot.weapontype,
            "power" : robot.power,
            "model" : default_stat.Mercenary[robot.robot_type]["Model"]
        }
        mercenary = Create_Mercenary_From_Save(list=create_stat, squadName=squadName, isGenerated=True)
        
        if chosen_template and find_robot_by_name(chosen_template["Name"]) != None and robot.robot_type != "Tank":
            mercenary.change_to_template(find_robot_by_name(chosen_template["Name"]), robot.cosmetics, robot_tag or [])
        else:
            mercenary.change_class(robot.robot_type, True)
            mercenary.Set_Stat(create_stat)
        
        return mercenary
    
    def create_tank(self, health = 20000):
        tank = Adding_New_Mercenary_To_Wave(isGenerate=True)
        tank.change_class("Tank")
        tank.stat["Health"] = health
        tank.stat["power"] = 5                
        return tank

class RandomWaveGenerator(object):
    def __init__(self):
        self._mission_settings = {
            "waves": 5, # Количество волн в миссии
            "difficulty": 2,  # 1 - Easy, 2 - Normal, 3 - Hard, 4 - Insane, 5 - Nightmare
            "progressive": 1.1, # Progressive factor for difficulty scaling
            "moneyForAllWave": 200,  # Total money for all waves
            "startMoney": 400,  # Starting money for the mission
        }
        self._robot_settings = {
            "max_cosmetics": 3,
            "max_attributes": 3,
            "max_type_same_class": 4,
            "max_giant": 2,
            "max_chief": 1,
            "chief_begin_at_wave": 0,
            "max_tanks": 1,
            "start_spawn_tank_wave": 3,
            "useTemplate": True,
            "teplate_start_at_wave": 2,
            "banned_classes": []
        }

    def Generate(self):
        WaveManagerGlobal.clearAll()
        
        InitSettingsGlobal.money = self._mission_settings["startMoney"]
        InitSettingsGlobal.setMoney()
        available_paths = [
            {
                "standard_path":    "Path one center side", 
                "tank_paths":       ["boss_path_1"], 
                "robot_tag" :       None, 
                "init_settings" :   "bombpath_set_1_path", 
                "where_spawn" :     ["spawnbot"]
            },
            {
                "standard_path":    "Path on left side", 
                "tank_paths":       ["boss_path_1"], 
                "robot_tag" :       ["path_2", "nav_prefer_flank_left"], 
                "init_settings" :   "bombpath_set_2_path", 
                "where_spawn" :     ["spawnbot"]
            },
            {
                "standard_path":    "Path on right side in house", 
                "tank_paths":       ["boss_path_2"], 
                "robot_tag" :       None, 
                "init_settings" :   "bombpath_set_3_path", 
                "where_spawn" :     ["spawnbot_path_3"]
            },
            {
                "standard_path":    "Path on right side in street", 
                "tank_paths":       ["boss_path_4"], 
                "robot_tag" :       None, 
                "init_settings" :   "bombpath_set_4_path", 
                "where_spawn" :     ["spawnbot_path_3"]
            },
        ]
        
        mission = Mission_Support(
            waves = self._mission_settings["waves"], 
            difficulty = self._mission_settings["difficulty"], 
            progression_factor = self._mission_settings["progressive"], 
            useTemplateBots = self._robot_settings["useTemplate"]
        )

        print(  '[bold yellow] Mission Parameters: [/bold yellow]')
        print(  f'[bold cyan]   Waves: [/bold cyan] [bold green]{self._mission_settings["waves"]}[/bold green]')
        print(  f'[bold red]   Difficulty: [/bold red] [bold yellow]{self._mission_settings["difficulty"]}[bold yellow]')
        print(  f'[bold green]   Progressive: [/bold green]{self._mission_settings["progressive"]}')
        print(  f'[bold blue]   Use Template: [/bold blue]{self._robot_settings["useTemplate"]}')

        for wave_number in range(1, self._mission_settings["waves"] + 1):
            print(f"\n\t[bold yellow]Generated Wave {wave_number}:[/bold yellow]")
            
            selected_path = random.choice(available_paths)
            mission.generate_wave(
                wave_number,
                self._mission_settings["moneyForAllWave"] / self._mission_settings["waves"],
                selected_path,
                self._robot_settings,
            )
            mission.recalculate_squad_attributes(wave_number, self._mission_settings["difficulty"])
        
    def mission_settings(self):
        return self._mission_settings.copy()
    
    def robot_settings(self):
        return self._robot_settings.copy()
    
    def set_mission_settings(self, settings):
        self._mission_settings.update(settings)
    
    def set_robot_settings(self, settings):
        self._robot_settings.update(settings)


class MissionGeneratorWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.generator = RandomWaveGenerator()

        # Импортируем генератор AI в конструкторе
        #from mission_generator_new import generate_mission_using_ai
        #self.generate_mission_json = generate_mission_using_ai
        
        # Список всех доступных путей
        self.available_paths = [
            {
                "name": "Main Path",
                "standard_path": "primary_path",
                "tank_paths": ["tank_path"],
                "robot_tag": None,
                "init_settings": "default_init",
                "where_spawn": ["spawnbot_main"],
            },
            {
                "name": "Flank Path",
                "standard_path": "flanking_path",
                "tank_paths": ["tank_path_alt"],
                "robot_tag": ["flank"],
                "init_settings": "flank_init",
                "where_spawn": ["spawnbot_flank"],
            },
        ]
        self.setupUi()

    def setupUi(self):
        """Настройка пользовательского интерфейса"""
        self.setWindowTitle("Mission Generator")
        self.setObjectName("MissionGenerator")
        self.resize(600, 800)

        # Получаем позицию курсора для отображения окна

        # Центральный виджет
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setStyleSheet("background-color: #252525;")
        self.setCentralWidget(self.centralwidget)

        # Основной layout
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        # === Общий стиль для всех виджетов ===
        self.setStyleSheet(
            """
            QWidget {
                font-family: 'TF2 Build';
                color: white;
                background-color: #454545;
            }
            QLabel {
                font-family: 'TF2 Build';
                color: white;
                padding: 8px;
                border-radius: 5px;
                background-color: #454545;
                font-size: 14px;
            }
            QSpinBox, QDoubleSpinBox, QComboBox, QLineEdit {
                font-family: 'TF2 Secondary';
                background-color: #454545;
                color: white;
                border-radius: 5px;
                padding: 8px;
                min-width: 120px;
                font-size: 14px;
            }
            QSpinBox::up-button, QSpinBox::down-button,
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                background-color: #454545;
                border-radius: 3px;
                color: white;
            }
            QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {
                background-color: white;
                width: 5px;
                height: 5px;
            }
            QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {
                background-color: white;
                width: 5px;
                height: 5px;
            }
            QComboBox::drop-down {
                border: none;
                border-left: 1px solid #353535;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: url(resources/icons/dropdown.png);
                width: 12px;
                height: 12px;
            }
            QCheckBox {
                font-family: 'TF2 Build';
                spacing: 5px;
                color: white;
            }
            QCheckBox::indicator {
                width: 25px;
                height: 25px;
                border-radius: 7px;
                background-color: rgb(89, 89, 89);
            }
            QCheckBox::indicator:checked {
                image: url("resources/Icons/Interface/59508.png");
                background-color: rgb(89, 89, 89);
                border-radius: 7px;
            }
        """
        )

        # === Настройки миссии ===
        self.mission_group = QtWidgets.QGroupBox("Mission Settings", self.centralwidget)
        self.mission_group.setStyleSheet(
            """
            QGroupBox {
                font-family: 'TF2 Build';
                color: white;
                background-color: #303030;
                border-radius: 10px;
                padding: 15px;
            }
        """
        )

        mission_layout = QtWidgets.QFormLayout(self.mission_group)
        mission_layout.setSpacing(10)

        # Создаем спинбоксы для настроек миссии
        self.waves_label = QtWidgets.QLabel("Waves:")
        self.waves_label.setStyleSheet("background-color: #454545;")
        self.waves_spin = self.create_spinbox(1, 100, self.generator.mission_settings()["waves"])
        self.waves_spin.setStyleSheet("background-color: #454545;")
        self.difficulty_label = QtWidgets.QLabel("Difficulty:")
        self.difficulty_label.setStyleSheet("background-color: #454545;")
        self.difficulty_spin = self.create_spinbox(1, 10, self.generator.mission_settings()["difficulty"])
        self.difficulty_spin.setStyleSheet("background-color: #454545;")
        self.progressive_label = QtWidgets.QLabel("Progressive:")
        self.progressive_label.setStyleSheet("background-color: #454545;")
        self.progressive_spin = self.create_double_spinbox(0.01, 5.0, self.generator.mission_settings()["progressive"])
        self.progressive_spin.setStyleSheet("background-color: #454545;")
        self.money_wave_label = QtWidgets.QLabel("Money per Wave:")
        self.money_wave_label.setStyleSheet("background-color: #454545;")
        self.money_wave_spin = self.create_spinbox(1, 100000, self.generator.mission_settings()["moneyForAllWave"])
        self.money_wave_spin.setSingleStep(10)
        self.money_wave_spin.setStyleSheet("background-color: #454545; width: 150px;")
        self.start_money_label = QtWidgets.QLabel("Start Money:")
        self.start_money_label.setStyleSheet("background-color: #454545;")
        self.start_money_spin = self.create_spinbox(1, 100000, self.generator.mission_settings()["startMoney"])
        self.start_money_spin.setSingleStep(10)
        self.start_money_spin.setStyleSheet("background-color: #454545; width: 150px;")

        mission_layout.addRow(self.waves_label, self.waves_spin)
        mission_layout.addRow(self.difficulty_label, self.difficulty_spin)
        mission_layout.addRow(self.progressive_label, self.progressive_spin)
        mission_layout.addRow(self.money_wave_label, self.money_wave_spin)
        mission_layout.addRow(self.start_money_label, self.start_money_spin)

        # === Настройки роботов ===
        self.robot_group = QtWidgets.QGroupBox("Robot Settings", self.centralwidget)
        self.robot_group.setStyleSheet(self.mission_group.styleSheet())

        robot_layout = QtWidgets.QFormLayout(self.robot_group)
        robot_layout.setSpacing(10)

        robot_settings = self.generator.robot_settings()

        # Создаем спинбоксы для настроек роботов
        self.max_cosmetics_label = QtWidgets.QLabel("Max Cosmetics:")
        self.max_cosmetics_label.setStyleSheet("background-color: #454545;")
        self.max_cosmetics_spin = self.create_spinbox(0, 10, robot_settings["max_cosmetics"])
        self.max_cosmetics_spin.setStyleSheet("background-color: #454545;")
        self.max_attributes_label = QtWidgets.QLabel("Max Attributes:")
        self.max_attributes_label.setStyleSheet("background-color: #454545;")
        self.max_attributes_spin = self.create_spinbox(0, 10, robot_settings["max_attributes"])
        self.max_attributes_spin.setStyleSheet("background-color: #454545;")
        self.max_same_class_label = QtWidgets.QLabel("Max Same Class:")
        self.max_same_class_label.setStyleSheet("background-color: #454545;")
        self.max_same_class_spin = self.create_spinbox(1, 10, robot_settings["max_type_same_class"])
        self.max_same_class_spin.setStyleSheet("background-color: #454545;")
        self.max_giant_label = QtWidgets.QLabel("Max Giants:")
        self.max_giant_label.setStyleSheet("background-color: #454545;")
        self.max_giant_spin = self.create_spinbox(0, 10, robot_settings["max_giant"])
        self.max_giant_spin.setStyleSheet("background-color: #454545;")

        robot_layout.addRow(self.max_cosmetics_label, self.max_cosmetics_spin)
        robot_layout.addRow(self.max_attributes_label, self.max_attributes_spin)
        robot_layout.addRow(self.max_same_class_label, self.max_same_class_spin)
        robot_layout.addRow(self.max_giant_label, self.max_giant_spin)

        # Настройки танков
        tank_widget = QtWidgets.QWidget()
        tank_layout = QtWidgets.QHBoxLayout(tank_widget)
        self.max_tanks_spin = self.create_spinbox(0, 5, robot_settings["max_tanks"])
        self.max_tanks_spin.setStyleSheet("background-color: #383838;")
        self.tank_wave_spin = self.create_spinbox(1, 100, robot_settings["start_spawn_tank_wave"])
        self.tank_wave_spin.setStyleSheet("background-color: #383838;")
        tank_layout.addWidget(self.max_tanks_spin)
        wave_label = QtWidgets.QLabel("Start at wave:")
        wave_label.setStyleSheet("background-color: #383838;")
        tank_layout.addWidget(wave_label)
        tank_layout.addWidget(self.tank_wave_spin)
        tank_layout.setSpacing(5)  # Уменьшаем отступы между элементами
        tank_widget.setStyleSheet(
            """
            QWidget {
                font-family: 'TF2 Build';
                color: white;
                background-color: #454545;
                border-radius: 10px;
            }
        """
        )
        self.tank_settings_label = QtWidgets.QLabel("Tank Settings:")
        self.tank_settings_label.setStyleSheet("background-color: #454545;")
        robot_layout.addRow(self.tank_settings_label, tank_widget)

        # Настройки шаблонов
        template_widget = QtWidgets.QWidget()
        template_layout = QtWidgets.QHBoxLayout(template_widget)
        self.use_template_check = QtWidgets.QCheckBox("Use Templates")
        self.use_template_check.setChecked(robot_settings["useTemplate"])
        self.use_template_check.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.use_template_check.setMinimumHeight(30)
        self.template_wave_spin = self.create_spinbox(1, 100, robot_settings["teplate_start_at_wave"])
        self.template_wave_spin.setStyleSheet("background-color: #383838;")
        wave_label = QtWidgets.QLabel("Start at wave:")
        wave_label.setStyleSheet("background-color: #383838;")
        template_layout.addWidget(self.use_template_check)
        template_widget.setStyleSheet(
            """
            QWidget {
                font-family: 'TF2 Build';
                color: white;
                background-color: #454545;
                border-radius: 10px;
            }
        """
        )
        template_layout.addWidget(wave_label)
        template_layout.addWidget(self.template_wave_spin)
        template_layout.setSpacing(5)  # Уменьшаем отступы между элементами
        self.templates_label = QtWidgets.QLabel("Templates:")
        self.templates_label.setStyleSheet("background-color: #454545;")
        robot_layout.addRow(self.templates_label, template_widget)

        # Добавляем группы в основной layout
        self.main_layout.addWidget(self.mission_group)
        self.main_layout.addWidget(self.robot_group)

        # Кнопки
        button_layout = QtWidgets.QHBoxLayout()

        self.generate_button = QtWidgets.QPushButton("Generate Mission")
        self.generate_button.setStyleSheet(
            """
            QPushButton {
                background-color: #009E1A;
                color: white;
                border-radius: 5px;
                padding: 10px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #00B81E;
            }
        """
        )
        self.generate_button.clicked.connect(self.generate_mission)

        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setStyleSheet(
            """
            QPushButton {
                background-color: #B72D2B;
                color: white;
                border-radius: 5px;
                padding: 10px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #D32F2D;
            }
        """
        )
        self.cancel_button.clicked.connect(self.close)

        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.cancel_button)

        self.main_layout.addLayout(button_layout)

        # === Настройки путей ===
        self.paths_tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.paths_tabs.setStyleSheet(
            """
                    QTabWidget {
                        background-color: #454545;
                        border-radius: 5px;
                    }
                    QTabBar::tab {
                        color: white;
                        padding: 10px;
                        border-top-left-radius: 5px;
                        border-top-right-radius: 5px;
                        margin-right: 10px;
                    }
                    QTabBar::tab:selected, QTabBar::tab:hover {
                        background-color: #454545;
                    }
                    QStackedWidget {
                        padding: 10px;
                        background-color: #454545;
                        border-radius: 5px;
                    }
                """
        )
        self.main_layout.addWidget(self.paths_tabs)

        # Вкладка со списком путей
        self.paths_list_widget = QtWidgets.QWidget()
        self.paths_list_widget.setObjectName("paths_list_widget")
        self.paths_list_widget.setStyleSheet(
            """
            QWidget#paths_list_widget {
                background-color: #292929;
                border-radius: 5px;
            }
        """
        )
        self.paths_list_layout = QtWidgets.QVBoxLayout(self.paths_list_widget)

        self.paths_list = QtWidgets.QListWidget(self.paths_list_widget)
        self.paths_list.setStyleSheet(
            """
            QListWidget {
                background-color: #292929;
                color: white;
                border-radius: 5px;
                padding: 5px;
                font-family: 'TF2 Build';
            }
            QListWidget::item {
                padding: 10px;
                margin: 2px;
                border-radius: 5px;
                background-color: #393939;
            }
            QListWidget::item:hover {
                background-color: #404040;
            }
            QListWidget::item:selected {
                background-color: #454545;
                color: white;
            }
        """
        )
        self.paths_list_layout.addWidget(self.paths_list)

        # Кнопки редактирования путей
        self.edit_path_button = QtWidgets.QPushButton("Edit Path")
        self.edit_path_button.setStyleSheet(
            """
            QPushButton {
                background-color: #0078D4;
                color: white;
                border-radius: 5px;
                padding: 10px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #0088E1;
            }
        """
        )
        self.edit_path_button.clicked.connect(self.edit_selected_path)

        self.delete_path_button = QtWidgets.QPushButton("Delete Path")
        self.delete_path_button.setStyleSheet(
            """
            QPushButton {
                background-color: #B72D2B;
                color: white;
                border-radius: 5px;
                padding: 10px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #D32F2D;
            }
        """
        )
        self.delete_path_button.clicked.connect(self.delete_selected_path)

        self.start_new_path_button = QtWidgets.QPushButton("New Path")
        self.start_new_path_button.setStyleSheet(
            """
            QPushButton {
                background-color: #009E1A;
                color: white;
                border-radius: 5px;
                padding: 10px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #00B81E;
            }
        """
        )
        self.start_new_path_button.clicked.connect(self.start_new_path)

        button_layout_paths = QtWidgets.QHBoxLayout()
        button_layout_paths.addWidget(self.start_new_path_button)
        button_layout_paths.addWidget(self.edit_path_button)
        button_layout_paths.addWidget(self.delete_path_button)

        self.paths_list_layout.addLayout(button_layout_paths)

        # Вкладка редактирования пути
        self.path_edit_widget = QtWidgets.QWidget()
        self.path_edit_widget.setObjectName("path_edit_widget")
        self.path_edit_widget.setStyleSheet(
            """
            QWidget {
                background-color: #292929;
            }
            QWidget > QLabel {
                background-color: #292929;
            }
            QLineEdit {
                background-color: #393939;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-family: 'TF2 Secondary';
                min-height: 20px;
            }
            QLineEdit:focus {
                background-color: #404040;
                border: 1px solid #454545;
            }
            QLabel {
                color: white;
                font-family: 'TF2 Build';
                background-color: #292929;
                padding: 5px;
            }
        """
        )
        self.path_edit_layout = QtWidgets.QFormLayout(self.path_edit_widget)
        self.path_edit_layout.setSpacing(10)  # Увеличиваем отступы между полями

        self.path_name_edit = QtWidgets.QLineEdit()
        self.path_standard_edit = QtWidgets.QLineEdit()
        self.path_tank_edit = QtWidgets.QLineEdit()
        self.path_robot_tag_edit = QtWidgets.QLineEdit()
        self.path_init_settings_edit = QtWidgets.QLineEdit()
        self.path_spawn_edit = QtWidgets.QLineEdit()

        self.path_edit_layout.addRow("Path Name:", self.path_name_edit)
        self.path_edit_layout.addRow("Standard Path:", self.path_standard_edit)
        self.path_edit_layout.addRow("Tank Paths:", self.path_tank_edit)
        self.path_edit_layout.addRow("Robot Tag:", self.path_robot_tag_edit)
        self.path_edit_layout.addRow("Init Settings:", self.path_init_settings_edit)
        self.path_edit_layout.addRow("Spawn Points:", self.path_spawn_edit)

        self.save_path_button = QtWidgets.QPushButton("Save Path")
        self.save_path_button.setStyleSheet(
            """
            QPushButton {
                background-color: #009E1A;
                color: white;
                border-radius: 5px;
                padding: 10px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #00B81E;
            }
        """
        )
        self.save_path_button.clicked.connect(self.save_path)

        self.cancel_edit_button = QtWidgets.QPushButton("Cancel")
        self.cancel_edit_button.setStyleSheet(
            """
            QPushButton {
                background-color: #B72D2B;
                color: white;
                border-radius: 5px;
                padding: 10px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #D32F2D;
            }
        """
        )
        self.cancel_edit_button.clicked.connect(self.cancel_edit)

        self.path_edit_layout.addRow(self.save_path_button, self.cancel_edit_button)

        # Добавляем вкладки в QTabWidget
        self.paths_tabs.addTab(self.paths_list_widget, "Paths List")
        self.paths_tabs.addTab(self.path_edit_widget, "Edit Path")

        # Добавляем вкладку AI Generation
        self.ai_generation_widget = QtWidgets.QWidget()
        self.ai_generation_widget.setObjectName("ai_generation_widget")
        self.ai_generation_widget.setStyleSheet(
            """
            QWidget#ai_generation_widget {
                background-color: #292929;
                border-radius: 5px;
            }
            QTextEdit, QPlainTextEdit {
                background-color: #393939;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-family: 'TF2 Secondary';
                font-size: 14px;
            }
            QCheckBox {
                font-family: 'TF2 Secondary';
                color: white;
                spacing: 5px;
            }
            QLabel {
                font-family: 'TF2 Build';
                color: white;
                background-color: #292929;
                padding: 5px;
            }
        """
        )

        ai_layout = QtWidgets.QVBoxLayout(self.ai_generation_widget)

        # Prompt редактор
        prompt_label = QtWidgets.QLabel("Enter your mission prompt:")
        self.prompt_editor = QtWidgets.QPlainTextEdit()
        self.prompt_editor.setMinimumHeight(150)

        # Checkboxes
        self.use_existing_paths = QtWidgets.QCheckBox("Use existing paths from list")
        self.use_existing_paths.setChecked(True)
        self.use_current_settings = QtWidgets.QCheckBox("Use current mission settings")
        self.use_current_settings.setChecked(True)

        # Кнопка генерации
        self.generate_ai_button = QtWidgets.QPushButton("Generate with AI")
        self.generate_ai_button.setStyleSheet(
            """
            QPushButton {
                background-color: #0078D4;
                color: white;
                border-radius: 5px;
                padding: 10px;
                min-width: 100px;
                font-family: 'TF2 Build';
            }
            QPushButton:hover {
                background-color: #0088E1;
            }
        """
        )
        self.generate_ai_button.clicked.connect(self.generate_with_ai)

        # Добавляем все элементы в layout
        ai_layout.addWidget(prompt_label)
        ai_layout.addWidget(self.prompt_editor)
        ai_layout.addWidget(self.use_existing_paths)
        ai_layout.addWidget(self.use_current_settings)
        ai_layout.addWidget(self.generate_ai_button)

        # Добавляем вкладку AI Generation
        #self.paths_tabs.addTab(self.ai_generation_widget, "AI Generation")

        # === Загрузка стандартных путей при старте ===
        self.load_default_paths()

    def create_spinbox(self, minimum: int, maximum: int, value: int) -> QtWidgets.QSpinBox:
        """Создает настроенный QSpinBox с заданными параметрами"""
        spinbox = QtWidgets.QSpinBox()
        spinbox.setMinimum(minimum)
        spinbox.setMaximum(maximum)
        spinbox.setValue(value)
        return spinbox

    def create_double_spinbox(self, minimum: float, maximum: float, value: float) -> QtWidgets.QDoubleSpinBox:
        """Создает настроенный QDoubleSpinBox с заданными параметрами"""
        spinbox = QtWidgets.QDoubleSpinBox()
        spinbox.setMinimum(minimum)
        spinbox.setMaximum(maximum)
        spinbox.setValue(value)
        spinbox.setSingleStep(0.1)
        return spinbox

    def generate_mission(self):
        """Собирает настройки и генерирует миссию"""
        mission_settings = {
            "waves": self.waves_spin.value(),
            "difficulty": self.difficulty_spin.value(),
            "progressive": self.progressive_spin.value(),
            "moneyForAllWave": self.money_wave_spin.value(),
            "startMoney": self.start_money_spin.value(),
        }

        robot_settings = {
            "max_cosmetics": self.max_cosmetics_spin.value(),
            "max_attributes": self.max_attributes_spin.value(),
            "max_type_same_class": self.max_same_class_spin.value(),
            "max_giant": self.max_giant_spin.value(),
            "max_tanks": self.max_tanks_spin.value(),
            "start_spawn_tank_wave": self.tank_wave_spin.value(),
            "useTemplate": self.use_template_check.isChecked(),
            "teplate_start_at_wave": self.template_wave_spin.value(),
            "max_chief": 0,
            "chief_begin_at_wave": 0,
            "banned_classes": [],
        }

        # Применяем настройки к генератору
        self.generator.set_mission_settings(mission_settings)
        self.generator.set_robot_settings(robot_settings)

        # Устанавливаем доступные пути для генератора
        self.generator._available_paths = self.available_paths.copy()

        # Генерируем миссию
        self.generator.Generate()
        self.close()

    def load_default_paths(self):
        """Загрузка стандартных путей Valve"""
        default_paths = [
            {
                "name": "Main Path",
                "standard_path": "primary_path",
                "tank_paths": ["tank_path"],
                "robot_tag": None,
                "init_settings": "default_init",
                "where_spawn": ["spawnbot_main"],
            },
            {
                "name": "Flank Path",
                "standard_path": "flanking_path",
                "tank_paths": ["tank_path_alt"],
                "robot_tag": ["flank"],
                "init_settings": "flank_init",
                "where_spawn": ["spawnbot_flank"],
            },
        ]
        for path in default_paths:
            self.add_path_to_list(path)

    def add_path_to_list(self, path_data):
        """Добавление пути в список"""
        self.available_paths.append(path_data)
        self.paths_list.addItem(path_data["name"])

    def start_new_path(self):
        """Начать создание нового пути"""
        self.paths_tabs.setCurrentIndex(1)  # Переключаемся на вкладку редактирования
        self.clear_path_edit_fields()

    def edit_selected_path(self):
        """Редактирование выбранного пути"""
        if selected_items := self.paths_list.selectedItems():
            index = self.paths_list.row(selected_items[0])
            path_data = self.available_paths[index]

            # Очищаем поля перед заполнением
            self.clear_path_edit_fields()

            # Заполняем актуальными данными
            self.path_name_edit.setText(path_data.get("name", ""))
            self.path_standard_edit.setText(path_data.get("standard_path", ""))
            self.path_tank_edit.setText(", ".join(path_data.get("tank_paths", [])))

            robot_tag = path_data.get("robot_tag", None)
            if isinstance(robot_tag, list):
                self.path_robot_tag_edit.setText(", ".join(robot_tag))

            self.path_init_settings_edit.setText(path_data.get("init_settings", ""))
            self.path_spawn_edit.setText(", ".join(path_data.get("where_spawn", [])))

            # Сохраняем индекс редактируемого пути
            self.editing_path_index = index

            self.paths_tabs.setCurrentIndex(1)

    def delete_selected_path(self):
        """Удаление выбранного пути"""
        if selected_items := self.paths_list.selectedItems():
            index = self.paths_list.row(selected_items[0])
            self.available_paths.pop(index)
            self.paths_list.takeItem(index)

    def save_path(self):
        """Сохранение пути"""
        path_data = {
            "name": self.path_name_edit.text().strip(),
            "standard_path": self.path_standard_edit.text().strip(),
            "tank_paths": [p.strip() for p in self.path_tank_edit.text().split(",") if p.strip()],
            "robot_tag": [t.strip() for t in self.path_robot_tag_edit.text().split(",") if t.strip()] or None,
            "init_settings": self.path_init_settings_edit.text().strip(),
            "where_spawn": [s.strip() for s in self.path_spawn_edit.text().split(",") if s.strip()],
        }

        if hasattr(self, "editing_path_index"):
            # Обновляем существующий путь
            index = self.editing_path_index
            self.available_paths[index] = path_data
            # Обновляем текст в списке, только если элемент существует
            if item := self.paths_list.item(index):
                item.setText(path_data["name"])
            else:
                self.paths_list.addItem(path_data["name"])
            delattr(self, "editing_path_index")
        else:
            # Добавляем новый путь
            self.add_path_to_list(path_data)

        self.paths_tabs.setCurrentIndex(0)  # Возвращаемся к списку
        self.clear_path_edit_fields()

    def cancel_edit(self):
        """Отмена редактирования"""
        self.paths_tabs.setCurrentIndex(0)
        self.clear_path_edit_fields()

    def clear_path_edit_fields(self):
        """Очистка полей редактирования"""
        self.path_name_edit.clear()
        self.path_standard_edit.clear()
        self.path_tank_edit.clear()
        self.path_robot_tag_edit.clear()
        self.path_init_settings_edit.clear()
        self.path_spawn_edit.clear()
        self.paths_list.clearSelection()

    def update_edit_buttons_state(self):
        """Обновление состояния кнопок редактирования"""
        has_selection = bool(self.paths_list.selectedItems())
        self.edit_path_button.setEnabled(has_selection)
        self.delete_path_button.setEnabled(has_selection)

    def generate_with_ai(self):
        """Генерация миссии с помощью AI с учетом настроек пользователя"""
        # Получаем текст промпта
        prompt = self.prompt_editor.toPlainText().strip()
        if not prompt:
            QtWidgets.QMessageBox.warning(
                self, "Предупреждение", 
                "Пожалуйста, введите описание миссии в поле промпта."
            )
            return

        # Собираем настройки из интерфейса
        settings = {
            "waves": self.waves_spin.value(),
            "difficulty": self.difficulty_spin.value(),
            "progressive": self.progressive_spin.value(),
            "money_per_wave": self.money_wave_spin.value(),
            "start_money": self.start_money_spin.value(),
            "max_cosmetics": self.max_cosmetics_spin.value(),
            "max_attributes": self.max_attributes_spin.value(),
            "max_same_class": self.max_same_class_spin.value(),
            "max_giants": self.max_giant_spin.value(),
            "max_tanks": self.max_tanks_spin.value(),
            "tank_start_wave": self.tank_wave_spin.value(),
            "use_templates": self.use_template_check.isChecked(),
            "template_start_wave": self.template_wave_spin.value(),
        }

        # Если указано использовать существующие пути
        if self.use_existing_paths.isChecked():
            settings["paths"] = self.available_paths

        try:
            # Генерируем миссию с помощью AI
            mission_json = self.generate_mission_json(prompt, settings)
            
            # Сохраняем результат в файл
            output_file = "generated_mission.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(mission_json, f, indent=2, ensure_ascii=False)
            
            QtWidgets.QMessageBox.information(
                self, "Успех", 
                f"Миссия успешно сгенерирована и сохранена в {output_file}"
            )
            
            # Закрываем окно
            self.close()
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, "Ошибка", 
                f"Произошла ошибка при генерации миссии:\n{str(e)}"
            )

class General(object):
    global WaveManagerGlobal
    global SquadSettingsGlobal
    global Mercenary_now
    global InitSettingsGlobal
    
    def __init__(self):
        self.buttonsGlobal = {}
        self.FinalCode = ""

    def bindExportButton(self, button):
        button.clicked.connect(self.createWavePop)

    def buttonAdd(self, name, param):
        self.buttonsGlobal[name] = param

    def createMission(self):
        initSettings = InitSettingsGlobal.returnConfiguration()
        return (
            f"""// MVM mission for Team Fortress 2
// Created by Zane Tf2 in program Gray Factory

#base robot_giant.pop
#base robot_standard.pop
#base robot_gatebot.pop

WaveSchedule
{{
    StartingCurrency    {initSettings[0]}
    RespawnWaveTime     {int(self.buttonsGlobal['fixedRespawn_text'].text())}
    CanBotsAttackWhileInSpawnRoom	no
"""
        )

    def createWaveSettings(self, wave):
        settings = wave["Settings"]
        text = "\n    Wave\n    {\n        WaitWhenDone 65\n        Checkpoint Yes\n"

        if settings.get("Description"):
            text += f'Description     "{settings["Description"]}"\n'
        if settings.get("Sound"):
            text += f'Sound   "{settings["Sound"]}"\n'

        for key, output in {"StartWaveOutput": "StartWaveOutput", "InitWaveOutput": "InitWaveOutput", "DoneOutput": "DoneOutput"}.items():
            if len(settings[key].replace("}", "").replace("\n", "")) > 5:
                text += f"\n        {output}\n        {{\n{settings[key].replace('}', '')}\n        }}"

        if settings.get("Custom"):
            text += f"\n{settings['Custom']}"

        return text

    def createSquad(self, squadSettings):
        spawn_positions = {
            0: "spawnbot",
            1: "spawnbot_mission_sniper",
            2: "spawnbot_mission_spy",
        }
        spawnPos = spawn_positions.get(squadSettings['SpawnPostion'], squadSettings['SpawnPostion'])

        conf = (
            f"""
        WaveSpawn
        {{
            Name   "{squadSettings['Name']}"
            TotalCurrency   {squadSettings['Credits For Squad']}
            TotalCount  {squadSettings['Total Squad']}
            MaxActive   {squadSettings['Max Alive Squads']}
            SpawnCount  {squadSettings['Squad Spawn']}
"""
        )

        conf += self.addWaitParams(
            squadSettings.get("Wait For All Spawn"),
            squadSettings.get("Wait For All Dead"),
            squadSettings.get("Wait Spawn Before"),
            squadSettings.get("Wait Spawn Between"),
        )

        conf += f'            Where	"{spawnPos}"\n'
        if squadSettings.get("Squad Is Support"):
            conf += "            Support 1\n"
        if squadSettings.get("Random Choice"):
            conf += "            RandomChoice 1\n"
        if squadSettings.get("Random Spawn"):
            conf += "            RandomSpawn 1\n"
        return conf

    def addWaitParams(self, wait_all_spawn, wait_all_dead, wait_spawn_before, wait_spawn_between):
        conf = ""
        if wait_all_spawn:
            conf += f'            WaitForAllSpawned "{wait_all_spawn}"\n'
        if wait_all_dead:
            conf += f'            WaitForAllDead "{wait_all_dead}"\n'
        if wait_spawn_before:
            conf += f"            WaitBeforeStarting {wait_spawn_before}\n"
        if wait_spawn_between:
            conf += f"            WaitBetweenSpawns {wait_spawn_between}\n"
        return conf
    
    def createMercenary(self, wave):
        Mers = ""
        
        if len(wave["Squad"]) > -1:
            for squad_name, squad_data in wave["Squad"].items():
                if len(squad_data["InSquad"]) > 0:
                    Mers += self.createSquad(squad_data)
                    Mers += "\n            Squad\n            {"
                    
                    for pers in squad_data["InSquad"]:
                        Skill = ["Easy", "Normal", "Hard", "Expert"][pers.stat["Skill"]]
                        WeaponRestrictions = ["All", "PrimaryOnly", "SecondaryOnly", "MeleeOnly"][pers.stat["Weapon Restriction"]]
                        class_names = [
                            "Scout", "Soldier", "Pyro", "Demoman", "HeavyWeapons",
                            "Engineer", "Medic", "Sniper", "Spy", "Tank"
                        ]
                        className = class_names[pers.stat["Class"]]

                        if pers.stat["Class"] == 9 or className == "Tank":
                            Mers += self.generateTank(pers, wave["Squad"][squad_name]["SpawnPostion"])
                        elif pers.stat["Template"]:
                            Mers += self.generateTemplate(pers)
                        else:
                            Mers += self.generateTFBot(pers, Skill, WeaponRestrictions, className)
                    
                    Mers += "\n            }\n        }"
            Mers += "\n    }"
        return Mers
    
    def generateTemplate(self, pers):
        bot = (f"\n                TFBot\n                {{\n                    Template {pers.stat['Template']}\n                ")

        _behavior = ["None", "Push", "Iddler", "Mobber"][pers.stat["Behavior"]]
        if _behavior != "None":
            bot += f"\n				    BehaviorModifiers  {_behavior}"
        
        bot += self.generateTags(pers.stat["Tag"])
        bot += self.generateCharacterAttributes(pers)
        bot += self.generateAttributesGlobal(pers)
        if int(pers.stat["AutoJump Min"]) > -1 or int(pers.stat["AutoJump Max"]) > -1:
            bot += self.autoJump(pers)
        bot += self.generateWeapons(pers)
        bot += self.generateCosmetics(pers.stat["Cosmetics"])
        bot += self.generateCustom(pers)
        bot += "\n                }"
        return bot
    
    def generateTFBot(self, pers : Mercenary, Skill, WeaponRestrictions, className):
        bot = (
            f"""
                TFBot
                {{
                    Name    "{pers.stat['Name']}"
                    ClassIcon  {pers.stat['Icon']}
                    Health  {pers.stat['Health']}
                    Class  {className}
                    Skill  {Skill}
                    Scale   {pers.stat['Scale']}
            """
        )
        if WeaponRestrictions != "All":
            bot += f"\n				    WeaponRestrictions  {WeaponRestrictions}"

        _behavior = ["None", "Push", "Iddler", "Mobber"][pers.stat["Behavior"]]
        if _behavior != "None":
            bot += f"\n				    BehaviorModifiers  {_behavior}"
        
        bot += self.generateTags(pers.stat["Tag"])
        bot += self.generateCharacterAttributes(pers)
        bot += self.generateAttributesGlobal(pers)
        if int(pers.stat["AutoJump Min"]) > -1 or int(pers.stat["AutoJump Max"]) > -1:
            bot += self.autoJump(pers)
        bot += self.generateWeapons(pers)
        bot += self.generateCosmetics(pers.stat["Cosmetics"])
        bot += self.generateCustom(pers)
        bot += "\n                }"
        return bot
    
    def autoJump(self, pers):
        return f"""
                    AutoJumpMin {pers.stat['AutoJump Min']}
                    AutoJumpMax {pers.stat['AutoJump Max']}
                    """

    def generateCustom(self, pers : Mercenary):
        return "".join(f'\n{pers.stat["Custom Parametrs"]}')
    
    def generateTank(self, pers, spawn_position):
        return (
            f"""
                Tank
                {{
                    Health  {pers.stat['Health']}
                    Speed   65
                    StartingPathTrackNode {spawn_position}
                    OnKilledOutput
                    {{
                        Target	boss_dead_relay
                        Action	Trigger
                    }}
                    OnBombDroppedOutput
                    {{
                        Target	boss_deploy_relay
                        Action	Trigger
                    }}
                }}
            """
        )

    def generateTags(self, tags):
        return "".join(f'\n                    Tag   "{tag}"' for tag in tags)

    def generateCharacterAttributes(self, pers):
        """
        Генерирует текстовый блок для CharacterAttributes в формате:
        CharacterAttributes
        {
            "name"    value
        }
        """
        attributes = ""

        if "CharacterAttributes" in pers.stat and len(pers.stat["CharacterAttributes"]) > 0:
            attributes += "\n                    CharacterAttributes"
            attributes += "\n                    {"
            
            for key, attribute in pers.stat["CharacterAttributes"].items():
                # Проверяем, что атрибут имеет ключи "Name" и "Value"
                if isinstance(attribute, dict) and "Name" in attribute and "Value" in attribute:
                    name = attribute["Name"]
                    value = attribute["Value"]
                    attributes += f'\n                        "{name}"    {value}'
                else:
                    print(f"Unexpected attribute structure for key '{key}': {attribute}")

            attributes += "\n                    }"

        return attributes
    
    def generateAttributesGlobal(self, pers):
        attributes = ""

        if "Attributes" in pers.stat:
            if isinstance(pers.stat["Attributes"], dict):
                for attribute in pers.stat["Attributes"]:
                    attributes += f'\n                    Attributes    {attribute}'
            elif isinstance(pers.stat["Attributes"], list):
                for attribute in pers.stat["Attributes"]:
                    print(attribute)
                    attributes += f'\n                    Attributes    {attribute}'
            else:
                print(f"Unexpected Attributes structure: {pers.stat['Attributes']}")
        return attributes
    
    def generateWeapons(self, pers):
        weapons = [pers.stat["Primary Weapon"], pers.stat["Secondary Weapons"], pers.stat["Melee"]]
        weapons_data = ""
        
        #if len(pers.stat["Template"]) > 0:
        #    return weapons_data
        
        for weapon in weapons:
            if not weapon:  # Пропускаем, если оружие отсутствует
                continue

            item_name = weapon.get().get("Name", "Unknown Weapon")
            attributes = weapon.get().get("Attributes", {})
            custom = weapon.get().get("Custom", {})
            weapons_data += f'\n                    Item    "{item_name}"'

            if attributes or len(custom) > 0:
                # Формируем блок ItemAttributes
                weapons_data += "\n                    ItemAttributes"
                weapons_data += "\n                    {"
                weapons_data += f'\n                        ItemName        "{item_name}"'
                
                if len(custom) > 0:  # Проверяем наличие пользовательских данных
                    weapons_data += f"\n{custom}\n"
                
                # Обработка списка атрибутов
                if isinstance(attributes, list):
                    for item in attributes:
                        if isinstance(item, dict) and "Name" in item and "Value" in item:
                            weapons_data += f'\n                        "{item["Name"]}"    {str(item["Value"]).replace(",", ".")}'
                        else:
                            print(f"Unexpected item structure in list: {item}")

                # Обработка словаря атрибутов
                elif isinstance(attributes, dict):
                    for key, attr in attributes.items():
                        if isinstance(attr, dict) and "Name" in attr and "Value" in attr:
                            weapons_data += f'\n                        "{attr["Name"]}"    {str(attr["Value"]).replace(",", ".")}'
                        else:
                            print(f"Unexpected attribute structure in dict: {attr}")
                weapons_data += "\n                    }"

        return weapons_data


    def generateCosmetics(self, cosmetics):
        allText = ""
        for cosmetic in cosmetics:
            item = parser.get_item_by_key(cosmetic)
            allText += f'\n                    Item "{item["name"]}"'
            
        return allText

    def createWavePop(self):
        SquadSettingsGlobal.clearSquad()
                
        self.FinalCode = self.createMission()

        for wave in WaveManagerGlobal.waveList.values():
            self.FinalCode += self.createWaveSettings(wave)
            self.FinalCode += self.createMercenary(wave)
        self.FinalCode += '\n}'
        # Генерация имени миссии
        mission_name = self.buttonsGlobal['mapName_text'].text()
        mission_suffix = self.buttonsGlobal['MissionName_text'].text()
        if mission_suffix:
            mission_name += f"_{mission_suffix}"

        # Диалог для сохранения файла
        Tk().withdraw()
        file_dialog = fd.asksaveasfile(
            title="Export Project",
            filetypes=[('PopFile Project', '*.pop')],
            initialfile=mission_name
        )
        Tk().destroy()

        # Проверка, если файл выбран
        if not file_dialog or not file_dialog.name:
            return

        # Сохранение содержимого в файл
        with open(f'{file_dialog.name.replace(".pop", "")}.pop', "w") as file:
            file.write(self.FinalCode)

class Button_Weapon_Atribute:
    global Mercenary_now
    def __init__(self, stat : WeaponData, index):
        self.stat = stat
        self.index = index
        
    def get(self, *arg):
        Mercenary_now.change_first_weapon_def(self.stat, gunIndex = self.index)
        
        global Addition_interface
        Addition_interface.close()
        Addition_interface = None
        
class Button_Cosmetic_Atribute:
    global Mercenary_now
    def __init__(self, stat):
        self.stat = stat
        
    def get(self, *arg):
        global cosmetic_list_class
        if self.stat is not None:
            Mercenary_now.stat["Cosmetics"].append(self.stat["index_item"])
            cosmetic_list_class.AddCosmeticsFromList(self.stat)
            
        # Закрываем окно выбора
        #global Addition_interface
        #if Addition_interface is not None:
        #    Addition_interface.close()
        #    Addition_interface = None

def Create_Mercenary_From_Save(list : dict, squadName, isGenerated = False):
    exemplar  = Mercenary(squadName)
    component = _AddButtonInWaveList.AddButton(exemplar)
    if component == False:
        return
    exemplar.setNewButtons(component)
    
    if isGenerated == False:
        exemplar.Set_Stat_from_Save(list)
    else:
        exemplar.Set_Stat(list)
    
    Button = component["Button"]
    Button.clicked.connect(lambda x: (Select_Mercenary(exemplar,component)) )
    Button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    Button.setMouseTracking(True)
    Button.click()
    listButtonForMercenary.append(component["Button"])
    return exemplar

def Adding_New_Mercenary_To_Wave(exemplar : Mercenary = None, isGenerate = False):
    global SquadSettingsGlobal
    global Mercenary_now
    
    if Mercenary_now != None:
        Mercenary_now.save()

    if exemplar == None or isGenerate or len(SquadSettingsGlobal.SquadList) <= 0:
        Mercenary_now = None
        nameSquad = SquadSettingsGlobal.CreateSquad()
        exemplar  = Mercenary(nameSquad)
        component = _AddButtonInWaveList.AddButton(exemplar)
        
        if component != False:
            exemplar.setNewButtons(component)

    else:
        stats = exemplar.stat
        component = _AddButtonInWaveList.AddButton(exemplar, title=stats["Name"], iconName=stats["Icon"])
        if component != False:
            exemplar.setNewButtons(component)
        else:
            return

    listButtonForMercenary.append(component["Button"])
    
    Button = component["Button"]
    Button.clicked.connect(lambda x: (Select_Mercenary(exemplar, component)) )
    Button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    Button.setMouseTracking(True)
    Button.click()
    
    return exemplar

def Select_Mercenary(mercenary : Mercenary, components = None):
    global Mercenary_now
    global SquadSettingsGlobal
    
    if Mercenary_now != None:
        Mercenary_now.save()
        
    if mercenary != Mercenary_now:
        if Mercenary_now != None:
            Mercenary_now.update_squad_icon()
            
        Mercenary_now = mercenary
        
        if components != None:
            Mercenary_now.setNewButtons(components)
        Mercenary_now.open()

def open_weapon(*arg, type = "Primary"):
    global Mercenary_now
    if Mercenary_now == None:
        return
    global type_now_weapon
    global Addition_interface

    if Addition_interface == None:
        type_now_weapon = type
        Ui_GroupBox().setupUi()
        _tile  = Tile()
        _stat = weapons_libary.Weapon_Libary[Mercenary_now.stat["Class Name"]][type]
        _tile.firstStat = _stat
        _tile.AddButton(items=_stat, index=type)
        
    elif type != type_now_weapon:
        Addition_interface.close()
        Addition_interface = None
        
        type_now_weapon = type
        Ui_GroupBox().setupUi()
        _tile  = Tile()
        _stat = weapons_libary.Weapon_Libary[Mercenary_now.stat["Class Name"]][type]
        _tile.firstStat = _stat
        _tile.AddButton(items=_stat, index=type)
    else:
        Addition_interface.close()
        Addition_interface = None
        type_now_weapon = None

def open_addition_panel(stat):
    Ui_GroupBox().setupUi(stat)
    Tile().AddButton(items = stat, index = -1)

def get_icon_from_game(iconKey : int) -> str:
    item = parser.get_item_by_key(iconKey)
    
    if item is None:
        item = parser.get_item_by_name(iconKey)
        if item:
            item = item[1]
        else:
            print(f"Item with key '{iconKey}' not found.")
            return None
    try:
        item_ico = parser.get_param_inChaos(item, "image_inventory")
                
        if len(item_ico) > 0:
            item_icon_path = f"materials/{item_ico['end']}.vtf"
        else:
            name = item.get("name", "unknown_item").replace(" ", "_").lower()
            item_icon_path = f"materials/backpack/weapons/w_models/w_{name}.vtf"

        if item_icon_path is None:
            print(f"Image URL not found for icon key '{iconKey}'")
            return None
        
        try:
            pakfile = vpk_file_texture.get_file(item_icon_path)
        except:
            try:
                item_icon_path = f"materials/backpack/weapons/c_models/c_{name}.vtf"
                pakfile = vpk_file_texture.get_file(item_icon_path)
            except:
                return None
            
        temp_path = Path(f"{resources()}/resources/temp")

        temp_vtf = f"{temp_path}/temp.vtf"
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
            
        pakfile.save(temp_vtf)
        
        vtf_parser = vtf2img_parser.Parser(temp_vtf)
        image = vtf_parser.get_image()
        
        name_image_file_clear = iconKey.replace("'", "")
        image_name = f'{temp_path}/{name_image_file_clear}.png'
        image.save(image_name)
        
        if os.path.exists(image_name):
            return str(image_name).replace("\\", "/")
        else:
            return None
        
    except AttributeError as e:
        print(f"Image URL not found for icon key '{iconKey}': {e}")
        return None
    
def close_app():
    """Закрытие приложения и очистка временных файлов"""
    if Addition_interface is not None:
        Addition_interface.close()
    temp = Path(f"{resources()}/resources/temp")
    if temp.exists():
        shutil.rmtree(temp)
        
colorQuality = {
    "Unique" :      "217, 210, 41",
    "Normal" :      "178, 178, 178",
    "Genuine" :     "77, 116, 85",
    "Vintage" :     "71, 98, 145",
    "Unusual" :     "134, 80, 172",
    "Strange" :     "207, 106, 50",
    "Collector" :   "170, 0, 0",
    "Haunted" :     "56, 243, 171",
    "Decorated" :   "250, 250, 250",
    "Community" :   "112, 176, 74",
    "Valve" :       "165, 15, 121",
}


# === Глобальные менеджеры и основные объекты приложения ===
generalGlobal = General()
SaveManagerGlobal = SaveManager()
InitSettingsGlobal = InitialSettings()
WaveManagerGlobal = WaveManager()
CustomAtributeGlobal = CustomAtributes()

# === Переменные для управления интерфейсом и состоянием ===
buttonMercenaryActive = None
started_click = False
SquadSettingsGlobal = None

ModelViewRuntime = None
mainWin = None
selfMainWin = None
TileGlobal = None
Addition_interface = None

# === Переменные для хранения данных и глобальных списков ===
Global_Components = {}
Atribute_global = None
cosmetic_list_class = None
type_now_weapon = None
_AddButtonInWaveList = None
General_Information_Robot = {}
AnchorModel = None

# === Переменные для работы с файлами и проектом ===
project_file = None
path_project_file = None

# === Переменные для текущего состояния и выбора ===
listButtonForMercenary = []
Mercenary_now = None
CurrentWave = None


def load_or_create_config(config_path: Path) -> dict:
    """
    Загружает конфигурацию из файла или создает новую, если файл не существует
    или не содержит необходимых данных.
    
    Args:
        config_path: Путь к файлу конфигурации
        
    Returns:
        dict: Словарь с конфигурацией
    """
    config = {}
    
    # Создаем директорию для конфига, если она не существует
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Пытаемся загрузить существующий конфиг
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as config_file:
                config = json.load(config_file)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка чтения конфигурации: {e}")
            config = {}
    
    return config


def get_game_folder(icon_path: Path = None) -> Path:
    """
    Открывает диалог выбора папки игры и проверяет корректность выбора.
    
    Args:
        icon_path: Путь к иконке для диалогового окна
        
    Returns:
        Path: Путь к папке игры или None, если выбор отменен
    """
    root = Tk()
    root.title('Select Game Folder')
    
    # Устанавливаем иконку, если путь предоставлен и файл существует
    if icon_path and icon_path.exists():
        try:
            root.iconbitmap(icon_path)
        except Exception:
            pass  # Игнорируем ошибки с иконкой
    
    root.withdraw()  # Скрываем главное окно
    
    try:
        selected_path = filedialog.askdirectory(title='Select Game Folder')
        
        if not selected_path:  # Пользователь отменил выбор
            return None
            
        game_path = Path(selected_path)
        
        # Проверяем, что выбранная папка существует, является директорией и называется "tf"
        if game_path.exists() and game_path.is_dir() and game_path.name == "tf":
            return game_path
        else:
            messagebox.showerror(
                "Error", 
                "Selected folder must be named 'tf' and exist on disk."
            )
            return None
            
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred when selecting the folder: {e}")
        return None
    finally:
        root.destroy()


def save_config(config_path: Path, config: dict) -> bool:
    """
    Сохраняет конфигурацию в файл.
    
    Args:
        config_path: Путь к файлу конфигурации
        config: Словарь с конфигурацией
        
    Returns:
        bool: True, если сохранение прошло успешно
    """
    try:
        with open(config_path, 'w', encoding='utf-8') as config_file:
            json.dump(config, config_file, indent=4, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Ошибка сохранения конфигурации: {e}")
        return False


def get_game_path(resources_func) -> Path:
    """
    Основная функция для получения пути к игре из конфигурации или через диалог выбора.
    
    Args:
        resources_func: Функция, возвращающая путь к ресурсам
        
    Returns:
        Path: Путь к папке игры
    """
    config_path = Path(resources_func()) / "resources" / "config.json"
    icon_path = Path(resources_func()) / "resources" / "Icons" / "icon" / "icon_gray_factory.png"
    
    # Загружаем конфигурацию
    config = load_or_create_config(config_path)
    
    # Проверяем, есть ли уже сохраненный путь к игре
    if config.get("game_path"):
        game_path = Path(config["game_path"])
        # Проверяем, что сохраненный путь все еще существует
        if game_path.exists() and game_path.is_dir():
            return game_path
        else:
            print("Сохраненный путь к игре не существует, требуется выбрать новый.")
    
    # Если пути нет или он недействителен, запрашиваем новый
    while True:
        game_path = get_game_folder(icon_path)
        
        if game_path is None:
            # Пользователь отменил выбор
            raise SystemExit("Выбор папки игры отменен пользователем.")
        
        # Сохраняем новый путь в конфигурацию
        config["game_path"] = str(game_path)
        if save_config(config_path, config):
            print(f"Путь к игре сохранен: {game_path}")
            return game_path
        else:
            print("Ошибка сохранения конфигурации, попробуйте еще раз.")

GamePath = get_game_path(resources)

items_file = Path(os.path.join(f"{GamePath}/scripts/items", 'items_game.txt'))
vpk_file = f"{GamePath}/tf2_textures_dir.vpk"
vpk_file_texture = vpk.open(vpk_file)

if items_file is not None:
    try:
        parser = TF2ItemsParser(items_file)
        parser.load()
        #all_game_items = parser.get_all_items()
        #print(f"\nTotal items loaded: {len(all_game_items)}")
        
    except ImportError as e:
        print(f"Ошибка импорта: {e}")
        sys.exit(1)
else:
    print(f"Файл items_game.txt не найден по пути: {items_file}")
    sys.exit(1)

if __name__ == "__main__":
    app = Ui_MainWindow()

    if Addition_interface is not None:
        Addition_interface.close()
        
    app.app.aboutToQuit.connect(close_app)
    
    sys.exit(app.app.exec())
