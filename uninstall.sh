#!/bin/bash
#
# Linux Store - Uninstallation Script
# سكربت إلغاء تثبيت متجر لينكس
#

echo "╔════════════════════════════════════════════════════════════╗"
echo "║           🐧 Linux Store - متجر لينكس                      ║"
echo "║              إلغاء التثبيت                                 ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# الألوان
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${YELLOW}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

# تأكيد الإلغاء
read -p "هل أنت متأكد من إلغاء تثبيت Linux Store؟ (y/N): " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "تم الإلغاء."
    exit 0
fi

echo ""

# حذف مجلد التثبيت
if [ -d "$HOME/.local/share/linux-store" ]; then
    print_status "حذف ملفات التطبيق..."
    rm -rf "$HOME/.local/share/linux-store"
    print_success "تم حذف ملفات التطبيق"
fi

# حذف اختصار سطح المكتب
if [ -f "$HOME/.local/share/applications/linux-store.desktop" ]; then
    print_status "حذف اختصار سطح المكتب..."
    rm -f "$HOME/.local/share/applications/linux-store.desktop"
    print_success "تم حذف اختصار سطح المكتب"
fi

# حذف الأمر
if [ -f "$HOME/.local/bin/linux-store" ]; then
    print_status "حذف الأمر..."
    rm -f "$HOME/.local/bin/linux-store"
    print_success "تم حذف الأمر"
fi

# تحديث قاعدة بيانات سطح المكتب
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              ✓ تم إلغاء التثبيت بنجاح!                     ║"
echo "╚════════════════════════════════════════════════════════════╝"
