#!/usr/bin/env python3
"""
Linux Store - Main Window
الواجهة الرسومية الرئيسية
"""

import sys
import os
from typing import Optional, List

# محاولة استخدام PyQt6 أو PyQt5
try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QPushButton, QLineEdit, QScrollArea, QFrame,
        QGridLayout, QStackedWidget, QProgressBar, QMessageBox,
        QSizePolicy, QSpacerItem, QComboBox, QToolButton
    )
    from PyQt6.QtCore import Qt, QSize, QThread, pyqtSignal, QTimer
    from PyQt6.QtGui import QIcon, QPixmap, QFont, QPalette, QColor, QCursor
    PYQT_VERSION = 6
except ImportError:
    try:
        from PyQt5.QtWidgets import (
            QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
            QLabel, QPushButton, QLineEdit, QScrollArea, QFrame,
            QGridLayout, QStackedWidget, QProgressBar, QMessageBox,
            QSizePolicy, QSpacerItem, QComboBox, QToolButton
        )
        from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal, QTimer
        from PyQt5.QtGui import QIcon, QPixmap, QFont, QPalette, QColor, QCursor
        PYQT_VERSION = 5
    except ImportError:
        print("خطأ: يرجى تثبيت PyQt6 أو PyQt5")
        print("pip install PyQt6")
        sys.exit(1)

from distro_detector import DistroDetector
from package_manager import PackageManager, AsyncPackageManager, PackageInfo
from app_database import AppDatabase, AppEntry


class InstallThread(QThread):
    """خيط التثبيت"""
    progress = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)
    
    def __init__(self, pkg_manager, app_entry, action='install'):
        super().__init__()
        self.pkg_manager = pkg_manager
        self.app_entry = app_entry
        self.action = action
    
    def run(self):
        try:
            # إنشاء PackageInfo من AppEntry
            pkg_info = PackageInfo(
                name=self.app_entry.id,
                display_name=self.app_entry.name,
                description=self.app_entry.description,
                category=self.app_entry.category,
                icon=self.app_entry.icon,
                package_names={
                    'pacman': self.app_entry.pacman,
                    'apt': self.app_entry.apt,
                    'dnf': self.app_entry.dnf,
                    'zypper': self.app_entry.zypper,
                },
                flatpak_id=self.app_entry.flatpak,
                snap_name=self.app_entry.snap,
            )
            
            if self.action == 'install':
                success = self.pkg_manager.install_package(pkg_info)
            else:
                success = self.pkg_manager.remove_package(pkg_info)
            
            self.finished_signal.emit(success, self.app_entry.name)
        except Exception as e:
            self.finished_signal.emit(False, str(e))


class AppCard(QFrame):
    """بطاقة التطبيق"""
    
    clicked = pyqtSignal(object)
    install_clicked = pyqtSignal(object)
    
    def __init__(self, app_entry: AppEntry, is_installed: bool = False, parent=None):
        super().__init__(parent)
        self.app_entry = app_entry
        self.is_installed = is_installed
        self._setup_ui()
    
    def _setup_ui(self):
        self.setObjectName("appCard")
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor if PYQT_VERSION == 6 else Qt.PointingHandCursor))
        self.setFixedSize(180, 220)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # أيقونة التطبيق
        icon_label = QLabel()
        icon_label.setFixedSize(64, 64)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        icon_label.setObjectName("appIcon")
        
        # محاولة تحميل الأيقونة
        icon_path = self._get_icon_path()
        if icon_path and os.path.exists(icon_path):
            pixmap = QPixmap(icon_path).scaled(64, 64, 
                Qt.AspectRatioMode.KeepAspectRatio if PYQT_VERSION == 6 else Qt.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation if PYQT_VERSION == 6 else Qt.SmoothTransformation)
            icon_label.setPixmap(pixmap)
        else:
            # أيقونة افتراضية نصية
            icon_label.setText(self.app_entry.name[0].upper())
            icon_label.setStyleSheet("""
                QLabel {
                    background-color: #4285f4;
                    color: white;
                    border-radius: 12px;
                    font-size: 28px;
                    font-weight: bold;
                }
            """)
        
        layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        
        # اسم التطبيق
        name_label = QLabel(self.app_entry.name)
        name_label.setObjectName("appName")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        name_label.setWordWrap(True)
        layout.addWidget(name_label)
        
        # الوصف المختصر
        desc_label = QLabel(self.app_entry.description_ar[:50] + "..." if len(self.app_entry.description_ar) > 50 else self.app_entry.description_ar)
        desc_label.setObjectName("appDesc")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        layout.addStretch()
        
        # زر التثبيت/الإزالة
        self.action_btn = QPushButton("إزالة" if self.is_installed else "تثبيت")
        self.action_btn.setObjectName("installBtn" if not self.is_installed else "removeBtn")
        self.action_btn.clicked.connect(lambda: self.install_clicked.emit(self.app_entry))
        layout.addWidget(self.action_btn)
    
    def _get_icon_path(self) -> Optional[str]:
        """الحصول على مسار الأيقونة"""
        icon_dirs = [
            '/usr/share/icons/hicolor/64x64/apps',
            '/usr/share/icons/hicolor/48x48/apps',
            '/usr/share/icons/hicolor/scalable/apps',
            '/usr/share/pixmaps',
            os.path.join(os.path.dirname(__file__), '..', 'icons'),
        ]
        
        extensions = ['.png', '.svg', '.xpm', '']
        
        for icon_dir in icon_dirs:
            for ext in extensions:
                path = os.path.join(icon_dir, f"{self.app_entry.icon}{ext}")
                if os.path.exists(path):
                    return path
        
        return None
    
    def mousePressEvent(self, event):
        self.clicked.emit(self.app_entry)
        super().mousePressEvent(event)
    
    def update_status(self, is_installed: bool):
        """تحديث حالة التثبيت"""
        self.is_installed = is_installed
        self.action_btn.setText("إزالة" if is_installed else "تثبيت")
        self.action_btn.setObjectName("removeBtn" if is_installed else "installBtn")
        self.action_btn.setStyle(self.action_btn.style())


class CategoryButton(QPushButton):
    """زر التصنيف"""
    
    def __init__(self, category_id: str, category_info: dict, parent=None):
        super().__init__(parent)
        self.category_id = category_id
        self.category_info = category_info
        
        self.setText(f"{category_info['icon']} {category_info['name_ar']}")
        self.setObjectName("categoryBtn")
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor if PYQT_VERSION == 6 else Qt.PointingHandCursor))
        self.setCheckable(True)


class AppDetailWidget(QWidget):
    """صفحة تفاصيل التطبيق"""
    
    back_clicked = pyqtSignal()
    install_clicked = pyqtSignal(object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.app_entry = None
        self.is_installed = False
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # شريط العنوان
        header = QHBoxLayout()
        
        self.back_btn = QPushButton("← رجوع")
        self.back_btn.setObjectName("backBtn")
        self.back_btn.clicked.connect(self.back_clicked.emit)
        header.addWidget(self.back_btn)
        
        header.addStretch()
        layout.addLayout(header)
        
        # معلومات التطبيق
        info_layout = QHBoxLayout()
        
        # الأيقونة
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(128, 128)
        self.icon_label.setObjectName("detailIcon")
        info_layout.addWidget(self.icon_label)
        
        # التفاصيل
        details_layout = QVBoxLayout()
        
        self.name_label = QLabel()
        self.name_label.setObjectName("detailName")
        details_layout.addWidget(self.name_label)
        
        self.category_label = QLabel()
        self.category_label.setObjectName("detailCategory")
        details_layout.addWidget(self.category_label)
        
        self.desc_label = QLabel()
        self.desc_label.setObjectName("detailDesc")
        self.desc_label.setWordWrap(True)
        details_layout.addWidget(self.desc_label)
        
        # أزرار الإجراءات
        btn_layout = QHBoxLayout()
        
        self.action_btn = QPushButton("تثبيت")
        self.action_btn.setObjectName("detailInstallBtn")
        self.action_btn.setFixedWidth(150)
        self.action_btn.clicked.connect(self._on_action)
        btn_layout.addWidget(self.action_btn)
        
        self.website_btn = QPushButton("الموقع الرسمي")
        self.website_btn.setObjectName("websiteBtn")
        self.website_btn.setFixedWidth(150)
        btn_layout.addWidget(self.website_btn)
        
        btn_layout.addStretch()
        details_layout.addLayout(btn_layout)
        
        info_layout.addLayout(details_layout)
        info_layout.addStretch()
        layout.addLayout(info_layout)
        
        # معلومات الحزمة
        self.package_info = QLabel()
        self.package_info.setObjectName("packageInfo")
        self.package_info.setWordWrap(True)
        layout.addWidget(self.package_info)
        
        layout.addStretch()
    
    def set_app(self, app_entry: AppEntry, is_installed: bool = False):
        """تعيين التطبيق"""
        self.app_entry = app_entry
        self.is_installed = is_installed
        
        self.name_label.setText(app_entry.name)
        self.category_label.setText(f"التصنيف: {app_entry.category}")
        self.desc_label.setText(app_entry.description_ar)
        
        # تحديث زر الإجراء
        self.action_btn.setText("إزالة" if is_installed else "تثبيت")
        self.action_btn.setObjectName("detailRemoveBtn" if is_installed else "detailInstallBtn")
        
        # معلومات الحزم
        pkg_info = []
        if app_entry.pacman:
            pkg_info.append(f"Pacman/Yay: {app_entry.pacman}")
        if app_entry.apt:
            pkg_info.append(f"APT: {app_entry.apt}")
        if app_entry.dnf:
            pkg_info.append(f"DNF: {app_entry.dnf}")
        if app_entry.flatpak:
            pkg_info.append(f"Flatpak: {app_entry.flatpak}")
        if app_entry.snap:
            pkg_info.append(f"Snap: {app_entry.snap}")
        
        self.package_info.setText("أسماء الحزم:\n" + "\n".join(pkg_info))
        
        # الأيقونة
        self.icon_label.setText(app_entry.name[0].upper())
        self.icon_label.setStyleSheet("""
            QLabel {
                background-color: #4285f4;
                color: white;
                border-radius: 20px;
                font-size: 48px;
                font-weight: bold;
            }
        """)
    
    def _on_action(self):
        if self.app_entry:
            self.install_clicked.emit(self.app_entry)
    
    def update_status(self, is_installed: bool):
        """تحديث حالة التثبيت"""
        self.is_installed = is_installed
        self.action_btn.setText("إزالة" if is_installed else "تثبيت")


class MainWindow(QMainWindow):
    """النافذة الرئيسية"""
    
    def __init__(self):
        super().__init__()
        
        # تهيئة المكونات
        self.detector = DistroDetector()
        self.pkg_manager = PackageManager(self.detector)
        self.app_db = AppDatabase()
        
        self.current_category = None
        self.install_thread = None
        
        self._setup_ui()
        self._apply_styles()
        self._load_apps()
    
    def _setup_ui(self):
        self.setWindowTitle("Linux Store - متجر لينكس")
        self.setMinimumSize(1000, 700)
        
        # الويدجت المركزي
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # الشريط الجانبي
        sidebar = self._create_sidebar()
        main_layout.addWidget(sidebar)
        
        # المحتوى الرئيسي
        content = QWidget()
        content.setObjectName("contentArea")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # شريط البحث
        search_bar = self._create_search_bar()
        content_layout.addWidget(search_bar)
        
        # منطقة المحتوى المتغير
        self.stack = QStackedWidget()
        
        # صفحة الرئيسية
        self.home_page = self._create_home_page()
        self.stack.addWidget(self.home_page)
        
        # صفحة التصنيف
        self.category_page = self._create_category_page()
        self.stack.addWidget(self.category_page)
        
        # صفحة التفاصيل
        self.detail_page = AppDetailWidget()
        self.detail_page.back_clicked.connect(self._go_back)
        self.detail_page.install_clicked.connect(self._on_install)
        self.stack.addWidget(self.detail_page)
        
        # صفحة البحث
        self.search_page = self._create_search_page()
        self.stack.addWidget(self.search_page)
        
        content_layout.addWidget(self.stack)
        
        # شريط الحالة
        status_bar = self._create_status_bar()
        content_layout.addWidget(status_bar)
        
        main_layout.addWidget(content, 1)
    
    def _create_sidebar(self) -> QWidget:
        """إنشاء الشريط الجانبي"""
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(10, 15, 10, 15)
        layout.setSpacing(5)
        
        # الشعار
        logo = QLabel("🐧 Linux Store")
        logo.setObjectName("logo")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        layout.addWidget(logo)
        
        # معلومات النظام
        sys_info = QLabel(f"📦 {self.detector.distro_name or 'Linux'}")
        sys_info.setObjectName("sysInfo")
        sys_info.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        layout.addWidget(sys_info)
        
        pkg_info = QLabel(f"⚙️ {self.detector.package_manager or 'N/A'}")
        pkg_info.setObjectName("pkgInfo")
        pkg_info.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        layout.addWidget(pkg_info)
        
        layout.addSpacing(20)
        
        # زر الرئيسية
        home_btn = QPushButton("🏠 الرئيسية")
        home_btn.setObjectName("navBtn")
        home_btn.clicked.connect(self._show_home)
        layout.addWidget(home_btn)
        
        # زر التطبيقات
        apps_btn = QPushButton("📱 التطبيقات")
        apps_btn.setObjectName("navBtn")
        apps_btn.clicked.connect(lambda: self._show_category_filter('apps'))
        layout.addWidget(apps_btn)
        
        # زر الحزم
        pkgs_btn = QPushButton("📦 الحزم")
        pkgs_btn.setObjectName("navBtn")
        pkgs_btn.clicked.connect(lambda: self._show_category_filter('packages'))
        layout.addWidget(pkgs_btn)
        
        layout.addSpacing(10)
        
        # التصنيفات
        cat_label = QLabel("التصنيفات")
        cat_label.setObjectName("sectionLabel")
        layout.addWidget(cat_label)
        
        # أزرار التصنيفات
        self.category_buttons = {}
        for cat_id, cat_info in self.app_db.get_categories().items():
            btn = CategoryButton(cat_id, cat_info)
            btn.clicked.connect(lambda checked, cid=cat_id: self._show_category(cid))
            self.category_buttons[cat_id] = btn
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # زر التحديث
        update_btn = QPushButton("🔄 تحديث النظام")
        update_btn.setObjectName("updateBtn")
        update_btn.clicked.connect(self._update_system)
        layout.addWidget(update_btn)
        
        return sidebar
    
    def _create_search_bar(self) -> QWidget:
        """إنشاء شريط البحث"""
        bar = QWidget()
        bar.setObjectName("searchBar")
        bar.setFixedHeight(60)
        
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(20, 10, 20, 10)
        
        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setPlaceholderText("🔍 ابحث عن تطبيقات وحزم...")
        self.search_input.returnPressed.connect(self._do_search)
        layout.addWidget(self.search_input)
        
        search_btn = QPushButton("بحث")
        search_btn.setObjectName("searchBtn")
        search_btn.clicked.connect(self._do_search)
        layout.addWidget(search_btn)
        
        return bar
    
    def _create_home_page(self) -> QWidget:
        """إنشاء الصفحة الرئيسية"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # التطبيقات المميزة
        featured_label = QLabel("⭐ التطبيقات المميزة")
        featured_label.setObjectName("sectionTitle")
        layout.addWidget(featured_label)
        
        self.featured_scroll = QScrollArea()
        self.featured_scroll.setObjectName("appScroll")
        self.featured_scroll.setWidgetResizable(True)
        self.featured_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff if PYQT_VERSION == 6 else Qt.ScrollBarAlwaysOff
        )
        self.featured_scroll.setFixedHeight(260)
        
        self.featured_container = QWidget()
        self.featured_layout = QHBoxLayout(self.featured_container)
        self.featured_layout.setContentsMargins(0, 0, 0, 0)
        self.featured_layout.setSpacing(15)
        self.featured_scroll.setWidget(self.featured_container)
        
        layout.addWidget(self.featured_scroll)
        
        # التطبيقات الشائعة
        popular_label = QLabel("🔥 الأكثر شعبية")
        popular_label.setObjectName("sectionTitle")
        layout.addWidget(popular_label)
        
        self.popular_scroll = QScrollArea()
        self.popular_scroll.setObjectName("appScroll")
        self.popular_scroll.setWidgetResizable(True)
        self.popular_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff if PYQT_VERSION == 6 else Qt.ScrollBarAlwaysOff
        )
        
        self.popular_container = QWidget()
        self.popular_layout = QGridLayout(self.popular_container)
        self.popular_layout.setContentsMargins(0, 0, 0, 0)
        self.popular_layout.setSpacing(15)
        self.popular_scroll.setWidget(self.popular_container)
        
        layout.addWidget(self.popular_scroll, 1)
        
        return page
    
    def _create_category_page(self) -> QWidget:
        """إنشاء صفحة التصنيف"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        self.category_title = QLabel()
        self.category_title.setObjectName("sectionTitle")
        layout.addWidget(self.category_title)
        
        self.category_scroll = QScrollArea()
        self.category_scroll.setObjectName("appScroll")
        self.category_scroll.setWidgetResizable(True)
        
        self.category_container = QWidget()
        self.category_grid = QGridLayout(self.category_container)
        self.category_grid.setContentsMargins(0, 0, 0, 0)
        self.category_grid.setSpacing(15)
        self.category_scroll.setWidget(self.category_container)
        
        layout.addWidget(self.category_scroll, 1)
        
        return page
    
    def _create_search_page(self) -> QWidget:
        """إنشاء صفحة البحث"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        self.search_title = QLabel("نتائج البحث")
        self.search_title.setObjectName("sectionTitle")
        layout.addWidget(self.search_title)
        
        self.search_scroll = QScrollArea()
        self.search_scroll.setObjectName("appScroll")
        self.search_scroll.setWidgetResizable(True)
        
        self.search_container = QWidget()
        self.search_grid = QGridLayout(self.search_container)
        self.search_grid.setContentsMargins(0, 0, 0, 0)
        self.search_grid.setSpacing(15)
        self.search_scroll.setWidget(self.search_container)
        
        layout.addWidget(self.search_scroll, 1)
        
        return page
    
    def _create_status_bar(self) -> QWidget:
        """إنشاء شريط الحالة"""
        bar = QWidget()
        bar.setObjectName("statusBar")
        bar.setFixedHeight(40)
        
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(20, 5, 20, 5)
        
        self.status_label = QLabel("جاهز")
        self.status_label.setObjectName("statusLabel")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setFixedWidth(200)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        return bar
    
    def _apply_styles(self):
        """تطبيق الأنماط"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            
            #sidebar {
                background-color: #2d2d2d;
                border-right: 1px solid #404040;
            }
            
            #logo {
                color: #ffffff;
                font-size: 20px;
                font-weight: bold;
                padding: 10px;
            }
            
            #sysInfo, #pkgInfo {
                color: #888888;
                font-size: 12px;
                padding: 2px;
            }
            
            #navBtn {
                background-color: transparent;
                color: #ffffff;
                border: none;
                padding: 12px 15px;
                text-align: left;
                font-size: 14px;
                border-radius: 8px;
            }
            
            #navBtn:hover {
                background-color: #404040;
            }
            
            #sectionLabel {
                color: #888888;
                font-size: 12px;
                padding: 5px 15px;
            }
            
            #categoryBtn {
                background-color: transparent;
                color: #cccccc;
                border: none;
                padding: 10px 15px;
                text-align: left;
                font-size: 13px;
                border-radius: 6px;
            }
            
            #categoryBtn:hover {
                background-color: #404040;
                color: #ffffff;
            }
            
            #categoryBtn:checked {
                background-color: #4285f4;
                color: #ffffff;
            }
            
            #updateBtn {
                background-color: #34a853;
                color: white;
                border: none;
                padding: 12px;
                font-size: 14px;
                border-radius: 8px;
            }
            
            #updateBtn:hover {
                background-color: #2d9249;
            }
            
            #contentArea {
                background-color: #f5f5f5;
            }
            
            #searchBar {
                background-color: #ffffff;
                border-bottom: 1px solid #e0e0e0;
            }
            
            #searchInput {
                background-color: #f0f0f0;
                border: 1px solid #e0e0e0;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 14px;
            }
            
            #searchInput:focus {
                border-color: #4285f4;
                background-color: #ffffff;
            }
            
            #searchBtn {
                background-color: #4285f4;
                color: white;
                border: none;
                padding: 10px 25px;
                border-radius: 20px;
                font-size: 14px;
            }
            
            #searchBtn:hover {
                background-color: #3367d6;
            }
            
            #sectionTitle {
                color: #333333;
                font-size: 18px;
                font-weight: bold;
            }
            
            #appScroll {
                border: none;
                background-color: transparent;
            }
            
            #appCard {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
            }
            
            #appCard:hover {
                border-color: #4285f4;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            
            #appName {
                color: #333333;
                font-size: 14px;
                font-weight: bold;
            }
            
            #appDesc {
                color: #666666;
                font-size: 11px;
            }
            
            #installBtn {
                background-color: #4285f4;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-size: 12px;
            }
            
            #installBtn:hover {
                background-color: #3367d6;
            }
            
            #removeBtn {
                background-color: #ea4335;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-size: 12px;
            }
            
            #removeBtn:hover {
                background-color: #d33426;
            }
            
            #backBtn {
                background-color: transparent;
                color: #4285f4;
                border: none;
                font-size: 14px;
            }
            
            #backBtn:hover {
                color: #3367d6;
            }
            
            #detailName {
                color: #333333;
                font-size: 24px;
                font-weight: bold;
            }
            
            #detailCategory {
                color: #666666;
                font-size: 14px;
            }
            
            #detailDesc {
                color: #444444;
                font-size: 14px;
                line-height: 1.5;
            }
            
            #detailInstallBtn {
                background-color: #4285f4;
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 8px;
                font-size: 14px;
            }
            
            #detailInstallBtn:hover {
                background-color: #3367d6;
            }
            
            #detailRemoveBtn {
                background-color: #ea4335;
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 8px;
                font-size: 14px;
            }
            
            #websiteBtn {
                background-color: #f0f0f0;
                color: #333333;
                border: 1px solid #e0e0e0;
                padding: 12px 30px;
                border-radius: 8px;
                font-size: 14px;
            }
            
            #websiteBtn:hover {
                background-color: #e0e0e0;
            }
            
            #packageInfo {
                color: #666666;
                font-size: 13px;
                background-color: #f8f8f8;
                padding: 15px;
                border-radius: 8px;
            }
            
            #statusBar {
                background-color: #ffffff;
                border-top: 1px solid #e0e0e0;
            }
            
            #statusLabel {
                color: #666666;
                font-size: 12px;
            }
            
            #progressBar {
                border: none;
                border-radius: 4px;
                background-color: #e0e0e0;
            }
            
            #progressBar::chunk {
                background-color: #4285f4;
                border-radius: 4px;
            }
            
            QScrollBar:vertical {
                background-color: #f5f5f5;
                width: 10px;
                border-radius: 5px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #cccccc;
                border-radius: 5px;
                min-height: 30px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #aaaaaa;
            }
            
            QScrollBar:horizontal {
                background-color: #f5f5f5;
                height: 10px;
                border-radius: 5px;
            }
            
            QScrollBar::handle:horizontal {
                background-color: #cccccc;
                border-radius: 5px;
                min-width: 30px;
            }
        """)
    
    def _load_apps(self):
        """تحميل التطبيقات"""
        # تحميل التطبيقات المميزة
        featured = self.app_db.get_featured_apps()
        for app in featured:
            card = AppCard(app)
            card.clicked.connect(self._show_app_detail)
            card.install_clicked.connect(self._on_install)
            self.featured_layout.addWidget(card)
        self.featured_layout.addStretch()
        
        # تحميل التطبيقات الشائعة
        popular = self.app_db.get_popular_apps()
        row, col = 0, 0
        for app in popular:
            card = AppCard(app)
            card.clicked.connect(self._show_app_detail)
            card.install_clicked.connect(self._on_install)
            self.popular_layout.addWidget(card, row, col)
            col += 1
            if col >= 4:
                col = 0
                row += 1
    
    def _show_home(self):
        """عرض الصفحة الرئيسية"""
        self.stack.setCurrentWidget(self.home_page)
        for btn in self.category_buttons.values():
            btn.setChecked(False)
    
    def _show_category(self, category_id: str):
        """عرض تصنيف معين"""
        # تحديث الأزرار
        for cid, btn in self.category_buttons.items():
            btn.setChecked(cid == category_id)
        
        # تحديث العنوان
        cat_info = self.app_db.get_categories().get(category_id, {})
        self.category_title.setText(f"{cat_info.get('icon', '')} {cat_info.get('name_ar', category_id)}")
        
        # مسح المحتوى السابق
        while self.category_grid.count():
            item = self.category_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # تحميل التطبيقات
        apps = self.app_db.get_apps_by_category(category_id)
        row, col = 0, 0
        for app in apps:
            card = AppCard(app)
            card.clicked.connect(self._show_app_detail)
            card.install_clicked.connect(self._on_install)
            self.category_grid.addWidget(card, row, col)
            col += 1
            if col >= 4:
                col = 0
                row += 1
        
        self.stack.setCurrentWidget(self.category_page)
    
    def _show_category_filter(self, filter_type: str):
        """عرض فلتر التطبيقات/الحزم"""
        for btn in self.category_buttons.values():
            btn.setChecked(False)
        
        if filter_type == 'apps':
            self.category_title.setText("📱 جميع التطبيقات")
            apps = self.app_db.get_applications()
        else:
            self.category_title.setText("📦 جميع الحزم")
            apps = self.app_db.get_packages()
        
        # مسح المحتوى السابق
        while self.category_grid.count():
            item = self.category_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # تحميل التطبيقات
        row, col = 0, 0
        for app in apps:
            card = AppCard(app)
            card.clicked.connect(self._show_app_detail)
            card.install_clicked.connect(self._on_install)
            self.category_grid.addWidget(card, row, col)
            col += 1
            if col >= 4:
                col = 0
                row += 1
        
        self.stack.setCurrentWidget(self.category_page)
    
    def _show_app_detail(self, app_entry: AppEntry):
        """عرض تفاصيل التطبيق"""
        self.detail_page.set_app(app_entry)
        self.stack.setCurrentWidget(self.detail_page)
    
    def _go_back(self):
        """العودة للصفحة السابقة"""
        self.stack.setCurrentWidget(self.home_page)
    
    def _do_search(self):
        """تنفيذ البحث"""
        query = self.search_input.text().strip()
        if not query:
            return
        
        # البحث
        results = self.app_db.search(query)
        
        # تحديث العنوان
        self.search_title.setText(f"نتائج البحث عن: {query} ({len(results)} نتيجة)")
        
        # مسح المحتوى السابق
        while self.search_grid.count():
            item = self.search_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # عرض النتائج
        row, col = 0, 0
        for app in results:
            card = AppCard(app)
            card.clicked.connect(self._show_app_detail)
            card.install_clicked.connect(self._on_install)
            self.search_grid.addWidget(card, row, col)
            col += 1
            if col >= 4:
                col = 0
                row += 1
        
        self.stack.setCurrentWidget(self.search_page)
    
    def _on_install(self, app_entry: AppEntry):
        """معالجة طلب التثبيت/الإزالة"""
        # التحقق من عدم وجود عملية جارية
        if self.install_thread and self.install_thread.isRunning():
            QMessageBox.warning(self, "تحذير", "هناك عملية جارية، يرجى الانتظار")
            return
        
        # تحديد نوع العملية
        action = 'remove' if self.pkg_manager.is_installed(self._create_pkg_info(app_entry)) else 'install'
        action_text = "إزالة" if action == 'remove' else "تثبيت"
        
        # تأكيد العملية
        reply = QMessageBox.question(
            self,
            f"تأكيد {action_text}",
            f"هل تريد {action_text} {app_entry.name}؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No if PYQT_VERSION == 6 else QMessageBox.Yes | QMessageBox.No
        )
        
        if reply != (QMessageBox.StandardButton.Yes if PYQT_VERSION == 6 else QMessageBox.Yes):
            return
        
        # بدء العملية
        self.status_label.setText(f"جاري {action_text} {app_entry.name}...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # وضع غير محدد
        
        self.install_thread = InstallThread(self.pkg_manager, app_entry, action)
        self.install_thread.finished_signal.connect(self._on_install_finished)
        self.install_thread.start()
    
    def _create_pkg_info(self, app_entry: AppEntry) -> PackageInfo:
        """إنشاء PackageInfo من AppEntry"""
        return PackageInfo(
            name=app_entry.id,
            display_name=app_entry.name,
            description=app_entry.description,
            category=app_entry.category,
            icon=app_entry.icon,
            package_names={
                'pacman': app_entry.pacman,
                'apt': app_entry.apt,
                'dnf': app_entry.dnf,
                'zypper': app_entry.zypper,
            },
            flatpak_id=app_entry.flatpak,
            snap_name=app_entry.snap,
        )
    
    def _on_install_finished(self, success: bool, message: str):
        """معالجة انتهاء التثبيت"""
        self.progress_bar.setVisible(False)
        
        if success:
            self.status_label.setText(f"تم بنجاح: {message}")
            QMessageBox.information(self, "نجاح", f"تمت العملية بنجاح: {message}")
        else:
            self.status_label.setText(f"فشل: {message}")
            QMessageBox.critical(self, "خطأ", f"فشلت العملية: {message}")
        
        # إعادة تعيين الحالة بعد 3 ثواني
        QTimer.singleShot(3000, lambda: self.status_label.setText("جاهز"))
    
    def _update_system(self):
        """تحديث النظام"""
        reply = QMessageBox.question(
            self,
            "تأكيد التحديث",
            "هل تريد تحديث النظام؟ قد يستغرق هذا بعض الوقت.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No if PYQT_VERSION == 6 else QMessageBox.Yes | QMessageBox.No
        )
        
        if reply != (QMessageBox.StandardButton.Yes if PYQT_VERSION == 6 else QMessageBox.Yes):
            return
        
        self.status_label.setText("جاري تحديث النظام...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        
        # تنفيذ التحديث في خيط منفصل
        # (يمكن تحسين هذا لاحقاً)
        QTimer.singleShot(1000, lambda: self._finish_update())
    
    def _finish_update(self):
        """إنهاء التحديث"""
        self.progress_bar.setVisible(False)
        self.status_label.setText("جاهز")
        QMessageBox.information(self, "معلومة", "يرجى تشغيل أمر التحديث من الطرفية لتحديث النظام بشكل كامل")


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Linux Store")
    app.setOrganizationName("LinuxStore")
    
    # تعيين الخط
    font = QFont()
    font.setFamily("Noto Sans Arabic, Arial, sans-serif")
    font.setPointSize(10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec() if PYQT_VERSION == 6 else app.exec_())


if __name__ == '__main__':
    main()
