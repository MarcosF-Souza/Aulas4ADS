import tkinter as tk
from tkinter import ttk

class MainView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.frame = ttk.Frame(root)
        
        self._criar_widgets()
    
    def _criar_widgets(self):
        # Título
        titulo = tk.Label(
            self.frame, 
            text="SISTEMA DE AGENDAMENTO DE CONSULTAS MÉDICAS",
            font=('Arial', 16, 'bold'),
            fg='darkblue'
        )
        titulo.pack(pady=(0, 40))
        
        # Subtítulo
        subtitulo = tk.Label(
            self.frame,
            text="Selecione o tipo de acesso:",
            font=('Arial', 12)
        )
        subtitulo.pack(pady=(0, 30))
        
        # Container para os botões
        botoes_frame = tk.Frame(self.frame)
        botoes_frame.pack(pady=20)
        
        # Botões de acesso
        botoes = [
            ("👤 ACESSO PACIENTE", self.acessar_paciente, "#4CAF50"),
            ("👨‍⚕️ ACESSO MÉDICO", self.acessar_medico, "#2196F3"),
            ("⚙️ ACESSO ADMINISTRADOR", self.acessar_admin, "#FF9800"),
        ]
        
        for texto, comando, cor in botoes:
            btn = tk.Button(
                botoes_frame,
                text=texto,
                font=('Arial', 11, 'bold'),
                bg=cor,
                fg='white',
                width=25,
                height=3,
                relief='raised',
                bd=3,
                command=comando
            )
            btn.pack(pady=15, padx=20)
        
        # Botão sair
        btn_sair = tk.Button(
            self.frame,
            text="🚪 SAIR DO SISTEMA",
            font=('Arial', 10),
            bg='#f44336',
            fg='white',
            width=20,
            height=2,
            command=self.sair
        )
        btn_sair.pack(pady=30)
    
    def acessar_paciente(self):
        self.controller.abrir_login_paciente()
    
    def acessar_medico(self):
        self.controller.abrir_login_medico()
    
    def acessar_admin(self):
        self.controller.abrir_login_admin()
    
    def sair(self):
        self.controller.sair_sistema()
    
    def mostrar(self):
        self.frame.pack(fill="both", expand=True)
    
    def ocultar(self):
        self.frame.pack_forget()