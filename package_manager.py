#!/usr/bin/env python3
"""
Linux Store - Package Manager
مدير الحزم للتثبيت والإزالة والبحث
"""

import subprocess
import threading
import queue
from typing import Callable, Optional, List, Dict
from dataclasses import dataclass
from enum import Enum

class PackageStatus(Enum):
    """حالة الحزمة"""
    NOT_INSTALLED = "not_installed"
    INSTALLED = "installed"
    INSTALLING = "installing"
    REMOVING = "removing"
    UPDATING = "updating"
    ERROR = "error"

@dataclass
class PackageInfo:
    """معلومات الحزمة"""
    name: str
    display_name: str
    description: str
    category: str
    icon: str
    package_names: Dict[str, str]  # {package_manager: package_name}
    flatpak_id: Optional[str] = None
    snap_name: Optional[str] = None
    website: Optional[str] = None
    version: Optional[str] = None
    size: Optional[str] = None
    is_app: bool = True  # True للتطبيقات، False للحزم

class PackageManager:
    """مدير العمليات على الحزم"""
    
    def __init__(self, distro_detector):
        self.detector = distro_detector
        self.operation_queue = queue.Queue()
        self.current_operation = None
        self.callbacks = {
            'on_start': None,
            'on_progress': None,
            'on_complete': None,
            'on_error': None,
        }
        self._worker_thread = None
        self._running = False
    
    def set_callback(self, event: str, callback: Callable):
        """تعيين callback لحدث معين"""
        if event in self.callbacks:
            self.callbacks[event] = callback
    
    def _notify(self, event: str, *args, **kwargs):
        """إرسال إشعار"""
        if self.callbacks.get(event):
            self.callbacks[event](*args, **kwargs)
    
    def install_package(self, package_info: PackageInfo, 
                       preferred_manager: str = None) -> bool:
        """تثبيت حزمة"""
        manager = preferred_manager or self._get_best_manager(package_info)
        package_name = self._get_package_name(package_info, manager)
        
        if not package_name:
            self._notify('on_error', package_info, "لم يتم العثور على اسم الحزمة")
            return False
        
        cmd = self.detector.get_install_command(package_name, manager)
        return self._execute_operation(
            'install', 
            package_info, 
            cmd, 
            manager
        )
    
    def remove_package(self, package_info: PackageInfo,
                      preferred_manager: str = None) -> bool:
        """إزالة حزمة"""
        manager = preferred_manager or self._get_best_manager(package_info)
        package_name = self._get_package_name(package_info, manager)
        
        if not package_name:
            self._notify('on_error', package_info, "لم يتم العثور على اسم الحزمة")
            return False
        
        cmd = self.detector.get_remove_command(package_name, manager)
        return self._execute_operation(
            'remove', 
            package_info, 
            cmd, 
            manager
        )
    
    def search_packages(self, query: str, 
                       manager: str = None) -> List[Dict]:
        """البحث عن حزم"""
        manager = manager or self.detector.package_manager
        cmd = self.detector.get_search_command(query, manager)
        
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return self._parse_search_results(result.stdout, manager)
        except subprocess.TimeoutExpired:
            return []
        except Exception as e:
            return []
    
    def update_system(self, manager: str = None) -> bool:
        """تحديث النظام"""
        manager = manager or self.detector.package_manager
        cmd = self.detector.get_update_command(manager)
        
        return self._execute_operation(
            'update',
            None,
            cmd,
            manager
        )
    
    def is_installed(self, package_info: PackageInfo) -> bool:
        """التحقق من تثبيت حزمة"""
        # التحقق من جميع مديري الحزم المتاحين
        for manager in self.detector.available_managers:
            package_name = self._get_package_name(package_info, manager)
            if package_name:
                if self._check_installed(package_name, manager):
                    return True
        return False
    
    def _check_installed(self, package_name: str, manager: str) -> bool:
        """التحقق من تثبيت حزمة بمدير معين"""
        check_commands = {
            'pacman': f'pacman -Q {package_name} 2>/dev/null',
            'yay': f'pacman -Q {package_name} 2>/dev/null',
            'paru': f'pacman -Q {package_name} 2>/dev/null',
            'apt': f'dpkg -l {package_name} 2>/dev/null | grep -q "^ii"',
            'apt-get': f'dpkg -l {package_name} 2>/dev/null | grep -q "^ii"',
            'nala': f'dpkg -l {package_name} 2>/dev/null | grep -q "^ii"',
            'dnf': f'rpm -q {package_name} 2>/dev/null',
            'yum': f'rpm -q {package_name} 2>/dev/null',
            'zypper': f'rpm -q {package_name} 2>/dev/null',
            'flatpak': f'flatpak list 2>/dev/null | grep -qi {package_name}',
            'snap': f'snap list {package_name} 2>/dev/null',
        }
        
        cmd = check_commands.get(manager)
        if not cmd:
            return False
        
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False
    
    def _get_best_manager(self, package_info: PackageInfo) -> str:
        """الحصول على أفضل مدير حزم للتطبيق"""
        # الأولوية: مدير النظام > flatpak > snap
        for manager in self.detector.available_managers:
            if manager in package_info.package_names:
                return manager
            if manager == 'flatpak' and package_info.flatpak_id:
                return 'flatpak'
            if manager == 'snap' and package_info.snap_name:
                return 'snap'
        
        return self.detector.package_manager
    
    def _get_package_name(self, package_info: PackageInfo, 
                         manager: str) -> Optional[str]:
        """الحصول على اسم الحزمة لمدير معين"""
        # التحقق من الاسم المحدد للمدير
        if manager in package_info.package_names:
            return package_info.package_names[manager]
        
        # التحقق من flatpak
        if manager == 'flatpak' and package_info.flatpak_id:
            return package_info.flatpak_id
        
        # التحقق من snap
        if manager == 'snap' and package_info.snap_name:
            return package_info.snap_name
        
        # استخدام الاسم الافتراضي
        return package_info.name
    
    def _execute_operation(self, operation: str, package_info: PackageInfo,
                          cmd: str, manager: str) -> bool:
        """تنفيذ عملية"""
        self._notify('on_start', operation, package_info, manager)
        
        try:
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            output_lines = []
            for line in iter(process.stdout.readline, ''):
                output_lines.append(line)
                self._notify('on_progress', operation, package_info, line.strip())
            
            process.wait()
            
            if process.returncode == 0:
                self._notify('on_complete', operation, package_info, True)
                return True
            else:
                error_msg = ''.join(output_lines[-5:]) if output_lines else "Unknown error"
                self._notify('on_error', package_info, error_msg)
                self._notify('on_complete', operation, package_info, False)
                return False
                
        except Exception as e:
            self._notify('on_error', package_info, str(e))
            self._notify('on_complete', operation, package_info, False)
            return False
    
    def _parse_search_results(self, output: str, manager: str) -> List[Dict]:
        """تحليل نتائج البحث"""
        results = []
        lines = output.strip().split('\n')
        
        if manager in ['pacman', 'yay', 'paru']:
            # تنسيق: repo/package version
            #     description
            i = 0
            while i < len(lines):
                if '/' in lines[i]:
                    parts = lines[i].split('/')
                    if len(parts) >= 2:
                        name_ver = parts[1].split()
                        name = name_ver[0] if name_ver else ''
                        version = name_ver[1] if len(name_ver) > 1 else ''
                        desc = lines[i+1].strip() if i+1 < len(lines) else ''
                        results.append({
                            'name': name,
                            'version': version,
                            'description': desc,
                            'repo': parts[0]
                        })
                        i += 2
                        continue
                i += 1
        
        elif manager in ['apt', 'apt-get', 'nala']:
            # تنسيق: package/repo version arch
            #     description
            for line in lines:
                if line and not line.startswith(' '):
                    parts = line.split('/')
                    if len(parts) >= 2:
                        name = parts[0]
                        rest = parts[1].split()
                        version = rest[1] if len(rest) > 1 else ''
                        results.append({
                            'name': name,
                            'version': version,
                            'description': '',
                        })
        
        elif manager in ['dnf', 'yum']:
            # تنسيق متنوع
            for line in lines:
                if line and '.' in line:
                    parts = line.split()
                    if parts:
                        name = parts[0].split('.')[0]
                        results.append({
                            'name': name,
                            'version': parts[1] if len(parts) > 1 else '',
                            'description': ' '.join(parts[2:]) if len(parts) > 2 else '',
                        })
        
        return results[:50]  # تحديد النتائج


class AsyncPackageManager(PackageManager):
    """مدير الحزم غير المتزامن"""
    
    def __init__(self, distro_detector):
        super().__init__(distro_detector)
        self._running = True
        self._worker_thread = threading.Thread(target=self._worker, daemon=True)
        self._worker_thread.start()
    
    def _worker(self):
        """معالج العمليات في الخلفية"""
        while self._running:
            try:
                operation = self.operation_queue.get(timeout=1)
                if operation:
                    op_type, package_info, manager = operation
                    if op_type == 'install':
                        super().install_package(package_info, manager)
                    elif op_type == 'remove':
                        super().remove_package(package_info, manager)
                    elif op_type == 'update':
                        super().update_system(manager)
            except queue.Empty:
                continue
    
    def install_package_async(self, package_info: PackageInfo,
                             preferred_manager: str = None):
        """تثبيت حزمة بشكل غير متزامن"""
        self.operation_queue.put(('install', package_info, preferred_manager))
    
    def remove_package_async(self, package_info: PackageInfo,
                            preferred_manager: str = None):
        """إزالة حزمة بشكل غير متزامن"""
        self.operation_queue.put(('remove', package_info, preferred_manager))
    
    def update_system_async(self, manager: str = None):
        """تحديث النظام بشكل غير متزامن"""
        self.operation_queue.put(('update', None, manager))
    
    def stop(self):
        """إيقاف المعالج"""
        self._running = False
        if self._worker_thread:
            self._worker_thread.join(timeout=2)
