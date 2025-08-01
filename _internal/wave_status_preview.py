from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import re

class WaveStatusPreview(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(260)
        self.setMaximumWidth(400)
        self.setStyleSheet('''
            background: #23272e;
            color: #d4d4d4;
            border-left: 1px solid #333;
        ''')
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)
        self.label = QLabel("Wave Status Preview")
        self.label.setFont(QFont('Consolas', 12, QFont.Weight.Bold))
        self.label.setStyleSheet('color: #7BD1FF;')
        layout.addWidget(self.label)
        # Заменяем QTextEdit на кастомный QLabel для визуального превью
        self.visual = QLabel()
        self.visual.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.visual.setStyleSheet('background: #23272e; color: #d4d4d4; border: none;')
        self.visual.setFont(QFont('Consolas', 10))
        self.visual.setMinimumHeight(120)
        self.visual.setText('Нет данных о волнах.')
        layout.addWidget(self.visual)
        self.setLayout(layout)

    def update_preview(self, pop_text):
        # Новый парсер: поддержка нескольких волн, корректный подсчёт, визуальный стиль
        waves = []
        wave_total = 0
        current = None
        lines = pop_text.splitlines()
        for idx, line in enumerate(lines):
            line = line.strip()
            if re.match(r'^Wave(\s+\d+)?\s*{', line):
                if current:
                    waves.append(current)
                wave_total += 1
                current = {'bot_types': {}, 'money': 0, 'wave': wave_total, 'start_line': idx}
            elif current is not None:
                if line.startswith('TotalCount'):
                    m = re.match(r'TotalCount\s+(\d+)', line)
                    if m:
                        current['bot_count'] = int(m.group(1))
                elif line.startswith('Template'):
                    m = re.match(r'Template\s+"?([\w_\-]+)"?', line)
                    if m:
                        t = m.group(1)
                        current['bot_types'][t] = current['bot_types'].get(t, 0)
                        current['last_template'] = t
                elif line.lower().startswith('currency'):
                    m = re.match(r'Currency\s+(\d+)', line, re.IGNORECASE)
                    if m:
                        current['money'] += int(m.group(1))
                elif line.startswith('Count'):
                    m = re.match(r'Count\s+(\d+)', line)
                    if m and 'last_template' in current:
                        t = current['last_template']
                        current['bot_types'][t] = current['bot_types'].get(t, 0) + int(m.group(1))
                elif line.startswith('Class'):
                    m = re.match(r'Class\s+"?([\w_\-]+)"?', line)
                    if m:
                        t = m.group(1)
                        current['last_template'] = t
                        current['bot_types'][t] = current['bot_types'].get(t, 0)
        if current:
            waves.append(current)
        if not waves:
            self.visual.setText("Нет данных о волнах.")
            return
        # Определяем положение курсора пользователя (по строке)
        parent = self.parent()
        editor = getattr(parent, 'editor', None)
        current_line = 0
        if editor:
            try:
                current_line, _ = editor.getCursorPosition()
            except Exception:
                current_line = 0
        # Находим ближайшую волну по позиции курсора
        active_wave = 0
        for i, w in enumerate(waves):
            if 'start_line' in w and current_line >= w['start_line']:
                active_wave = i
        # Прогресс-бар: позиция = (active_wave+1)/len(waves)
        progress = (active_wave + 1) / max(1, len(waves))
        w = waves[active_wave]
        wave_num = w.get('wave', 1)
        total_waves = len(waves)
        money = w.get('money', 0)
        bots = w.get('bot_types', {})
        # Стилизация текста (можно заменить на rich text/HTML)
        bar_width = int(200 * progress)
        html = f"""
        <div style='background:#35323a; border-radius:8px; border:2px solid #888; padding:8px; min-width:220px; text-align:center;'>
            <div style='font-family:Consolas,sans-serif; font-size:18px; font-weight:bold; color:#fff; letter-spacing:2px;'>
                WAVE {wave_num} / {total_waves} <span style='color:#7ec06c;'>${money}</span>
            </div>
            <div style='margin:8px 0 8px 0; position:relative; height:18px; background:#6b7a8f; border-radius:6px; border:1px solid #bfc9d1; width:90%; margin-left:auto; margin-right:auto;'>
                <div style='position:absolute; left:0; top:0; height:100%; width:{bar_width}px; background:#bfc9d1; border-radius:6px;'></div>
            </div>
            <div style='margin:8px 0 0 0;'>
        """
        if bots:
            for t, count in bots.items():
                html += f"<div style='display:inline-block; margin:4px 12px 0 12px;'><div style='width:48px; height:48px; background:#e6e0d0; border-radius:8px; display:flex; align-items:center; justify-content:center; margin:auto;'><span style='font-size:32px;'>🦾</span></div><div style='font-size:18px; color:#fff;'>{count if count else '?'}</div></div>"
        else:
            html += "<div style='color:#aaa;'>-</div>"
        html += "</div></div>"
        self.visual.setText(html)
