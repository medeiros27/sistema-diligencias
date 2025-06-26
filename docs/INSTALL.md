# Guia de Instalação - Sistema de Diligências

## Requisitos do Sistema

### Python
- Python 3.7 ou superior
- tkinter (geralmente incluído com Python)

### Sistemas Operacionais Suportados
- Windows 7/8/10/11
- Linux (Ubuntu, Debian, CentOS, etc.)
- macOS 10.12 ou superior

## Instalação Automática (Recomendada)

### Windows
1. Baixe e descompacte o sistema
2. Execute o arquivo `scripts/deploy_windows.bat`
3. Aguarde a instalação automática das dependências
4. O executável será criado em `dist/SistemaDiligencias.exe`

### Linux/macOS
1. Baixe e descompacte o sistema
2. Torne o script executável: `chmod +x scripts/deploy_linux.sh`
3. Execute: `./scripts/deploy_linux.sh`
4. O executável será criado na pasta `dist/`

## Instalação Manual

### 1. Verificar Python
```bash
python --version
# ou
python3 --version
```

### 2. Instalar Dependências
```bash
# Opção 1: Script automático
python scripts/install_dependencies.py

# Opção 2: Manual
pip install -r requirements.txt
```

### 3. Executar Sistema
```bash
python src/main.py
```

## Dependências Necessárias

- **pandas**: Manipulação de dados e exportação Excel
- **matplotlib**: Gráficos e relatórios visuais
- **openpyxl**: Suporte a arquivos Excel
- **Pillow**: Processamento de imagens
- **tkinter**: Interface gráfica (geralmente já incluído)

## Solução de Problemas

### Erro: "tkinter não encontrado"
**Linux:**
```bash
sudo apt-get install python3-tk
```

**macOS:**
```bash
brew install python-tk
```

### Erro: "Módulo não encontrado"
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Erro de Permissão (Linux/macOS)
```bash
sudo python scripts/install_dependencies.py
```

## Estrutura de Arquivos

```
sistema_diligencias/
├── src/                    # Código fonte
├── scripts/               # Scripts de instalação
├── docs/                  # Documentação
├── assets/               # Recursos (ícones, imagens)
├── tests/                # Testes automatizados
└── dist/                 # Executáveis (após build)
```

## Primeira Execução

1. Execute o sistema
2. O banco de dados será criado automaticamente
3. Os diretórios de dados serão criados em:
   - **Windows**: `%APPDATA%/SistemaDiligencias/`
   - **Linux/macOS**: `~/.sistema_diligencias/`

## Suporte

Para problemas ou dúvidas:
1. Verifique os logs em `logs/`
2. Execute os testes: `python tests/test_deploy.py`
3. Consulte o manual do usuário em `docs/USER_MANUAL.md`