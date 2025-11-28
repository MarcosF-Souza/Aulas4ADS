# views/paciente/meus_dados_view.py
import tkinter as tk
from tkinter import ttk, messagebox

class MeusDadosView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.frame = tk.Frame(root, bg='#f0f0f0')
        
        self.paciente = None
        
        self._criar_widgets()
    
    def _criar_widgets(self):
        # Título
        self.titulo = tk.Label(
            self.frame, 
            text="MEUS DADOS PESSOAIS",
            font=('Arial', 18, 'bold'),
            fg='#2E7D32',
            bg='#f0f0f0'
        )
        self.titulo.pack(pady=(30, 20))
        
        # Container do formulário
        self.form_frame = tk.Frame(self.frame, bg='#f0f0f0')
        self.form_frame.pack(pady=20, padx=50, fill='x')
        
        # Nome
        tk.Label(
            self.form_frame,
            text="Nome Completo:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=0, column=0, sticky='w', pady=8)
        
        self.nome_var = tk.StringVar()
        self.entry_nome = tk.Entry(
            self.form_frame,
            textvariable=self.nome_var,
            font=('Arial', 10),
            width=40,
            state='readonly'  # Inicialmente somente leitura
        )
        self.entry_nome.grid(row=0, column=1, pady=8, padx=10)
        
        # Email
        tk.Label(
            self.form_frame,
            text="E-mail:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=1, column=0, sticky='w', pady=8)
        
        self.email_var = tk.StringVar()
        self.entry_email = tk.Entry(
            self.form_frame,
            textvariable=self.email_var,
            font=('Arial', 10),
            width=40,
            state='readonly'
        )
        self.entry_email.grid(row=1, column=1, pady=8, padx=10)
        
        # Telefone
        tk.Label(
            self.form_frame,
            text="Telefone:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=2, column=0, sticky='w', pady=8)
        
        self.telefone_var = tk.StringVar()
        self.entry_telefone = tk.Entry(
            self.form_frame,
            textvariable=self.telefone_var,
            font=('Arial', 10),
            width=40,
            state='readonly'
        )
        self.entry_telefone.grid(row=2, column=1, pady=8, padx=10)
        
        # Data de Nascimento
        tk.Label(
            self.form_frame,
            text="Data de Nascimento:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=3, column=0, sticky='w', pady=8)
        
        self.data_nascimento_var = tk.StringVar()
        self.entry_data_nascimento = tk.Entry(
            self.form_frame,
            textvariable=self.data_nascimento_var,
            font=('Arial', 10),
            width=40,
            state='readonly'
        )
        self.entry_data_nascimento.grid(row=3, column=1, pady=8, padx=10)
        
        # Endereço
        tk.Label(
            self.form_frame,
            text="Endereço:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=4, column=0, sticky='w', pady=8)
        
        # Usar Text widget para endereço (pode ser multiline)
        self.text_endereco = tk.Text(
            self.form_frame,
            font=('Arial', 10),
            width=38,
            height=3,
            state='disabled'
        )
        self.text_endereco.grid(row=4, column=1, pady=8, padx=10)
        
        # Data de Cadastro (informação somente leitura)
        tk.Label(
            self.form_frame,
            text="Data de Cadastro:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=5, column=0, sticky='w', pady=8)
        
        self.lbl_data_cadastro = tk.Label(
            self.form_frame,
            text="",
            font=('Arial', 10),
            bg='#f0f0f0',
            fg='#666666'
        )
        self.lbl_data_cadastro.grid(row=5, column=1, pady=8, padx=10, sticky='w')
        
        # Status da conta
        tk.Label(
            self.form_frame,
            text="Status da Conta:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=6, column=0, sticky='w', pady=8)
        
        self.lbl_status = tk.Label(
            self.form_frame,
            text="",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        )
        self.lbl_status.grid(row=6, column=1, pady=8, padx=10, sticky='w')
        
        # Botões
        botoes_frame = tk.Frame(self.frame, bg='#f0f0f0')
        botoes_frame.pack(pady=30)
        
        self.btn_editar = tk.Button(
            botoes_frame,
            text="✏️ EDITAR DADOS",
            font=('Arial', 12, 'bold'),
            bg='#2196F3',
            fg='white',
            width=15,
            command=self.habilitar_edicao
        )
        self.btn_editar.grid(row=0, column=0, padx=5)
        
        self.btn_salvar = tk.Button(
            botoes_frame,
            text="💾 SALVAR",
            font=('Arial', 12, 'bold'),
            bg='#4CAF50',
            fg='white',
            width=15,
            command=self.salvar_dados,
            state='disabled'  # Inicialmente desabilitado
        )
        self.btn_salvar.grid(row=0, column=1, padx=5)
        
        self.btn_voltar = tk.Button(
            botoes_frame,
            text="↩️ VOLTAR",
            font=('Arial', 12),
            bg='#757575',
            fg='white',
            width=15,
            command=self.voltar
        )
        self.btn_voltar.grid(row=0, column=2, padx=5)
    
    def carregar_dados_paciente(self):
        """Carrega os dados do paciente logado"""
        self.paciente = self.controller.obter_usuario_logado()
        
        if not self.paciente:
            messagebox.showerror("Erro", "Nenhum paciente logado. Faça login novamente.")
            self.controller.voltar_principal()
            return False
        
        # Preencher os campos com os dados do paciente
        self.nome_var.set(self.paciente.nome)
        self.email_var.set(self.paciente.email)
        self.telefone_var.set(self.paciente.telefone or "Não informado")
        self.data_nascimento_var.set(self.paciente.data_nascimento or "Não informada")
        
        # Limpar e preencher o campo de endereço
        self.text_endereco.config(state='normal')
        self.text_endereco.delete('1.0', tk.END)
        self.text_endereco.insert('1.0', self.paciente.endereco or "Não informado")
        self.text_endereco.config(state='disabled')
        
        # Preencher dados de cadastro e status
        data_cadastro = self.paciente.data_criacao or "Não disponível"
        self.lbl_data_cadastro.config(text=data_cadastro)
        
        status = "Ativa" if self.paciente.ativo else "Inativa"
        cor_status = '#4CAF50' if self.paciente.ativo else '#F44336'
        self.lbl_status.config(text=status, fg=cor_status)
        
        return True
    
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
        """Mostra a view e carrega os dados do paciente"""
        # Carregar dados do paciente sempre que a view for mostrada
        if not self.carregar_dados_paciente():
            return
        
        self.frame.pack(fill="both", expand=True)
    
    def ocultar(self):
        """Oculta a view"""
        self.frame.pack_forget()