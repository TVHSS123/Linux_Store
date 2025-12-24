#!/usr/bin/env python3
"""
Linux Store - Distro Detector & Package Manager Handler
يكتشف نوع التوزيعة ويحدد مدير الحزم المناسب
"""

import subprocess
import os
import re
from typing import Dict, Optional, List, Tuple

class DistroDetector:
    """كلاس لاكتشاف توزيعة لينكس ومدير الحزم"""
    
    # قائمة التوزيعات المدعومة ومديري الحزم
    DISTRO_PACKAGE_MANAGERS = {
        # Arch-based
        'arch': ['yay', 'paru', 'pacman'],
        'manjaro': ['yay', 'paru', 'pacman'],
        'endeavouros': ['yay', 'paru', 'pacman'],
        'garuda': ['paru', 'yay', 'pacman'],
        'artix': ['yay', 'pacman'],
        'arcolinux': ['yay', 'pacman'],
        
        # Debian-based
        'debian': ['apt', 'apt-get', 'nala'],
        'ubuntu': ['apt', 'apt-get', 'nala', 'snap'],
        'linuxmint': ['apt', 'apt-get', 'nala'],
        'pop': ['apt', 'apt-get'],
        'elementary': ['apt', 'apt-get'],
        'zorin': ['apt', 'apt-get'],
        'kali': ['apt', 'apt-get'],
        'parrot': ['apt', 'apt-get'],
        'mx': ['apt', 'apt-get'],
        
        # Red Hat-based
        'fedora': ['dnf', 'yum'],
        'centos': ['dnf', 'yum'],
        'rhel': ['dnf', 'yum'],
        'rocky': ['dnf', 'yum'],
        'alma': ['dnf', 'yum'],
        'nobara': ['dnf', 'yum'],
        
        # SUSE-based
        'opensuse': ['zypper'],
        'opensuse-leap': ['zypper'],
        'opensuse-tumbleweed': ['zypper'],
        
        # Other
        'void': ['xbps-install'],
        'gentoo': ['emerge'],
        'alpine': ['apk'],
        'nixos': ['nix-env'],
        'solus': ['eopkg'],
        'clear': ['swupd'],
    }
    
    # أوامر التثبيت لكل مدير حزم
    INSTALL_COMMANDS = {
        'pacman': 'sudo pacman -S --noconfirm',
        'yay': 'yay -S --noconfirm',
        'paru': 'paru -S --noconfirm',
        'apt': 'sudo apt install -y',
        'apt-get': 'sudo apt-get install -y',
        'nala': 'sudo nala install -y',
        'snap': 'sudo snap install',
        'flatpak': 'flatpak install -y',
        'dnf': 'sudo dnf install -y',
        'yum': 'sudo yum install -y',
        'zypper': 'sudo zypper install -y',
        'xbps-install': 'sudo xbps-install -y',
        'emerge': 'sudo emerge',
        'apk': 'sudo apk add',
        'nix-env': 'nix-env -iA',
        'eopkg': 'sudo eopkg install -y',
        'swupd': 'sudo swupd bundle-add',
    }
    
    # أوامر الإزالة لكل مدير حزم
    REMOVE_COMMANDS = {
        'pacman': 'sudo pacman -R --noconfirm',
        'yay': 'yay -R --noconfirm',
        'paru': 'paru -R --noconfirm',
        'apt': 'sudo apt remove -y',
        'apt-get': 'sudo apt-get remove -y',
        'nala': 'sudo nala remove -y',
        'snap': 'sudo snap remove',
        'flatpak': 'flatpak uninstall -y',
        'dnf': 'sudo dnf remove -y',
        'yum': 'sudo yum remove -y',
        'zypper': 'sudo zypper remove -y',
        'xbps-install': 'sudo xbps-remove -y',
        'emerge': 'sudo emerge --unmerge',
        'apk': 'sudo apk del',
        'nix-env': 'nix-env -e',
        'eopkg': 'sudo eopkg remove -y',
        'swupd': 'sudo swupd bundle-remove',
    }
    
    # أوامر البحث لكل مدير حزم
    SEARCH_COMMANDS = {
        'pacman': 'pacman -Ss',
        'yay': 'yay -Ss',
        'paru': 'paru -Ss',
        'apt': 'apt search',
        'apt-get': 'apt-cache search',
        'nala': 'nala search',
        'dnf': 'dnf search',
        'yum': 'yum search',
        'zypper': 'zypper search',
        'xbps-install': 'xbps-query -Rs',
        'emerge': 'emerge --search',
        'apk': 'apk search',
        'nix-env': 'nix-env -qaP',
        'eopkg': 'eopkg search',
        'swupd': 'swupd search',
    }
    
    # أوامر التحديث لكل مدير حزم
    UPDATE_COMMANDS = {
        'pacman': 'sudo pacman -Syu --noconfirm',
        'yay': 'yay -Syu --noconfirm',
        'paru': 'paru -Syu --noconfirm',
        'apt': 'sudo apt update && sudo apt upgrade -y',
        'apt-get': 'sudo apt-get update && sudo apt-get upgrade -y',
        'nala': 'sudo nala update && sudo nala upgrade -y',
        'dnf': 'sudo dnf upgrade -y',
        'yum': 'sudo yum update -y',
        'zypper': 'sudo zypper update -y',
        'xbps-install': 'sudo xbps-install -Su',
        'emerge': 'sudo emerge --update --deep @world',
        'apk': 'sudo apk update && sudo apk upgrade',
        'nix-env': 'nix-channel --update && nix-env -u',
        'eopkg': 'sudo eopkg upgrade -y',
        'swupd': 'sudo swupd update',
    }
    
    def __init__(self):
        self.distro_id = None
        self.distro_name = None
        self.distro_version = None
        self.package_manager = None
        self.available_managers = []
        self.arch = None
        self._detect()
    
    def _detect(self):
        """اكتشاف التوزيعة ومدير الحزم"""
        self._detect_distro()
        self._detect_arch()
        self._detect_package_managers()
    
    def _detect_distro(self):
        """اكتشاف التوزيعة من ملفات النظام"""
        # محاولة قراءة /etc/os-release
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release', 'r') as f:
                content = f.read()
                
            # استخراج ID
            id_match = re.search(r'^ID=(.*)$', content, re.MULTILINE)
            if id_match:
                self.distro_id = id_match.group(1).strip('"').lower()
            
            # استخراج NAME
            name_match = re.search(r'^NAME=(.*)$', content, re.MULTILINE)
            if name_match:
                self.distro_name = name_match.group(1).strip('"')
            
            # استخراج VERSION_ID
            version_match = re.search(r'^VERSION_ID=(.*)$', content, re.MULTILINE)
            if version_match:
                self.distro_version = version_match.group(1).strip('"')
            
            # استخراج ID_LIKE للتوزيعات المشتقة
            id_like_match = re.search(r'^ID_LIKE=(.*)$', content, re.MULTILINE)
            if id_like_match:
                self.distro_like = id_like_match.group(1).strip('"').split()
            else:
                self.distro_like = []
        
        # محاولة قراءة /etc/lsb-release كبديل
        elif os.path.exists('/etc/lsb-release'):
            with open('/etc/lsb-release', 'r') as f:
                content = f.read()
            
            id_match = re.search(r'^DISTRIB_ID=(.*)$', content, re.MULTILINE)
            if id_match:
                self.distro_id = id_match.group(1).strip('"').lower()
            
            name_match = re.search(r'^DISTRIB_DESCRIPTION=(.*)$', content, re.MULTILINE)
            if name_match:
                self.distro_name = name_match.group(1).strip('"')
    
    def _detect_arch(self):
        """اكتشاف معمارية النظام"""
        try:
            result = subprocess.run(['uname', '-m'], capture_output=True, text=True)
            self.arch = result.stdout.strip()
        except:
            self.arch = 'unknown'
    
    def _detect_package_managers(self):
        """اكتشاف مديري الحزم المتاحين"""
        self.available_managers = []
        
        # الحصول على قائمة مديري الحزم المحتملين للتوزيعة
        potential_managers = self.DISTRO_PACKAGE_MANAGERS.get(
            self.distro_id, 
            self._get_managers_by_like()
        )
        
        # إضافة flatpak و snap كخيارات عامة
        all_managers = list(potential_managers) + ['flatpak', 'snap']
        
        # التحقق من المتاح
        for manager in all_managers:
            if self._is_command_available(manager):
                self.available_managers.append(manager)
        
        # تحديد المدير الافتراضي
        if self.available_managers:
            self.package_manager = self.available_managers[0]
    
    def _get_managers_by_like(self) -> List[str]:
        """الحصول على مديري الحزم بناءً على ID_LIKE"""
        if hasattr(self, 'distro_like'):
            for like in self.distro_like:
                if like in self.DISTRO_PACKAGE_MANAGERS:
                    return self.DISTRO_PACKAGE_MANAGERS[like]
        return ['apt', 'dnf', 'pacman']  # افتراضي
    
    def _is_command_available(self, command: str) -> bool:
        """التحقق من توفر أمر معين"""
        try:
            result = subprocess.run(
                ['which', command], 
                capture_output=True, 
                text=True
            )
            return result.returncode == 0
        except:
            return False
    
    def get_install_command(self, package: str, manager: str = None) -> str:
        """الحصول على أمر التثبيت"""
        manager = manager or self.package_manager
        base_cmd = self.INSTALL_COMMANDS.get(manager, '')
        return f"{base_cmd} {package}"
    
    def get_remove_command(self, package: str, manager: str = None) -> str:
        """الحصول على أمر الإزالة"""
        manager = manager or self.package_manager
        base_cmd = self.REMOVE_COMMANDS.get(manager, '')
        return f"{base_cmd} {package}"
    
    def get_search_command(self, query: str, manager: str = None) -> str:
        """الحصول على أمر البحث"""
        manager = manager or self.package_manager
        base_cmd = self.SEARCH_COMMANDS.get(manager, '')
        return f"{base_cmd} {query}"
    
    def get_update_command(self, manager: str = None) -> str:
        """الحصول على أمر التحديث"""
        manager = manager or self.package_manager
        return self.UPDATE_COMMANDS.get(manager, '')
    
    def get_info(self) -> Dict:
        """الحصول على معلومات النظام"""
        return {
            'distro_id': self.distro_id,
            'distro_name': self.distro_name,
            'distro_version': self.distro_version,
            'architecture': self.arch,
            'package_manager': self.package_manager,
            'available_managers': self.available_managers,
        }
    
    def is_package_installed(self, package: str) -> bool:
        """التحقق من تثبيت حزمة"""
        check_commands = {
            'pacman': f'pacman -Q {package}',
            'yay': f'yay -Q {package}',
            'paru': f'paru -Q {package}',
            'apt': f'dpkg -l {package}',
            'apt-get': f'dpkg -l {package}',
            'nala': f'dpkg -l {package}',
            'dnf': f'rpm -q {package}',
            'yum': f'rpm -q {package}',
            'zypper': f'rpm -q {package}',
            'flatpak': f'flatpak list | grep -i {package}',
            'snap': f'snap list {package}',
        }
        
        cmd = check_commands.get(self.package_manager, '')
        if not cmd:
            return False
        
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True
            )
            return result.returncode == 0
        except:
            return False


if __name__ == '__main__':
    detector = DistroDetector()
    info = detector.get_info()
    print("=== معلومات النظام ===")
    for key, value in info.items():
        print(f"{key}: {value}")
