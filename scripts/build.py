#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de build para gerar executável
"""

import subprocess
import sys
import os
import shutil

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


def check_pyinstaller():
    """Verifica se PyInstaller está instalado"""
    try:
        import PyInstaller
        return True
    except ImportError:
        print("📦 Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return True


def build_executable():
    """Constrói o executável"""
    print("🔨 Construindo executável...")
    
    # Diretórios
    src_dir = Path("src")
    dist_dir = Path("dist")
    build_dir = Path("build")
    assets_dir = Path("assets")
    
    # Limpar diretórios anteriores
    if dist_dir.exists():
        shutil.rmtree(str(dist_dir))
    if build_dir.exists():
        shutil.rmtree(str(build_dir))
    
    # Comando PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=SistemaDiligencias",
        "--distpath=dist",
        "--workpath=build",
        str(src_dir / "main.py")
    ]
    
    # Adicionar ícone se existir
    icon_path = assets_dir / "icon.ico"
    if icon_path.exists():
        cmd.extend(["--icon", str(icon_path)])
    
    # Adicionar dados extras
    if assets_dir.exists():
        cmd.extend(["--add-data", f"{assets_dir}{os.pathsep}assets"])
    
    try:
        subprocess.check_call(cmd)
        print("✅ Executável criado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no build: {e}")
        return False


def create_distribution():
    """Cria pacote de distribuição"""
    print("📦 Criando pacote de distribuição...")
    
    dist_dir = Path("dist")
    package_dir = dist_dir / "SistemaDiligencias_v2.0"
    
    # Criar diretório do pacote
    package_dir.mkdir(exist_ok=True)
    
    # Copiar executável
    exe_path = dist_dir / "SistemaDiligencias.exe"
    if exe_path.exists():
        shutil.copy2(str(exe_path), str(package_dir))
    
    # Copiar documentação
    docs = ["README.md", "INSTALL.md", "USER_MANUAL.md"]
    for doc in docs:
        doc_path = Path("docs") / doc
        if doc_path.exists():
            shutil.copy2(str(doc_path), str(package_dir))
    
    # Criar diretório de exemplos
    examples_dir = package_dir / "exemplos"
    examples_dir.mkdir(exist_ok=True)
    
    print(f"✅ Pacote criado em: {package_dir}")
    return True


def main():
    """Função principal de build"""
    print("🚀 Build do Sistema de Diligências")
    print("=" * 50)
    
    # Verificar PyInstaller
    if not check_pyinstaller():
        return 1
    
    # Build do executável
    if not build_executable():
        return 1
    
    # Criar distribuição
    if not create_distribution():
        return 1
    
    print("\n🎉 Build concluído com sucesso!")
    print("📁 Arquivos disponíveis em: dist/")
    return 0


if __name__ == "__main__":
    sys.exit(main())