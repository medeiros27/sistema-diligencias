#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes de deploy e verificação do sistema
"""

import sys
import os
import tempfile
import unittest
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestDeploy(unittest.TestCase):
    """Testes para verificar se o deploy está funcionando"""
    
    def test_python_version(self):
        """Testa se a versão do Python é compatível"""
        self.assertGreaterEqual(sys.version_info, (3, 7), 
                               "Python 3.7+ é necessário")
    
    def test_imports(self):
        """Testa se todos os imports necessários funcionam"""
        modules_to_test = [
            'sqlite3',
            'pandas', 
            'matplotlib',
            'openpyxl'
        ]
        
        for module in modules_to_test:
            with self.subTest(module=module):
                try:
                    __import__(module)
                except ImportError as e:
                    self.fail(f"Módulo {module} não encontrado: {e}")
    
    def test_tkinter_import(self):
        """Testa se tkinter está disponível"""
        try:
            import tkinter as tk
            # Teste básico de criação de janela
            root = tk.Tk()
            root.withdraw()  # Não mostrar janela
            root.destroy()
        except ImportError:
            try:
                import Tkinter as tk
                root = tk.Tk()
                root.withdraw()
                root.destroy()
            except ImportError:
                self.fail("tkinter não está disponível")
    
    def test_database_creation(self):
        """Testa criação do banco de dados"""
        try:
            from database import DatabaseManager
            
            # Usar arquivo temporário para teste
            with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
                db_path = tmp.name
            
            try:
                db = DatabaseManager(db_path)
                
                # Testar inserção básica
                query = '''INSERT INTO diligencias 
                          (data_solicitacao, solicitante, tipo_demanda)
                          VALUES (?, ?, ?)'''
                params = ('2024-01-01', 'Teste', 'Audiência')
                
                result_id = db.execute_query(query, params)
                self.assertIsNotNone(result_id)
                
                # Testar consulta
                query = 'SELECT * FROM diligencias WHERE id = ?'
                result = db.execute_query(query, (result_id,), fetch=True)
                self.assertEqual(len(result), 1)
                self.assertEqual(result[0]['solicitante'], 'Teste')
                
            finally:
                # Limpar arquivo temporário
                if os.path.exists(db_path):
                    os.unlink(db_path)
                    
        except Exception as e:
            self.fail(f"Erro ao testar banco de dados: {e}")
    
    def test_utils_functions(self):
        """Testa funções utilitárias"""
        try:
            from utils import convert_date, format_date, format_currency
            
            # Testar conversão de datas
            self.assertEqual(convert_date('01/12/2024'), '2024-12-01')
            self.assertEqual(format_date('2024-12-01'), '01/12/2024')
            
            # Testar formatação de moeda
            self.assertIn('R$', format_currency(100.50))
            
        except Exception as e:
            self.fail(f"Erro ao testar utilitários: {e}")
    
    def test_config_loading(self):
        """Testa carregamento de configurações"""
        try:
            from config import VERSION, APP_NAME, DATABASE_PATH
            
            self.assertIsInstance(VERSION, str)
            self.assertIsInstance(APP_NAME, str)
            self.assertIsNotNone(DATABASE_PATH)
            
        except Exception as e:
            self.fail(f"Erro ao testar configurações: {e}")


def run_tests():
    """Executa todos os testes"""
    print("🧪 Executando testes de deploy...")
    print("=" * 50)
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDeploy)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ Todos os testes passaram!")
        return 0
    else:
        print("❌ Alguns testes falharam!")
        print(f"Falhas: {len(result.failures)}")
        print(f"Erros: {len(result.errors)}")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())