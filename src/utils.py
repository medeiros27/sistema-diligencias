#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitários e funções auxiliares
"""

import locale
import os
import logging
import sys
import shutil
from datetime import datetime

# Fallback para pathlib se não estiver disponível
try:
    from pathlib import Path
    PATHLIB_AVAILABLE = True
except ImportError:
    PATHLIB_AVAILABLE = False
    # Implementação básica de Path para compatibilidade
    class Path:
        def __init__(self, path):
            self.path = str(path)
        
        def __str__(self):
            return self.path
        
        def __truediv__(self, other):
            return Path(os.path.join(self.path, str(other)))
        
        def exists(self):
            return os.path.exists(self.path)
        
        def mkdir(self, exist_ok=False):
            if not self.exists() or not exist_ok:
                try:
                    os.makedirs(self.path, exist_ok=exist_ok)
                except OSError:
                    pass
        
        @classmethod
        def home(cls):
            return cls(os.path.expanduser("~"))

# Imports condicionais para compatibilidade
try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
    TKINTER_AVAILABLE = True
except ImportError:
    try:
        import Tkinter as tk
        import ttk
        from tkMessageBox import messagebox
        from tkFileDialog import filedialog
        TKINTER_AVAILABLE = True
    except ImportError:
        TKINTER_AVAILABLE = False


def setup_locale():
    """Configura locale brasileiro com fallbacks robustos"""
    locales_to_try = [
        'pt_BR.UTF-8',
        'Portuguese_Brazil.1252',
        'pt_BR',
        'C.UTF-8',
        'en_US.UTF-8',
        'C'
    ]
    
    for loc in locales_to_try:
        try:
            locale.setlocale(locale.LC_ALL, loc)
            logging.info(f"Locale configurado: {loc}")
            return True
        except locale.Error:
            continue
    
    logging.warning("Não foi possível configurar locale brasileiro")
    return False


def setup_logging():
    """Configura sistema de logging"""
    try:
        from config import LOGS_DIR
        logs_dir = LOGS_DIR
    except ImportError:
        # Fallback se config não estiver disponível
        logs_dir = get_app_data_dir() / "logs" if PATHLIB_AVAILABLE else Path(os.path.join(get_app_data_dir().path, "logs"))
        if hasattr(logs_dir, 'mkdir'):
            logs_dir.mkdir(exist_ok=True)
        else:
            os.makedirs(str(logs_dir), exist_ok=True)
    
    log_file = logs_dir / f"diligencias_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(str(log_file), encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def check_dependencies():
    """Verifica se todas as dependências estão disponíveis"""
    required_modules = [
        'pandas',
        'matplotlib',
        'openpyxl',
        'sqlite3'
    ]
    
    missing = []
    
    if not TKINTER_AVAILABLE:
        missing.append('tkinter')
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        logging.error(f"Módulos não encontrados: {', '.join(missing)}")
        return False
    
    logging.info("Todas as dependências estão disponíveis")
    return True


def convert_date(date_str):
    """Converte data do formato dd/mm/yyyy para yyyy-mm-dd"""
    if not date_str:
        return None
    try:
        if '/' in date_str:
            day, month, year = date_str.split('/')
            return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        return date_str
    except ValueError:
        logging.warning(f"Formato de data inválido: {date_str}")
        return None


def format_date(date_str):
    """Converte data do formato yyyy-mm-dd para dd/mm/yyyy"""
    if not date_str:
        return ""
    try:
        if '-' in date_str:
            year, month, day = date_str.split('-')
            return f"{day.zfill(2)}/{month.zfill(2)}/{year}"
        return date_str
    except ValueError:
        logging.warning(f"Formato de data inválido: {date_str}")
        return date_str


def format_currency(value):
    """Formata valor como moeda brasileira"""
    if value is None:
        return "R$ 0,00"
    try:
        return f"R$ {float(value):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except (ValueError, TypeError):
        return "R$ 0,00"


def validate_phone(phone):
    """Valida formato de telefone brasileiro"""
    if not phone:
        return True
    
    # Remove caracteres não numéricos
    numbers_only = ''.join(filter(str.isdigit, phone))
    
    # Telefone fixo: 10 dígitos (com DDD)
    # Celular: 11 dígitos (com DDD)
    return len(numbers_only) in [10, 11]


def validate_email(email):
    """Valida formato básico de email"""
    if not email:
        return True
    
    return '@' in email and '.' in email.split('@')[-1]


def backup_database(db_path):
    """Cria backup do banco de dados"""
    if not os.path.exists(db_path):
        return False
    
    try:
        from config import BACKUPS_DIR
        backups_dir = BACKUPS_DIR
    except ImportError:
        # Fallback se config não estiver disponível
        backups_dir = get_app_data_dir() / "backups" if PATHLIB_AVAILABLE else Path(os.path.join(get_app_data_dir().path, "backups"))
        if hasattr(backups_dir, 'mkdir'):
            backups_dir.mkdir(exist_ok=True)
        else:
            os.makedirs(str(backups_dir), exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = backups_dir / f"diligencias_backup_{timestamp}.db"
    
    try:
        shutil.copy2(db_path, str(backup_path))
        logging.info(f"Backup criado: {backup_path}")
        return True
    except Exception as e:
        logging.error(f"Erro ao criar backup: {e}")
        return False


def get_app_data_dir():
    """Retorna diretório de dados da aplicação"""
    if sys.platform == "win32":
        app_data = os.getenv('APPDATA')
        if app_data:
            app_dir = Path(os.path.join(app_data, "SistemaDiligencias"))
        else:
            app_dir = Path(os.path.join(os.path.expanduser("~"), "SistemaDiligencias"))
    else:
        home_dir = os.path.expanduser("~")
        app_dir = Path(os.path.join(home_dir, ".sistema_diligencias"))
    
    if hasattr(app_dir, 'mkdir'):
        app_dir.mkdir(exist_ok=True)
    else:
        os.makedirs(str(app_dir), exist_ok=True)
    
    return app_dir