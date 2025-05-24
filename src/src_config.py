#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configurações centralizadas do sistema
"""

import os
from pathlib import Path
from utils import get_app_data_dir

# Versão da aplicação
VERSION = "2.0.0"
APP_NAME = "Sistema de Controle de Diligências"
AUTHOR = "medeiros27"

# Diretórios
APP_DATA_DIR = get_app_data_dir()
DATABASE_DIR = APP_DATA_DIR / "data"
LOGS_DIR = APP_DATA_DIR / "logs"
BACKUPS_DIR = APP_DATA_DIR / "backups"
EXPORTS_DIR = APP_DATA_DIR / "exports"

# Criar diretórios se não existirem
for directory in [DATABASE_DIR, LOGS_DIR, BACKUPS_DIR, EXPORTS_DIR]:
    directory.mkdir(exist_ok=True)

# Banco de dados
DATABASE_PATH = DATABASE_DIR / "diligencias.db"

# Interface
WINDOW_TITLE = f"{APP_NAME} v{VERSION}"
WINDOW_SIZE = "1200x800"
WINDOW_MIN_SIZE = "800x600"

# Cores da interface
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72', 
    'success': '#28A745',
    'warning': '#FFC107',
    'danger': '#DC3545',
    'light': '#F8F9FA',
    'dark': '#343A40'
}

# Configurações de relatório
REPORT_TYPES = {
    'DIARIO': 'Diário',
    'SEMANAL': 'Semanal', 
    'MENSAL': 'Mensal',
    'ANUAL': 'Anual'
}

# Tipos de demanda
DEMANDA_TYPES = [
    'Audiência',
    'Cópia',
    'Protocolo', 
    'Citação',
    'Intimação',
    'Outros'
]

# Status das diligências
STATUS_OPTIONS = [
    'Pendente',
    'Cumprida', 
    'Cancelada'
]

# Configurações de backup
BACKUP_FREQUENCY_DAYS = 7
MAX_BACKUPS = 30

# Configurações de log
LOG_LEVEL = "INFO"
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5

# Configurações de exportação
EXCEL_DATE_FORMAT = "DD/MM/YYYY"
EXCEL_CURRENCY_FORMAT = "R$ #,##0.00"

# Validações
MAX_TEXT_LENGTH = 255
MAX_PHONE_LENGTH = 20
MAX_PROCESS_LENGTH = 50