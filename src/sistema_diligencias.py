#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface gráfica principal do Sistema de Diligências
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import logging
from datetime import datetime, date
import pandas as pd
from pathlib import Path

from config import (
    WINDOW_TITLE, WINDOW_SIZE, WINDOW_MIN_SIZE, COLORS, 
    DEMANDA_TYPES, STATUS_OPTIONS, EXPORTS_DIR
)
from database import DatabaseManager
from utils import (
    format_date, convert_date, format_currency, 
    validate_phone, validate_email
)


class SistemaDiligencias:
    """Classe principal da interface gráfica"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db = DatabaseManager()
        
        # Configurar janela principal
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.minsize(*map(int, WINDOW_MIN_SIZE.split('x')))
        
        # Variáveis de controle
        self.selected_diligencia = None
        
        # Construir interface
        self._setup_styles()
        self._build_ui()
        self._load_data()
        
        self.logger.info("Interface gráfica inicializada")
    
    def _setup_styles(self):
        """Configura estilos da interface"""
        style = ttk.Style()
        
        # Configurar tema
        try:
            style.theme_use('clam')
        except tk.TclError:
            pass  # Usar tema padrão se clam não estiver disponível
        
        # Estilos personalizados
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 10, 'bold'))
        style.configure('Success.TButton', background='#28a745')
        style.configure('Danger.TButton', background='#dc3545')
    
    def _build_ui(self):
        """Constrói a interface principal"""
        # Menu principal
        self._create_menu()
        
        # Notebook para abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Abas
        self._create_diligencias_tab()
        self._create_correspondentes_tab()
        self._create_relatorios_tab()
        
        # Barra de status
        self._create_status_bar()
    
    def _create_menu(self):
        """Cria menu principal"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Nova Diligência", command=self._nova_diligencia)
        file_menu.add_separator()
        file_menu.add_command(label="Exportar Excel", command=self._exportar_excel)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)
        
        # Menu Ferramentas
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ferramentas", menu=tools_menu)
        tools_menu.add_command(label="Backup", command=self._criar_backup)
        tools_menu.add_command(label="Estatísticas", command=self._mostrar_estatisticas)
        
        # Menu Ajuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Sobre", command=self._mostrar_sobre)
    
    def _create_diligencias_tab(self):
        """Cria aba de diligências"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Diligências")
        
        # Frame superior - botões
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Nova", command=self._nova_diligencia).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Editar", command=self._editar_diligencia).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Excluir", command=self._excluir_diligencia).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Atualizar", command=self._load_data).pack(side='left', padx=2)
        
        # Frame da tabela
        table_frame = ttk.Frame(frame)
        table_frame.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Treeview para listar diligências
        columns = ('ID', 'Data', 'Solicitante', 'Tipo', 'Status', 'Valor')
        self.diligencias_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configurar colunas
        self.diligencias_tree.heading('ID', text='ID')
        self.diligencias_tree.heading('Data', text='Data Solicitação')
        self.diligencias_tree.heading('Solicitante', text='Solicitante')
        self.diligencias_tree.heading('Tipo', text='Tipo Demanda')
        self.diligencias_tree.heading('Status', text='Status')
        self.diligencias_tree.heading('Valor', text='Valor')
        
        # Largura das colunas
        self.diligencias_tree.column('ID', width=50)
        self.diligencias_tree.column('Data', width=100)
        self.diligencias_tree.column('Solicitante', width=200)
        self.diligencias_tree.column('Tipo', width=120)
        self.diligencias_tree.column('Status', width=100)
        self.diligencias_tree.column('Valor', width=100)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.diligencias_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal', command=self.diligencias_tree.xview)
        self.diligencias_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack da tabela e scrollbars
        self.diligencias_tree.pack(side='left', expand=True, fill='both')
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Bind para seleção
        self.diligencias_tree.bind('<<TreeviewSelect>>', self._on_diligencia_select)
    
    def _create_correspondentes_tab(self):
        """Cria aba de correspondentes"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Correspondentes")
        
        label = ttk.Label(frame, text="Gestão de Correspondentes", style='Title.TLabel')
        label.pack(pady=20)
        
        # Placeholder para funcionalidade futura
        info_label = ttk.Label(frame, text="Funcionalidade em desenvolvimento")
        info_label.pack(pady=10)
    
    def _create_relatorios_tab(self):
        """Cria aba de relatórios"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Relatórios")
        
        label = ttk.Label(frame, text="Relatórios e Estatísticas", style='Title.TLabel')
        label.pack(pady=20)
        
        # Frame para botões de relatório
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Estatísticas Gerais", command=self._mostrar_estatisticas).pack(pady=5)
        ttk.Button(btn_frame, text="Exportar Excel", command=self._exportar_excel).pack(pady=5)
    
    def _create_status_bar(self):
        """Cria barra de status"""
        self.status_bar = ttk.Label(self.root, text="Pronto", relief='sunken', anchor='w')
        self.status_bar.pack(side='bottom', fill='x')
    
    def _load_data(self):
        """Carrega dados das diligências"""
        try:
            # Limpar tabela
            for item in self.diligencias_tree.get_children():
                self.diligencias_tree.delete(item)
            
            # Carregar diligências
            diligencias = self.db.get_all_diligencias()
            
            for dilig in diligencias:
                values = (
                    dilig['id'],
                    format_date(dilig['data_solicitacao']),
                    dilig['solicitante'],
                    dilig['tipo_demanda'],
                    dilig['status'],
                    format_currency(dilig['valor_receber'])
                )
                self.diligencias_tree.insert('', 'end', values=values)
            
            self.status_bar.config(text=f"Carregadas {len(diligencias)} diligências")
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar dados: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")
    
    def _on_diligencia_select(self, event):
        """Callback para seleção de diligência"""
        selection = self.diligencias_tree.selection()
        if selection:
            item = self.diligencias_tree.item(selection[0])
            self.selected_diligencia = item['values'][0]  # ID da diligência
    
    def _nova_diligencia(self):
        """Abre janela para nova diligência"""
        DiligenciaDialog(self.root, self.db, callback=self._load_data)
    
    def _editar_diligencia(self):
        """Edita diligência selecionada"""
        if not self.selected_diligencia:
            messagebox.showwarning("Aviso", "Selecione uma diligência para editar")
            return
        
        DiligenciaDialog(self.root, self.db, diligencia_id=self.selected_diligencia, callback=self._load_data)
    
    def _excluir_diligencia(self):
        """Exclui diligência selecionada"""
        if not self.selected_diligencia:
            messagebox.showwarning("Aviso", "Selecione uma diligência para excluir")
            return
        
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir esta diligência?"):
            try:
                self.db.delete_diligencia(self.selected_diligencia)
                self._load_data()
                messagebox.showinfo("Sucesso", "Diligência excluída com sucesso")
            except Exception as e:
                self.logger.error(f"Erro ao excluir diligência: {e}")
                messagebox.showerror("Erro", f"Erro ao excluir diligência: {e}")
    
    def _exportar_excel(self):
        """Exporta dados para Excel"""
        try:
            diligencias = self.db.get_all_diligencias()
            
            if not diligencias:
                messagebox.showinfo("Info", "Não há dados para exportar")
                return
            
            # Converter para DataFrame
            df = pd.DataFrame(diligencias)
            
            # Formatar datas
            date_columns = ['data_solicitacao', 'data_demanda', 'data_pagamento']
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%d/%m/%Y')
            
            # Salvar arquivo
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = EXPORTS_DIR / f"diligencias_{timestamp}.xlsx"
            
            df.to_excel(filename, index=False, sheet_name='Diligências')
            
            messagebox.showinfo("Sucesso", f"Dados exportados para:\n{filename}")
            
        except Exception as e:
            self.logger.error(f"Erro ao exportar Excel: {e}")
            messagebox.showerror("Erro", f"Erro ao exportar: {e}")
    
    def _criar_backup(self):
        """Cria backup do banco de dados"""
        try:
            from utils import backup_database
            if backup_database(str(self.db.db_path)):
                messagebox.showinfo("Sucesso", "Backup criado com sucesso")
            else:
                messagebox.showerror("Erro", "Falha ao criar backup")
        except Exception as e:
            self.logger.error(f"Erro ao criar backup: {e}")
            messagebox.showerror("Erro", f"Erro ao criar backup: {e}")
    
    def _mostrar_estatisticas(self):
        """Mostra estatísticas do sistema"""
        try:
            stats = self.db.get_statistics()
            
            if not stats:
                messagebox.showinfo("Info", "Não há dados para estatísticas")
                return
            
            # Criar janela de estatísticas
            EstatisticasDialog(self.root, stats)
            
        except Exception as e:
            self.logger.error(f"Erro ao obter estatísticas: {e}")
            messagebox.showerror("Erro", f"Erro ao obter estatísticas: {e}")
    
    def _mostrar_sobre(self):
        """Mostra informações sobre o sistema"""
        from config import VERSION, APP_NAME, AUTHOR
        
        about_text = f"""
{APP_NAME}
Versão: {VERSION}
Desenvolvido por: {AUTHOR}

Sistema para controle e gestão de diligências jurídicas.
        """
        
        messagebox.showinfo("Sobre", about_text)
    
    def run(self):
        """Inicia a aplicação"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.logger.info("Aplicação interrompida pelo usuário")
        except Exception as e:
            self.logger.error(f"Erro na execução da aplicação: {e}")
            messagebox.showerror("Erro Fatal", f"Erro na aplicação: {e}")


class DiligenciaDialog:
    """Dialog para criar/editar diligências"""
    
    def __init__(self, parent, db, diligencia_id=None, callback=None):
        self.db = db
        self.diligencia_id = diligencia_id
        self.callback = callback
        
        # Criar janela
        self.window = tk.Toplevel(parent)
        self.window.title("Nova Diligência" if not diligencia_id else "Editar Diligência")
        self.window.geometry("600x500")
        self.window.transient(parent)
        self.window.grab_set()
        
        # Variáveis
        self.vars = {}
        
        self._build_form()
        
        # Carregar dados se editando
        if diligencia_id:
            self._load_diligencia()
    
    def _build_form(self):
        """Constrói formulário"""
        main_frame = ttk.Frame(self.window)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Campos do formulário
        fields = [
            ('data_solicitacao', 'Data Solicitação:', 'entry'),
            ('solicitante', 'Solicitante:', 'entry'),
            ('telefone_contato', 'Telefone:', 'entry'),
            ('tipo_demanda', 'Tipo Demanda:', 'combo'),
            ('numero_processo', 'Nº Processo:', 'entry'),
            ('data_demanda', 'Data Demanda:', 'entry'),
            ('status', 'Status:', 'combo'),
            ('horario', 'Horário:', 'entry'),
            ('local_realizacao', 'Local:', 'entry'),
            ('valor_receber', 'Valor a Receber:', 'entry'),
            ('observacoes', 'Observações:', 'text')
        ]
        
        row = 0
        for field_name, label_text, field_type in fields:
            # Label
            ttk.Label(main_frame, text=label_text).grid(row=row, column=0, sticky='w', pady=2)
            
            # Campo
            if field_type == 'entry':
                var = tk.StringVar()
                entry = ttk.Entry(main_frame, textvariable=var, width=40)
                entry.grid(row=row, column=1, sticky='ew', pady=2, padx=(5, 0))
                self.vars[field_name] = var
                
            elif field_type == 'combo':
                var = tk.StringVar()
                if field_name == 'tipo_demanda':
                    values = DEMANDA_TYPES
                elif field_name == 'status':
                    values = STATUS_OPTIONS
                else:
                    values = []
                
                combo = ttk.Combobox(main_frame, textvariable=var, values=values, width=37)
                combo.grid(row=row, column=1, sticky='ew', pady=2, padx=(5, 0))
                self.vars[field_name] = var
                
            elif field_type == 'text':
                var = tk.StringVar()
                text_frame = ttk.Frame(main_frame)
                text_frame.grid(row=row, column=1, sticky='ew', pady=2, padx=(5, 0))
                
                text_widget = tk.Text(text_frame, height=4, width=40)
                scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
                text_widget.configure(yscrollcommand=scrollbar.set)
                
                text_widget.pack(side='left', expand=True, fill='both')
                scrollbar.pack(side='right', fill='y')
                
                self.vars[field_name] = text_widget  # Text widget é diferente
            
            row += 1
        
        # Configurar grid
        main_frame.columnconfigure(1, weight=1)
        
        # Botões
        btn_frame = ttk.Frame(self.window)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Salvar", command=self._save).pack(side='right', padx=2)
        ttk.Button(btn_frame, text="Cancelar", command=self.window.destroy).pack(side='right', padx=2)
    
    def _load_diligencia(self):
        """Carrega dados da diligência para edição"""
        try:
            query = 'SELECT * FROM diligencias WHERE id = ?'
            result = self.db.execute_query(query, (self.diligencia_id,), fetch=True)
            
            if result:
                data = result[0]
                
                for field_name, var in self.vars.items():
                    value = data.get(field_name, '')
                    
                    if isinstance(var, tk.Text):
                        var.delete('1.0', 'end')
                        if value:
                            var.insert('1.0', str(value))
                    else:
                        if field_name in ['data_solicitacao', 'data_demanda', 'data_pagamento']:
                            value = format_date(value) if value else ''
                        var.set(str(value) if value else '')
                        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar diligência: {e}")
    
    def _save(self):
        """Salva diligência"""
        try:
            # Coletar dados
            data = {}
            for field_name, var in self.vars.items():
                if isinstance(var, tk.Text):
                    value = var.get('1.0', 'end-1c').strip()
                else:
                    value = var.get().strip()
                
                # Converter datas
                if field_name in ['data_solicitacao', 'data_demanda', 'data_pagamento']:
                    value = convert_date(value) if value else None
                
                data[field_name] = value if value else None
            
            # Validações básicas
            if not data.get('solicitante'):
                messagebox.showerror("Erro", "Solicitante é obrigatório")
                return
            
            if not data.get('tipo_demanda'):
                messagebox.showerror("Erro", "Tipo de demanda é obrigatório")
                return
            
            # Validar telefone
            if data.get('telefone_contato') and not validate_phone(data['telefone_contato']):
                messagebox.showerror("Erro", "Formato de telefone inválido")
                return
            
            # Salvar
            if self.diligencia_id:
                self.db.update_diligencia(self.diligencia_id, data)
                messagebox.showinfo("Sucesso", "Diligência atualizada com sucesso")
            else:
                self.db.insert_diligencia(data)
                messagebox.showinfo("Sucesso", "Diligência criada com sucesso")
            
            # Callback e fechar
            if self.callback:
                self.callback()
            
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")


class EstatisticasDialog:
    """Dialog para mostrar estatísticas"""
    
    def __init__(self, parent, stats):
        self.window = tk.Toplevel(parent)
        self.window.title("Estatísticas do Sistema")
        self.window.geometry("500x400")
        self.window.transient(parent)
        self.window.grab_set()
        
        self._build_stats(stats)
    
    def _build_stats(self, stats):
        """Constrói interface de estatísticas"""
        main_frame = ttk.Frame(self.window)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Título
        ttk.Label(main_frame, text="Estatísticas Gerais", style='Title.TLabel').pack(pady=10)
        
        # Diligências
        dilig_frame = ttk.LabelFrame(main_frame, text="Diligências")
        dilig_frame.pack(fill='x', pady=5)
        
        dilig_stats = stats.get('diligencias', {})
        
        stats_text = f"""
Total: {dilig_stats.get('total', 0)}
Pendentes: {dilig_stats.get('pendentes', 0)}
Cumpridas: {dilig_stats.get('cumpridas', 0)}
Canceladas: {dilig_stats.get('canceladas', 0)}

Faturamento Total: {format_currency(dilig_stats.get('faturamento_total', 0))}
Recebido: {format_currency(dilig_stats.get('recebido', 0))}
A Receber: {format_currency(dilig_stats.get('a_receber', 0))}
        """
        
        ttk.Label(dilig_frame, text=stats_text.strip()).pack(padx=10, pady=10)
        
        # Correspondentes
        corresp_frame = ttk.LabelFrame(main_frame, text="Correspondentes")
        corresp_frame.pack(fill='x', pady=5)
        
        corresp_stats = stats.get('correspondentes', {})
        
        corresp_text = f"""
Total: {corresp_stats.get('total', 0)}
Custos Total: {format_currency(corresp_stats.get('custos_total', 0))}
Pago: {format_currency(corresp_stats.get('pago', 0))}
A Pagar: {format_currency(corresp_stats.get('a_pagar', 0))}
        """
        
        ttk.Label(corresp_frame, text=corresp_text.strip()).pack(padx=10, pady=10)
        
        # Botão fechar
        ttk.Button(main_frame, text="Fechar", command=self.window.destroy).pack(pady=10)