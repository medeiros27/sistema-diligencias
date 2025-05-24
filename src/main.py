#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ponto de entrada principal da aplicação
"""

import sys
import os
import logging

# Garante import relativo da pasta src
sys.path.insert(0, os.path.dirname(__file__))

from utils import setup_logging, setup_locale, check_dependencies
from sistema_diligencias import SistemaDiligencias


def main():
    """Função principal"""
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Iniciando Sistema de Diligências v2.0")

    if not setup_locale():
        logger.warning("Locale não configurado corretamente")

    if not check_dependencies():
        logger.error("Dependências faltando. Rode scripts/install_dependencies.py")
        return 1

    try:
        app = SistemaDiligencias()
        app.run()
        logger.info("Aplicação finalizada com sucesso")
        return 0
    except Exception as e:
        logger.exception("Falha inesperada:")
        return 1


if __name__ == "__main__":
    sys.exit(main())