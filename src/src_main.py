#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Controle de Diligências
Ponto de entrada principal da aplicação
Versão: 2.0
Autor: medeiros27
"""

import sys
import os
import logging

# Adicionar diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from utils import setup_logging, setup_locale, check_dependencies
from sistema_diligencias import SistemaDiligencias


def main():
    """Função principal da aplicação"""
    try:
        # Configurar logging
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Iniciando Sistema de Controle de Diligências v2.0")
        
        # Configurar locale
        setup_locale()
        
        # Verificar dependências
        if not check_dependencies():
            logger.error("Dependências não atendidas. Execute install_dependencies.py")
            return 1
        
        # Iniciar aplicação
        app = SistemaDiligencias()
        app.run()
        
        logger.info("Aplicação finalizada com sucesso")
        return 0
        
    except Exception as e:
        if 'logger' in locals():
            logger.error(f"Erro fatal na aplicação: {e}")
        else:
            print(f"Erro fatal: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())