# views/paciente/meus_dados_view.py
import tkinter as tk
from tkinter import ttk, messagebox

class MeusDadosView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.frame = tk.Frame(root, bg='#f0f0f0')
        
        self._criar_widgets()
    
    def _criar_widgets(self):
        # Título
        titulo = tk.Label(
            self.frame, 
            text="MEUS DADOS PESSOAIS",
            font=('Arial', 18, 'bold'),
            fg='#2E7D32',
            bg='#f0f0f0'
        )
        titulo.pack(pady=(30, 20))
        
        # Container do formulário
        form_frame = tk.Frame(self.frame, bg='#f0f0f0')
        form_frame.pack(pady=20, padx=50, fill='x')
        
        # Obter dados do paciente logado
        paciente = self.controller.obter_usuario_logado()
        
        if not paciente:
            messagebox.showerror("Erro", "Nenhum paciente logado")
            return
        
        # Nome
        tk.Label(
            form_frame,
            text="Nome Completo:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=0, column=0, sticky='w', pady=8)
        
        self.nome_var = tk.StringVar(value=paciente.nome)
        entry_nome = tk.Entry(
            form_frame,
            textvariable=self.nome_var,
            font=('Arial', 10),
            width=40,
            state='readonly'  # Inicialmente somente leitura
        )
        entry_nome.grid(row=0, column=1, pady=8, padx=10)
        
        # Email
        tk.Label(
            form_frame,
            text="E-mail:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=1, column=0, sticky='w', pady=8)
        
        self.email_var = tk.StringVar(value=paciente.email)
        entry_email = tk.Entry(
            form_frame,
            textvariable=self.email_var,
            font=('Arial', 10),
            width=40,
            state='readonly'
        )
        entry_email.grid(row=1, column=1, pady=8, padx=10)
        
        # Telefone
        tk.Label(
            form_frame,
            text="Telefone:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=2, column=0, sticky='w', pady=8)
        
        self.telefone_var = tk.StringVar(value=paciente.telefone or "Não informado")
        entry_telefone = tk.Entry(
            form_frame,
            textvariable=self.telefone_var,
            font=('Arial', 10),
            width=40,
            state='readonly'
        )
        entry_telefone.grid(row=2, column=1, pady=8, padx=10)
        
        # Data de Nascimento
        tk.Label(
            form_frame,
            text="Data de Nascimento:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=3, column=0, sticky='w', pady=8)
        
        self.data_nascimento_var = tk.StringVar(value=paciente.data_nascimento or "Não informada")
        entry_data_nascimento = tk.Entry(
            form_frame,
            textvariable=self.data_nascimento_var,
            font=('Arial', 10),
            width=40,
            state='readonly'
        )
        entry_data_nascimento.grid(row=3, column=1, pady=8, padx=10)
        
        # Endereço
        tk.Label(
            form_frame,
            text="Endereço:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=4, column=0, sticky='w', pady=8)
        
        self.endereco_var = tk.StringVar(value=paciente.endereco or "Não informado")
        # Usar Text widget para endereço (pode ser multiline)
        self.text_endereco = tk.Text(
            form_frame,
            font=('Arial', 10),
            width=38,
            height=3,
            state='disabled'
        )
        self.text_endereco.grid(row=4, column=1, pady=8, padx=10)
        self.text_endereco.insert('1.0', paciente.endereco or "Não informado")
        
        # Data de Cadastro (informação somente leitura)
        tk.Label(
            form_frame,
            text="Data de Cadastro:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=5, column=0, sticky='w', pady=8)
        
        data_cadastro = paciente.data_criacao or "Não disponível"
        lbl_data_cadastro = tk.Label(
            form_frame,
            text=data_cadastro,
            font=('Arial', 10),
            bg='#f0f0f0',
            fg='#666666'
        )
        lbl_data_cadastro.grid(row=5, column=1, pady=8, padx=10, sticky='w')
        
        # Status da conta
        tk.Label(
            form_frame,
            text="Status da Conta:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=6, column=0, sticky='w', pady=8)
        
        status = "Ativa" if paciente.ativo else "Inativa"
        cor_status = '#4CAF50' if paciente.ativo else '#F44336'
        lbl_status = tk.Label(
            form_frame,
            text=status,
            font=('Arial', 10, 'bold'),
            fg=cor_status,
            bg='#f0f0f0'
        )
        lbl_status.grid(row=6, column=1, pady=8, padx=10, sticky='w')
        
        # Botões
        botoes_frame = tk.Frame(self.frame, bg='#f0f0f0')
        botoes_frame.pack(pady=30)
        
        tk.Button(
            botoes_frame,
            text="✏️ EDITAR DADOS",
            font=('Arial', 12, 'bold'),
            bg='#2196F3',
            fg='white',
            width=15,
            command=self.habilitar_edicao
        ).grid(row=0, column=0, padx=5)
        
        tk.Button(
            botoes_frame,
            text="💾 SALVAR",
            font=('Arial', 12, 'bold'),
            bg='#4CAF50',
            fg='white',
            width=15,
            command=self.salvar_dados,
            state='disabled'  # Inicialmente desabilitado
        ).grid(row=0, column=1, padx=5)
        
        tk.Button(
            botoes_frame,
            text="↩️ VOLTAR",
            font=('Arial', 12),
            bg='#757575',
            fg='white',
            width=15,
            command=self.voltar
        ).grid(row=0, column=2, padx=5)
        
        # Referência aos botões para poder alterar o estado depois
        self.btn_editar = botoes_frame.grid_slaves(row=0, column=0)[0]
        self.btn_salvar = botoes_frame.grid_slaves(row=0, column=1)[0]
        self.btn_voltar = botoes_frame.grid_slaves(row=0, column=2)[0]
        
        # Referência aos campos de entrada
        self.entry_nome = entry_nome
        self.entry_email = entry_email
        self.entry_telefone = entry_telefone
        self.entry_data_nascimento = entry_data_nascimento
    
    def habilitar_edicao(self):
        """Habilita a edição dos campos"""
        self.entry_nome.config(state='normal')
        self.entry_telefone.config(state='normal')
        self.entry_data_nascimento.config(state='normal')
        self.text_endereco.config(state='normal')
        
        # Desabilita botão editar e habilita salvar
        self.btn_editar.config(state='disabled')
        self.btn_salvar.config(state='normal')
    
    def salvar_dados(self):
        """Salva os dados editados"""
        # Coletar dados dos campos
        novo_nome = self.nome_var.get()
        novo_telefone = self.telefone_var.get()
        nova_data_nascimento = self.data_nascimento_var.get()
        novo_endereco = self.text_endereco.get('1.0', 'end-1c')
        
        # Validações básicas
        if not novo_nome.strip():
            messagebox.showerror("Erro", "O nome é obrigatório.")
            return
        
        # Aqui você implementaria a lógica para salvar no banco de dados
        # Por enquanto, vamos apenas mostrar uma mensagem
        messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
        
        # Desabilita edição novamente
        self.entry_nome.config(state='readonly')
        self.entry_telefone.config(state='readonly')
        self.entry_data_nascimento.config(state='readonly')
        self.text_endereco.config(state='disabled')
        
        # Habilita botão editar e desabilita salvar
        self.btn_editar.config(state='normal')
        self.btn_salvar.config(state='disabled')
    
    def voltar(self):
        self.controller.mostrar_menu_paciente()
    
    def mostrar(self):
        self.frame.pack(fill="both", expand=True)
    
    def ocultar(self):
        self.frame.pack_forget()