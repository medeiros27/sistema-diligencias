#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitários e funções auxiliares
"""

import locale
import os
import logging
import sys
from datetime import datetime
from pathlib import Path

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
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"diligencias_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
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
    
    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = backup_dir / f"diligencias_backup_{timestamp}.db"
    
    try:
        import shutil
        shutil.copy2(db_path, backup_path)
        logging.info(f"Backup criado: {backup_path}")
        return True
    except Exception as e:
        logging.error(f"Erro ao criar backup: {e}")
        return False


def get_app_data_dir():
    """Retorna diretório de dados da aplicação"""
    if sys.platform == "win32":
        app_data = os.getenv('APPDATA')
        app_dir = Path(app_data) / "SistemaDiligencias"
    else:
        home = Path.home()
        app_dir = home / ".sistema_diligencias"
    
    app_dir.mkdir(exist_ok=True)
    return app_dir