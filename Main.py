"""
TeleAI-AutoPoster v1.0.2
Telegram AI Content Generation & Auto-Posting System
Developer: https://github.com/BSHF-PER
"""
import sys
import os
import json
import time
import threading
import requests
import sqlite3
import base64
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QCheckBox, QSpinBox, QDoubleSpinBox, QGroupBox, QFormLayout,
    QStatusBar, QMessageBox, QSplitter, QComboBox, QScrollArea,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog,
    QTimeEdit, QDateEdit, QRadioButton, QButtonGroup, QProgressBar,
    QMenu, QAction, QInputDialog, QSizePolicy, QGraphicsDropShadowEffect,
    QGraphicsBlurEffect
)
from PyQt5.QtCore import (
    Qt, QTimer, pyqtSignal, QObject, QThread, QDate, QTime,
    QDateTime, QSize, QUrl, QRect, QPoint
)
from PyQt5.QtGui import (
    QFont, QTextCursor, QColor, QPalette, QIcon, QPixmap,
    QLinearGradient, QPainter, QBrush, QPen, QFontMetrics,
    QDesktopServices, QCursor, QPainterPath, QRadialGradient,
    QImage
)
from PyQt5.QtSvg import QSvgRenderer
from openai import OpenAI


# ============================================================================
# SVG Icon System
# ============================================================================
class SVGIcons:
    """High-quality SVG icon renderer"""

    @staticmethod
    def _render_svg(svg_string: str, size: int = 20, color: str = "#e0e0e0") -> QIcon:
        """Render SVG string to QIcon"""
        svg_string = svg_string.replace("currentColor", color)
        renderer = QSvgRenderer(svg_string.encode('utf-8'))
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        return QIcon(pixmap)

    @staticmethod
    def settings(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68 1.65 1.65 0 0 0 10 3.17V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def edit(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def upload(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def terminal(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def help(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def info(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def play(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="{color}" stroke="none"><polygon points="5 3 19 12 5 21 5 3"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def stop(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="{color}" stroke="none"><rect x="4" y="4" width="16" height="16" rx="2"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def save(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def refresh(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def trash(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def key(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def send(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def clock(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def image(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def target(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def github(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="{color}"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def user(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def code(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def zap(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="{color}" stroke="none"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def folder(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def plus(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def external_link(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def reset(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def list(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def database(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def globe(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def calendar(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def filter(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)

    @staticmethod
    def activity(size=20, color="#e0e0e0"):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>'''
        return SVGIcons._render_svg(svg, size, color)


# ============================================================================
# Database Manager
# ============================================================================
class DatabaseManager:
    def __init__(self, db_path="teleai_database.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS content_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT, content_type TEXT NOT NULL,
                text_content TEXT, media_type TEXT, media_path TEXT,
                scheduled_time TEXT, status TEXT DEFAULT 'pending',
                created_at TEXT, platforms TEXT, priority INTEGER DEFAULT 0)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT,
                level TEXT, category TEXT, message TEXT)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT,
                posts_count INTEGER DEFAULT 0, images_count INTEGER DEFAULT 0,
                total_cost REAL DEFAULT 0.0)''')
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Database initialization error: {e}")

    def add_to_queue(self, content_data: dict) -> int:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO content_queue 
                (content_type, text_content, media_type, media_path, 
                 scheduled_time, status, created_at, platforms, priority)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                content_data.get('content_type', 'ai'),
                content_data.get('text_content', ''),
                content_data.get('media_type', ''),
                content_data.get('media_path', ''),
                content_data.get('scheduled_time', ''),
                content_data.get('status', 'pending'),
                datetime.now().isoformat(),
                json.dumps(content_data.get('platforms', [])),
                content_data.get('priority', 0)))
            content_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return content_id
        except Exception as e:
            print(f"Add to queue error: {e}")
            return -1

    def get_pending_content(self, limit=10) -> List[dict]:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM content_queue WHERE status = 'pending' 
                ORDER BY scheduled_time ASC, priority DESC LIMIT ?''', (limit,))
            rows = cursor.fetchall()
            conn.close()
            return [{'id': r[0], 'content_type': r[1], 'text_content': r[2],
                     'media_type': r[3], 'media_path': r[4], 'scheduled_time': r[5],
                     'status': r[6], 'created_at': r[7],
                     'platforms': json.loads(r[8]) if r[8] else [], 'priority': r[9]} for r in rows]
        except Exception as e:
            print(f"Get pending content error: {e}")
            return []

    def update_content_status(self, content_id: int, status: str):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('UPDATE content_queue SET status = ? WHERE id = ?', (status, content_id))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Update status error: {e}")

    def delete_content(self, content_id: int):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM content_queue WHERE id = ?', (content_id,))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Delete content error: {e}")

    def add_log(self, level: str, category: str, message: str):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO logs (timestamp, level, category, message) VALUES (?, ?, ?, ?)',
                          (datetime.now().isoformat(), level, category, message))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Add log error: {e}")

    def get_logs(self, level_filter=None, category_filter=None, limit=100) -> List[dict]:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            query = "SELECT * FROM logs WHERE 1=1"
            params = []
            if level_filter:
                query += " AND level = ?"
                params.append(level_filter)
            if category_filter:
                query += " AND category = ?"
                params.append(category_filter)
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()
            return [{'id': r[0], 'timestamp': r[1], 'level': r[2], 'category': r[3], 'message': r[4]} for r in rows]
        except Exception as e:
            print(f"Get logs error: {e}")
            return []

    def update_statistics(self, date: str, posts: int = 0, images: int = 0, cost: float = 0.0):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO statistics (date, posts_count, images_count, total_cost) VALUES (?, ?, ?, ?)',
                          (date, posts, images, cost))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Update statistics error: {e}")


# ============================================================================
# Telegram Sender
# ============================================================================
class TelegramSender:
    def __init__(self, bot_token, channel_id, log_callback=None):
        self.bot_token = bot_token
        self.channel_id = channel_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        self.log = log_callback or print

    def send_message(self, text, media_path=None, media_type='text'):
        try:
            if media_path and os.path.exists(media_path):
                with open(media_path, 'rb') as f:
                    if media_type == 'photo':
                        files, endpoint = {'photo': f}, '/sendPhoto'
                    elif media_type == 'video':
                        files, endpoint = {'video': f}, '/sendVideo'
                    elif media_type == 'audio':
                        files, endpoint = {'audio': f}, '/sendAudio'
                    else:
                        files, endpoint = {'document': f}, '/sendDocument'
                    data = {'chat_id': self.channel_id, 'caption': text}
                    response = requests.post(f"{self.base_url}{endpoint}", files=files, data=data, timeout=120)
            else:
                response = requests.post(f"{self.base_url}/sendMessage",
                    json={'chat_id': self.channel_id, 'text': text}, timeout=30)
            if response.status_code == 200:
                self.log("Telegram: Message sent successfully")
                return True
            else:
                self.log(f"Telegram: Error {response.status_code} - {response.text[:300]}")
                return False
        except Exception as e:
            self.log(f"Telegram: Connection error - {e}")
            return False


# ============================================================================
# GitHub Profile Fetcher
# ============================================================================
class GitHubProfileFetcher(QThread):
    profile_loaded = pyqtSignal(dict)
    profile_error = pyqtSignal(str)

    def __init__(self, username):
        super().__init__()
        self.username = username

    def run(self):
        try:
            response = requests.get(f"https://api.github.com/users/{self.username}",
                timeout=10, headers={"Accept": "application/vnd.github.v3+json"})
            if response.status_code == 200:
                self.profile_loaded.emit(response.json())
            else:
                self.profile_error.emit(f"HTTP {response.status_code}")
        except Exception as e:
            self.profile_error.emit(str(e))


# ============================================================================
# Agent Worker
# ============================================================================
class AgentSignals(QObject):
    log_message = pyqtSignal(str, str, str)
    stats_update = pyqtSignal(dict)
    finished = pyqtSignal()
    error = pyqtSignal(str)


class AgentWorker(QThread):
    def __init__(self, config, db_manager):
        super().__init__()
        self.config = config
        self.db = db_manager
        self.signals = AgentSignals()
        self.is_running = True
        self.client = None
        self.sender = None
        self.stats = {"total_posts": 0, "total_images": 0, "total_cost": 0.0, "last_run": None}

    def log(self, message, level="INFO", category="GENERAL"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.signals.log_message.emit(level, category, f"[{timestamp}] [{level}] [{category}] {message}")
        self.db.add_log(level, category, message)

    def stop(self):
        self.is_running = False
        self.log("Stop request received...", "WARNING", "SYSTEM")

    def run(self):
        try:
            self.log("Initializing TeleAI-AutoPoster v1.0.2...", "INFO", "SYSTEM")
            api_key = self.config["OPENAI_API_KEY"]
            base_url = self.config.get("OPENAI_BASE_URL", "").strip()
            client_kwargs = {"api_key": api_key}
            if base_url:
                client_kwargs["base_url"] = base_url
            self.client = OpenAI(**client_kwargs)
            self.log(f"OpenAI client initialized (Base URL: {base_url or 'default'})", "INFO", "OPENAI")

            if self.config["TELEGRAM"]["bot_token"] and self.config["TELEGRAM"]["channel_id"]:
                self.sender = TelegramSender(
                    self.config["TELEGRAM"]["bot_token"],
                    self.config["TELEGRAM"]["channel_id"],
                    lambda msg: self.log(msg, "INFO", "TELEGRAM"))
                self.log("Telegram sender activated", "INFO", "PLATFORM")
            else:
                self.log("Telegram configuration incomplete!", "ERROR", "SYSTEM")
                self.signals.error.emit("Telegram configuration incomplete")
                return

            interval_minutes = self.config.get("INTERVAL_MINUTES", 5)
            self.log(f"Run mode: Continuous (every {interval_minutes} minutes)", "INFO", "SYSTEM")
            self.run_continuous(interval_minutes)
            self.log("Agent execution completed", "INFO", "SYSTEM")
            self.signals.finished.emit()
        except Exception as e:
            self.log(f"Critical error: {str(e)}", "ERROR", "SYSTEM")
            self.signals.error.emit(str(e))

    def generate_text_content(self) -> Optional[str]:
        self.log("Generating text content...", "INFO", "CONTENT")
        prompt_settings = self.config.get('prompt_settings', {})
        text_model = self.config.get("TEXT_MODEL", "").strip()
        if not text_model:
            self.log("No text model specified!", "ERROR", "CONTENT")
            return None
        prompt = f"""Topic: {self.config['WORK_TOPIC']}
Tone: {prompt_settings.get('tone', 'formal')}
Target Audience: {prompt_settings.get('target_audience', 'general')}
Writing Style: {prompt_settings.get('style', 'educational')}
Content Rules:
{self.config['CONTENT_RULES']}
Required Keywords: {', '.join(prompt_settings.get('required_keywords', []))}
Forbidden Words: {', '.join(prompt_settings.get('forbidden_keywords', []))}
Generate fresh, original content. Return only the final post text."""
        try:
            response = self.client.chat.completions.create(
                model=text_model,
                messages=[
                    {"role": "system", "content": "You are a professional content writer. Return only the final post text."},
                    {"role": "user", "content": prompt}],
                temperature=prompt_settings.get('temperature', 0.8),
                max_tokens=prompt_settings.get('max_tokens', 600))
            text_content = response.choices[0].message.content
            if response.usage:
                cost = (response.usage.prompt_tokens * 0.000001) + (response.usage.completion_tokens * 0.000002)
                self.stats["total_cost"] += cost
                self.log(f"Text generated (tokens: {response.usage.total_tokens})", "INFO", "CONTENT")
            return text_content
        except Exception as e:
            self.log(f"Text generation error: {e}", "ERROR", "CONTENT")
            return None

    def should_generate_image(self, text_content) -> bool:
        image_mode = self.config.get('image_mode', 'smart')
        if image_mode == 'always':
            return True
        elif image_mode == 'never':
            return False
        elif image_mode == 'smart':
            text_model = self.config.get("TEXT_MODEL", "").strip()
            if not text_model:
                return False
            try:
                response = self.client.chat.completions.create(
                    model=text_model,
                    messages=[
                        {"role": "system", "content": "Respond with only YES or NO."},
                        {"role": "user", "content": f"Does this text need an image? Answer YES only if it describes visual concepts, step-by-step content, comparisons, or statistics.\n\nText:\n{text_content}"}],
                    temperature=0.1, max_tokens=5)
                return response.choices[0].message.content.strip().upper() == "YES"
            except:
                return False
        return False

    def generate_image_for_content(self, text_content) -> Optional[str]:
        self.log("Generating related image...", "INFO", "IMAGE")
        text_model = self.config.get("TEXT_MODEL", "").strip()
        image_model = self.config.get("IMAGE_MODEL", "").strip()
        if not image_model:
            self.log("No image model specified, skipping", "WARNING", "IMAGE")
            return None
        try:
            response = self.client.chat.completions.create(
                model=text_model,
                messages=[
                    {"role": "system", "content": "Return only the image prompt in English."},
                    {"role": "user", "content": f"Write a short image generation prompt for this text:\n{text_content}"}],
                temperature=0.5, max_tokens=100)
            image_prompt = response.choices[0].message.content.strip()
            self.log(f"Image prompt: {image_prompt}", "INFO", "IMAGE")
            image_response = self.client.images.generate(
                model=image_model, prompt=image_prompt, size="1024x1024", n=1, response_format="b64_json")
            image_data = None
            if image_response.data and len(image_response.data) > 0:
                img_info = image_response.data[0]
                if hasattr(img_info, 'b64_json') and img_info.b64_json:
                    image_data = base64.b64decode(img_info.b64_json)
                elif hasattr(img_info, 'url') and img_info.url:
                    img_resp = requests.get(img_info.url, timeout=60)
                    if img_resp.status_code == 200:
                        image_data = img_resp.content
            if not image_data:
                self.log("No image data received", "ERROR", "IMAGE")
                return None
            temp_dir = Path("temp_images")
            temp_dir.mkdir(exist_ok=True)
            media_path = temp_dir / f"temp_{int(time.time())}_{random.randint(1000, 9999)}.jpg"
            with open(media_path, 'wb') as f:
                f.write(image_data)
            self.log(f"Image saved: {media_path}", "INFO", "IMAGE")
            self.stats["total_images"] += 1
            return str(media_path)
        except Exception as e:
            self.log(f"Image generation error: {e}", "ERROR", "IMAGE")
            return None

    def send_to_telegram(self, text_content, media_path=None, media_type='text') -> bool:
        self.log("Sending to Telegram...", "INFO", "SEND")
        full_text = text_content
        footer = self.config.get("POST_FOOTER", "").strip()
        if footer:
            full_text += f"\n\n{footer}"
        if media_path and not os.path.exists(media_path):
            media_path = None
        success = self.sender.send_message(full_text, media_path, media_type)
        if success:
            self.stats["total_posts"] += 1
            self.stats["last_run"] = datetime.now()
            self.signals.stats_update.emit(self.stats.copy())
        return success

    def process_manual_content(self, content_item: dict) -> bool:
        self.log(f"Processing manual content ID: {content_item['id']}", "INFO", "MANUAL")
        success = self.send_to_telegram(
            content_item.get('text_content', ''),
            content_item.get('media_path', ''),
            content_item.get('media_type', 'text'))
        if success:
            self.db.update_content_status(content_item['id'], 'sent')
        return success

    def run_once(self):
        self.log("=" * 50)
        self.log(f"New cycle - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        pending = self.db.get_pending_content(limit=1)
        for item in pending:
            try:
                if datetime.fromisoformat(item['scheduled_time']) <= datetime.now():
                    self.process_manual_content(item)
                    continue
            except:
                pass
        text_content = self.generate_text_content()
        if not text_content:
            return False
        media_path = None
        media_type = 'text'
        if self.should_generate_image(text_content):
            media_path = self.generate_image_for_content(text_content)
            if media_path:
                media_type = 'photo'
        success = self.send_to_telegram(text_content, media_path, media_type)
        if media_path and os.path.exists(media_path):
            try:
                os.remove(media_path)
            except:
                pass
        self.log(f"Stats: {self.stats['total_posts']} posts | {self.stats['total_images']} images | ${self.stats['total_cost']:.6f}", "INFO", "STATS")
        return success

    def run_continuous(self, interval_minutes: int):
        interval_seconds = interval_minutes * 60
        while self.is_running:
            try:
                self.run_once()
                if not self.is_running:
                    break
                self.log(f"Next run in {interval_minutes} minutes...", "INFO", "SYSTEM")
                for _ in range(int(interval_seconds)):
                    if not self.is_running:
                        break
                    time.sleep(1)
            except Exception as e:
                self.log(f"Cycle error: {e}", "ERROR", "SYSTEM")
                if self.is_running:
                    for _ in range(60):
                        if not self.is_running:
                            break
                        time.sleep(1)


# ============================================================================
# Constants
# ============================================================================
CONFIG_FILE = "teleai_config.json"
APP_VERSION = "v1.0.2"
GITHUB_USERNAME = "BSHF-PER"
GITHUB_URL = f"https://github.com/{GITHUB_USERNAME}"

DEFAULT_CONFIG = {
    "OPENAI_API_KEY": "",
    "OPENAI_BASE_URL": "",
    "TEXT_MODEL": "",
    "IMAGE_MODEL": "",
    "TELEGRAM": {"bot_token": "", "channel_id": ""},
    "WORK_TOPIC": "Describe the topic to guide generated content",
    "CONTENT_RULES": """Content generation rules:
- Each post should be between 150 to 300 words
- Use formal and fluent language with an engaging tone
- Include an interactive question at the end
- Provide accurate and up-to-date information
- Avoid clichés and repetitive sentences
- Add 3 relevant hashtags at the end""",
    "INTERVAL_MINUTES": 5,
    "POST_FOOTER": "",
    "prompt_settings": {
        "tone": "formal", "target_audience": "general", "style": "educational",
        "required_keywords": [], "forbidden_keywords": [],
        "temperature": 0.8, "max_tokens": 600},
    "image_mode": "smart"
}

# ============================================================================
# GLASSMORPHISM DARK THEME (Black to White spectrum)
# ============================================================================
GLASS_DARK_STYLE = """
QMainWindow {
    background-color: #08080c;
}
QWidget {
    font-family: 'Segoe UI', 'Inter', 'SF Pro Display', -apple-system, sans-serif;
    font-size: 13px;
    color: #e8e8ec;
    background-color: transparent;
}

/* Scrollbar */
QScrollArea { border: none; background-color: transparent; }
QScrollArea > QWidget > QWidget { background-color: transparent; }
QScrollBar:vertical { background: #08080c; width: 6px; border-radius: 3px; }
QScrollBar::handle:vertical { background: rgba(255,255,255,0.12); border-radius: 3px; min-height: 30px; }
QScrollBar::handle:vertical:hover { background: rgba(255,255,255,0.25); }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QScrollBar:horizontal { background: #08080c; height: 6px; border-radius: 3px; }
QScrollBar::handle:horizontal { background: rgba(255,255,255,0.12); border-radius: 3px; }
QScrollBar::handle:horizontal:hover { background: rgba(255,255,255,0.25); }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0px; }

QLabel { color: #d0d0d8; background: transparent; }

/* Glass GroupBox */
QGroupBox {
    color: rgba(255,255,255,0.9);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    margin-top: 16px;
    font-weight: 600;
    font-size: 13px;
    background-color: rgba(255,255,255,0.03);
    padding: 22px 16px 16px 16px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 18px;
    padding: 0 10px;
    color: rgba(255,255,255,0.85);
    font-weight: 700;
}

/* Inputs - Glass effect */
QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QTimeEdit, QDateEdit {
    background-color: rgba(255,255,255,0.04);
    color: #e8e8ec;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 9px;
    padding: 9px 13px;
    selection-background-color: rgba(255,255,255,0.2);
    selection-color: #ffffff;
    font-size: 13px;
}
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus, QTimeEdit:focus, QDateEdit:focus {
    border: 1px solid rgba(255,255,255,0.3);
    background-color: rgba(255,255,255,0.06);
}
QLineEdit:hover, QSpinBox:hover, QDoubleSpinBox:hover, QComboBox:hover {
    border: 1px solid rgba(255,255,255,0.18);
}

QTextEdit {
    background-color: rgba(255,255,255,0.04);
    color: #e8e8ec;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 9px;
    padding: 9px;
    selection-background-color: rgba(255,255,255,0.2);
    selection-color: #ffffff;
}
QTextEdit:focus { border: 1px solid rgba(255,255,255,0.3); }

/* ComboBox */
QComboBox::drop-down { border: none; width: 30px; }
QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid rgba(255,255,255,0.5);
    margin-right: 10px;
}
QComboBox QAbstractItemView {
    background-color: #141418;
    color: #e8e8ec;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
    padding: 4px;
    selection-background-color: rgba(255,255,255,0.12);
}

/* SpinBox arrows */
QSpinBox::up-button, QDoubleSpinBox::up-button {
    subcontrol-origin: border; subcontrol-position: top right;
    width: 24px; border: none;
    background: rgba(255,255,255,0.05);
    border-top-right-radius: 9px;
}
QSpinBox::down-button, QDoubleSpinBox::down-button {
    subcontrol-origin: border; subcontrol-position: bottom right;
    width: 24px; border: none;
    background: rgba(255,255,255,0.05);
    border-bottom-right-radius: 9px;
}
QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {
    image: none; border-left: 4px solid transparent;
    border-right: 4px solid transparent; border-bottom: 5px solid rgba(255,255,255,0.5);
}
QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {
    image: none; border-left: 4px solid transparent;
    border-right: 4px solid transparent; border-top: 5px solid rgba(255,255,255,0.5);
}

/* Buttons - Glass */
QPushButton {
    background-color: rgba(255,255,255,0.06);
    color: #d0d0d8;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 9px;
    padding: 9px 20px;
    font-weight: 600;
    font-size: 13px;
    min-height: 26px;
}
QPushButton:hover {
    background-color: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    color: #ffffff;
}
QPushButton:pressed { background-color: rgba(255,255,255,0.15); }
QPushButton:disabled {
    background-color: rgba(255,255,255,0.02);
    color: rgba(255,255,255,0.2);
    border: 1px solid rgba(255,255,255,0.05);
}

/* Start Button */
QPushButton#startBtn {
    background: rgba(255,255,255,0.12);
    color: #ffffff;
    border: 1px solid rgba(255,255,255,0.25);
    font-weight: 700;
    padding: 12px 32px;
    font-size: 14px;
    border-radius: 11px;
}
QPushButton#startBtn:hover {
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.4);
}
QPushButton#startBtn:disabled {
    background: rgba(255,255,255,0.03);
    color: rgba(255,255,255,0.2);
    border: 1px solid rgba(255,255,255,0.06);
}

/* Stop Button */
QPushButton#stopBtn {
    background: rgba(255,255,255,0.06);
    color: #ff6b6b;
    border: 1px solid rgba(255,107,107,0.3);
    font-weight: 700;
    padding: 12px 32px;
    font-size: 14px;
    border-radius: 11px;
}
QPushButton#stopBtn:hover {
    background: rgba(255,107,107,0.12);
    border: 1px solid rgba(255,107,107,0.5);
}
QPushButton#stopBtn:disabled {
    background: rgba(255,255,255,0.03);
    color: rgba(255,255,255,0.2);
    border: 1px solid rgba(255,255,255,0.06);
}

/* Checkbox */
QCheckBox { color: #d0d0d8; spacing: 8px; }
QCheckBox::indicator {
    width: 20px; height: 20px;
    background-color: rgba(255,255,255,0.04);
    border: 1.5px solid rgba(255,255,255,0.2);
    border-radius: 5px;
}
QCheckBox::indicator:checked {
    background-color: rgba(255,255,255,0.9);
    border: 1.5px solid rgba(255,255,255,0.9);
}
QCheckBox::indicator:hover { border: 1.5px solid rgba(255,255,255,0.4); }

/* Tabs - Glass */
QTabWidget::pane {
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    background-color: rgba(255,255,255,0.02);
    top: -1px;
}
QTabBar::tab {
    background-color: transparent;
    color: rgba(255,255,255,0.4);
    padding: 12px 22px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    margin-right: 3px;
    border: 1px solid transparent;
    border-bottom: none;
    font-weight: 600;
    font-size: 13px;
}
QTabBar::tab:selected {
    background-color: rgba(255,255,255,0.05);
    color: #ffffff;
    border: 1px solid rgba(255,255,255,0.1);
    border-bottom: 2px solid rgba(255,255,255,0.6);
}
QTabBar::tab:hover:!selected {
    background-color: rgba(255,255,255,0.03);
    color: rgba(255,255,255,0.7);
}

/* Status Bar */
QStatusBar {
    background-color: rgba(255,255,255,0.02);
    color: rgba(255,255,255,0.4);
    border-top: 1px solid rgba(255,255,255,0.06);
    font-size: 12px;
    padding: 4px;
}

/* Table */
QTableWidget {
    background-color: rgba(255,255,255,0.02);
    alternate-background-color: rgba(255,255,255,0.04);
    gridline-color: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    font-size: 12px;
}
QTableWidget::item {
    padding: 7px 9px;
    color: #d0d0d8;
    border-bottom: 1px solid rgba(255,255,255,0.03);
}
QTableWidget::item:selected {
    background-color: rgba(255,255,255,0.1);
    color: #ffffff;
}
QHeaderView::section {
    background-color: rgba(255,255,255,0.04);
    color: rgba(255,255,255,0.7);
    padding: 9px;
    border: none;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    font-weight: 700;
    font-size: 12px;
}

/* Tooltip */
QToolTip {
    background-color: #1a1a20;
    color: #e8e8ec;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 7px;
    padding: 7px 11px;
    font-size: 12px;
}
"""


# ============================================================================
# Main Window
# ============================================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.db = DatabaseManager()
        self.config = self.load_config()
        self.github_fetcher = None
        self.init_ui()
        self.load_config_to_ui()

    def init_ui(self):
        self.setWindowTitle(f"TeleAI-AutoPoster {APP_VERSION}")
        self.setGeometry(100, 100, 1150, 780)
        self.setStyleSheet(GLASS_DARK_STYLE)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(14, 14, 14, 10)
        main_layout.setSpacing(12)

        # Header
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.07);
                border-radius: 14px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(22, 14, 22, 14)

        # Logo icon
        logo_label = QLabel()
        logo_label.setPixmap(SVGIcons.zap(26, "#ffffff").pixmap(26, 26))
        logo_label.setStyleSheet("background: transparent;")
        header_layout.addWidget(logo_label)

        title_label = QLabel("TeleAI-AutoPoster")
        title_label.setStyleSheet("font-size: 21px; font-weight: 800; color: #ffffff; background: transparent; letter-spacing: -0.3px;")
        header_layout.addWidget(title_label)

        ver_label = QLabel(APP_VERSION)
        ver_label.setStyleSheet("""
            font-size: 11px; font-weight: 700; color: rgba(255,255,255,0.9);
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 6px; padding: 3px 10px;
        """)
        header_layout.addWidget(ver_label)
        header_layout.addStretch()

        github_btn = QPushButton("  GitHub")
        github_btn.setIcon(SVGIcons.github(16, "#d0d0d8"))
        github_btn.setCursor(QCursor(Qt.PointingHandCursor))
        github_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.06);
                color: #d0d0d8;
                border: 1px solid rgba(255,255,255,0.12);
                border-radius: 9px;
                padding: 7px 16px;
                font-weight: 600; font-size: 12px;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.12);
                color: #ffffff;
                border: 1px solid rgba(255,255,255,0.25);
            }
        """)
        github_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(GITHUB_URL)))
        header_layout.addWidget(github_btn)

        main_layout.addWidget(header_frame)

        # Tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.settings_tab = QWidget()
        self.tabs.addTab(self.settings_tab, "  Settings")
        self.tabs.setTabIcon(0, SVGIcons.settings(16, "#d0d0d8"))
        self.create_settings_tab()

        self.content_tab = QWidget()
        self.tabs.addTab(self.content_tab, "  Content")
        self.tabs.setTabIcon(1, SVGIcons.edit(16, "#d0d0d8"))
        self.create_content_tab()

        self.manual_tab = QWidget()
        self.tabs.addTab(self.manual_tab, "  Manual")
        self.tabs.setTabIcon(2, SVGIcons.upload(16, "#d0d0d8"))
        self.create_manual_tab()

        self.control_tab = QWidget()
        self.tabs.addTab(self.control_tab, "  Control")
        self.tabs.setTabIcon(3, SVGIcons.terminal(16, "#d0d0d8"))
        self.create_control_tab()

        self.help_tab = QWidget()
        self.tabs.addTab(self.help_tab, "  Help")
        self.tabs.setTabIcon(4, SVGIcons.help(16, "#d0d0d8"))
        self.create_help_tab()

        self.about_tab = QWidget()
        self.tabs.addTab(self.about_tab, "  About")
        self.tabs.setTabIcon(5, SVGIcons.info(16, "#d0d0d8"))
        self.create_about_tab()

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(f"  TeleAI-AutoPoster {APP_VERSION}   |   Ready   |   github.com/{GITHUB_USERNAME}")

        self.ui_timer = QTimer()
        self.ui_timer.timeout.connect(self.update_ui_state)
        self.ui_timer.start(500)

    # ========================================================================
    # SETTINGS TAB
    # ========================================================================
    def create_settings_tab(self):
        layout = QVBoxLayout(self.settings_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(14)

        # OpenAI
        openai_group = QGroupBox("OpenAI Configuration")
        openai_layout = QFormLayout(openai_group)
        openai_layout.setSpacing(10)
        openai_layout.setContentsMargins(18, 26, 18, 18)

        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.setPlaceholderText("Enter your OpenAI API Key (sk-...)")
        openai_layout.addRow("API Key:", self.api_key_input)

        self.base_url_input = QLineEdit()
        self.base_url_input.setPlaceholderText("Custom Base URL (leave empty for default)")
        openai_layout.addRow("Base URL:", self.base_url_input)

        self.text_model_input = QLineEdit()
        self.text_model_input.setPlaceholderText("e.g., gpt-4o, gpt-4o-mini, gpt-3.5-turbo")
        openai_layout.addRow("Text Model:", self.text_model_input)

        self.image_model_input = QLineEdit()
        self.image_model_input.setPlaceholderText("e.g., dall-e-3, dall-e-2 (empty to disable)")
        openai_layout.addRow("Image Model:", self.image_model_input)

        scroll_layout.addWidget(openai_group)

        # Telegram
        telegram_group = QGroupBox("Telegram Configuration")
        telegram_layout = QFormLayout(telegram_group)
        telegram_layout.setSpacing(10)
        telegram_layout.setContentsMargins(18, 26, 18, 18)

        self.telegram_token = QLineEdit()
        self.telegram_token.setPlaceholderText("Bot Token from @BotFather")
        telegram_layout.addRow("Bot Token:", self.telegram_token)

        self.telegram_channel = QLineEdit()
        self.telegram_channel.setPlaceholderText("@your_channel or -100xxxxxxxxxx")
        telegram_layout.addRow("Channel ID:", self.telegram_channel)

        scroll_layout.addWidget(telegram_group)

        # Timing
        timing_group = QGroupBox("Timing Configuration")
        timing_layout = QFormLayout(timing_group)
        timing_layout.setSpacing(10)
        timing_layout.setContentsMargins(18, 26, 18, 18)

        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 1440)
        self.interval_spin.setValue(5)
        self.interval_spin.setSuffix("  minutes")
        timing_layout.addRow("Post Interval:", self.interval_spin)

        timing_info = QLabel("The agent generates and posts content at this interval continuously until stopped.")
        timing_info.setWordWrap(True)
        timing_info.setStyleSheet("color: rgba(255,255,255,0.35); font-size: 11px; padding: 4px 0;")
        timing_layout.addRow("", timing_info)

        scroll_layout.addWidget(timing_group)

        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        save_btn = QPushButton("  Save Settings")
        save_btn.setIcon(SVGIcons.save(15, "#d0d0d8"))
        save_btn.clicked.connect(self.save_config_from_ui)
        buttons_layout.addWidget(save_btn)

        load_btn = QPushButton("  Reload")
        load_btn.setIcon(SVGIcons.refresh(15, "#d0d0d8"))
        load_btn.clicked.connect(self.load_config_to_ui)
        buttons_layout.addWidget(load_btn)

        reset_btn = QPushButton("  Reset")
        reset_btn.setIcon(SVGIcons.reset(15, "#d0d0d8"))
        reset_btn.clicked.connect(self.reset_to_default)
        buttons_layout.addWidget(reset_btn)

        buttons_layout.addStretch()
        scroll_layout.addLayout(buttons_layout)
        scroll_layout.addStretch()

        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

    # ========================================================================
    # CONTENT TAB
    # ========================================================================
    def create_content_tab(self):
        layout = QVBoxLayout(self.content_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(14)

        topic_group = QGroupBox("Topic & Rules")
        topic_layout = QFormLayout(topic_group)
        topic_layout.setSpacing(10)
        topic_layout.setContentsMargins(18, 26, 18, 18)

        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("Enter main content topic...")
        topic_layout.addRow("Topic:", self.topic_input)

        self.rules_input = QTextEdit()
        self.rules_input.setMaximumHeight(130)
        self.rules_input.setPlaceholderText("Content creation rules...")
        topic_layout.addRow("Rules:", self.rules_input)

        self.footer_input = QLineEdit()
        self.footer_input.setPlaceholderText("Optional footer appended to every post")
        topic_layout.addRow("Post Footer:", self.footer_input)

        scroll_layout.addWidget(topic_group)

        prompt_group = QGroupBox("Prompt Settings")
        prompt_layout = QFormLayout(prompt_group)
        prompt_layout.setSpacing(10)
        prompt_layout.setContentsMargins(18, 26, 18, 18)

        self.tone_combo = QComboBox()
        self.tone_combo.addItems(["formal", "friendly", "educational", "promotional", "humorous"])
        prompt_layout.addRow("Tone:", self.tone_combo)

        self.audience_combo = QComboBox()
        self.audience_combo.addItems(["general", "professionals", "youth", "children", "seniors"])
        prompt_layout.addRow("Audience:", self.audience_combo)

        self.style_combo = QComboBox()
        self.style_combo.addItems(["educational", "narrative", "listicle", "analytical", "news"])
        prompt_layout.addRow("Style:", self.style_combo)

        self.required_keywords_input = QLineEdit()
        self.required_keywords_input.setPlaceholderText("Comma separated")
        prompt_layout.addRow("Required Keywords:", self.required_keywords_input)

        self.forbidden_keywords_input = QLineEdit()
        self.forbidden_keywords_input.setPlaceholderText("Comma separated")
        prompt_layout.addRow("Forbidden Words:", self.forbidden_keywords_input)

        self.temperature_spin = QDoubleSpinBox()
        self.temperature_spin.setRange(0.0, 2.0)
        self.temperature_spin.setSingleStep(0.1)
        self.temperature_spin.setValue(0.8)
        prompt_layout.addRow("Temperature:", self.temperature_spin)

        self.max_tokens_spin = QSpinBox()
        self.max_tokens_spin.setRange(100, 4096)
        self.max_tokens_spin.setValue(600)
        prompt_layout.addRow("Max Tokens:", self.max_tokens_spin)

        scroll_layout.addWidget(prompt_group)

        image_group = QGroupBox("Image Generation")
        image_layout = QFormLayout(image_group)
        image_layout.setSpacing(10)
        image_layout.setContentsMargins(18, 26, 18, 18)

        self.image_mode_combo = QComboBox()
        self.image_mode_combo.addItems(["Smart (AI decides)", "Always", "Never"])
        image_layout.addRow("Image Mode:", self.image_mode_combo)

        scroll_layout.addWidget(image_group)

        buttons_layout = QHBoxLayout()
        save_btn = QPushButton("  Save Settings")
        save_btn.setIcon(SVGIcons.save(15, "#d0d0d8"))
        save_btn.clicked.connect(self.save_config_from_ui)
        buttons_layout.addWidget(save_btn)
        buttons_layout.addStretch()
        scroll_layout.addLayout(buttons_layout)
        scroll_layout.addStretch()

        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

    # ========================================================================
    # MANUAL TAB
    # ========================================================================
    def create_manual_tab(self):
        layout = QVBoxLayout(self.manual_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)

        upload_group = QGroupBox("Upload New Content")
        upload_layout = QFormLayout(upload_group)
        upload_layout.setSpacing(10)
        upload_layout.setContentsMargins(18, 26, 18, 18)

        self.manual_text_input = QTextEdit()
        self.manual_text_input.setMaximumHeight(100)
        self.manual_text_input.setPlaceholderText("Enter content text...")
        upload_layout.addRow("Text:", self.manual_text_input)

        media_layout = QHBoxLayout()
        self.media_type_combo = QComboBox()
        self.media_type_combo.addItems(["No File", "Image", "Video", "Audio"])
        media_layout.addWidget(QLabel("Type:"))
        media_layout.addWidget(self.media_type_combo)

        self.media_path_input = QLineEdit()
        self.media_path_input.setReadOnly(True)
        self.media_path_input.setPlaceholderText("No file selected")
        media_layout.addWidget(self.media_path_input)

        browse_btn = QPushButton("  Browse")
        browse_btn.setIcon(SVGIcons.folder(14, "#d0d0d8"))
        browse_btn.clicked.connect(self.browse_media_file)
        media_layout.addWidget(browse_btn)
        upload_layout.addRow("File:", media_layout)

        schedule_layout = QHBoxLayout()
        self.schedule_date = QDateEdit()
        self.schedule_date.setCalendarPopup(True)
        self.schedule_date.setDate(QDate.currentDate())
        schedule_layout.addWidget(QLabel("Date:"))
        schedule_layout.addWidget(self.schedule_date)

        self.schedule_time = QTimeEdit()
        self.schedule_time.setTime(QTime.currentTime())
        schedule_layout.addWidget(QLabel("Time:"))
        schedule_layout.addWidget(self.schedule_time)
        schedule_layout.addStretch()
        upload_layout.addRow("Schedule:", schedule_layout)

        add_btn = QPushButton("  Add to Queue")
        add_btn.setIcon(SVGIcons.plus(15, "#d0d0d8"))
        add_btn.clicked.connect(self.add_manual_content)
        upload_layout.addRow("", add_btn)

        layout.addWidget(upload_group)

        queue_group = QGroupBox("Content Queue")
        queue_layout = QVBoxLayout(queue_group)
        queue_layout.setContentsMargins(18, 26, 18, 18)

        self.content_queue_table = QTableWidget()
        self.content_queue_table.setColumnCount(6)
        self.content_queue_table.setHorizontalHeaderLabels(["ID", "Type", "Text", "File", "Scheduled", "Actions"])
        self.content_queue_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.content_queue_table.setAlternatingRowColors(True)
        queue_layout.addWidget(self.content_queue_table)

        btn_layout = QHBoxLayout()
        refresh_btn = QPushButton("  Refresh")
        refresh_btn.setIcon(SVGIcons.refresh(14, "#d0d0d8"))
        refresh_btn.clicked.connect(self.refresh_content_queue)
        btn_layout.addWidget(refresh_btn)

        delete_btn = QPushButton("  Delete Selected")
        delete_btn.setIcon(SVGIcons.trash(14, "#d0d0d8"))
        delete_btn.clicked.connect(self.delete_selected_content)
        btn_layout.addWidget(delete_btn)
        btn_layout.addStretch()
        queue_layout.addLayout(btn_layout)

        layout.addWidget(queue_group)
        self.refresh_content_queue()

    # ========================================================================
    # CONTROL TAB
    # ========================================================================
    def create_control_tab(self):
        layout = QVBoxLayout(self.control_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        control_frame = QFrame()
        control_frame.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.02);
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 14px;
            }
        """)
        control_panel = QHBoxLayout(control_frame)
        control_panel.setContentsMargins(18, 14, 18, 14)

        self.start_btn = QPushButton("  Start")
        self.start_btn.setObjectName("startBtn")
        self.start_btn.setIcon(SVGIcons.play(16, "#ffffff"))
        self.start_btn.clicked.connect(self.start_agent)
        self.start_btn.setMinimumHeight(44)
        self.start_btn.setMinimumWidth(130)
        control_panel.addWidget(self.start_btn)

        self.stop_btn = QPushButton("  Stop")
        self.stop_btn.setObjectName("stopBtn")
        self.stop_btn.setIcon(SVGIcons.stop(16, "#ff6b6b"))
        self.stop_btn.clicked.connect(self.stop_agent)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setMinimumHeight(44)
        self.stop_btn.setMinimumWidth(130)
        control_panel.addWidget(self.stop_btn)

        self.clear_log_btn = QPushButton("  Clear")
        self.clear_log_btn.setIcon(SVGIcons.trash(14, "#d0d0d8"))
        self.clear_log_btn.clicked.connect(self.clear_log)
        self.clear_log_btn.setMinimumHeight(44)
        control_panel.addWidget(self.clear_log_btn)

        control_panel.addSpacing(20)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Level:"))
        self.log_level_filter = QComboBox()
        self.log_level_filter.addItems(["All", "INFO", "WARNING", "ERROR"])
        self.log_level_filter.currentTextChanged.connect(self.filter_logs)
        filter_layout.addWidget(self.log_level_filter)

        filter_layout.addWidget(QLabel("Category:"))
        self.log_category_filter = QComboBox()
        self.log_category_filter.addItems(["All", "SYSTEM", "OPENAI", "CONTENT", "IMAGE", "TELEGRAM", "SEND", "MANUAL", "STATS"])
        self.log_category_filter.currentTextChanged.connect(self.filter_logs)
        filter_layout.addWidget(self.log_category_filter)
        control_panel.addLayout(filter_layout)

        control_panel.addStretch()

        self.stats_label = QLabel("0 posts  |  0 images  |  $0.000000")
        self.stats_label.setStyleSheet("font-size: 13px; font-weight: 700; color: rgba(255,255,255,0.7); background: transparent;")
        control_panel.addWidget(self.stats_label)

        layout.addWidget(control_frame)

        log_header = QHBoxLayout()
        log_icon = QLabel()
        log_icon.setPixmap(SVGIcons.activity(16, "rgba(255,255,255,0.6)").pixmap(16, 16))
        log_header.addWidget(log_icon)
        log_label = QLabel("System Log")
        log_label.setStyleSheet("font-weight: 700; font-size: 14px; color: rgba(255,255,255,0.7);")
        log_header.addWidget(log_label)
        log_header.addStretch()
        layout.addLayout(log_header)

        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0,0,0,0.4);
                color: #d0d0d8;
                font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', 'Consolas', monospace;
                font-size: 12px;
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 12px;
                padding: 12px;
            }
        """)
        layout.addWidget(self.log_display)

        bottom_frame = QFrame()
        bottom_frame.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.02);
                border: 1px solid rgba(255,255,255,0.05);
                border-radius: 10px;
            }
        """)
        bottom_status = QHBoxLayout(bottom_frame)
        bottom_status.setContentsMargins(14, 9, 14, 9)

        self.status_label = QLabel("Status: Ready")
        self.status_label.setStyleSheet("font-size: 13px; font-weight: 700; color: rgba(255,255,255,0.6); background: transparent;")
        bottom_status.addWidget(self.status_label)
        bottom_status.addStretch()

        version_label = QLabel(f"TeleAI-AutoPoster {APP_VERSION}  ·  github.com/{GITHUB_USERNAME}")
        version_label.setStyleSheet("font-size: 11px; color: rgba(255,255,255,0.25); background: transparent;")
        bottom_status.addWidget(version_label)
        layout.addWidget(bottom_frame)

    # ========================================================================
    # HELP TAB
    # ========================================================================
    def create_help_tab(self):
        layout = QVBoxLayout(self.help_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(4, 4, 4, 4)

        help_content = """
<div style="font-family: 'Segoe UI', sans-serif; color: #d0d0d8; line-height: 1.9; padding: 12px;">

<h2 style="color: #ffffff; font-size: 20px; margin-bottom: 2px; font-weight: 800;">TeleAI-AutoPoster — User Guide</h2>
<p style="color: rgba(255,255,255,0.35); font-size: 12px; margin-top: 0;">Version v1.0.2 &nbsp;·&nbsp; Developer: BSHF-PER</p>

<hr style="border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 18px 0;">

<h3 style="color: rgba(255,255,255,0.9); font-size: 15px;">1. Getting Started</h3>
<p>TeleAI-AutoPoster is an intelligent Telegram content automation tool. It uses OpenAI-compatible 
APIs to generate text and image content, then automatically publishes them to your Telegram channel 
at regular intervals.</p>

<h3 style="color: rgba(255,255,255,0.9); font-size: 15px;">2. Settings Tab</h3>
<table style="width: 100%; border-collapse: collapse; margin: 8px 0;">
<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
<td style="padding: 9px; color: rgba(255,255,255,0.7); font-weight: 600; width: 150px;">API Key</td>
<td style="padding: 9px;">Your OpenAI API key (starts with sk-). Required for all AI operations.</td>
</tr>
<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
<td style="padding: 9px; color: rgba(255,255,255,0.7); font-weight: 600;">Base URL</td>
<td style="padding: 9px;">Optional custom API endpoint for OpenAI-compatible services. Leave empty for official API.</td>
</tr>
<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
<td style="padding: 9px; color: rgba(255,255,255,0.7); font-weight: 600;">Text Model</td>
<td style="padding: 9px;">Model for text generation: <code style="background: rgba(255,255,255,0.06); padding: 2px 7px; border-radius: 4px; font-size: 12px;">gpt-4o</code>, <code style="background: rgba(255,255,255,0.06); padding: 2px 7px; border-radius: 4px; font-size: 12px;">gpt-4o-mini</code>, <code style="background: rgba(255,255,255,0.06); padding: 2px 7px; border-radius: 4px; font-size: 12px;">gpt-3.5-turbo</code></td>
</tr>
<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
<td style="padding: 9px; color: rgba(255,255,255,0.7); font-weight: 600;">Image Model</td>
<td style="padding: 9px;">Model for image generation: <code style="background: rgba(255,255,255,0.06); padding: 2px 7px; border-radius: 4px; font-size: 12px;">dall-e-3</code>, <code style="background: rgba(255,255,255,0.06); padding: 2px 7px; border-radius: 4px; font-size: 12px;">dall-e-2</code>. Empty to disable.</td>
</tr>
<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
<td style="padding: 9px; color: rgba(255,255,255,0.7); font-weight: 600;">Bot Token</td>
<td style="padding: 9px;">Telegram Bot token from <b>@BotFather</b>.</td>
</tr>
<tr>
<td style="padding: 9px; color: rgba(255,255,255,0.7); font-weight: 600;">Channel ID</td>
<td style="padding: 9px;">Channel username (@my_channel) or numeric ID (-1001234567890). Bot must be admin.</td>
</tr>
</table>

<h3 style="color: rgba(255,255,255,0.9); font-size: 15px;">3. Timing</h3>
<p>Set the <b>Post Interval</b> in minutes. When you press <b>Start</b>, the agent will:</p>
<ol style="margin-left: 10px;">
<li>Generate AI content (text + optional image)</li>
<li>Publish to your Telegram channel</li>
<li>Wait for the specified interval</li>
<li>Repeat until you press <b>Stop</b></li>
</ol>
<p style="color: rgba(255,255,255,0.35); font-size: 12px;">Example: 60 minutes = one post every hour, continuously.</p>

<h3 style="color: rgba(255,255,255,0.9); font-size: 15px;">4. Content Tab</h3>
<ul style="margin-left: 10px;">
<li><b>Topic:</b> Main subject for AI-generated content.</li>
<li><b>Rules:</b> Detailed instructions for the AI writer.</li>
<li><b>Post Footer:</b> Optional text appended to every post.</li>
<li><b>Tone / Audience / Style:</b> Fine-tune writing approach.</li>
<li><b>Temperature:</b> Creativity control (0.0 = deterministic, 2.0 = creative).</li>
<li><b>Image Mode:</b> Smart (AI decides), Always, or Never.</li>
</ul>

<h3 style="color: rgba(255,255,255,0.9); font-size: 15px;">5. Manual Content</h3>
<p>Add content manually with optional media files. Scheduled manual content is sent before AI content in each cycle.</p>

<h3 style="color: rgba(255,255,255,0.9); font-size: 15px;">6. Control & Log</h3>
<ul style="margin-left: 10px;">
<li><b>Start:</b> Begins the continuous posting loop.</li>
<li><b>Stop:</b> Gracefully stops the agent.</li>
<li><b>Clear:</b> Clears the visible log display.</li>
<li><b>Filters:</b> Filter logs by level or category.</li>
</ul>

<h3 style="color: rgba(255,255,255,0.9); font-size: 15px;">7. Troubleshooting</h3>
<table style="width: 100%; border-collapse: collapse; margin: 8px 0;">
<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
<td style="padding: 9px; color: #ff6b6b; font-weight: 600; width: 190px;">API Key invalid</td>
<td style="padding: 9px;">Check your API key. Ensure it starts with sk- and has credits.</td>
</tr>
<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
<td style="padding: 9px; color: #ff6b6b; font-weight: 600;">Telegram: Error 403</td>
<td style="padding: 9px;">Bot is not admin of the channel, or channel ID is wrong.</td>
</tr>
<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
<td style="padding: 9px; color: #ff6b6b; font-weight: 600;">Model not found</td>
<td style="padding: 9px;">Verify model name. Use exact names like gpt-4o, dall-e-3.</td>
</tr>
<tr>
<td style="padding: 9px; color: #ff6b6b; font-weight: 600;">No image generated</td>
<td style="padding: 9px;">Ensure Image Model is set. Verify Base URL supports images API.</td>
</tr>
</table>

<hr style="border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 18px 0;">
<p style="color: rgba(255,255,255,0.25); font-size: 11px; text-align: center;">
TeleAI-AutoPoster v1.0.2 &nbsp;·&nbsp; OpenAI API &nbsp;·&nbsp; 
<a href="https://github.com/BSHF-PER" style="color: rgba(255,255,255,0.5);">github.com/BSHF-PER</a>
</p>
</div>
"""
        help_display = QTextEdit()
        help_display.setReadOnly(True)
        help_display.setHtml(help_content)
        help_display.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255,255,255,0.02);
                border: 1px solid rgba(255,255,255,0.05);
                border-radius: 12px;
                padding: 10px;
            }
        """)
        scroll_layout.addWidget(help_display)
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

    # ========================================================================
    # ABOUT TAB
    # ========================================================================
    def create_about_tab(self):
        layout = QVBoxLayout(self.about_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(16)
        scroll_layout.setContentsMargins(20, 20, 20, 20)

        # Title Card
        title_card = QFrame()
        title_card.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 18px;
            }
        """)
        title_card_layout = QVBoxLayout(title_card)
        title_card_layout.setContentsMargins(30, 35, 30, 35)
        title_card_layout.setAlignment(Qt.AlignCenter)

        app_icon_label = QLabel()
        app_icon_label.setPixmap(SVGIcons.zap(48, "#ffffff").pixmap(48, 48))
        app_icon_label.setAlignment(Qt.AlignCenter)
        app_icon_label.setStyleSheet("background: transparent;")
        title_card_layout.addWidget(app_icon_label)

        app_name_label = QLabel("TeleAI-AutoPoster")
        app_name_label.setStyleSheet("font-size: 26px; font-weight: 800; color: #ffffff; background: transparent; letter-spacing: -0.5px; margin-top: 8px;")
        app_name_label.setAlignment(Qt.AlignCenter)
        title_card_layout.addWidget(app_name_label)

        app_ver_label = QLabel(APP_VERSION)
        app_ver_label.setStyleSheet("""
            font-size: 12px; font-weight: 700; color: rgba(255,255,255,0.8);
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 7px; padding: 4px 14px;
        """)
        app_ver_label.setAlignment(Qt.AlignCenter)
        app_ver_label.setFixedWidth(100)
        title_card_layout.addWidget(app_ver_label, alignment=Qt.AlignCenter)

        app_desc_label = QLabel(
            "\n\nIntelligent Telegram content automation powered by OpenAI.\n"
            "Generate AI text & images, auto-post to your channel on schedule.\n\n"
        )
        app_desc_label.setStyleSheet("font-size: 13px; color: rgba(255,255,255,0.4); background: transparent; margin-top: 10px;")
        app_desc_label.setAlignment(Qt.AlignCenter)
        app_desc_label.setWordWrap(True)
        title_card_layout.addWidget(app_desc_label)

        scroll_layout.addWidget(title_card)

        # Developer Profile Card
        dev_card = QGroupBox("Developer Profile")
        dev_card_layout = QVBoxLayout(dev_card)
        dev_card_layout.setContentsMargins(20, 30, 20, 20)
        dev_card_layout.setSpacing(14)

        self.github_profile_frame = QFrame()
        self.github_profile_frame.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.07);
                border-radius: 14px;
            }
        """)
        profile_layout = QHBoxLayout(self.github_profile_frame)
        profile_layout.setContentsMargins(18, 18, 18, 18)

        self.avatar_label = QLabel()
        self.avatar_label.setPixmap(SVGIcons.user(40, "rgba(255,255,255,0.3)").pixmap(40, 40))
        self.avatar_label.setStyleSheet("""
            background: rgba(255,255,255,0.04);
            border-radius: 32px;
            min-width: 64px; min-height: 64px;
            max-width: 64px; max-height: 64px;
        """)
        self.avatar_label.setAlignment(Qt.AlignCenter)
        profile_layout.addWidget(self.avatar_label)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        self.profile_name_label = QLabel("Loading profile...")
        self.profile_name_label.setStyleSheet("font-size: 17px; font-weight: 700; color: #ffffff; background: transparent;")
        info_layout.addWidget(self.profile_name_label)

        self.profile_username_label = QLabel(f"@{GITHUB_USERNAME}")
        self.profile_username_label.setStyleSheet("font-size: 13px; color: rgba(255,255,255,0.5); background: transparent;")
        info_layout.addWidget(self.profile_username_label)

        self.profile_bio_label = QLabel("")
        self.profile_bio_label.setStyleSheet("font-size: 12px; color: rgba(255,255,255,0.35); background: transparent;")
        self.profile_bio_label.setWordWrap(True)
        info_layout.addWidget(self.profile_bio_label)

        profile_layout.addLayout(info_layout)
        profile_layout.addStretch()
        dev_card_layout.addWidget(self.github_profile_frame)

        # Stats
        self.github_stats_frame = QFrame()
        self.github_stats_frame.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.02);
                border: 1px solid rgba(255,255,255,0.05);
                border-radius: 11px;
            }
        """)
        stats_row = QHBoxLayout(self.github_stats_frame)
        stats_row.setContentsMargins(14, 11, 14, 11)

        self.stat_repos = QLabel("Repos: —")
        self.stat_repos.setStyleSheet("font-size: 12px; color: rgba(255,255,255,0.6); font-weight: 600; background: transparent;")
        self.stat_repos.setAlignment(Qt.AlignCenter)
        stats_row.addWidget(self.stat_repos)

        sep1 = QFrame()
        sep1.setFrameShape(QFrame.VLine)
        sep1.setStyleSheet("color: rgba(255,255,255,0.08);")
        sep1.setFixedWidth(1)
        stats_row.addWidget(sep1)

        self.stat_followers = QLabel("Followers: —")
        self.stat_followers.setStyleSheet("font-size: 12px; color: rgba(255,255,255,0.6); font-weight: 600; background: transparent;")
        self.stat_followers.setAlignment(Qt.AlignCenter)
        stats_row.addWidget(self.stat_followers)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.VLine)
        sep2.setStyleSheet("color: rgba(255,255,255,0.08);")
        sep2.setFixedWidth(1)
        stats_row.addWidget(sep2)

        self.stat_following = QLabel("Following: —")
        self.stat_following.setStyleSheet("font-size: 12px; color: rgba(255,255,255,0.6); font-weight: 600; background: transparent;")
        self.stat_following.setAlignment(Qt.AlignCenter)
        stats_row.addWidget(self.stat_following)

        sep3 = QFrame()
        sep3.setFrameShape(QFrame.VLine)
        sep3.setStyleSheet("color: rgba(255,255,255,0.08);")
        sep3.setFixedWidth(1)
        stats_row.addWidget(sep3)

        self.stat_joined = QLabel("Joined: —")
        self.stat_joined.setStyleSheet("font-size: 12px; color: rgba(255,255,255,0.6); font-weight: 600; background: transparent;")
        self.stat_joined.setAlignment(Qt.AlignCenter)
        stats_row.addWidget(self.stat_joined)

        dev_card_layout.addWidget(self.github_stats_frame)

        # Buttons
        gh_btn_layout = QHBoxLayout()

        gh_profile_btn = QPushButton("  Open GitHub Profile")
        gh_profile_btn.setIcon(SVGIcons.external_link(14, "#ffffff"))
        gh_profile_btn.setCursor(QCursor(Qt.PointingHandCursor))
        gh_profile_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.1);
                color: #ffffff;
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 9px;
                padding: 10px 22px;
                font-weight: 700; font-size: 13px;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.16);
                border: 1px solid rgba(255,255,255,0.35);
            }
        """)
        gh_profile_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(GITHUB_URL)))
        gh_btn_layout.addWidget(gh_profile_btn)

        refresh_btn = QPushButton("  Refresh")
        refresh_btn.setIcon(SVGIcons.refresh(14, "#d0d0d8"))
        refresh_btn.clicked.connect(self.fetch_github_profile)
        gh_btn_layout.addWidget(refresh_btn)

        gh_btn_layout.addStretch()
        dev_card_layout.addLayout(gh_btn_layout)

        scroll_layout.addWidget(dev_card)

        # Footer
        footer_label = QLabel(
            f"TeleAI-AutoPoster {APP_VERSION}  ·  © 2026 Behzad Shahbazi Fard  ·  "
            f'<a href="{GITHUB_URL}" style="color: rgba(255,255,255,0.4);">{GITHUB_URL}</a>'
        )
        footer_label.setOpenExternalLinks(True)
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("font-size: 12px; color: rgba(255,255,255,0.25); padding: 12px;")
        scroll_layout.addWidget(footer_label)
        scroll_layout.addStretch()

        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

        QTimer.singleShot(500, self.fetch_github_profile)

    def fetch_github_profile(self):
        self.profile_name_label.setText("Loading profile...")
        self.profile_name_label.setStyleSheet("font-size: 17px; font-weight: 700; color: rgba(255,255,255,0.4); background: transparent;")
        self.github_fetcher = GitHubProfileFetcher(GITHUB_USERNAME)
        self.github_fetcher.profile_loaded.connect(self.on_github_profile_loaded)
        self.github_fetcher.profile_error.connect(self.on_github_profile_error)
        self.github_fetcher.start()

    def on_github_profile_loaded(self, data):
        name = data.get('name') or data.get('login', GITHUB_USERNAME)
        login = data.get('login', GITHUB_USERNAME)
        bio = data.get('bio') or ''
        avatar_url = data.get('avatar_url', '')
        repos = data.get('public_repos', 0)
        followers = data.get('followers', 0)
        following = data.get('following', 0)
        created = data.get('created_at', '')

        self.profile_name_label.setText(name)
        self.profile_name_label.setStyleSheet("font-size: 17px; font-weight: 700; color: #ffffff; background: transparent;")
        self.profile_username_label.setText(f"@{login}")

        bio_text = bio
        if created:
            try:
                created_date = datetime.fromisoformat(created.replace('Z', '+00:00')).strftime('%B %Y')
                bio_text += f"\nJoined GitHub: {created_date}" if bio_text else f"Joined GitHub: {created_date}"
            except:
                pass
        self.profile_bio_label.setText(bio_text)

        self.stat_repos.setText(f"Repos: {repos}")
        self.stat_followers.setText(f"Followers: {followers}")
        self.stat_following.setText(f"Following: {following}")
        if created:
            try:
                self.stat_joined.setText(f"Joined: {datetime.fromisoformat(created.replace('Z', '+00:00')).strftime('%b %Y')}")
            except:
                self.stat_joined.setText("Joined: —")

        if avatar_url:
            threading.Thread(target=self._download_avatar, args=(avatar_url,), daemon=True).start()

    def on_github_profile_error(self, error):
        self.profile_name_label.setText("Behzad Shahbazi Fard")
        self.profile_name_label.setStyleSheet("font-size: 17px; font-weight: 700; color: #ffffff; background: transparent;")
        self.profile_bio_label.setText(f"Could not load profile: {error}")

    def _download_avatar(self, url):
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(resp.content)
                scaled = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                QTimer.singleShot(0, lambda: self._set_avatar(scaled))
        except:
            pass

    def _set_avatar(self, pixmap):
        self.avatar_label.setPixmap(pixmap)
        self.avatar_label.setStyleSheet("""
            background: rgba(255,255,255,0.04);
            border-radius: 32px;
            min-width: 64px; min-height: 64px;
            max-width: 64px; max-height: 64px;
        """)

    # ========================================================================
    # Config Methods
    # ========================================================================
    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                merged = DEFAULT_CONFIG.copy()
                merged.update(config)
                return merged
            except:
                return DEFAULT_CONFIG.copy()
        return DEFAULT_CONFIG.copy()

    def save_config(self, config):
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save configuration:\n{e}")
            return False

    def load_config_to_ui(self):
        self.config = self.load_config()
        self.api_key_input.setText(self.config.get("OPENAI_API_KEY", ""))
        self.base_url_input.setText(self.config.get("OPENAI_BASE_URL", ""))
        self.text_model_input.setText(self.config.get("TEXT_MODEL", ""))
        self.image_model_input.setText(self.config.get("IMAGE_MODEL", ""))
        self.telegram_token.setText(self.config["TELEGRAM"]["bot_token"])
        self.telegram_channel.setText(self.config["TELEGRAM"]["channel_id"])
        self.interval_spin.setValue(self.config.get("INTERVAL_MINUTES", 5))
        self.topic_input.setText(self.config.get("WORK_TOPIC", ""))
        self.rules_input.setPlainText(self.config.get("CONTENT_RULES", ""))
        self.footer_input.setText(self.config.get("POST_FOOTER", ""))
        ps = self.config.get('prompt_settings', {})
        self.tone_combo.setCurrentText(ps.get('tone', 'formal'))
        self.audience_combo.setCurrentText(ps.get('target_audience', 'general'))
        self.style_combo.setCurrentText(ps.get('style', 'educational'))
        self.required_keywords_input.setText(', '.join(ps.get('required_keywords', [])))
        self.forbidden_keywords_input.setText(', '.join(ps.get('forbidden_keywords', [])))
        self.temperature_spin.setValue(ps.get('temperature', 0.8))
        self.max_tokens_spin.setValue(ps.get('max_tokens', 600))
        im = self.config.get('image_mode', 'smart')
        self.image_mode_combo.setCurrentIndex({'smart': 0, 'always': 1, 'never': 2}.get(im, 0))
        self.add_log("INFO", "SYSTEM", "Configuration loaded successfully")

    def save_config_from_ui(self):
        image_mode_map = {0: 'smart', 1: 'always', 2: 'never'}
        self.config = {
            "OPENAI_API_KEY": self.api_key_input.text().strip(),
            "OPENAI_BASE_URL": self.base_url_input.text().strip(),
            "TEXT_MODEL": self.text_model_input.text().strip(),
            "IMAGE_MODEL": self.image_model_input.text().strip(),
            "TELEGRAM": {"bot_token": self.telegram_token.text().strip(), "channel_id": self.telegram_channel.text().strip()},
            "WORK_TOPIC": self.topic_input.text(),
            "CONTENT_RULES": self.rules_input.toPlainText(),
            "INTERVAL_MINUTES": self.interval_spin.value(),
            "POST_FOOTER": self.footer_input.text(),
            "prompt_settings": {
                "tone": self.tone_combo.currentText(),
                "target_audience": self.audience_combo.currentText(),
                "style": self.style_combo.currentText(),
                "required_keywords": [k.strip() for k in self.required_keywords_input.text().split(',') if k.strip()],
                "forbidden_keywords": [k.strip() for k in self.forbidden_keywords_input.text().split(',') if k.strip()],
                "temperature": self.temperature_spin.value(),
                "max_tokens": self.max_tokens_spin.value()},
            "image_mode": image_mode_map.get(self.image_mode_combo.currentIndex(), 'smart')
        }
        if self.save_config(self.config):
            self.add_log("INFO", "SYSTEM", "Configuration saved successfully")
            QMessageBox.information(self, "Success", "Settings saved successfully!")

    def reset_to_default(self):
        reply = QMessageBox.question(self, "Confirm Reset", "Reset all settings to default?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.config = DEFAULT_CONFIG.copy()
            self.save_config(self.config)
            self.load_config_to_ui()

    # ========================================================================
    # Manual Content
    # ========================================================================
    def browse_media_file(self):
        media_type = self.media_type_combo.currentText()
        filters = {"Image": "Images (*.jpg *.jpeg *.png *.gif *.bmp *.webp)",
                   "Video": "Videos (*.mp4 *.avi *.mkv *.mov)",
                   "Audio": "Audio (*.mp3 *.wav *.ogg *.m4a)"}
        file_filter = filters.get(media_type, "All Files (*.*)")
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", file_filter)
        if file_path:
            self.media_path_input.setText(file_path)

    def add_manual_content(self):
        text = self.manual_text_input.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Error", "Please enter content text!")
            return
        media_type_map = {"No File": "text", "Image": "photo", "Video": "video", "Audio": "audio"}
        media_type = media_type_map.get(self.media_type_combo.currentText(), "text")
        media_path = self.media_path_input.text()
        if media_type != "text" and not media_path:
            QMessageBox.warning(self, "Error", "Please select a file!")
            return
        schedule_dt = QDateTime(self.schedule_date.date(), self.schedule_time.time()).toPyDateTime()
        content_data = {'content_type': 'manual', 'text_content': text, 'media_type': media_type,
                       'media_path': media_path, 'scheduled_time': schedule_dt.isoformat(),
                       'platforms': ['telegram'], 'priority': 0}
        content_id = self.db.add_to_queue(content_data)
        if content_id > 0:
            QMessageBox.information(self, "Success", f"Content added with ID {content_id}!")
            self.manual_text_input.clear()
            self.media_path_input.clear()
            self.refresh_content_queue()

    def refresh_content_queue(self):
        pending = self.db.get_pending_content(limit=50)
        self.content_queue_table.setRowCount(0)
        for content in pending:
            row = self.content_queue_table.rowCount()
            self.content_queue_table.insertRow(row)
            self.content_queue_table.setItem(row, 0, QTableWidgetItem(str(content['id'])))
            self.content_queue_table.setItem(row, 1, QTableWidgetItem(content['content_type']))
            text_preview = content['text_content'][:50] + "..." if len(content['text_content']) > 50 else content['text_content']
            self.content_queue_table.setItem(row, 2, QTableWidgetItem(text_preview))
            media_info = f"{content['media_type']}: {os.path.basename(content['media_path'])}" if content['media_path'] else "—"
            self.content_queue_table.setItem(row, 3, QTableWidgetItem(media_info))
            try:
                st = datetime.fromisoformat(content['scheduled_time']).strftime('%Y-%m-%d %H:%M')
            except:
                st = content['scheduled_time']
            self.content_queue_table.setItem(row, 4, QTableWidgetItem(st))
            delete_btn = QPushButton()
            delete_btn.setIcon(SVGIcons.trash(14, "#ff6b6b"))
            delete_btn.setFixedWidth(36)
            delete_btn.setStyleSheet("QPushButton { border: none; background: transparent; padding: 4px; } QPushButton:hover { background: rgba(255,107,107,0.1); border-radius: 6px; }")
            delete_btn.clicked.connect(lambda checked, cid=content['id']: self.delete_content_item(cid))
            self.content_queue_table.setCellWidget(row, 5, delete_btn)

    def delete_content_item(self, content_id):
        reply = QMessageBox.question(self, "Confirm", f"Delete content ID {content_id}?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.delete_content(content_id)
            self.refresh_content_queue()

    def delete_selected_content(self):
        selected_rows = set(item.row() for item in self.content_queue_table.selectedItems())
        if not selected_rows:
            QMessageBox.warning(self, "Error", "Select at least one row!")
            return
        reply = QMessageBox.question(self, "Confirm", f"Delete {len(selected_rows)} items?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            for row in sorted(selected_rows, reverse=True):
                self.db.delete_content(int(self.content_queue_table.item(row, 0).text()))
            self.refresh_content_queue()

    # ========================================================================
    # Agent Control
    # ========================================================================
    def start_agent(self):
        self.save_config_from_ui()
        if not self.config["OPENAI_API_KEY"]:
            QMessageBox.critical(self, "Error", "Please enter your OpenAI API Key!")
            return
        if not self.config["TEXT_MODEL"]:
            QMessageBox.critical(self, "Error", "Please specify a Text Model!")
            return
        if not self.config["TELEGRAM"]["bot_token"] or not self.config["TELEGRAM"]["channel_id"]:
            QMessageBox.critical(self, "Error", "Please configure Telegram Bot Token and Channel ID!")
            return
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_label.setText("Status: Running")
        self.status_label.setStyleSheet("font-size: 13px; font-weight: 700; color: rgba(255,255,255,0.9); background: transparent;")
        self.worker = AgentWorker(self.config, self.db)
        self.worker.signals.log_message.connect(self.add_log)
        self.worker.signals.stats_update.connect(self.update_stats)
        self.worker.signals.finished.connect(self.on_agent_finished)
        self.worker.signals.error.connect(self.on_agent_error)
        self.worker.start()
        self.add_log("INFO", "SYSTEM", f"Agent started | Interval: {self.config['INTERVAL_MINUTES']} min")

    def stop_agent(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait(10000)
            self.add_log("WARNING", "SYSTEM", "Agent stopped by user")
        self.on_agent_finished()

    def on_agent_finished(self):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText("Status: Ready")
        self.status_label.setStyleSheet("font-size: 13px; font-weight: 700; color: rgba(255,255,255,0.6); background: transparent;")
        self.worker = None

    def on_agent_error(self, error_msg):
        QMessageBox.critical(self, "Agent Error", f"Error:\n{error_msg}")
        self.on_agent_finished()

    def update_ui_state(self):
        if self.worker and self.worker.isRunning():
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
        elif not self.worker:
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)

    # ========================================================================
    # Log
    # ========================================================================
    def add_log(self, level, category, message):
        color_map = {"INFO": "#d0d0d8", "WARNING": "#ffd93d", "ERROR": "#ff6b6b"}
        color = color_map.get(level, "#d0d0d8")
        self.log_display.append(f'<span style="color: {color};">{message}</span>')
        cursor = self.log_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.log_display.setTextCursor(cursor)

    def filter_logs(self):
        level_filter = self.log_level_filter.currentText()
        category_filter = self.log_category_filter.currentText()
        if level_filter == "All": level_filter = None
        if category_filter == "All": category_filter = None
        logs = self.db.get_logs(level_filter, category_filter, limit=200)
        self.log_display.clear()
        for log in reversed(logs):
            ts = datetime.fromisoformat(log['timestamp']).strftime("%H:%M:%S")
            self.add_log(log['level'], log['category'], f"[{ts}] [{log['level']}] [{log['category']}] {log['message']}")

    def clear_log(self):
        self.log_display.clear()
        self.add_log("INFO", "SYSTEM", "Log cleared")

    def update_stats(self, stats):
        self.stats_label.setText(f"{stats['total_posts']} posts  |  {stats['total_images']} images  |  ${stats['total_cost']:.6f}")

    def closeEvent(self, event):
        if self.worker and self.worker.isRunning():
            reply = QMessageBox.question(self, "Confirm Exit", "Agent is running. Exit anyway?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.stop_agent()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


# ============================================================================
# Entry Point
# ============================================================================
def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setFont(QFont("Segoe UI", 10))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()