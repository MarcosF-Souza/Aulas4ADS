# views/consulta/remarcar_consulta_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class RemarcarConsultaView:
    def __init__(self, root, controller, consulta=None):
        self.root = root
        self.controller = controller
        self.consulta = consulta  # Pode ser None inicialmente
        self.frame = tk.Frame(root, bg='#f0f0f0')
        
        self._criar_widgets()
        if consulta:
            self._preencher_dados_consulta()
    
    def _criar_widgets(self):
        # Título
        titulo = tk.Label(
            self.frame, 
            text="REMARCAR CONSULTA",
            font=('Arial', 18, 'bold'),
            fg='#2E7D32',
            bg='#f0f0f0'
        )
        titulo.pack(pady=(30, 20))
        
        # Container do formulário
        form_frame = tk.Frame(self.frame, bg='#f0f0f0')
        form_frame.pack(pady=20, padx=50, fill='x')
        
        # Informações atuais (somente leitura)
        # Médico
        tk.Label(
            form_frame,
            text="Médico:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=0, column=0, sticky='w', pady=10)
        
        # ✅ ALTERAÇÃO: Transformar em atributo
        self.medico_label = tk.Label(
            form_frame,
            text="Carregando...",
            font=('Arial', 10),
            bg='#f0f0f0',
            fg='#666666'
        )
        self.medico_label.grid(row=0, column=1, sticky='w', pady=10, padx=10)
        
        # Data atual
        tk.Label(
            form_frame,
            text="Data atual:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=1, column=0, sticky='w', pady=10)
        
        # ✅ ALTERAÇÃO: Transformar em atributo
        self.data_atual_label = tk.Label(
            form_frame,
            text="Carregando...",
            font=('Arial', 10),
            bg='#f0f0f0',
            fg='#666666'
        )
        self.data_atual_label.grid(row=1, column=1, sticky='w', pady=10, padx=10)
        
        # Hora atual
        tk.Label(
            form_frame,
            text="Hora atual:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=2, column=0, sticky='w', pady=10)
        
        # ✅ ALTERAÇÃO: Transformar em atributo
        self.hora_atual_label = tk.Label(
            form_frame,
            text="Carregando...",
            font=('Arial', 10),
            bg='#f0f0f0',
            fg='#666666'
        )
        self.hora_atual_label.grid(row=2, column=1, sticky='w', pady=10, padx=10)
        
        # Motivo atual
        tk.Label(
            form_frame,
            text="Motivo atual:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=3, column=0, sticky='w', pady=10)
        
        # ✅ ALTERAÇÃO: Transformar em atributo
        self.motivo_atual_label = tk.Label(
            form_frame,
            text="Carregando...",
            font=('Arial', 10),
            bg='#f0f0f0',
            fg='#666666',
            wraplength=300
        )
        self.motivo_atual_label.grid(row=3, column=1, sticky='w', pady=10, padx=10)
        
        # Separador
        separator = ttk.Separator(form_frame, orient='horizontal')
        separator.grid(row=4, column=0, columnspan=2, sticky='ew', pady=20)
        
        # NOVOS DADOS
        novoTitulo = tk.Label(
            form_frame,
            text="NOVOS DADOS:",
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            fg='#2E7D32'
        )
        novoTitulo.grid(row=5, column=0, columnspan=2, sticky='w', pady=10)
        
        # Nova Data
        tk.Label(
            form_frame,
            text="Nova Data:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=6, column=0, sticky='w', pady=10)
        
        self.nova_data_var = tk.StringVar()
        self.entry_nova_data = tk.Entry(
            form_frame,
            textvariable=self.nova_data_var,
            font=('Arial', 10),
            width=42
        )
        self.entry_nova_data.grid(row=6, column=1, pady=10, padx=10)
        # Sugerir data de amanhã
        amanha = (datetime.now() + timedelta(days=1)).strftime('%d/%m/%Y')
        self.entry_nova_data.insert(0, amanha)
        
        # Nova Hora
        tk.Label(
            form_frame,
            text="Nova Hora:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=7, column=0, sticky='w', pady=10)
        
        self.nova_hora_var = tk.StringVar()
        self.combo_nova_hora = ttk.Combobox(
            form_frame,
            textvariable=self.nova_hora_var,
            font=('Arial', 10),
            state='readonly',
            width=40
        )
        self.combo_nova_hora.grid(row=7, column=1, pady=10, padx=10)
        # Preencher horários
        self.combo_nova_hora['values'] = ['08:00', '09:00', '10:00', '11:00', '14:00', '15:00', '16:00', '17:00']
        
        # Novo Motivo
        tk.Label(
            form_frame,
            text="Novo Motivo:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=8, column=0, sticky='w', pady=10)
        
        self.novo_motivo_var = tk.StringVar()
        self.entry_novo_motivo = tk.Entry(
            form_frame,
            textvariable=self.novo_motivo_var,
            font=('Arial', 10),
            width=42
        )
        self.entry_novo_motivo.grid(row=8, column=1, pady=10, padx=10)
        
        # Botões
        botoes_frame = tk.Frame(self.frame, bg='#f0f0f0')
        botoes_frame.pack(pady=30)
        
        tk.Button(
            botoes_frame,
            text="🔄 REMARCAR",
            font=('Arial', 12, 'bold'),
            bg='#FF9800',
            fg='white',
            width=15,
            command=self.remarcar_consulta
        ).grid(row=0, column=0, padx=10)
        
        tk.Button(
            botoes_frame,
            text="❌ CANCELAR",
            font=('Arial', 12),
            bg='#757575',
            fg='white',
            width=15,
            command=self.voltar
        ).grid(row=0, column=1, padx=10)
    
    def remarcar_consulta(self):
        nova_data = self.nova_data_var.get()
        nova_hora = self.nova_hora_var.get()
        novo_motivo = self.novo_motivo_var.get()
        
        if not nova_data or not nova_hora:
            messagebox.showerror("Erro", "Por favor, preencha a nova data e hora.")
            return
        
        try:
            # Converter data de DD/MM/AAAA para AAAA-MM-DD
            data_obj = datetime.strptime(nova_data, '%d/%m/%Y')
            data_formatada = data_obj.strftime('%Y-%m-%d')
            
            # Verificar se data não é no passado
            if data_obj.date() < datetime.now().date():
                messagebox.showerror("Erro", "Não é possível remarcar para datas passadas.")
                return
                
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido. Use DD/MM/AAAA.")
            return
        
        # Chamar o controller para remarcar a consulta
        sucesso, mensagem, consulta = self.controller.remarcar_consulta(
            consulta_id=self.consulta.id,
            nova_data=data_formatada,
            nova_hora=nova_hora,
            novo_motivo=novo_motivo
        )
        
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.voltar()
        else:
            messagebox.showerror("Erro", mensagem)
    
    def voltar(self):
        self.controller.mostrar_minhas_consultas()
    
    def mostrar(self):
        """Mostra a view e atualiza os dados da consulta"""
        if self.consulta:
            self._preencher_dados_consulta()
        self.frame.pack(fill="both", expand=True)
    
    def ocultar(self):
        self.frame.pack_forget()

    def _preencher_dados_consulta(self):
        """Preenche os dados da consulta nos widgets"""
        if not self.consulta:
            return
            
        try:
            # Buscar informações completas do médico
            from models.medico import Medico
            medico = Medico.buscar_por_id(self.consulta.id_medico)
            
            if medico:
                medico_texto = f"Dr. {medico.nome} - {medico.especialidade}"
                # Atualizar os labels (precisamos torná-los atributos)
                if hasattr(self, 'medico_label'):
                    self.medico_label.config(text=medico_texto)
                if hasattr(self, 'data_atual_label'):
                    self.data_atual_label.config(text=self.consulta.data_consulta)
                if hasattr(self, 'hora_atual_label'):
                    self.hora_atual_label.config(text=self.consulta.hora_consulta)
                if hasattr(self, 'motivo_atual_label'):
                    self.motivo_atual_label.config(text=self.consulta.motivo or "Não informado")
                
                # Preencher o novo motivo com o atual
                if hasattr(self, 'novo_motivo_var'):
                    self.novo_motivo_var.set(self.consulta.motivo or "")
                    
        except Exception as e:
            print(f"Erro ao preencher dados da consulta: {e}")