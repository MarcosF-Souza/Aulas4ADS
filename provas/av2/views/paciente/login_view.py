import tkinter as tk
from tkinter import ttk, messagebox

class LoginPacienteView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.frame = ttk.Frame(root)
        
        self._criar_widgets()
    
    def _criar_widgets(self):
        # Título
        titulo = tk.Label(
            self.frame, 
            text="ACESSO DO PACIENTE",
            font=('Arial', 14, 'bold'),
            fg='darkgreen'
        )
        titulo.pack(pady=(0, 30))
        
        # Container dos campos
        campos_frame = tk.Frame(self.frame)
        campos_frame.pack(pady=20)
        
        # Campos de login
        tk.Label(campos_frame, text="E-mail:", font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=8)
        self.entry_email = tk.Entry(campos_frame, width=30, font=('Arial', 10))
        self.entry_email.grid(row=0, column=1, pady=8, padx=10)
        
        tk.Label(campos_frame, text="Senha:", font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=8)
        self.entry_senha = tk.Entry(campos_frame, width=30, show="*", font=('Arial', 10))
        self.entry_senha.grid(row=1, column=1, pady=8, padx=10)
        
        # Botões
        botoes_frame = tk.Frame(self.frame)
        botoes_frame.pack(pady=30)
        
        tk.Button(
            botoes_frame, 
            text="🔐 ENTRAR", 
            font=('Arial', 10, 'bold'),
            bg='#4CAF50',
            fg='white',
            width=12,
            command=self.fazer_login
        ).grid(row=0, column=0, padx=10)
        
        tk.Button(
            botoes_frame, 
            text="📝 CADASTRAR", 
            font=('Arial', 10),
            bg='#2196F3',
            fg='white',
            width=12,
            command=self.cadastrar
        ).grid(row=0, column=1, padx=10)
        
        tk.Button(
            botoes_frame, 
            text="↩️ VOLTAR", 
            font=('Arial', 10),
            bg='#757575',
            fg='white',
            width=12,
            command=self.voltar
        ).grid(row=0, column=2, padx=10)
    
    def fazer_login(self):
        email = self.entry_email.get().strip()
        senha = self.entry_senha.get().strip()
        
        # Validação básica
        if not email or not senha:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos")
            return
        
        # DEBUG: Mostrar o que está sendo enviado
        print(f"Tentando login - Email: {email}, Senha: {senha}")
        
        # Chamar o controller - com tratamento de erro caso o método não exista
        try:
            if hasattr(self.controller, 'fazer_login_paciente'):
                self.controller.fazer_login_paciente(email, senha)
            else:
                messagebox.showerror("Erro", "Método de login não disponível")
                print("ERRO: Controller não tem método 'fazer_login_paciente'")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro durante o login: {str(e)}")
            print(f"ERRO EXCEÇÃO: {e}")
    
    def cadastrar(self):
        try:
            if hasattr(self.controller, 'abrir_cadastro_paciente'):
                self.controller.abrir_cadastro_paciente()
            else:
                messagebox.showerror("Erro", "Funcionalidade de cadastro não disponível")
                print("ERRO: Controller não tem método 'abrir_cadastro_paciente'")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir cadastro: {str(e)}")
    
    def voltar(self):
        try:
            if hasattr(self.controller, 'voltar_principal'):
                self.controller.voltar_principal()
            else:
                # Fallback: tentar voltar de outra forma
                self.frame.pack_forget()
                from views.main_view import MainView
                MainView(self.root)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao voltar: {str(e)}")
    
    def mostrar(self):
        self.frame.pack(fill="both", expand=True)
    
    def ocultar(self):
        self.frame.pack_forget()
    
    def limpar_campos(self):
        self.entry_email.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)