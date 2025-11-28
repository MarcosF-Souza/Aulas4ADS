# views/medico/prontuarios_medico_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class ProntuariosMedicoView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.frame = tk.Frame(root, bg='#f0f0f0')
        
        self.consultas = []  # Lista para armazenar consultas do médico
        self.consulta_selecionada = None
        
        self._criar_widgets()
    
    def _criar_widgets(self):
        # Título
        titulo = tk.Label(
            self.frame, 
            text="PRONTUÁRIOS - MÉDICO",
            font=('Arial', 18, 'bold'),
            fg='#2E7D32',
            bg='#f0f0f0'
        )
        titulo.pack(pady=(30, 20))
        
        # Container principal
        main_frame = tk.Frame(self.frame, bg='#f0f0f0')
        main_frame.pack(pady=20, padx=50, fill='both', expand=True)
        
        # Frame da lista de consultas (esquerda)
        lista_frame = tk.Frame(main_frame, bg='#f0f0f0')
        lista_frame.pack(side='left', fill='both', expand=True, padx=(0, 20))
        
        # Título da lista
        tk.Label(
            lista_frame,
            text="CONSULTAS DO PACIENTE",
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            fg='#2E7D32'
        ).pack(anchor='w', pady=(0, 10))
        
        # Container com scrollbar para a lista
        container_lista = tk.Frame(lista_frame)
        container_lista.pack(fill='both', expand=True)
        
        self.canvas = tk.Canvas(container_lista, bg='#f0f0f0', height=300)
        scrollbar = ttk.Scrollbar(container_lista, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#f0f0f0')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame do formulário de prontuário (direita)
        form_frame = tk.Frame(main_frame, bg='#f0f0f0', relief='solid', borderwidth=1)
        form_frame.pack(side='right', fill='both', expand=True, padx=(20, 0))
        
        # Título do formulário
        tk.Label(
            form_frame,
            text="PRONTUÁRIO MÉDICO",
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            fg='#2E7D32'
        ).pack(anchor='w', pady=(15, 10), padx=15)
        
        # Informações da consulta selecionada
        self.info_consulta_frame = tk.Frame(form_frame, bg='#f8f9fa', relief='solid', borderwidth=1)
        self.info_consulta_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(
            self.info_consulta_frame,
            text="Selecione uma consulta para criar/editar o prontuário",
            font=('Arial', 10),
            bg='#f8f9fa',
            fg='#666666',
            wraplength=300
        ).pack(padx=10, pady=15)
        
        # Campos do prontuário
        campos_frame = tk.Frame(form_frame, bg='#f0f0f0')
        campos_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Diagnóstico
        tk.Label(
            campos_frame,
            text="Diagnóstico:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=0, column=0, sticky='w', pady=10)
        
        self.diagnostico_text = tk.Text(
            campos_frame,
            font=('Arial', 10),
            width=40,
            height=4,
            wrap='word'
        )
        self.diagnostico_text.grid(row=0, column=1, pady=10, padx=10, sticky='ew')
        
        # Prescrição médica
        tk.Label(
            campos_frame,
            text="Prescrição Médica:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=1, column=0, sticky='w', pady=10)
        
        self.prescricao_text = tk.Text(
            campos_frame,
            font=('Arial', 10),
            width=40,
            height=4,
            wrap='word'
        )
        self.prescricao_text.grid(row=1, column=1, pady=10, padx=10, sticky='ew')
        
        # Observações médicas
        tk.Label(
            campos_frame,
            text="Observações:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=2, column=0, sticky='w', pady=10)
        
        self.observacoes_text = tk.Text(
            campos_frame,
            font=('Arial', 10),
            width=40,
            height=4,
            wrap='word'
        )
        self.observacoes_text.grid(row=2, column=1, pady=10, padx=10, sticky='ew')
        
        # Configurar grid weights
        campos_frame.columnconfigure(1, weight=1)
        
        # Botões do formulário
        botoes_form_frame = tk.Frame(form_frame, bg='#f0f0f0')
        botoes_form_frame.pack(fill='x', padx=15, pady=20)
        
        tk.Button(
            botoes_form_frame,
            text="💾 SALVAR PRONTUÁRIO",
            font=('Arial', 11, 'bold'),
            bg='#4CAF50',
            fg='white',
            width=20,
            command=self.salvar_prontuario
        ).pack(side='left', padx=5)
        
        tk.Button(
            botoes_form_frame,
            text="🔄 LIMPAR",
            font=('Arial', 11),
            bg='#FF9800',
            fg='white',
            width=15,
            command=self.limpar_formulario
        ).pack(side='left', padx=5)
        
        # Botões de navegação
        botoes_frame = tk.Frame(self.frame, bg='#f0f0f0')
        botoes_frame.pack(pady=30)
        
        tk.Button(
            botoes_frame,
            text="🔄 ATUALIZAR LISTA",
            font=('Arial', 12),
            bg='#2196F3',
            fg='white',
            width=18,
            command=self.carregar_consultas
        ).pack(side='left', padx=10)
        
        tk.Button(
            botoes_frame,
            text="↩️ VOLTAR",
            font=('Arial', 12),
            bg='#757575',
            fg='white',
            width=15,
            command=self.voltar
        ).pack(side='left', padx=10)
    
    def carregar_consultas(self):
        """Carrega as consultas do médico"""
        try:
            medico = self.controller.obter_usuario_logado()
            if not medico:
                messagebox.showerror("Erro", "Nenhum médico logado")
                return
            
            # Buscar consultas do médico
            self.consultas = self.controller.buscar_consultas_por_medico(medico.id)
            
            # Atualizar a lista
            self._preencher_lista_consultas()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar consultas: {str(e)}")
    
    def _preencher_lista_consultas(self):
        # Limpar o frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not self.consultas:
            tk.Label(
                self.scrollable_frame,
                text="Nenhuma consulta encontrada",
                font=('Arial', 10),
                bg='#f0f0f0',
                fg='#757575'
            ).pack(pady=20)
            return
        
        # Adicionar cada consulta na lista
        for i, consulta in enumerate(self.consultas):
            linha = tk.Frame(self.scrollable_frame, bg='#ffffff' if i % 2 == 0 else '#f9f9f9')
            linha.pack(fill='x', pady=2)
            
            # Informações básicas
            info_texto = f"{consulta.data_consulta} {consulta.hora_consulta} - {consulta.paciente_nome}"
            tk.Label(
                linha,
                text=info_texto,
                font=('Arial', 9),
                bg=linha.cget('bg'),
                anchor='w'
            ).pack(side='left', fill='x', expand=True, padx=10, pady=5)
            
            # Status
            cor_status = {
                'agendada': '#FFA000',
                'confirmada': '#2196F3',
                'realizada': '#4CAF50',
                'cancelada': '#F44336'
            }.get(consulta.status, '#757575')
            
            status_label = tk.Label(
                linha,
                text=consulta.status.upper(),
                font=('Arial', 8, 'bold'),
                fg=cor_status,
                bg=linha.cget('bg')
            )
            status_label.pack(side='right', padx=10, pady=5)
            
            # Botão selecionar
            btn_selecionar = tk.Button(
                linha,
                text="📝",
                font=('Arial', 10),
                bg='#2196F3',
                fg='white',
                width=3,
                command=lambda c=consulta: self.selecionar_consulta(c)
            )
            btn_selecionar.pack(side='right', padx=5, pady=5)
    
    def selecionar_consulta(self, consulta):
        """Seleciona uma consulta para editar o prontuário"""
        self.consulta_selecionada = consulta
        
        # Atualizar informações da consulta
        for widget in self.info_consulta_frame.winfo_children():
            widget.destroy()
        
        info_texto = f"Paciente: {consulta.paciente_nome}\nData: {consulta.data_consulta} {consulta.hora_consulta}\nMotivo: {consulta.motivo}"
        tk.Label(
            self.info_consulta_frame,
            text=info_texto,
            font=('Arial', 10),
            bg='#f8f9fa',
            fg='#333333',
            justify='left'
        ).pack(padx=10, pady=10, anchor='w')
        
        # Preencher campos existentes
        self.diagnostico_text.delete('1.0', tk.END)
        self.prescricao_text.delete('1.0', tk.END)
        self.observacoes_text.delete('1.0', tk.END)
        
        if consulta.diagnostico:
            self.diagnostico_text.insert('1.0', consulta.diagnostico)
        if consulta.prescricao:
            self.prescricao_text.insert('1.0', consulta.prescricao)
        if consulta.observacoes_medicas:
            self.observacoes_text.insert('1.0', consulta.observacoes_medicas)
    
    def salvar_prontuario(self):
        """Salva o prontuário da consulta selecionada"""
        if not self.consulta_selecionada:
            messagebox.showerror("Erro", "Selecione uma consulta primeiro")
            return
        
        diagnostico = self.diagnostico_text.get('1.0', tk.END).strip()
        prescricao = self.prescricao_text.get('1.0', tk.END).strip()
        observacoes = self.observacoes_text.get('1.0', tk.END).strip()
        
        try:
            # Chamar controller para salvar prontuário
            sucesso, mensagem = self.controller.salvar_prontuario(
                self.consulta_selecionada.id,
                diagnostico,
                prescricao,
                observacoes
            )
            
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                # Atualizar status da consulta para "realizada"
                self.controller.finalizar_consulta(self.consulta_selecionada.id, observacoes)
                self.carregar_consultas()
            else:
                messagebox.showerror("Erro", mensagem)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar prontuário: {str(e)}")
    
    def limpar_formulario(self):
        """Limpa o formulário de prontuário"""
        self.diagnostico_text.delete('1.0', tk.END)
        self.prescricao_text.delete('1.0', tk.END)
        self.observacoes_text.delete('1.0', tk.END)
        self.consulta_selecionada = None
        
        # Restaurar mensagem padrão
        for widget in self.info_consulta_frame.winfo_children():
            widget.destroy()
        
        tk.Label(
            self.info_consulta_frame,
            text="Selecione uma consulta para criar/editar o prontuário",
            font=('Arial', 10),
            bg='#f8f9fa',
            fg='#666666',
            wraplength=300
        ).pack(padx=10, pady=15)
    
    def voltar(self):
        self.controller.abrir_menu_medico()
    
    def mostrar(self):
        self.carregar_consultas()
        self.limpar_formulario()
        self.frame.pack(fill="both", expand=True)
    
    def ocultar(self):
        self.frame.pack_forget()