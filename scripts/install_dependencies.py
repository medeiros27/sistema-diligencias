#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de instalação automática de dependências
"""

import subprocess
import sys
import os

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


def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ é necessário")
        print(f"Versão atual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} OK")
    return True


def install_package(package):
    """Instala um pacote Python"""
    try:
        print(f"📦 Instalando {package}...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", package, "--upgrade"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✅ {package} instalado com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar {package}: {e}")
        return False


def check_tkinter():
    """Verifica se tkinter está disponível"""
    try:
        import tkinter
        print("✅ tkinter OK")
        return True
    except ImportError:
        print("❌ tkinter não encontrado")
        if sys.platform.startswith('linux'):
            print("Execute: sudo apt-get install python3-tk")
        elif sys.platform == 'darwin':
            print("Execute: brew install python-tk")
        return False


def main():
    """Função principal de instalação"""
    print("🚀 Sistema de Controle de Diligências")
    print("=" * 50)
    print("📋 Verificando e instalando dependências...\n")
    
    # Verificar Python
    if not check_python_version():
        return 1
    
    # Verificar tkinter
    if not check_tkinter():
        print("\n⚠️  tkinter é necessário para a interface gráfica")
    
    # Lista de dependências
    packages = [
        'pandas>=1.3.0',
        'matplotlib>=3.3.0', 
        'openpyxl>=3.0.0',
        'Pillow>=8.0.0'  # Para suporte a imagens
    ]
    
    # Instalar pacotes
    failed_packages = []
    for package in packages:
        if not install_package(package):
            failed_packages.append(package)
    
    print("\n" + "=" * 50)
    
    if failed_packages:
        print("❌ Falha na instalação dos seguintes pacotes:")
        for package in failed_packages:
            print(f"   - {package}")
        print("\n💡 Tente executar manualmente:")
        print(f"   pip install {' '.join(failed_packages)}")
        return 1
    else:
        print("✅ Todas as dependências foram instaladas com sucesso!")
        print("\n🎉 Sistema pronto para uso!")
        print("Execute: python src/main.py")
        return 0


if __name__ == "__main__":
    sys.exit(main())