import tkinter as tk
from tkinter import ttk, messagebox

class CadastroPacienteView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.frame = ttk.Frame(root)
        
        self._criar_widgets()
    
    def _criar_widgets(self):
        # Título
        titulo = tk.Label(
            self.frame, 
            text="CADASTRO DE PACIENTE",
            font=('Arial', 14, 'bold'),
            fg='darkgreen'
        )
        titulo.pack(pady=(0, 20))
        
        # Frame com scroll para muitos campos
        canvas = tk.Canvas(self.frame)
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Campos do formulário
        campos = [
            ("Nome completo:", "nome"),
            ("E-mail:", "email"),
            ("Telefone:", "telefone"),
            ("Data Nascimento (DD/MM/AAAA):", "data_nascimento"),
            ("Endereço completo:", "endereco"),
            ("Senha:", "senha"),
            ("Confirmar Senha:", "confirmar_senha")
        ]
        
        self.campos = {}
        for i, (label, nome) in enumerate(campos):
            tk.Label(scrollable_frame, text=label, font=('Arial', 9)).grid(row=i, column=0, sticky='w', pady=8, padx=10)
            entry = tk.Entry(scrollable_frame, width=35, font=('Arial', 9), 
                           show="*" if "senha" in nome else "")
            entry.grid(row=i, column=1, pady=8, padx=10)
            self.campos[nome] = entry
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botões
        botoes_frame = tk.Frame(self.frame)
        botoes_frame.pack(pady=20)
        
        tk.Button(
            botoes_frame,
            text="💾 CADASTRAR",
            font=('Arial', 10, 'bold'),
            bg='#4CAF50',
            fg='white',
            width=15,
            command=self.cadastrar
        ).grid(row=0, column=0, padx=10)
        
        tk.Button(
            botoes_frame,
            text="↩️ VOLTAR",
            font=('Arial', 10),
            bg='#757575',
            fg='white',
            width=15,
            command=self.voltar
        ).grid(row=0, column=1, padx=10)
    
    def cadastrar(self):
        dados = {nome: entry.get() for nome, entry in self.campos.items()}
        self.controller.cadastrar_paciente(dados)
    
    def voltar(self):
        self.controller.voltar_login_paciente()
    
    def mostrar(self):
        self.frame.pack(fill="both", expand=True)
    
    def ocultar(self):
        self.frame.pack_forget()
    
    def limpar_campos(self):
        for entry in self.campos.values():
            entry.delete(0, tk.END)