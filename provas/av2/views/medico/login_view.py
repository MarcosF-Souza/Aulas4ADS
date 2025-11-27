import tkinter as tk
from tkinter import ttk

class LoginMedicoView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.frame = ttk.Frame(root)
        
        self._criar_widgets()
    
    def _criar_widgets(self):
        titulo = tk.Label(
            self.frame, 
            text="ACESSO DO MÉDICO",
            font=('Arial', 14, 'bold'),
            fg='darkblue'
        )
        titulo.pack(pady=(0, 30))
        
        campos_frame = tk.Frame(self.frame)
        campos_frame.pack(pady=20)
        
        tk.Label(campos_frame, text="CRM:", font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=8)
        self.entry_crm = tk.Entry(campos_frame, width=30, font=('Arial', 10))
        self.entry_crm.grid(row=0, column=1, pady=8, padx=10)
        
        tk.Label(campos_frame, text="Senha:", font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=8)
        self.entry_senha = tk.Entry(campos_frame, width=30, show="*", font=('Arial', 10))
        self.entry_senha.grid(row=1, column=1, pady=8, padx=10)
        
        botoes_frame = tk.Frame(self.frame)
        botoes_frame.pack(pady=30)
        
        tk.Button(
            botoes_frame, 
            text="🔐 ENTRAR", 
            font=('Arial', 10, 'bold'),
            bg='#2196F3',
            fg='white',
            width=12,
            command=self.fazer_login
        ).grid(row=0, column=0, padx=10)
        
        tk.Button(
            botoes_frame, 
            text="↩️ VOLTAR", 
            font=('Arial', 10),
            bg='#757575',
            fg='white',
            width=12,
            command=self.voltar
        ).grid(row=0, column=1, padx=10)
    
    def fazer_login(self):
        crm = self.entry_crm.get()
        senha = self.entry_senha.get()
        self.controller.fazer_login_medico(crm, senha)
    
    def voltar(self):
        self.controller.voltar_principal()
    
    def mostrar(self):
        self.frame.pack(fill="both", expand=True)
    
    def ocultar(self):
        self.frame.pack_forget()
    
    def limpar_campos(self):
        self.entry_crm.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)