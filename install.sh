#!/bin/bash
#
# Linux Store - Installation Script
# سكربت تثبيت متجر لينكس
#

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║           🐧 Linux Store - متجر لينكس                      ║"
echo "║              سكربت التثبيت                                 ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# الألوان
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# دالة الطباعة الملونة
print_status() {
    echo -e "${BLUE}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# اكتشاف التوزيعة
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO_ID=$ID
        DISTRO_NAME=$NAME
    elif [ -f /etc/lsb-release ]; then
        . /etc/lsb-release
        DISTRO_ID=$DISTRIB_ID
        DISTRO_NAME=$DISTRIB_DESCRIPTION
    else
        DISTRO_ID="unknown"
        DISTRO_NAME="Unknown Linux"
    fi
    
    echo ""
    print_status "التوزيعة المكتشفة: $DISTRO_NAME"
}

# تثبيت التبعيات
install_dependencies() {
    print_status "جاري تثبيت التبعيات..."
    
    case $DISTRO_ID in
        arch|manjaro|endeavouros|garuda|artix|arcolinux)
            print_status "استخدام pacman..."
            sudo pacman -S --noconfirm python python-pip python-pyqt6 2>/dev/null || \
            sudo pacman -S --noconfirm python python-pip python-pyqt5 2>/dev/null || \
            print_warning "فشل تثبيت PyQt من pacman، سيتم استخدام pip"
            ;;
        
        debian|ubuntu|linuxmint|pop|elementary|zorin|kali|parrot|mx)
            print_status "استخدام apt..."
            sudo apt update
            sudo apt install -y python3 python3-pip python3-pyqt6 2>/dev/null || \
            sudo apt install -y python3 python3-pip python3-pyqt5 2>/dev/null || \
            print_warning "فشل تثبيت PyQt من apt، سيتم استخدام pip"
            ;;
        
        fedora|centos|rhel|rocky|alma|nobara)
            print_status "استخدام dnf..."
            sudo dnf install -y python3 python3-pip python3-qt6 2>/dev/null || \
            sudo dnf install -y python3 python3-pip python3-qt5 2>/dev/null || \
            print_warning "فشل تثبيت PyQt من dnf، سيتم استخدام pip"
            ;;
        
        opensuse*)
            print_status "استخدام zypper..."
            sudo zypper install -y python3 python3-pip python3-qt6 2>/dev/null || \
            sudo zypper install -y python3 python3-pip python3-qt5 2>/dev/null || \
            print_warning "فشل تثبيت PyQt من zypper، سيتم استخدام pip"
            ;;
        
        *)
            print_warning "توزيعة غير معروفة، سيتم استخدام pip"
            ;;
    esac
    
    # محاولة تثبيت PyQt6 عبر pip إذا لم يكن مثبتاً
    if ! python3 -c "import PyQt6" 2>/dev/null && ! python3 -c "import PyQt5" 2>/dev/null; then
        print_status "تثبيت PyQt6 عبر pip..."
        pip3 install --user PyQt6 || pip3 install --user PyQt5
    fi
    
    print_success "تم تثبيت التبعيات"
}

# إنشاء اختصار سطح المكتب
create_desktop_entry() {
    print_status "إنشاء اختصار سطح المكتب..."
    
    INSTALL_DIR="$HOME/.local/share/linux-store"
    DESKTOP_FILE="$HOME/.local/share/applications/linux-store.desktop"
    
    # إنشاء مجلد التثبيت
    mkdir -p "$INSTALL_DIR"
    mkdir -p "$HOME/.local/share/applications"
    
    # نسخ الملفات
    cp -r "$(dirname "$0")"/* "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/linux-store.py"
    
    # إنشاء ملف .desktop
    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Name=Linux Store
Name[ar]=متجر لينكس
Comment=Application store for Linux
Comment[ar]=متجر تطبيقات لنظام لينكس
Exec=python3 $INSTALL_DIR/linux-store.py
Icon=system-software-install
Terminal=false
Type=Application
Categories=System;PackageManager;
Keywords=store;apps;packages;install;
EOF
    
    chmod +x "$DESKTOP_FILE"
    
    # تحديث قاعدة بيانات سطح المكتب
    if command -v update-desktop-database &> /dev/null; then
        update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
    fi
    
    print_success "تم إنشاء اختصار سطح المكتب"
}

# إنشاء أمر في PATH
create_command() {
    print_status "إنشاء أمر linux-store..."
    
    BIN_DIR="$HOME/.local/bin"
    mkdir -p "$BIN_DIR"
    
    cat > "$BIN_DIR/linux-store" << EOF
#!/bin/bash
python3 $HOME/.local/share/linux-store/linux-store.py "\$@"
EOF
    
    chmod +x "$BIN_DIR/linux-store"
    
    # التحقق من وجود المسار في PATH
    if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
        print_warning "أضف المسار التالي إلى PATH: $BIN_DIR"
        print_warning "أضف هذا السطر إلى ~/.bashrc أو ~/.zshrc:"
        echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
    fi
    
    print_success "تم إنشاء الأمر linux-store"
}

# التثبيت الرئيسي
main() {
    detect_distro
    echo ""
    
    # التحقق من Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 غير مثبت!"
        exit 1
    fi
    
    print_success "Python 3 موجود: $(python3 --version)"
    echo ""
    
    # تثبيت التبعيات
    install_dependencies
    echo ""
    
    # إنشاء الاختصارات
    create_desktop_entry
    create_command
    
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║              ✓ تم التثبيت بنجاح!                          ║"
    echo "╠════════════════════════════════════════════════════════════╣"
    echo "║  لتشغيل التطبيق:                                          ║"
    echo "║    • من القائمة: ابحث عن 'Linux Store'                    ║"
    echo "║    • من الطرفية: linux-store                              ║"
    echo "║    • مباشرة: python3 linux-store.py                       ║"
    echo "╚════════════════════════════════════════════════════════════╝"
}

# تشغيل
main "$@"
