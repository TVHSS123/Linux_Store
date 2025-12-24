#!/usr/bin/env python3
"""
Linux Store - Application Database
قاعدة بيانات التطبيقات والحزم
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import json
import os

@dataclass
class AppEntry:
    """إدخال تطبيق في قاعدة البيانات"""
    id: str
    name: str
    description: str
    description_ar: str
    category: str
    icon: str
    is_app: bool = True
    website: str = ""
    
    # أسماء الحزم لمختلف مديري الحزم
    pacman: str = ""
    apt: str = ""
    dnf: str = ""
    zypper: str = ""
    flatpak: str = ""
    snap: str = ""
    
    # معلومات إضافية
    keywords: List[str] = field(default_factory=list)
    featured: bool = False
    popular: bool = False

class AppDatabase:
    """قاعدة بيانات التطبيقات"""
    
    # التصنيفات
    CATEGORIES = {
        'internet': {'name': 'Internet', 'name_ar': 'الإنترنت', 'icon': '🌐'},
        'development': {'name': 'Development', 'name_ar': 'التطوير', 'icon': '💻'},
        'games': {'name': 'Games', 'name_ar': 'الألعاب', 'icon': '🎮'},
        'graphics': {'name': 'Graphics', 'name_ar': 'الرسومات', 'icon': '🎨'},
        'multimedia': {'name': 'Multimedia', 'name_ar': 'الوسائط', 'icon': '🎬'},
        'office': {'name': 'Office', 'name_ar': 'المكتب', 'icon': '📄'},
        'system': {'name': 'System', 'name_ar': 'النظام', 'icon': '⚙️'},
        'utilities': {'name': 'Utilities', 'name_ar': 'الأدوات', 'icon': '🔧'},
        'security': {'name': 'Security', 'name_ar': 'الأمان', 'icon': '🔒'},
        'science': {'name': 'Science', 'name_ar': 'العلوم', 'icon': '🔬'},
        'education': {'name': 'Education', 'name_ar': 'التعليم', 'icon': '📚'},
        'packages': {'name': 'Packages', 'name_ar': 'الحزم', 'icon': '📦'},
    }
    
    def __init__(self):
        self.apps: Dict[str, AppEntry] = {}
        self._load_default_apps()
    
    def _load_default_apps(self):
        """تحميل التطبيقات الافتراضية"""
        
        # ============ تطبيقات الإنترنت ============
        self._add_app(AppEntry(
            id='firefox',
            name='Firefox',
            description='Fast, private and secure web browser',
            description_ar='متصفح ويب سريع وخاص وآمن',
            category='internet',
            icon='firefox',
            pacman='firefox',
            apt='firefox',
            dnf='firefox',
            zypper='firefox',
            flatpak='org.mozilla.firefox',
            snap='firefox',
            website='https://firefox.com',
            keywords=['browser', 'web', 'mozilla'],
            featured=True,
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='chromium',
            name='Chromium',
            description='Open-source web browser',
            description_ar='متصفح ويب مفتوح المصدر',
            category='internet',
            icon='chromium',
            pacman='chromium',
            apt='chromium-browser',
            dnf='chromium',
            zypper='chromium',
            flatpak='org.chromium.Chromium',
            snap='chromium',
            website='https://chromium.org',
            keywords=['browser', 'web', 'chrome'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='google-chrome',
            name='Google Chrome',
            description='Fast and secure web browser by Google',
            description_ar='متصفح ويب سريع وآمن من جوجل',
            category='internet',
            icon='google-chrome',
            pacman='google-chrome',  # AUR
            apt='google-chrome-stable',
            dnf='google-chrome-stable',
            flatpak='com.google.Chrome',
            website='https://google.com/chrome',
            keywords=['browser', 'web', 'google'],
            featured=True,
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='brave',
            name='Brave Browser',
            description='Privacy-focused browser with ad blocker',
            description_ar='متصفح يركز على الخصوصية مع حاجب إعلانات',
            category='internet',
            icon='brave',
            pacman='brave-bin',  # AUR
            apt='brave-browser',
            dnf='brave-browser',
            flatpak='com.brave.Browser',
            snap='brave',
            website='https://brave.com',
            keywords=['browser', 'privacy', 'ads'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='thunderbird',
            name='Thunderbird',
            description='Free email application',
            description_ar='تطبيق بريد إلكتروني مجاني',
            category='internet',
            icon='thunderbird',
            pacman='thunderbird',
            apt='thunderbird',
            dnf='thunderbird',
            zypper='thunderbird',
            flatpak='org.mozilla.Thunderbird',
            snap='thunderbird',
            website='https://thunderbird.net',
            keywords=['email', 'mail', 'mozilla'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='telegram',
            name='Telegram Desktop',
            description='Fast and secure messaging app',
            description_ar='تطبيق مراسلة سريع وآمن',
            category='internet',
            icon='telegram',
            pacman='telegram-desktop',
            apt='telegram-desktop',
            dnf='telegram-desktop',
            flatpak='org.telegram.desktop',
            snap='telegram-desktop',
            website='https://telegram.org',
            keywords=['chat', 'messaging', 'social'],
            featured=True,
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='discord',
            name='Discord',
            description='Voice, video and text chat for gamers',
            description_ar='دردشة صوتية ومرئية ونصية للاعبين',
            category='internet',
            icon='discord',
            pacman='discord',
            apt='discord',
            flatpak='com.discordapp.Discord',
            snap='discord',
            website='https://discord.com',
            keywords=['chat', 'voice', 'gaming', 'social'],
            featured=True,
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='slack',
            name='Slack',
            description='Team communication and collaboration',
            description_ar='تواصل وتعاون الفريق',
            category='internet',
            icon='slack',
            pacman='slack-desktop',  # AUR
            apt='slack-desktop',
            flatpak='com.slack.Slack',
            snap='slack',
            website='https://slack.com',
            keywords=['chat', 'team', 'work', 'collaboration'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='zoom',
            name='Zoom',
            description='Video conferencing and meetings',
            description_ar='مؤتمرات الفيديو والاجتماعات',
            category='internet',
            icon='zoom',
            pacman='zoom',  # AUR
            apt='zoom',
            flatpak='us.zoom.Zoom',
            snap='zoom-client',
            website='https://zoom.us',
            keywords=['video', 'meeting', 'conference'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='qbittorrent',
            name='qBittorrent',
            description='Free and open-source BitTorrent client',
            description_ar='عميل تورنت مجاني ومفتوح المصدر',
            category='internet',
            icon='qbittorrent',
            pacman='qbittorrent',
            apt='qbittorrent',
            dnf='qbittorrent',
            zypper='qbittorrent',
            flatpak='org.qbittorrent.qBittorrent',
            website='https://qbittorrent.org',
            keywords=['torrent', 'download', 'p2p'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='filezilla',
            name='FileZilla',
            description='FTP, FTPS and SFTP client',
            description_ar='عميل FTP و FTPS و SFTP',
            category='internet',
            icon='filezilla',
            pacman='filezilla',
            apt='filezilla',
            dnf='filezilla',
            zypper='filezilla',
            flatpak='org.filezillaproject.Filezilla',
            website='https://filezilla-project.org',
            keywords=['ftp', 'sftp', 'transfer', 'upload'],
        ))
        
        # ============ تطبيقات التطوير ============
        self._add_app(AppEntry(
            id='vscode',
            name='Visual Studio Code',
            description='Powerful source code editor',
            description_ar='محرر كود مصدري قوي',
            category='development',
            icon='visual-studio-code',
            pacman='code',
            apt='code',
            dnf='code',
            flatpak='com.visualstudio.code',
            snap='code',
            website='https://code.visualstudio.com',
            keywords=['editor', 'ide', 'programming', 'code'],
            featured=True,
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='sublime-text',
            name='Sublime Text',
            description='Sophisticated text editor for code',
            description_ar='محرر نصوص متطور للكود',
            category='development',
            icon='sublime-text',
            pacman='sublime-text-4',  # AUR
            apt='sublime-text',
            flatpak='com.sublimetext.three',
            snap='sublime-text',
            website='https://sublimetext.com',
            keywords=['editor', 'text', 'programming'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='atom',
            name='Atom',
            description='Hackable text editor',
            description_ar='محرر نصوص قابل للتخصيص',
            category='development',
            icon='atom',
            pacman='atom',  # AUR
            apt='atom',
            flatpak='io.atom.Atom',
            snap='atom',
            website='https://atom.io',
            keywords=['editor', 'text', 'github'],
        ))
        
        self._add_app(AppEntry(
            id='jetbrains-toolbox',
            name='JetBrains Toolbox',
            description='Manage JetBrains IDEs',
            description_ar='إدارة بيئات تطوير JetBrains',
            category='development',
            icon='jetbrains-toolbox',
            pacman='jetbrains-toolbox',  # AUR
            flatpak='com.jetbrains.Toolbox',
            website='https://jetbrains.com/toolbox-app',
            keywords=['ide', 'jetbrains', 'pycharm', 'intellij'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='pycharm',
            name='PyCharm Community',
            description='Python IDE for professional developers',
            description_ar='بيئة تطوير بايثون للمحترفين',
            category='development',
            icon='pycharm',
            pacman='pycharm-community-edition',
            apt='pycharm-community',
            flatpak='com.jetbrains.PyCharm-Community',
            snap='pycharm-community',
            website='https://jetbrains.com/pycharm',
            keywords=['ide', 'python', 'jetbrains'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='android-studio',
            name='Android Studio',
            description='Official IDE for Android development',
            description_ar='بيئة التطوير الرسمية لأندرويد',
            category='development',
            icon='android-studio',
            pacman='android-studio',  # AUR
            apt='android-studio',
            flatpak='com.google.AndroidStudio',
            snap='android-studio',
            website='https://developer.android.com/studio',
            keywords=['ide', 'android', 'mobile', 'google'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='postman',
            name='Postman',
            description='API development and testing tool',
            description_ar='أداة تطوير واختبار API',
            category='development',
            icon='postman',
            pacman='postman-bin',  # AUR
            flatpak='com.getpostman.Postman',
            snap='postman',
            website='https://postman.com',
            keywords=['api', 'rest', 'testing', 'http'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='docker-desktop',
            name='Docker Desktop',
            description='Container development platform',
            description_ar='منصة تطوير الحاويات',
            category='development',
            icon='docker',
            pacman='docker-desktop',  # AUR
            apt='docker-desktop',
            website='https://docker.com',
            keywords=['container', 'docker', 'devops', 'virtualization'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='github-desktop',
            name='GitHub Desktop',
            description='Git client for GitHub',
            description_ar='عميل Git لـ GitHub',
            category='development',
            icon='github-desktop',
            pacman='github-desktop-bin',  # AUR
            flatpak='io.github.shiftey.Desktop',
            website='https://desktop.github.com',
            keywords=['git', 'github', 'version control'],
        ))
        
        self._add_app(AppEntry(
            id='gitkraken',
            name='GitKraken',
            description='Git GUI client',
            description_ar='عميل Git بواجهة رسومية',
            category='development',
            icon='gitkraken',
            pacman='gitkraken',  # AUR
            flatpak='com.axosoft.GitKraken',
            snap='gitkraken',
            website='https://gitkraken.com',
            keywords=['git', 'gui', 'version control'],
        ))
        
        self._add_app(AppEntry(
            id='dbeaver',
            name='DBeaver',
            description='Universal database tool',
            description_ar='أداة قواعد بيانات شاملة',
            category='development',
            icon='dbeaver',
            pacman='dbeaver',
            apt='dbeaver-ce',
            flatpak='io.dbeaver.DBeaverCommunity',
            snap='dbeaver-ce',
            website='https://dbeaver.io',
            keywords=['database', 'sql', 'mysql', 'postgresql'],
            popular=True
        ))
        
        # ============ الألعاب ============
        self._add_app(AppEntry(
            id='steam',
            name='Steam',
            description='Gaming platform by Valve',
            description_ar='منصة ألعاب من Valve',
            category='games',
            icon='steam',
            pacman='steam',
            apt='steam',
            dnf='steam',
            flatpak='com.valvesoftware.Steam',
            website='https://store.steampowered.com',
            keywords=['gaming', 'games', 'valve', 'store'],
            featured=True,
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='lutris',
            name='Lutris',
            description='Open gaming platform for Linux',
            description_ar='منصة ألعاب مفتوحة للينكس',
            category='games',
            icon='lutris',
            pacman='lutris',
            apt='lutris',
            dnf='lutris',
            flatpak='net.lutris.Lutris',
            website='https://lutris.net',
            keywords=['gaming', 'wine', 'emulator'],
            featured=True,
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='heroic',
            name='Heroic Games Launcher',
            description='Epic Games and GOG launcher',
            description_ar='مشغل ألعاب Epic و GOG',
            category='games',
            icon='heroic',
            pacman='heroic-games-launcher-bin',  # AUR
            flatpak='com.heroicgameslauncher.hgl',
            website='https://heroicgameslauncher.com',
            keywords=['gaming', 'epic', 'gog', 'launcher'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='retroarch',
            name='RetroArch',
            description='Multi-system emulator frontend',
            description_ar='واجهة محاكي متعدد الأنظمة',
            category='games',
            icon='retroarch',
            pacman='retroarch',
            apt='retroarch',
            dnf='retroarch',
            flatpak='org.libretro.RetroArch',
            snap='retroarch',
            website='https://retroarch.com',
            keywords=['emulator', 'retro', 'gaming'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='minecraft',
            name='Minecraft',
            description='Popular sandbox game',
            description_ar='لعبة ساندبوكس شهيرة',
            category='games',
            icon='minecraft',
            pacman='minecraft-launcher',  # AUR
            flatpak='com.mojang.Minecraft',
            website='https://minecraft.net',
            keywords=['gaming', 'sandbox', 'mojang'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='bottles',
            name='Bottles',
            description='Run Windows software on Linux',
            description_ar='تشغيل برامج ويندوز على لينكس',
            category='games',
            icon='bottles',
            pacman='bottles',
            flatpak='com.usebottles.bottles',
            website='https://usebottles.com',
            keywords=['wine', 'windows', 'gaming', 'compatibility'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='gamemode',
            name='GameMode',
            description='Optimize Linux for gaming',
            description_ar='تحسين لينكس للألعاب',
            category='games',
            icon='gamemode',
            pacman='gamemode',
            apt='gamemode',
            dnf='gamemode',
            website='https://github.com/FeralInteractive/gamemode',
            keywords=['gaming', 'performance', 'optimization'],
        ))
        
        # ============ الرسومات ============
        self._add_app(AppEntry(
            id='gimp',
            name='GIMP',
            description='GNU Image Manipulation Program',
            description_ar='برنامج معالجة الصور GNU',
            category='graphics',
            icon='gimp',
            pacman='gimp',
            apt='gimp',
            dnf='gimp',
            zypper='gimp',
            flatpak='org.gimp.GIMP',
            snap='gimp',
            website='https://gimp.org',
            keywords=['image', 'photo', 'editor', 'photoshop'],
            featured=True,
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='inkscape',
            name='Inkscape',
            description='Vector graphics editor',
            description_ar='محرر رسومات متجهة',
            category='graphics',
            icon='inkscape',
            pacman='inkscape',
            apt='inkscape',
            dnf='inkscape',
            zypper='inkscape',
            flatpak='org.inkscape.Inkscape',
            snap='inkscape',
            website='https://inkscape.org',
            keywords=['vector', 'svg', 'graphics', 'illustrator'],
            featured=True,
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='krita',
            name='Krita',
            description='Digital painting application',
            description_ar='تطبيق الرسم الرقمي',
            category='graphics',
            icon='krita',
            pacman='krita',
            apt='krita',
            dnf='krita',
            zypper='krita',
            flatpak='org.kde.krita',
            snap='krita',
            website='https://krita.org',
            keywords=['painting', 'drawing', 'art', 'digital'],
            featured=True,
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='blender',
            name='Blender',
            description='3D creation suite',
            description_ar='مجموعة إنشاء ثلاثية الأبعاد',
            category='graphics',
            icon='blender',
            pacman='blender',
            apt='blender',
            dnf='blender',
            zypper='blender',
            flatpak='org.blender.Blender',
            snap='blender',
            website='https://blender.org',
            keywords=['3d', 'modeling', 'animation', 'render'],
            featured=True,
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='darktable',
            name='Darktable',
            description='Photography workflow application',
            description_ar='تطبيق سير عمل التصوير',
            category='graphics',
            icon='darktable',
            pacman='darktable',
            apt='darktable',
            dnf='darktable',
            flatpak='org.darktable.Darktable',
            snap='darktable',
            website='https://darktable.org',
            keywords=['photo', 'raw', 'photography', 'lightroom'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='rawtherapee',
            name='RawTherapee',
            description='RAW image processing',
            description_ar='معالجة صور RAW',
            category='graphics',
            icon='rawtherapee',
            pacman='rawtherapee',
            apt='rawtherapee',
            dnf='rawtherapee',
            flatpak='com.rawtherapee.RawTherapee',
            website='https://rawtherapee.com',
            keywords=['photo', 'raw', 'photography'],
        ))
        
        self._add_app(AppEntry(
            id='shotwell',
            name='Shotwell',
            description='Photo manager for GNOME',
            description_ar='مدير صور لـ GNOME',
            category='graphics',
            icon='shotwell',
            pacman='shotwell',
            apt='shotwell',
            dnf='shotwell',
            flatpak='org.gnome.Shotwell',
            website='https://wiki.gnome.org/Apps/Shotwell',
            keywords=['photo', 'manager', 'gallery'],
        ))
        
        # ============ الوسائط المتعددة ============
        self._add_app(AppEntry(
            id='vlc',
            name='VLC Media Player',
            description='Multimedia player for all formats',
            description_ar='مشغل وسائط لجميع الصيغ',
            category='multimedia',
            icon='vlc',
            pacman='vlc',
            apt='vlc',
            dnf='vlc',
            zypper='vlc',
            flatpak='org.videolan.VLC',
            snap='vlc',
            website='https://videolan.org',
            keywords=['video', 'audio', 'player', 'media'],
            featured=True,
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='mpv',
            name='mpv',
            description='Minimalist media player',
            description_ar='مشغل وسائط بسيط',
            category='multimedia',
            icon='mpv',
            pacman='mpv',
            apt='mpv',
            dnf='mpv',
            zypper='mpv',
            flatpak='io.mpv.Mpv',
            website='https://mpv.io',
            keywords=['video', 'audio', 'player', 'minimal'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='spotify',
            name='Spotify',
            description='Music streaming service',
            description_ar='خدمة بث الموسيقى',
            category='multimedia',
            icon='spotify',
            pacman='spotify',  # AUR
            apt='spotify-client',
            flatpak='com.spotify.Client',
            snap='spotify',
            website='https://spotify.com',
            keywords=['music', 'streaming', 'audio'],
            featured=True,
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='audacity',
            name='Audacity',
            description='Audio editor and recorder',
            description_ar='محرر ومسجل صوت',
            category='multimedia',
            icon='audacity',
            pacman='audacity',
            apt='audacity',
            dnf='audacity',
            zypper='audacity',
            flatpak='org.audacityteam.Audacity',
            website='https://audacityteam.org',
            keywords=['audio', 'editor', 'recording', 'sound'],
            featured=True,
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='obs-studio',
            name='OBS Studio',
            description='Video recording and streaming',
            description_ar='تسجيل وبث الفيديو',
            category='multimedia',
            icon='obs',
            pacman='obs-studio',
            apt='obs-studio',
            dnf='obs-studio',
            flatpak='com.obsproject.Studio',
            website='https://obsproject.com',
            keywords=['streaming', 'recording', 'video', 'broadcast'],
            featured=True,
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='kdenlive',
            name='Kdenlive',
            description='Video editor by KDE',
            description_ar='محرر فيديو من KDE',
            category='multimedia',
            icon='kdenlive',
            pacman='kdenlive',
            apt='kdenlive',
            dnf='kdenlive',
            flatpak='org.kde.kdenlive',
            website='https://kdenlive.org',
            keywords=['video', 'editor', 'editing', 'movie'],
            featured=True,
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='shotcut',
            name='Shotcut',
            description='Cross-platform video editor',
            description_ar='محرر فيديو متعدد المنصات',
            category='multimedia',
            icon='shotcut',
            pacman='shotcut',
            apt='shotcut',
            dnf='shotcut',
            flatpak='org.shotcut.Shotcut',
            snap='shotcut',
            website='https://shotcut.org',
            keywords=['video', 'editor', 'editing'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='handbrake',
            name='HandBrake',
            description='Video transcoder',
            description_ar='محول صيغ الفيديو',
            category='multimedia',
            icon='handbrake',
            pacman='handbrake',
            apt='handbrake',
            dnf='handbrake',
            flatpak='fr.handbrake.ghb',
            website='https://handbrake.fr',
            keywords=['video', 'converter', 'transcoder', 'encode'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='rhythmbox',
            name='Rhythmbox',
            description='Music player for GNOME',
            description_ar='مشغل موسيقى لـ GNOME',
            category='multimedia',
            icon='rhythmbox',
            pacman='rhythmbox',
            apt='rhythmbox',
            dnf='rhythmbox',
            flatpak='org.gnome.Rhythmbox3',
            website='https://wiki.gnome.org/Apps/Rhythmbox',
            keywords=['music', 'player', 'audio'],
        ))
        
        # ============ المكتب ============
        self._add_app(AppEntry(
            id='libreoffice',
            name='LibreOffice',
            description='Free office suite',
            description_ar='مجموعة مكتبية مجانية',
            category='office',
            icon='libreoffice-main',
            pacman='libreoffice-fresh',
            apt='libreoffice',
            dnf='libreoffice',
            zypper='libreoffice',
            flatpak='org.libreoffice.LibreOffice',
            snap='libreoffice',
            website='https://libreoffice.org',
            keywords=['office', 'word', 'excel', 'document'],
            featured=True,
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='onlyoffice',
            name='ONLYOFFICE',
            description='Office suite compatible with MS Office',
            description_ar='مجموعة مكتبية متوافقة مع MS Office',
            category='office',
            icon='onlyoffice',
            pacman='onlyoffice-bin',  # AUR
            apt='onlyoffice-desktopeditors',
            flatpak='org.onlyoffice.desktopeditors',
            snap='onlyoffice-desktopeditors',
            website='https://onlyoffice.com',
            keywords=['office', 'word', 'excel', 'document'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='okular',
            name='Okular',
            description='Universal document viewer',
            description_ar='عارض مستندات شامل',
            category='office',
            icon='okular',
            pacman='okular',
            apt='okular',
            dnf='okular',
            flatpak='org.kde.okular',
            website='https://okular.kde.org',
            keywords=['pdf', 'document', 'viewer', 'reader'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='evince',
            name='Evince',
            description='Document viewer for GNOME',
            description_ar='عارض مستندات لـ GNOME',
            category='office',
            icon='evince',
            pacman='evince',
            apt='evince',
            dnf='evince',
            flatpak='org.gnome.Evince',
            website='https://wiki.gnome.org/Apps/Evince',
            keywords=['pdf', 'document', 'viewer'],
        ))
        
        self._add_app(AppEntry(
            id='obsidian',
            name='Obsidian',
            description='Knowledge base and note-taking',
            description_ar='قاعدة معرفة وتدوين ملاحظات',
            category='office',
            icon='obsidian',
            pacman='obsidian',  # AUR
            flatpak='md.obsidian.Obsidian',
            snap='obsidian',
            website='https://obsidian.md',
            keywords=['notes', 'markdown', 'knowledge', 'writing'],
            featured=True,
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='notion',
            name='Notion',
            description='All-in-one workspace',
            description_ar='مساحة عمل شاملة',
            category='office',
            icon='notion',
            pacman='notion-app-electron',  # AUR
            flatpak='com.notion.Notion',
            snap='notion-snap-reborn',
            website='https://notion.so',
            keywords=['notes', 'workspace', 'productivity'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='calibre',
            name='Calibre',
            description='E-book management',
            description_ar='إدارة الكتب الإلكترونية',
            category='office',
            icon='calibre',
            pacman='calibre',
            apt='calibre',
            dnf='calibre',
            flatpak='com.calibre_ebook.calibre',
            website='https://calibre-ebook.com',
            keywords=['ebook', 'reader', 'library', 'kindle'],
            popular=True
        ))
        
        # ============ النظام ============
        self._add_app(AppEntry(
            id='gnome-tweaks',
            name='GNOME Tweaks',
            description='Advanced GNOME settings',
            description_ar='إعدادات GNOME المتقدمة',
            category='system',
            icon='gnome-tweaks',
            pacman='gnome-tweaks',
            apt='gnome-tweaks',
            dnf='gnome-tweaks',
            flatpak='org.gnome.tweaks',
            website='https://wiki.gnome.org/Apps/Tweaks',
            keywords=['gnome', 'settings', 'customization'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='timeshift',
            name='Timeshift',
            description='System restore utility',
            description_ar='أداة استعادة النظام',
            category='system',
            icon='timeshift',
            pacman='timeshift',
            apt='timeshift',
            dnf='timeshift',
            website='https://github.com/linuxmint/timeshift',
            keywords=['backup', 'restore', 'snapshot', 'system'],
            featured=True,
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='gparted',
            name='GParted',
            description='Partition editor',
            description_ar='محرر الأقسام',
            category='system',
            icon='gparted',
            pacman='gparted',
            apt='gparted',
            dnf='gparted',
            zypper='gparted',
            flatpak='org.gnome.GParted',
            website='https://gparted.org',
            keywords=['partition', 'disk', 'format', 'storage'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='htop',
            name='htop',
            description='Interactive process viewer',
            description_ar='عارض عمليات تفاعلي',
            category='system',
            icon='htop',
            pacman='htop',
            apt='htop',
            dnf='htop',
            zypper='htop',
            snap='htop',
            website='https://htop.dev',
            keywords=['process', 'monitor', 'system', 'task'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='btop',
            name='btop++',
            description='Resource monitor',
            description_ar='مراقب الموارد',
            category='system',
            icon='btop',
            pacman='btop',
            apt='btop',
            dnf='btop',
            snap='btop',
            website='https://github.com/aristocratos/btop',
            keywords=['process', 'monitor', 'system', 'cpu'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='neofetch',
            name='Neofetch',
            description='System information tool',
            description_ar='أداة معلومات النظام',
            category='system',
            icon='neofetch',
            pacman='neofetch',
            apt='neofetch',
            dnf='neofetch',
            website='https://github.com/dylanaraps/neofetch',
            keywords=['system', 'info', 'fetch', 'terminal'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='virtualbox',
            name='VirtualBox',
            description='Virtualization software',
            description_ar='برنامج المحاكاة الافتراضية',
            category='system',
            icon='virtualbox',
            pacman='virtualbox',
            apt='virtualbox',
            dnf='VirtualBox',
            zypper='virtualbox',
            website='https://virtualbox.org',
            keywords=['virtual', 'machine', 'vm', 'virtualization'],
            featured=True,
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='gnome-boxes',
            name='GNOME Boxes',
            description='Simple virtualization',
            description_ar='محاكاة افتراضية بسيطة',
            category='system',
            icon='gnome-boxes',
            pacman='gnome-boxes',
            apt='gnome-boxes',
            dnf='gnome-boxes',
            flatpak='org.gnome.Boxes',
            website='https://wiki.gnome.org/Apps/Boxes',
            keywords=['virtual', 'machine', 'vm'],
        ))
        
        # ============ الأدوات ============
        self._add_app(AppEntry(
            id='flameshot',
            name='Flameshot',
            description='Screenshot tool',
            description_ar='أداة لقطات الشاشة',
            category='utilities',
            icon='flameshot',
            pacman='flameshot',
            apt='flameshot',
            dnf='flameshot',
            flatpak='org.flameshot.Flameshot',
            website='https://flameshot.org',
            keywords=['screenshot', 'capture', 'screen'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='peek',
            name='Peek',
            description='GIF screen recorder',
            description_ar='مسجل شاشة GIF',
            category='utilities',
            icon='peek',
            pacman='peek',
            apt='peek',
            dnf='peek',
            flatpak='com.uploadedlobster.peek',
            website='https://github.com/phw/peek',
            keywords=['gif', 'screen', 'recorder', 'capture'],
        ))
        
        self._add_app(AppEntry(
            id='bitwarden',
            name='Bitwarden',
            description='Password manager',
            description_ar='مدير كلمات المرور',
            category='utilities',
            icon='bitwarden',
            pacman='bitwarden',
            apt='bitwarden',
            flatpak='com.bitwarden.desktop',
            snap='bitwarden',
            website='https://bitwarden.com',
            keywords=['password', 'security', 'manager', 'vault'],
            featured=True,
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='keepassxc',
            name='KeePassXC',
            description='Password manager',
            description_ar='مدير كلمات المرور',
            category='utilities',
            icon='keepassxc',
            pacman='keepassxc',
            apt='keepassxc',
            dnf='keepassxc',
            flatpak='org.keepassxc.KeePassXC',
            snap='keepassxc',
            website='https://keepassxc.org',
            keywords=['password', 'security', 'manager'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='syncthing',
            name='Syncthing',
            description='File synchronization',
            description_ar='مزامنة الملفات',
            category='utilities',
            icon='syncthing',
            pacman='syncthing',
            apt='syncthing',
            dnf='syncthing',
            flatpak='me.kozec.syncthingtk',
            website='https://syncthing.net',
            keywords=['sync', 'files', 'backup', 'cloud'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='rclone',
            name='Rclone',
            description='Cloud storage sync',
            description_ar='مزامنة التخزين السحابي',
            category='utilities',
            icon='rclone',
            pacman='rclone',
            apt='rclone',
            dnf='rclone',
            website='https://rclone.org',
            keywords=['cloud', 'sync', 'storage', 'backup'],
        ))
        
        self._add_app(AppEntry(
            id='bleachbit',
            name='BleachBit',
            description='System cleaner',
            description_ar='منظف النظام',
            category='utilities',
            icon='bleachbit',
            pacman='bleachbit',
            apt='bleachbit',
            dnf='bleachbit',
            flatpak='org.bleachbit.BleachBit',
            website='https://bleachbit.org',
            keywords=['cleaner', 'privacy', 'disk', 'cache'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='stacer',
            name='Stacer',
            description='System optimizer',
            description_ar='محسن النظام',
            category='utilities',
            icon='stacer',
            pacman='stacer',  # AUR
            apt='stacer',
            website='https://oguzhaninan.github.io/Stacer-Web',
            keywords=['optimizer', 'cleaner', 'system', 'monitor'],
        ))
        
        # ============ الأمان ============
        self._add_app(AppEntry(
            id='protonvpn',
            name='ProtonVPN',
            description='Secure VPN service',
            description_ar='خدمة VPN آمنة',
            category='security',
            icon='protonvpn',
            pacman='protonvpn',  # AUR
            apt='protonvpn',
            flatpak='com.protonvpn.www',
            website='https://protonvpn.com',
            keywords=['vpn', 'privacy', 'security', 'network'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='mullvad-vpn',
            name='Mullvad VPN',
            description='Privacy-focused VPN',
            description_ar='VPN يركز على الخصوصية',
            category='security',
            icon='mullvad-vpn',
            pacman='mullvad-vpn',  # AUR
            apt='mullvad-vpn',
            website='https://mullvad.net',
            keywords=['vpn', 'privacy', 'security'],
        ))
        
        self._add_app(AppEntry(
            id='clamav',
            name='ClamAV',
            description='Antivirus engine',
            description_ar='محرك مكافحة الفيروسات',
            category='security',
            icon='clamav',
            pacman='clamav',
            apt='clamav',
            dnf='clamav',
            zypper='clamav',
            website='https://clamav.net',
            keywords=['antivirus', 'security', 'malware', 'scan'],
        ))
        
        self._add_app(AppEntry(
            id='veracrypt',
            name='VeraCrypt',
            description='Disk encryption',
            description_ar='تشفير القرص',
            category='security',
            icon='veracrypt',
            pacman='veracrypt',
            apt='veracrypt',
            website='https://veracrypt.fr',
            keywords=['encryption', 'security', 'disk', 'privacy'],
            popular=True
        ))
        
        # ============ الحزم والأدوات البرمجية ============
        self._add_app(AppEntry(
            id='git',
            name='Git',
            description='Version control system',
            description_ar='نظام التحكم في الإصدارات',
            category='packages',
            icon='git',
            is_app=False,
            pacman='git',
            apt='git',
            dnf='git',
            zypper='git',
            website='https://git-scm.com',
            keywords=['version', 'control', 'vcs', 'development'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='nodejs',
            name='Node.js',
            description='JavaScript runtime',
            description_ar='بيئة تشغيل جافاسكريبت',
            category='packages',
            icon='nodejs',
            is_app=False,
            pacman='nodejs',
            apt='nodejs',
            dnf='nodejs',
            zypper='nodejs',
            website='https://nodejs.org',
            keywords=['javascript', 'node', 'npm', 'development'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='python',
            name='Python',
            description='Programming language',
            description_ar='لغة برمجة',
            category='packages',
            icon='python',
            is_app=False,
            pacman='python',
            apt='python3',
            dnf='python3',
            zypper='python3',
            website='https://python.org',
            keywords=['programming', 'language', 'development'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='rust',
            name='Rust',
            description='Systems programming language',
            description_ar='لغة برمجة الأنظمة',
            category='packages',
            icon='rust',
            is_app=False,
            pacman='rust',
            apt='rustc',
            dnf='rust',
            website='https://rust-lang.org',
            keywords=['programming', 'language', 'systems'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='go',
            name='Go',
            description='Programming language by Google',
            description_ar='لغة برمجة من جوجل',
            category='packages',
            icon='go',
            is_app=False,
            pacman='go',
            apt='golang',
            dnf='golang',
            website='https://go.dev',
            keywords=['programming', 'language', 'google'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='docker',
            name='Docker',
            description='Container platform',
            description_ar='منصة الحاويات',
            category='packages',
            icon='docker',
            is_app=False,
            pacman='docker',
            apt='docker.io',
            dnf='docker',
            website='https://docker.com',
            keywords=['container', 'devops', 'virtualization'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='yay',
            name='yay',
            description='AUR helper for Arch Linux',
            description_ar='مساعد AUR لـ Arch Linux',
            category='packages',
            icon='package',
            is_app=False,
            pacman='yay',  # AUR
            website='https://github.com/Jguer/yay',
            keywords=['aur', 'arch', 'helper', 'package'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='paru',
            name='paru',
            description='Feature-rich AUR helper',
            description_ar='مساعد AUR غني بالميزات',
            category='packages',
            icon='package',
            is_app=False,
            pacman='paru',  # AUR
            website='https://github.com/Morganamilo/paru',
            keywords=['aur', 'arch', 'helper', 'package'],
        ))
        
        self._add_app(AppEntry(
            id='flatpak',
            name='Flatpak',
            description='Application sandboxing',
            description_ar='عزل التطبيقات',
            category='packages',
            icon='flatpak',
            is_app=False,
            pacman='flatpak',
            apt='flatpak',
            dnf='flatpak',
            zypper='flatpak',
            website='https://flatpak.org',
            keywords=['sandbox', 'package', 'universal'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='snapd',
            name='Snapd',
            description='Snap package manager',
            description_ar='مدير حزم Snap',
            category='packages',
            icon='snapcraft',
            is_app=False,
            pacman='snapd',  # AUR
            apt='snapd',
            dnf='snapd',
            website='https://snapcraft.io',
            keywords=['snap', 'package', 'universal'],
        ))
        
        self._add_app(AppEntry(
            id='neovim',
            name='Neovim',
            description='Hyperextensible Vim-based editor',
            description_ar='محرر Vim قابل للتوسيع',
            category='packages',
            icon='nvim',
            is_app=False,
            pacman='neovim',
            apt='neovim',
            dnf='neovim',
            snap='nvim',
            website='https://neovim.io',
            keywords=['editor', 'vim', 'terminal', 'text'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='tmux',
            name='tmux',
            description='Terminal multiplexer',
            description_ar='مضاعف الطرفية',
            category='packages',
            icon='terminal',
            is_app=False,
            pacman='tmux',
            apt='tmux',
            dnf='tmux',
            website='https://github.com/tmux/tmux',
            keywords=['terminal', 'multiplexer', 'session'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='zsh',
            name='Zsh',
            description='Z shell',
            description_ar='صدفة Z',
            category='packages',
            icon='terminal',
            is_app=False,
            pacman='zsh',
            apt='zsh',
            dnf='zsh',
            website='https://zsh.org',
            keywords=['shell', 'terminal', 'bash'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='fish',
            name='Fish',
            description='Friendly interactive shell',
            description_ar='صدفة تفاعلية ودية',
            category='packages',
            icon='terminal',
            is_app=False,
            pacman='fish',
            apt='fish',
            dnf='fish',
            website='https://fishshell.com',
            keywords=['shell', 'terminal', 'friendly'],
        ))
        
        self._add_app(AppEntry(
            id='wget',
            name='wget',
            description='Network downloader',
            description_ar='أداة تحميل من الشبكة',
            category='packages',
            icon='download',
            is_app=False,
            pacman='wget',
            apt='wget',
            dnf='wget',
            website='https://gnu.org/software/wget',
            keywords=['download', 'network', 'http'],
        ))
        
        self._add_app(AppEntry(
            id='curl',
            name='curl',
            description='Data transfer tool',
            description_ar='أداة نقل البيانات',
            category='packages',
            icon='download',
            is_app=False,
            pacman='curl',
            apt='curl',
            dnf='curl',
            website='https://curl.se',
            keywords=['download', 'network', 'http', 'api'],
        ))
        
        self._add_app(AppEntry(
            id='ffmpeg',
            name='FFmpeg',
            description='Multimedia framework',
            description_ar='إطار عمل الوسائط المتعددة',
            category='packages',
            icon='video',
            is_app=False,
            pacman='ffmpeg',
            apt='ffmpeg',
            dnf='ffmpeg',
            website='https://ffmpeg.org',
            keywords=['video', 'audio', 'convert', 'encode'],
            popular=True
        ))
        
        self._add_app(AppEntry(
            id='imagemagick',
            name='ImageMagick',
            description='Image manipulation',
            description_ar='معالجة الصور',
            category='packages',
            icon='image',
            is_app=False,
            pacman='imagemagick',
            apt='imagemagick',
            dnf='ImageMagick',
            website='https://imagemagick.org',
            keywords=['image', 'convert', 'edit', 'graphics'],
        ))
        
        self._add_app(AppEntry(
            id='nginx',
            name='Nginx',
            description='Web server',
            description_ar='خادم ويب',
            category='packages',
            icon='server',
            is_app=False,
            pacman='nginx',
            apt='nginx',
            dnf='nginx',
            website='https://nginx.org',
            keywords=['web', 'server', 'http', 'proxy'],
        ))
        
        self._add_app(AppEntry(
            id='apache',
            name='Apache',
            description='HTTP server',
            description_ar='خادم HTTP',
            category='packages',
            icon='server',
            is_app=False,
            pacman='apache',
            apt='apache2',
            dnf='httpd',
            website='https://httpd.apache.org',
            keywords=['web', 'server', 'http'],
        ))
        
        self._add_app(AppEntry(
            id='mysql',
            name='MySQL',
            description='Relational database',
            description_ar='قاعدة بيانات علائقية',
            category='packages',
            icon='database',
            is_app=False,
            pacman='mysql',
            apt='mysql-server',
            dnf='mysql-server',
            website='https://mysql.com',
            keywords=['database', 'sql', 'server'],
        ))
        
        self._add_app(AppEntry(
            id='postgresql',
            name='PostgreSQL',
            description='Advanced database',
            description_ar='قاعدة بيانات متقدمة',
            category='packages',
            icon='database',
            is_app=False,
            pacman='postgresql',
            apt='postgresql',
            dnf='postgresql-server',
            website='https://postgresql.org',
            keywords=['database', 'sql', 'server'],
        ))
        
        self._add_app(AppEntry(
            id='redis',
            name='Redis',
            description='In-memory data store',
            description_ar='مخزن بيانات في الذاكرة',
            category='packages',
            icon='database',
            is_app=False,
            pacman='redis',
            apt='redis-server',
            dnf='redis',
            website='https://redis.io',
            keywords=['database', 'cache', 'memory'],
        ))
        
        self._add_app(AppEntry(
            id='mongodb',
            name='MongoDB',
            description='NoSQL database',
            description_ar='قاعدة بيانات NoSQL',
            category='packages',
            icon='database',
            is_app=False,
            pacman='mongodb-bin',  # AUR
            apt='mongodb',
            website='https://mongodb.com',
            keywords=['database', 'nosql', 'document'],
        ))
    
    def _add_app(self, app: AppEntry):
        """إضافة تطبيق للقاعدة"""
        self.apps[app.id] = app
    
    def get_app(self, app_id: str) -> Optional[AppEntry]:
        """الحصول على تطبيق بالمعرف"""
        return self.apps.get(app_id)
    
    def get_all_apps(self) -> List[AppEntry]:
        """الحصول على جميع التطبيقات"""
        return list(self.apps.values())
    
    def get_apps_by_category(self, category: str) -> List[AppEntry]:
        """الحصول على تطبيقات حسب التصنيف"""
        return [app for app in self.apps.values() if app.category == category]
    
    def get_featured_apps(self) -> List[AppEntry]:
        """الحصول على التطبيقات المميزة"""
        return [app for app in self.apps.values() if app.featured]
    
    def get_popular_apps(self) -> List[AppEntry]:
        """الحصول على التطبيقات الشائعة"""
        return [app for app in self.apps.values() if app.popular]
    
    def get_applications(self) -> List[AppEntry]:
        """الحصول على التطبيقات فقط (ليس الحزم)"""
        return [app for app in self.apps.values() if app.is_app]
    
    def get_packages(self) -> List[AppEntry]:
        """الحصول على الحزم فقط"""
        return [app for app in self.apps.values() if not app.is_app]
    
    def search(self, query: str) -> List[AppEntry]:
        """البحث في التطبيقات"""
        query = query.lower()
        results = []
        
        for app in self.apps.values():
            # البحث في الاسم
            if query in app.name.lower():
                results.append(app)
                continue
            
            # البحث في الوصف
            if query in app.description.lower() or query in app.description_ar:
                results.append(app)
                continue
            
            # البحث في الكلمات المفتاحية
            if any(query in kw.lower() for kw in app.keywords):
                results.append(app)
                continue
        
        return results
    
    def get_categories(self) -> Dict:
        """الحصول على التصنيفات"""
        return self.CATEGORIES
    
    def export_to_json(self, filepath: str):
        """تصدير القاعدة إلى JSON"""
        data = {
            'categories': self.CATEGORIES,
            'apps': {
                app_id: {
                    'id': app.id,
                    'name': app.name,
                    'description': app.description,
                    'description_ar': app.description_ar,
                    'category': app.category,
                    'icon': app.icon,
                    'is_app': app.is_app,
                    'website': app.website,
                    'pacman': app.pacman,
                    'apt': app.apt,
                    'dnf': app.dnf,
                    'zypper': app.zypper,
                    'flatpak': app.flatpak,
                    'snap': app.snap,
                    'keywords': app.keywords,
                    'featured': app.featured,
                    'popular': app.popular,
                }
                for app_id, app in self.apps.items()
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def import_from_json(self, filepath: str):
        """استيراد القاعدة من JSON"""
        if not os.path.exists(filepath):
            return
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for app_id, app_data in data.get('apps', {}).items():
            self._add_app(AppEntry(**app_data))


if __name__ == '__main__':
    db = AppDatabase()
    print(f"عدد التطبيقات: {len(db.get_all_apps())}")
    print(f"عدد التطبيقات المميزة: {len(db.get_featured_apps())}")
    print(f"عدد التصنيفات: {len(db.get_categories())}")
    
    # تصدير للاختبار
    db.export_to_json('/tmp/apps.json')
