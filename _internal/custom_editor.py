# pop_editor_with_update.py

import os
import requests
from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QApplication,
    QListWidget,
    QMessageBox,
    QHBoxLayout,
    QPushButton
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.Qsci import (
    QsciScintilla,
    QsciLexerCustom,
    QsciAPIs
)
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtWidgets import QPlainTextEdit
import re
# Попробуем использовать json5 для более толерантного парсинга сниппетов
import json
try:
    import json5 as json_parser  # pip install json5
except ImportError:
    import json as json_parser

def set_dark_palette(app):
    """Устанавливает темную тему для всего приложения"""
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#1e1e1e"))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Base, QColor("#1e1e1e"))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#23272e"))
    palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Button, QColor("#23272e"))
    palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    palette.setColor(QPalette.ColorRole.Link, QColor("#3794ff"))
    palette.setColor(QPalette.ColorRole.Highlight, QColor("#264F78"))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
    app.setPalette(palette)

def download_latest_snippets(github_path="snippets/popfile.json", gitlab_path="snippets/popfile.tmLanguage.json"):
    """
    Скачивает сниппеты GitHub и синтаксис из GitLab.
    """
    RAW_URL = (
        "https://raw.githubusercontent.com/"
        "xyantoaster/xyantoaster-popfile-snippets/"
        "main/snippets/popfile.json"
    )
    GITLAB_URL = (
        "https://gitlab.com/Swordstone/popfile-language-support-vscode/-/raw/master/syntaxes/popfile.tmLanguage.json"
    )
    # GitHub
    github_snippets = {}
    try:
        resp = requests.get(RAW_URL, timeout=10)
        resp.raise_for_status()
        main_snip = resp.content
        main_snip_str = main_snip.decode("utf-8")
        github_snippets = json_parser.loads(main_snip_str)
    except Exception as e:
        print(f"Ошибка загрузки или парсинга github snippets: {e}")
    # GitLab
    gitlab_snippets = {}
    try:
        resp2 = requests.get(GITLAB_URL, timeout=10)
        resp2.raise_for_status()
        gitlab_json = resp2.json()
        repo = gitlab_json.get("repository", {})
        for k, v in repo.items():
            gitlab_snippets[k] = {
                "prefix": k,
                "body": v.get("patterns", []) if isinstance(v.get("patterns"), list) else [],
                "description": v.get("name", "")
            }
    except Exception as e:
        print(f"Ошибка загрузки или парсинга gitlab snippets: {e}")
    # Сохраняем отдельно
    os.makedirs(os.path.dirname(github_path), exist_ok=True)
    with open(github_path, "w", encoding="utf-8") as f:
        json.dump(github_snippets, f, ensure_ascii=False, indent=2)
    with open(gitlab_path, "w", encoding="utf-8") as f:
        json.dump(gitlab_snippets, f, ensure_ascii=False, indent=2)
    print(f"GitHub snippets: {github_path}\nGitLab snippets: {gitlab_path}")
    return True


def load_snippets(path):
    """
    Пытаемся загрузить сниппеты через json5 (если установлен), иначе — через стандартный json.
    """
    with open(path, encoding="utf-8") as f:
        return json_parser.load(f)


class PopLexer(QsciLexerCustom):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Определяем стили
        self._styles = {
            'Default': 0,
            'Section': 1,
            'Key': 2,
            'Value': 3,
            'Number': 4,
            'Boolean': 5,
            'String': 6,
            'Comment': 7,
            'Keyword': 8,
            'Operator': 9,
            'Identifier': 10
        }
        
        # Базовые ключевые слова
        self._keywords = {
            'WaveSpawn', 'StartWave', 'EndWave', 'TotalCurrency', 'Support', 
            'Tank', 'Action', 'Squad', 'TFBot', 'Class', 'Skill', 'Where',
            'TotalCount', 'MaxActive', 'SpawnCount', 'WaitBeforeStarting', 
            'WaitBetweenSpawns'
        }
        
        # Загружаем синтаксис из JSON
        self._syntax_rules = self._load_syntax_rules()
        
        # Кэш для токенов
        self._token_cache = {}
        
        # Настройка цветов (сохраняем существующую цветовую схему)
        self.setColor(QColor('#569CD6'), self._styles['Section'])
        self.setColor(QColor("#36BCB0"), self._styles['Key'])
        self.setColor(QColor("#B5CEA8"), self._styles['Value'])
        self.setColor(QColor('#A7CE89'), self._styles['Number'])
        self.setColor(QColor('#4EC9B0'), self._styles['Boolean'])
        self.setColor(QColor('#CE9178'), self._styles['String'])
        self.setColor(QColor('#6A9955'), self._styles['Comment'])
        self.setColor(QColor('#C586C0'), self._styles['Keyword'])
        self.setColor(QColor('#9CDCFE'), self._styles['Identifier'])
        self.setColor(QColor('#D4D4D4'), self._styles['Default'])
        
        # Установка шрифта
        font = QFont('Consolas', 11)
        for style in self._styles.values():
            self.setFont(font, style)
    
    def _load_syntax_rules(self):
        """Загрузка правил синтаксиса из JSON файла"""
        try:
            with open("snippets/popfile.tmLanguage.json", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("patterns", [])
        except Exception as e:
            print(f"Ошибка загрузки правил синтаксиса: {e}")
            return []

    def get_autocomplete_keywords(self):
        """Возвращает все ключевые слова для автодополнения"""
        # Начинаем с базового набора ключевых слов
        keywords = set(self._keywords)
        
        # Добавляем ключевые слова из правил синтаксиса
        if hasattr(self, '_syntax_rules') and self._syntax_rules:
            try:
                # Извлекаем ключевые слова из patterns в правилах
                for rule in self._syntax_rules:
                    if 'match' in rule:
                        # Извлекаем слова из match-паттернов, убирая спецсимволы
                        pattern = rule['match']
                        # Убираем regex-символы и получаем чистые слова
                        clean_words = re.findall(r'\b\w+\b', pattern)
                        keywords.update(clean_words)
            except Exception as e:
                print(f"Ошибка при извлечении ключевых слов из синтаксиса: {e}")
        
        return keywords

    def language(self):
        return "POP"

    def description(self, style):
        """Возвращает описание стиля"""
        matching_styles = [name for name, s in self._styles.items() if s == style]
        return matching_styles[0] if matching_styles else 'Default'
    
    def _get_token_type(self, text):
        """Определяет тип токена на основе правил синтаксиса"""
        # Кэширование для производительности
        if text in self._token_cache:
            return self._token_cache[text]
            
        # Базовые правила
        if text.startswith('//'):
            token_type = 'Comment'
        elif text.startswith('"') and text.endswith('"'):
            token_type = 'String'
        elif text.lower() in ['true', 'false']:
            token_type = 'Boolean'
        elif text.isdigit() or (text.startswith('-') and text[1:].isdigit()):
            token_type = 'Number'
        elif text in ['WaveSpawn', 'StartWave', 'EndWave', 'TotalCurrency', 'Support', 'Tank', 'Action', 'Squad']:
            token_type = 'Keyword'
        elif text in ['{', '}', '[', ']', '(', ')', '=', ',', ':']:
            token_type = 'Operator'
        else:
            # Проверка по правилам из JSON
            token_type = 'Default'
            for rule in self._syntax_rules:
                if 'match' in rule and re.match(rule['match'], text):
                    token_type = rule.get('name', 'Default').split('.')[-1]
                    break
        
        self._token_cache[text] = token_type
        return token_type

    def styleText(self, start, end):
        """Применение стилей к тексту"""
        editor = self.editor()
        if not editor:
            return
            
        text = editor.text()[start:end]
        if not text:
            return
            
        self.startStyling(start)
        
        # Токенизация и стилизация
        tokens = self._tokenize(text)
        
        for token, length in tokens:
            style = self._styles.get(self._get_token_type(token), self._styles['Default'])
            self.setStyling(length, style)
    
    def _tokenize(self, text):
        """Разбивает текст на токены"""
        tokens = []
        current_token = ''
        i = 0
        
        while i < len(text):
            char = text[i]
            
            # Обработка комментариев
            if char == '/' and i + 1 < len(text) and text[i + 1] == '/':
                end = text.find('\n', i)
                if end == -1:
                    end = len(text)
                tokens.append((text[i:end], end - i))
                i = end
                continue
                
            # Обработка строк
            if char == '"':
                end = i + 1
                while end < len(text):
                    if text[end] == '"' and text[end - 1] != '\\':
                        end += 1
                        break
                    end += 1
                tokens.append((text[i:end], end - i))
                i = end
                continue
                
            # Обработка специальных символов
            if char in '{}[]()=,:':
                if current_token:
                    tokens.append((current_token, len(current_token)))
                    current_token = ''
                tokens.append((char, 1))
                i += 1
                continue
                
            # Обработка пробельных символов
            if char.isspace():
                if current_token:
                    tokens.append((current_token, len(current_token)))
                    current_token = ''
                tokens.append((char, 1))
                i += 1
                continue
                
            current_token += char
            i += 1
            
        if current_token:
            tokens.append((current_token, len(current_token)))
            
        return tokens
        


from PyQt6.QtWidgets import QMessageBox, QTextEdit
import random


# Новый менеджер: два источника
class SnippetManager:
    def __init__(self, github_file):
        self.snippets_github = {}
        self.snippet_bodies_github = {}
        self.load_snippets(github_file)
    
    def load_snippets(self, github_path):
        try:
            self.snippets_github = load_snippets(github_path)
        except Exception as e:
            QMessageBox.critical(None, "Ошибка загрузки GitHub-сниппетов", f"{e}")
            self.snippets_github = {}
        self.snippet_bodies_github = {}
        for name, entry in self.snippets_github.items():
            prefix = entry.get("prefix")
            body = entry.get("body", [])
            display_name = name
            if isinstance(prefix, list):
                for p in prefix:
                    self.snippet_bodies_github[display_name] = (body, p)
            else:
                self.snippet_bodies_github[display_name] = (body, prefix)


    def get_filtered(self, prefix):
        prefix = prefix.lower()
        return [name for name, (body, pfx) in self.snippet_bodies_github.items()
                if str(pfx).lower().startswith(prefix) or name.lower().startswith(prefix)]

    def get_body(self, name):
        return self.snippet_bodies_github.get(name, ([], ''))[0]

    def get_prefix(self, name):
        return self.snippet_bodies_github.get(name, ([], ''))[1]

    def render_snippet(self, body):
        import re
        rendered = []
        for line in body:
            if not isinstance(line, str):
                line = str(line)
            def repl(m):
                val = m.group(1)
                if ',' in val:
                    options = [v.strip() for v in val.split(',')]
                    return random.choice(options)
                return val
            rendered.append(re.sub(r'\$\{\d+:(.+?)\}', repl, line))
        return rendered

# Класс отдельного окна редактора
class PopEditorWindow(QWidget):  # Используем QWidget как базовый класс
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gray Factory — POP Editor")
        
        # Применяем темную тему для всего приложения
        app = QApplication.instance()
        if app:
            set_dark_palette(app)
        
        # Включаем масштабируемость окна
        self.setMinimumSize(600, 400)  # Минимальный размер окна
        
        # Инициализируем базовые атрибуты
        self.apis = None
        self.snippet_manager = None
        self.gitlab_snippets = {}
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Устанавливаем тёмную тему для всего окна
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #d4d4d4;
            }
        """)
        
        # Инициализируем компоненты
        self.setup_editor()
        
        # Создаём простой SnippetManager без загрузки файла
        self.snippet_manager = SnippetManager.__new__(SnippetManager)
        self.snippet_manager.snippets_github = {}
        self.snippet_manager.snippet_bodies_github = {}
        
        # Откладываем загрузку сниппетов
        QTimer.singleShot(50, self.load_snippets)  # 50ms задержка для быстрого запуска
    
    def load_snippets(self):
        """Асинхронная загрузка сниппетов"""
        try:
            # Проверяем существование файла перед загрузкой
            github_path = "snippets/popfile_github.code-snippets"
            if os.path.exists(github_path):
                print(f"Загружаем сниппеты из {github_path}")
                self.snippet_manager = SnippetManager(github_path)
                print(f"Загружено сниппетов: {len(self.snippet_manager.snippets_github)}")
            else:
                print(f"Файл сниппетов не найден: {github_path}")
                # Создаем директорию если её нет
                os.makedirs(os.path.dirname(github_path), exist_ok=True)
                
            try:
                gitlab_path = "snippets/popfile_gitlab.code-snippets"
                if os.path.exists(gitlab_path):
                    print(f"Загружаем GitLab сниппеты из {gitlab_path}")
                    self.gitlab_snippets = load_snippets(gitlab_path)
                    print(f"Загружено GitLab сниппетов: {len(self.gitlab_snippets)}")
            except Exception as e:
                print(f"Ошибка загрузки GitLab сниппетов: {e}")
                self.gitlab_snippets = {}
                
            # Обновляем API после загрузки сниппетов
            print("Обновляем API...")
            self.update_apis()
            print("API обновлено")
                
            # Пробуем обновить в фоне
            QTimer.singleShot(200, self.update_snippets)
        except Exception as e:
            print(f"Ошибка загрузки сниппетов: {e}")
            
    def update_apis(self):
        """Обновляем API после загрузки сниппетов"""
        try:
            # Проверяем что у нас есть все необходимые объекты
            if not hasattr(self, 'editor') or not hasattr(self, 'snippet_manager'):
                return
                
            # Создаём новый API объект
            if self.editor and self.editor.lexer():
                self.apis = QsciAPIs(self.editor.lexer())
            else:
                return
                
            # Добавляем сниппеты если они есть
            if (self.snippet_manager and hasattr(self.snippet_manager, 'snippet_bodies_github') 
                and self.snippet_manager.snippet_bodies_github):
                for name, (body, prefix) in self.snippet_manager.snippet_bodies_github.items():
                    if isinstance(prefix, list):
                        for p in prefix:
                            if p:  # Проверяем что префикс не пустой
                                self.apis.add(str(p))
                    else:
                        if prefix:  # Проверяем что префикс не пустой
                            self.apis.add(str(prefix))
                            
            # Подготавливаем API
            if self.apis:
                self.apis.prepare()
        except Exception as e:
            print(f"Ошибка обновления API: {e}")
            
    def update_snippets(self):
        """Фоновое обновление сниппетов"""
        try:
            # Скачиваем актуальные файлы
            download_latest_snippets(
                "snippets/popfile.json",
                "snippets/popfile.tmLanguage.json"
            )
            # Перезагружаем после обновления
            self.snippet_manager = SnippetManager("snippets/popfile.json")
            # Обновляем API
            self.update_apis()
            # Перезагружаем подсветку синтаксиса
            self.reload_syntax_highlighting()
            print("Сниппеты и синтаксис успешно обновлены")
        except Exception as e:
            print(f"Ошибка обновления сниппетов: {e}")
            
    def setup_editor(self):
        """Настройка редактора и его компонентов"""
        # Создаем главный layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Создаем редактор
        self.editor = QsciScintilla()
        self.editor.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Создаем error_panel
        self.error_panel = QPlainTextEdit()
        self.error_panel.setReadOnly(True)
        self.error_panel.setMaximumHeight(100)
        self.error_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.error_panel.hide()
        
        # Добавляем виджеты в layout
        main_layout.addWidget(self.editor, stretch=1)
        main_layout.addWidget(self.error_panel)
        
        # Настраиваем внешний вид редактора
        self.editor.setUtf8(True)
        self.editor.setFont(QFont('Consolas', 10))
        
        # Устанавливаем темную тему для всего редактора (используем цвета из глобальной темы)
        app = QApplication.instance()
        palette = app.palette() if app else QPalette()
        
        bg_color = palette.color(QPalette.ColorRole.Base)  # Основной фон
        fg_color = palette.color(QPalette.ColorRole.Text)  # Основной текст
        margin_bg = palette.color(QPalette.ColorRole.Window)  # Фон отступов
        margin_fg = QColor('#858585')  # Цвет номеров строк
        selection_bg = palette.color(QPalette.ColorRole.Highlight)  # Цвет выделения
        caret_line_bg = palette.color(QPalette.ColorRole.AlternateBase)  # Цвет текущей строки

        # Применяем цвета к редактору
        self.editor.setColor(fg_color)
        self.editor.setPaper(bg_color)
        self.editor.setMarginsBackgroundColor(margin_bg)
        self.editor.setMarginsForegroundColor(margin_fg)
        self.editor.setSelectionBackgroundColor(selection_bg)
        self.editor.setSelectionForegroundColor(palette.color(QPalette.ColorRole.HighlightedText))
        self.editor.setCaretLineBackgroundColor(caret_line_bg)
        self.editor.setCaretForegroundColor(fg_color)
        self.editor.setCaretLineVisible(True)
        self.editor.setCaretWidth(2)

        # Устанавливаем фон для всех стилей
        for style in range(128):
            self.editor.SendScintilla(self.editor.SCI_STYLESETBACK, style, bg_color.rgb() & 0xFFFFFF)
            self.editor.SendScintilla(self.editor.SCI_STYLESETFORE, style, fg_color.rgb() & 0xFFFFFF)

        # Устанавливаем базовый стиль
        self.editor.SendScintilla(self.editor.SCI_STYLESETBACK, self.editor.STYLE_DEFAULT, bg_color.rgb() & 0xFFFFFF)
        self.editor.SendScintilla(self.editor.SCI_STYLESETFORE, self.editor.STYLE_DEFAULT, fg_color.rgb() & 0xFFFFFF)
        self.editor.SendScintilla(self.editor.SCI_STYLECLEARALL)
        self.editor.SendScintilla(self.editor.SCI_SETVIEWWS, self.editor.SCWS_INVISIBLE)
        self.editor.SendScintilla(self.editor.SCI_SETWHITESPACEBACK, True, bg_color.rgb() & 0xFFFFFF)

        # Также явно задаём фон для стандартных стилей Scintilla
        self.editor.SendScintilla(self.editor.SCI_STYLESETBACK, self.editor.STYLE_DEFAULT, bg_color.rgb() & 0xFFFFFF)
        self.editor.SendScintilla(self.editor.SCI_STYLESETFORE, self.editor.STYLE_DEFAULT, fg_color.rgb() & 0xFFFFFF)
        self.editor.SendScintilla(self.editor.SCI_STYLECLEARALL)
        
        # Отключаем белые линии
        self.editor.setWhitespaceVisibility(QsciScintilla.WhitespaceVisibility.WsInvisible)
        self.editor.setWrapMode(QsciScintilla.WrapMode.WrapWord)
        
        # Настраиваем отступы
        self.editor.setIndentationsUseTabs(False)
        self.editor.setTabWidth(4)
        self.editor.setAutoIndent(True)
        self.editor.setIndentationGuides(False)  # отключаем пунктирные линии табуляции
        self.editor.setCaretLineVisible(True)
        self.editor.setCaretLineBackgroundColor(QColor("#1e1e1e"))
        self.editor.setMarginsBackgroundColor(QColor("#1e1e1e"))
        self.editor.setMarginsForegroundColor(QColor("#858585")) 
        # --- Цветные скобки как в VSCode ---
        self.editor.setBraceMatching(QsciScintilla.BraceMatch.SloppyBraceMatch)
        self.set_brace_colors()
        self.editor.setFolding(QsciScintilla.FoldStyle.BoxedTreeFoldStyle)
        self.editor.setEdgeMode(QsciScintilla.EdgeMode.EdgeNone)  # убираем белую полосу
        self.editor.setUtf8(True)
        self.editor.setFont(QFont('Consolas', 11))
        # Отключаем стандартное автодополнение QScintilla
        self.editor.setAutoCompletionSource(QsciScintilla.AutoCompletionSource.AcsNone)
        # Цвет курсора
        self.editor.setCaretForegroundColor(QColor("#ffffff"))
        self.editor.setCaretWidth(2)
        # Цвет полосы прокрутки
        self.editor.SendScintilla(self.editor.SCI_SETHSCROLLBAR, True)
        self.editor.SendScintilla(self.editor.SCI_SETVSCROLLBAR, True)
        self.editor.setEolMode(QsciScintilla.EolMode.EolUnix)
        self.editor.setTabIndents(True)
        self.editor.setBackspaceUnindents(True)
        self.editor.setIndentationWidth(4)
        self.editor.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        self.editor.setMarginWidth(0, "0000")
        # Убираем белую линию между номерами строк и текстом через стили
        self.editor.setStyleSheet(self.editor.styleSheet() + """
QsciScintilla {
    border: none;
}
QsciScintilla::margin {
    border: none;
    background: #1e1e1e;
}
""")

        # 3. Лексер
        lexer = PopLexer(self.editor)
        self.editor.setLexer(lexer)

        # 4. Настройка автодополнения
        self.editor.setAutoCompletionSource(QsciScintilla.AutoCompletionSource.AcsAPIs)
        self.editor.setAutoCompletionThreshold(1)  # Показывать после первого символа
        self.editor.setAutoCompletionCaseSensitivity(False)
        self.editor.setAutoCompletionReplaceWord(True)
        self.editor.setAutoCompletionUseSingle(QsciScintilla.AutoCompletionUseSingle.AcusNever)
        
        # Создаем API для автодополнения
        self.apis = QsciAPIs(lexer)
        if self.snippet_manager is not None and hasattr(self.snippet_manager, 'snippet_bodies_github'):
            for name, (body, prefix) in self.snippet_manager.snippet_bodies_github.items():
                if isinstance(prefix, list):
                    for p in prefix:
                        self.apis.add(str(p))
                else:
                    self.apis.add(str(prefix))
        self.apis.prepare()
        # Загружаем GitLab-сниппеты для синтакс-проверки (не для автодополнения)
        try:
            self.gitlab_snippets = load_snippets("snippets/popfile_gitlab.code-snippets")
        except Exception as e:
            self.gitlab_snippets = {}

        # --- Кастомное окно автодополнения и превью ---
        
        self.snippet_popup = QListWidget(self)
        self.snippet_popup.setWindowFlags(self.snippet_popup.windowFlags() | Qt.WindowType.ToolTip)
        self.snippet_popup.setStyleSheet('''
            QListWidget {
                background: #23272e;
                color: #d4d4d4;
                border: 1px solid #333;
                font-family: Consolas, monospace;
                font-size: 13px;
                padding: 0px;
                outline: none;
            }
            QListWidget::item:selected {
                background: #2c2c32;
                color: #fff;
            }
        ''')
        self.snippet_popup.hide()
        self.snippet_preview = QTextEdit(self)
        self.snippet_preview.setReadOnly(True)
        self.snippet_preview.setWindowFlags(self.snippet_preview.windowFlags() | Qt.WindowType.ToolTip)
        self.snippet_preview.setStyleSheet('''
            background: #23272e;
            color: #d4d4d4;
            border: 1px solid #333;
            font-family: Consolas, monospace;
            font-size: 12px;
            padding: 6px;
        ''')
        self.snippet_preview.hide()

        
        self.error_panel = QPlainTextEdit(self)
        self.error_panel.setReadOnly(True)
        self.error_panel.setMaximumHeight(80)
        self.error_panel.setStyleSheet('''
            background: #2c2323;
            color: #ff6a6a;
            border: 1px solid #a33;
            font-family: Consolas, monospace;
            font-size: 12px;
            padding: 4px;
        ''')
        self.error_panel.hide()

        # 5. Добавляем виджеты в layout
        self.main_layout.addWidget(self.editor)
        self.main_layout.addWidget(self.error_panel)

        # 6. Автоматическое добавление закрывающей скобки и включение подсказок
        self.editor.keyPressEvent = self.wrap_keypress(self.editor.keyPressEvent)
        self.editor.textChanged.connect(self.on_text_changed)
        self.snippet_popup.itemSelectionChanged.connect(self.update_snippet_preview)
        self.snippet_popup.itemClicked.connect(self.insert_selected_snippet)
        # Перекраска скроллбаров (через стиль)
        self.editor.setStyleSheet('''
            QScrollBar:vertical, QScrollBar:horizontal {
                background: #23272e;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: #3d3d42;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::add-line, QScrollBar::sub-line {
                background: none;
                border: none;
            }
            QScrollBar::add-page, QScrollBar::sub-page {
                background: none;
            }
        ''')

        # --- Закрытие popup при уходе курсора ---
        self.editor.cursorPositionChanged.connect(self.on_cursor_moved)

        # --- Горячая клавиша Alt+Shift+F для форматирования ---
        self.editor.installEventFilter(self)

        # Проверка ошибок при каждом изменении текста
        self.editor.textChanged.connect(self.check_errors)

    def check_errors(self):
        """
        Проверяет синтаксические ошибки в редакторе:
        - Баланс фигурных скобок
        - Незакрытые кавычи
        - Незакрытые скобки других типов
        """
        text = self.editor.text()
        errors = []
        
        # Проверка баланса фигурных скобок и других
        brackets = {'{': '}', '[': ']', '(': ')'}
        stack = []
        
        for i, line in enumerate(text.splitlines(), 1):
            for j, char in enumerate(line):
                if char in brackets:  # открывающая скобка
                    stack.append((char, i, j))
                elif char in brackets.values():  # закрывающая скобка
                    if not stack:
                        errors.append(f"Строка {i}: Лишняя закрывающая скобка '{char}'")
                    else:
                        last_open = stack[-1]
                        if last_open[0] in brackets and char == brackets[last_open[0]]:
                            stack.pop()
                        else:
                            errors.append(f"Строка {i}: Несоответствие скобок '{last_open[0]}' и '{char}'")
                            stack.pop()
                # Проверка кавычей (учитываем экранирование)
                if char == '"' and (j == 0 or line[j-1] != '\\'):
                    if stack and stack[-1][0] == '"':
                        stack.pop()
                    else:
                        stack.append(('"', i, j))
        # Проверяем незакрытые скобки и кавычи
        for char, line, pos in stack:
            if char == '"':
                errors.append(f"Строка {line}: Незакрытая кавычка")
            else:
                errors.append(f"Строка {line}: Незакрытая скобка '{char}'")
        # Обновляем error_panel
        if errors:
            error_text = "\n".join(errors)
            self.error_panel.setPlainText(error_text)
            self.error_panel.show()
        else:
            self.error_panel.clear()
            self.error_panel.hide()

    # Вызовем on_text_changed один раз для инициализации подсказок при запуске
    def showEvent(self, event):
        super().showEvent(event)
        self.on_text_changed()
    def eventFilter(self, obj, event):
        from PyQt6.QtCore import Qt
        if obj == self.editor and event.type() == event.Type.KeyPress:
            if event.key() == Qt.Key.Key_F and event.modifiers() & Qt.KeyboardModifier.AltModifier and event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                self.format_code()
                return True
        return super().eventFilter(obj, event)

    def format_code(self):
        """
        Форматирование POP-файла: автоотступы, переносы, скобки, выравнивание.
        """
        text = self.editor.text()
        lines = text.splitlines()
        indent = 0
        formatted = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                formatted.append("")
                continue
            # Уменьшаем отступ перед закрывающей скобкой
            if stripped.startswith("}"):
                indent = max(0, indent - 1)
            formatted.append("    " * indent + stripped)
            # Увеличиваем отступ после открывающей скобки
            if stripped.endswith("{"):
                indent += 1
        self.editor.setText("\n".join(formatted))

    def on_cursor_moved(self):
        """
        Закрывает popup и preview, если курсор ушёл с текущего слова.
        """
        if self.snippet_popup.isVisible():
            # Получить текущее слово перед курсором
            line, index = self.editor.getCursorPosition()
            text = self.editor.text(line)[:index]
            import re
            match = re.search(r'(\w{1,40})$', text)
            prefix = match.group(1) if match else ''
            # Используем SnippetManager для фильтрации
            filtered = self.snippet_manager.get_filtered(prefix) if prefix else []
            if not prefix or not filtered:
                self.snippet_popup.hide()
                self.snippet_preview.hide()

    # update_apis и on_snippet_changed больше не нужны

    def wrap_keypress(self, orig_keypress):
        from PyQt6.QtCore import Qt
        def new_keypress(event):
            key = event.key()
            cursor = self.editor.getCursorPosition()
            line, index = cursor
            text_line = self.editor.text(line)
            # Проверка Backspace
            if key == Qt.Key.Key_Backspace and index > 0 and index < len(text_line):
                left = text_line[index-1]
                right = text_line[index]
                pairs = {'{': '}', '(': ')', '[': ']'},
                if left in pairs and right == pairs[left]:
                    # Проверяем, что между ними ничего нет
                    if text_line[index-1:index+1] == left+right:
                        self.editor.setSelection(line, index-1, line, index+1)
                        self.editor.removeSelectedText()
                        return
            # Проверка Delete
            if key == Qt.Key.Key_Delete and index < len(text_line)-1 and index >= 0:
                left = text_line[index]
                right = text_line[index+1]
                pairs = {'{': '}', '(': ')', '[': ']'},
                if left in pairs and right == pairs[left]:
                    if text_line[index:index+2] == left+right:
                        self.editor.setSelection(line, index, line, index+2)
                        self.editor.removeSelectedText()
                        return
            orig_keypress(event)
        return new_keypress

    def on_text_changed(self):
        """Обработка изменения текста: объединяем сниппеты и синтаксис в одной панели"""
        if not self.isActiveWindow():
            self.snippet_popup.hide()
            self.snippet_preview.hide()
            return

        # Получаем текущую позицию и текст
        line, index = self.editor.getCursorPosition()
        text = self.editor.text(line)[:index]
        match = re.search(r'(\w{1,40})$', text)
        prefix = match.group(1) if match else ''

        # Сниппеты
        snippet_names = set()
        if prefix and hasattr(self, 'snippet_manager') and self.snippet_manager:
            snippet_names = set(self.snippet_manager.get_filtered(prefix))

        # Ключевые слова из синтаксиса
        keywords = set()
        lexer = self.editor.lexer()
        if prefix and isinstance(lexer, PopLexer):
            for kw in lexer.get_autocomplete_keywords():
                if kw.lower().startswith(prefix.lower()):
                    keywords.add(kw)

        # Объединяем и сортируем
        all_suggestions = sorted(snippet_names | keywords)

        if prefix and all_suggestions:
            self.snippet_popup.clear()
            for name in all_suggestions:
                from PyQt6.QtWidgets import QListWidgetItem
                item = QListWidgetItem(name)
                self.snippet_popup.addItem(item)
            self.snippet_popup.setCurrentRow(0)
            pos = self.get_cursor_screen_position()
            self.snippet_popup.move(pos.x(), pos.y() + 5)
            self.snippet_popup.resize(320, min(200, 24 * len(all_suggestions)))
            self.snippet_popup.show()
            self.update_snippet_preview()
            self.show_ghost_text(prefix, all_suggestions[0])
        else:
            self.snippet_popup.hide()
            self.snippet_preview.hide()
        # Обновляем подсветку синтаксиса
        if hasattr(self, 'editor') and self.editor and isinstance(self.editor.lexer(), PopLexer):
            self.editor.recolor()

    def show_ghost_text(self, prefix, suggestion_name):
        """Показывает полупрозрачный текст подсказки"""
        try:
            # Очищаем предыдущий ghost-текст
            self.editor.SendScintilla(self.editor.SCI_SETINDICATORCURRENT, 0)
            self.editor.SendScintilla(self.editor.SCI_INDICATORCLEARRANGE, 0, self.editor.length())
            
            if not suggestion_name or not self.snippet_manager:
                return
                
            # Получаем содержимое сниппета
            body = self.snippet_manager.get_body(suggestion_name)
            if not body:
                print(f"Нет тела для сниппета: {suggestion_name}")
                return
                
            # Рендерим сниппет
            rendered = self.snippet_manager.render_snippet(body)
            if not rendered:
                print(f"Ошибка рендеринга сниппета: {suggestion_name}")
                return
                
            ghost = rendered[0]  # Берем первую строку
            
            # Проверяем соответствие префиксу
            if ghost.lower().startswith(prefix.lower()):
                ghost_tail = ghost[len(prefix):]
                if ghost_tail:
                    print(f"Показываем ghost-текст: {ghost_tail}")
                    
                    # Настраиваем индикатор
                    self.editor.SendScintilla(self.editor.SCI_INDICSETSTYLE, 0, self.editor.INDIC_PLAIN)
                    self.editor.SendScintilla(self.editor.SCI_INDICSETFORE, 0, QColor(128, 128, 128, 100).rgb() & 0xFFFFFF)
                    self.editor.SendScintilla(self.editor.SCI_INDICSETALPHA, 0, 100)
                    
                    # Получаем позицию для вставки
                    line, col = self.editor.getCursorPosition()
                    pos = self.editor.positionFromLineIndex(line, col)
                    
                    # Показываем ghost-текст
                    self.editor.SendScintilla(self.editor.SCI_INDICATORFILLRANGE, pos, len(ghost_tail))
            
        except Exception as e:
            print(f"Ошибка при показе ghost-текста: {e}")

    def update_snippet_preview(self):
        if not self.snippet_popup.isVisible() or self.snippet_popup.currentItem() is None or not self.isActiveWindow():
            self.snippet_preview.hide()
            return
        display_name = self.snippet_popup.currentItem().text()
        body = self.snippet_manager.get_body(display_name)
        if body:
            body = self.snippet_manager.render_snippet(body)
            preview_text = display_name + "\n\n" + ("\n".join(body) if body else "")
        else:
            preview_text = display_name  # Для ключевых слов просто название
        self.snippet_preview.setPlainText(preview_text)
        # Позиционируем preview справа от popup
        popup_geo = self.snippet_popup.geometry()
        self.snippet_preview.move(popup_geo.right() + 8, popup_geo.top())
        self.snippet_preview.resize(520, min(320, 18*(len(body) if body else 1)+60))
        self.snippet_preview.show()
        self.snippet_preview.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.snippet_preview.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def insert_selected_snippet(self):
        if not self.snippet_popup.isVisible() or self.snippet_popup.currentItem() is None:
            return
        display_name = self.snippet_popup.currentItem().text()
        body = self.snippet_manager.get_body(display_name)
        prefix = self.snippet_manager.get_prefix(display_name)
        line, index = self.editor.getCursorPosition()
        if body:  # Это сниппет
            body = self.snippet_manager.render_snippet(body)
            prefix_len = len(str(prefix))
            self.editor.setSelection(line, index - prefix_len, line, index)
            self.editor.replaceSelectedText("\n".join(body))
        else:  # Это ключевое слово синтаксиса
            prefix_len = len(str(prefix)) if prefix else len(display_name)
            self.editor.setSelection(line, index - prefix_len, line, index)
            self.editor.replaceSelectedText(display_name)
        self.snippet_popup.hide()
        self.snippet_preview.hide()

    def show_snippet_preview(self, *args):
        # Получить выбранный display_name
        display_name = self.editor.autoCompletionSelectedText()
        snippet = self.snippet_bodies.get(display_name)
        if not snippet:
            self.snippet_preview.hide()
            return
        body, _ = snippet
        preview_text = '\n'.join(body)
        self.snippet_preview.setText(preview_text)
        # Позиционируем окно под автокомплитом
        pos = self.editor.mapToGlobal(self.editor.cursorRect().bottomRight())
        self.snippet_preview.move(pos.x() + 10, pos.y() + 10)
        self.snippet_preview.adjustSize()
        self.snippet_preview.show()

    def hide_snippet_preview(self, *args):
        self.snippet_preview.hide()

    def set_brace_colors(self):
        # Цвета VSCode: розовый, синий, жёлтый, по кругу
        brace_colors = [QColor("#D16D9E"), QColor("#569CD6"), QColor("#D7BA7D")]
        for i, color in enumerate(brace_colors):
            # Используем color.rgb() & 0xFFFFFF чтобы избежать переполнения
            self.editor.SendScintilla(self.editor.SCI_STYLESETFORE, 34 + i, color.rgb() & 0xFFFFFF)
        # Тонкая обводка для скобок
        self.editor.SendScintilla(self.editor.SCI_STYLESETBOLD, 34, False)
        self.editor.SendScintilla(self.editor.SCI_STYLESETBOLD, 35, False)
        self.editor.SendScintilla(self.editor.SCI_STYLESETBOLD, 36, False)
        # Установить стиль для всех уровней вложенности (по кругу)
        for level in range(9):
            self.editor.SendScintilla(self.editor.SCI_BRACEHIGHLIGHTINDICATOR, level, 34 + (level % 3))

    def load_snippets(self):
        """Асинхронная загрузка сниппетов"""
        try:
            # Проверяем существование файла перед загрузкой
            github_path = "snippets/popfile.json"
            if os.path.exists(github_path):
                print(f"Загружаем сниппеты из {github_path}")
                self.snippet_manager = SnippetManager(github_path)
                print(f"Загружено сниппетов: {len(self.snippet_manager.snippets_github)}")
            else:
                print(f"Файл сниппетов не найден: {github_path}")
                # Создаем директорию если её нет
                os.makedirs(os.path.dirname(github_path), exist_ok=True)
                
            # Обновляем API после загрузки сниппетов
            print("Обновляем API...")
            self.update_apis()
            print("API обновлено")
                
            # Пробуем обновить в фоне
            QTimer.singleShot(200, self.update_snippets)
            
        except Exception as e:
            print(f"Ошибка загрузки сниппетов: {e}")

    def update_syntax_rules(self):
        """Обновляет правила синтаксиса для лексера"""
        if hasattr(self, 'editor') and self.editor:
            lexer = self.editor.lexer()
            if isinstance(lexer, PopLexer):
                lexer._syntax_rules = lexer._load_syntax_rules()
                self.editor.recolor()
                
    def reload_syntax_highlighting(self):
        """Перезагружает подсветку синтаксиса"""
        if hasattr(self, 'editor') and self.editor:
            self.update_syntax_rules()
            # Обновляем весь текст
            self.editor.recolor()        

    def get_cursor_screen_position(self):
        """Возвращает экранные координаты текущей позиции курсора"""
        line, index = self.editor.getCursorPosition()
        # Получаем пиксельную позицию для строки и колонки
        x = self.editor.SendScintilla(self.editor.SCI_POINTXFROMPOSITION, 0, 
                                    self.editor.positionFromLineIndex(line, index))
        y = self.editor.SendScintilla(self.editor.SCI_POINTYFROMPOSITION, 0,
                                    self.editor.positionFromLineIndex(line, index))
        # Добавляем высоту строки для показа popup под курсором
        line_height = self.editor.textHeight(line)
        # Преобразуем локальные координаты в глобальные
        pos = self.editor.mapToGlobal(QtCore.QPoint(x, y + line_height))
        return pos

class EditorButtonPanel(QWidget):
    """Панель с кнопками Save/Cancel для редактора с тёмной темой"""
    def __init__(self, parent=None, on_save=None, on_cancel=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 0)
        layout.setSpacing(8)
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        self.save_btn.setMinimumHeight(32)
        self.cancel_btn.setMinimumHeight(32)
        button_style = """
            QPushButton {
                background-color: #1e1e1e !important;
                color: white !important;
                border: none !important;
            }
            QPushButton:hover {
                background-color: #282828 !important;
            }
            QPushButton:pressed {
                background-color: #232323 !important;
            }
            QPushButton:focus {
                outline: none !important;
            }
        """
        self.save_btn.setStyleSheet(button_style)
        self.cancel_btn.setStyleSheet(button_style)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.cancel_btn)
        if on_save:
            self.save_btn.clicked.connect(on_save)
        if on_cancel:
            self.cancel_btn.clicked.connect(on_cancel)