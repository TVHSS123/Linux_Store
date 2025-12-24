#!/usr/bin/env python3
"""
Linux Store - متجر لينكس
تطبيق متجر تطبيقات لنظام لينكس مشابه لـ Google Play Store

الاستخدام:
    python3 linux-store.py
    أو
    ./linux-store.py
"""

import sys
import os

# إضافة مجلد src للمسار
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main_window import main

if __name__ == '__main__':
    main()
