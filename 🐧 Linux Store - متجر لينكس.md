# 🐧 Linux Store - متجر لينكس

<div align="center">

![Linux Store Logo](https://img.shields.io/badge/Linux-Store-blue?style=for-the-badge&logo=linux&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt-6-orange?style=for-the-badge&logo=qt&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**متجر تطبيقات لنظام لينكس مشابه لـ Google Play Store و Apple App Store**

[English](#english) | [العربية](#العربية)

</div>

---

## العربية

### 📖 ما هو Linux Store؟

Linux Store هو متجر تطبيقات مفتوح المصدر لنظام لينكس، يوفر واجهة رسومية جميلة وسهلة الاستخدام لتثبيت وإزالة التطبيقات والحزم. يعمل على جميع توزيعات لينكس الشائعة ويكتشف تلقائياً نوع التوزيعة ومدير الحزم المناسب.

### ✨ المميزات

- 🎨 **واجهة جميلة**: تصميم عصري مشابه لـ Google Play Store
- 🔍 **اكتشاف تلقائي**: يكتشف التوزيعة ومدير الحزم تلقائياً
- 📦 **دعم متعدد**: يدعم pacman, apt, dnf, zypper, flatpak, snap
- 🏷️ **تصنيفات متعددة**: إنترنت، تطوير، ألعاب، رسومات، وسائط، مكتب، نظام، أدوات، أمان
- 🔎 **بحث سريع**: ابحث في التطبيقات والحزم بسهولة
- ⚡ **خفيف وسريع**: مصمم ليعمل على جميع الأجهزة
- 🌐 **دعم عربي**: واجهة ثنائية اللغة (عربي/إنجليزي)

### 🖥️ التوزيعات المدعومة

| التوزيعة | مدير الحزم | الحالة |
|---------|-----------|--------|
| Arch Linux | pacman, yay, paru | ✅ مدعوم |
| Manjaro | pacman, yay | ✅ مدعوم |
| EndeavourOS | pacman, yay | ✅ مدعوم |
| Garuda Linux | paru, pacman | ✅ مدعوم |
| Ubuntu | apt, snap | ✅ مدعوم |
| Debian | apt | ✅ مدعوم |
| Linux Mint | apt | ✅ مدعوم |
| Pop!_OS | apt | ✅ مدعوم |
| Kali Linux | apt | ✅ مدعوم |
| Fedora | dnf | ✅ مدعوم |
| CentOS | dnf, yum | ✅ مدعوم |
| openSUSE | zypper | ✅ مدعوم |
| Void Linux | xbps | ✅ مدعوم |
| Alpine | apk | ✅ مدعوم |

### 📥 التثبيت

#### الطريقة السريعة (موصى بها)

```bash
# استنساخ المستودع
git clone https://github.com/YOUR_USERNAME/linux-store.git
cd linux-store

# تشغيل سكربت التثبيت
chmod +x install.sh
./install.sh
```

#### التثبيت اليدوي

```bash
# تثبيت التبعيات
# Arch Linux
sudo pacman -S python python-pyqt6

# Ubuntu/Debian
sudo apt install python3 python3-pyqt6

# Fedora
sudo dnf install python3 python3-qt6

# أو عبر pip
pip3 install PyQt6

# تشغيل التطبيق
python3 linux-store.py
```

### 🚀 الاستخدام

```bash
# من الطرفية
linux-store

# أو مباشرة
python3 linux-store.py

# أو من قائمة التطبيقات
# ابحث عن "Linux Store"
```

### 📸 لقطات الشاشة

```
┌─────────────────────────────────────────────────────────────┐
│  🐧 Linux Store                    🔍 ابحث عن تطبيقات...    │
├─────────────────────────────────────────────────────────────┤
│ ┌──────────┐                                                │
│ │ 🏠 الرئيسية │  ⭐ التطبيقات المميزة                        │
│ │ 📱 التطبيقات│  ┌────┐ ┌────┐ ┌────┐ ┌────┐               │
│ │ 📦 الحزم   │  │ 🦊 │ │ 💬 │ │ 🎮 │ │ 🎨 │               │
│ ├──────────┤  │Fire│ │Tele│ │Steam│ │GIMP│               │
│ │ التصنيفات │  │fox │ │gram│ │    │ │    │               │
│ │ 🌐 الإنترنت│  └────┘ └────┘ └────┘ └────┘               │
│ │ 💻 التطوير │                                              │
│ │ 🎮 الألعاب │  🔥 الأكثر شعبية                             │
│ │ 🎨 الرسومات│  ┌────┐ ┌────┐ ┌────┐ ┌────┐               │
│ │ 🎬 الوسائط │  │ 📝 │ │ 🎵 │ │ 📹 │ │ 🔒 │               │
│ │ 📄 المكتب │  │VS  │ │Spot│ │OBS │ │Bit │               │
│ │ ⚙️ النظام │  │Code│ │ify │ │    │ │ward│               │
│ │ 🔧 الأدوات │  └────┘ └────┘ └────┘ └────┘               │
│ └──────────┘                                                │
├─────────────────────────────────────────────────────────────┤
│ 📦 Ubuntu 22.04 | ⚙️ apt                          جاهز     │
└─────────────────────────────────────────────────────────────┘
```

### 📂 هيكل المشروع

```
linux-store/
├── linux-store.py      # الملف الرئيسي
├── install.sh          # سكربت التثبيت
├── uninstall.sh        # سكربت إلغاء التثبيت
├── requirements.txt    # التبعيات
├── README.md           # التوثيق
├── LICENSE             # الرخصة
└── src/
    ├── __init__.py
    ├── main_window.py      # الواجهة الرئيسية
    ├── distro_detector.py  # اكتشاف التوزيعة
    ├── package_manager.py  # مدير الحزم
    └── app_database.py     # قاعدة بيانات التطبيقات
```

### 🤝 المساهمة

نرحب بمساهماتكم! يمكنكم:

1. Fork المستودع
2. إنشاء فرع جديد (`git checkout -b feature/amazing-feature`)
3. Commit التغييرات (`git commit -m 'Add amazing feature'`)
4. Push للفرع (`git push origin feature/amazing-feature`)
5. فتح Pull Request

### 📝 الرخصة

هذا المشروع مرخص تحت رخصة MIT - انظر ملف [LICENSE](LICENSE) للتفاصيل.

---

## English

### 📖 What is Linux Store?

Linux Store is an open-source application store for Linux, providing a beautiful and easy-to-use graphical interface for installing and removing applications and packages. It works on all popular Linux distributions and automatically detects the distribution type and appropriate package manager.

### ✨ Features

- 🎨 **Beautiful Interface**: Modern design similar to Google Play Store
- 🔍 **Auto Detection**: Automatically detects distro and package manager
- 📦 **Multi Support**: Supports pacman, apt, dnf, zypper, flatpak, snap
- 🏷️ **Multiple Categories**: Internet, Development, Games, Graphics, Multimedia, Office, System, Utilities, Security
- 🔎 **Fast Search**: Search apps and packages easily
- ⚡ **Light & Fast**: Designed to work on all devices
- 🌐 **Arabic Support**: Bilingual interface (Arabic/English)

### 📥 Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/linux-store.git
cd linux-store

# Run installation script
chmod +x install.sh
./install.sh
```

### 🚀 Usage

```bash
# From terminal
linux-store

# Or directly
python3 linux-store.py
```

### 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**صنع بـ ❤️ للمجتمع العربي ومجتمع لينكس**

Made with ❤️ for the Arabic and Linux community

</div>
