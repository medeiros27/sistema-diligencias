#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerenciamento do banco de dados SQLite
"""

import sqlite3
import logging
from pathlib import Path
from datetime import datetime
from config import DATABASE_PATH
from utils import backup_database


class DatabaseManager:
    """Gerenciador do banco de dados"""
    
    def __init__(self, db_path=None):
        self.db_path = db_path or DATABASE_PATH
        self.logger = logging.getLogger(__name__)
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados e cria as tabelas"""
        try:
            # Criar backup se database já existe
            if self.db_path.exists():
                backup_database(str(self.db_path))
            
            with sqlite3.connect(str(self.db_path)) as conn:
                cursor = conn.cursor()
                
                # Tabela de diligências
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS diligencias (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        data_solicitacao DATE NOT NULL,
                        solicitante TEXT NOT NULL,
                        telefone_contato TEXT,
                        tipo_demanda TEXT NOT NULL,
                        numero_processo TEXT,
                        data_demanda DATE,
                        status TEXT NOT NULL DEFAULT 'Pendente',
                        horario TEXT,
                        local_realizacao TEXT,
                        valor_receber REAL DEFAULT 0,
                        data_pagamento DATE,
                        pago BOOLEAN DEFAULT 0,
                        observacoes TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Tabela de correspondentes
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS correspondentes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome_contratado TEXT NOT NULL,
                        telefone TEXT,
                        email TEXT,
                        endereco TEXT,
                        valor_cobrado REAL DEFAULT 0,
                        prazo_pagamento DATE,
                        pago BOOLEAN DEFAULT 0,
                        diligencia_id INTEGER,
                        observacoes TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (diligencia_id) REFERENCES diligencias (id)
                    )
                ''')
                
                # Índices para performance
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_diligencias_data 
                    ON diligencias (data_solicitacao)
                ''')
                
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_diligencias_status 
                    ON diligencias (status)
                ''')
                
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_correspondentes_diligencia 
                    ON correspondentes (diligencia_id)
                ''')
                
                # Triggers para atualizar timestamp
                cursor.execute('''
                    CREATE TRIGGER IF NOT EXISTS update_diligencias_timestamp 
                    AFTER UPDATE ON diligencias
                    BEGIN
                        UPDATE diligencias SET updated_at = CURRENT_TIMESTAMP 
                        WHERE id = NEW.id;
                    END
                ''')
                
                cursor.execute('''
                    CREATE TRIGGER IF NOT EXISTS update_correspondentes_timestamp 
                    AFTER UPDATE ON correspondentes
                    BEGIN
                        UPDATE correspondentes SET updated_at = CURRENT_TIMESTAMP 
                        WHERE id = NEW.id;
                    END
                ''')
                
                conn.commit()
                self.logger.info("Banco de dados inicializado com sucesso")
                
        except Exception as e:
            self.logger.error(f"Erro ao inicializar banco de dados: {e}")
            raise
    
    def execute_query(self, query, params=None, fetch=False):
        """Executa uma query no banco de dados com tratamento de erro"""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                # Configurar row factory para resultados nomeados
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                if fetch:
                    result = cursor.fetchall()
                    return [dict(row) for row in result]
                else:
                    conn.commit()
                    return cursor.lastrowid
                    
        except sqlite3.Error as e:
            self.logger.error(f"Erro na query: {query} | Params: {params} | Erro: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Erro inesperado na query: {e}")
            raise
    
    def get_statistics(self):
        """Retorna estatísticas do banco de dados"""
        try:
            stats = {}
            
            # Estatísticas de diligências
            query = '''
                SELECT 
                    COUNT(*) as total,
                    COUNT(CASE WHEN status = 'Pendente' THEN 1 END) as pendentes,
                    COUNT(CASE WHEN status = 'Cumprida' THEN 1 END) as cumpridas,
                    COUNT(CASE WHEN status = 'Cancelada' THEN 1 END) as canceladas,
                    COALESCE(SUM(valor_receber), 0) as faturamento_total,
                    COALESCE(SUM(CASE WHEN pago = 1 THEN valor_receber ELSE 0 END), 0) as recebido,
                    COALESCE(SUM(CASE WHEN pago = 0 THEN valor_receber ELSE 0 END), 0) as a_receber
                FROM diligencias
            '''
            
            dilig_stats = self.execute_query(query, fetch=True)[0]
            stats['diligencias'] = dilig_stats
            
            # Estatísticas de correspondentes
            query = '''
                SELECT 
                    COUNT(*) as total,
                    COALESCE(SUM(valor_cobrado), 0) as custos_total,
                    COALESCE(SUM(CASE WHEN pago = 1 THEN valor_cobrado ELSE 0 END), 0) as pago,
                    COALESCE(SUM(CASE WHEN pago = 0 THEN valor_cobrado ELSE 0 END), 0) as a_pagar
                FROM correspondentes
            '''
            
            corresp_stats = self.execute_query(query, fetch=True)[0]
            stats['correspondentes'] = corresp_stats
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Erro ao obter estatísticas: {e}")
            return {}
    
    def cleanup_old_records(self, days=365):
        """Remove registros antigos (opcional)"""
        try:
            query = '''
                DELETE FROM diligencias 
                WHERE created_at < date('now', '-{} days')
                AND status = 'Cancelada'
            '''.format(days)
            
            cursor = self.execute_query(query)
            self.logger.info(f"Limpeza de registros executada")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro na limpeza de registros: {e}")
            return False
    
    def insert_diligencia(self, data):
        """Insere nova diligência"""
        query = '''
            INSERT INTO diligencias 
            (data_solicitacao, solicitante, telefone_contato, tipo_demanda, 
             numero_processo, data_demanda, status, horario, local_realizacao, 
             valor_receber, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        params = (
            data.get('data_solicitacao'),
            data.get('solicitante'),
            data.get('telefone_contato'),
            data.get('tipo_demanda'),
            data.get('numero_processo'),
            data.get('data_demanda'),
            data.get('status', 'Pendente'),
            data.get('horario'),
            data.get('local_realizacao'),
            data.get('valor_receber', 0),
            data.get('observacoes')
        )
        
        return self.execute_query(query, params)
    
    def get_all_diligencias(self):
        """Retorna todas as diligências"""
        query = '''
            SELECT * FROM diligencias 
            ORDER BY data_solicitacao DESC
        '''
        return self.execute_query(query, fetch=True)
    
    def update_diligencia(self, diligencia_id, data):
        """Atualiza uma diligência"""
        query = '''
            UPDATE diligencias 
            SET data_solicitacao=?, solicitante=?, telefone_contato=?, 
                tipo_demanda=?, numero_processo=?, data_demanda=?, 
                status=?, horario=?, local_realizacao=?, valor_receber=?, 
                observacoes=?
            WHERE id=?
        '''
        
        params = (
            data.get('data_solicitacao'),
            data.get('solicitante'),
            data.get('telefone_contato'),
            data.get('tipo_demanda'),
            data.get('numero_processo'),
            data.get('data_demanda'),
            data.get('status'),
            data.get('horario'),
            data.get('local_realizacao'),
            data.get('valor_receber', 0),
            data.get('observacoes'),
            diligencia_id
        )
        
        return self.execute_query(query, params)
    
    def delete_diligencia(self, diligencia_id):
        """Remove uma diligência"""
        query = 'DELETE FROM diligencias WHERE id = ?'
        return self.execute_query(query, (diligencia_id,))