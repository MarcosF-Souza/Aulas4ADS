# views/main_view.py
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
            text="SISTEMA DE AGENDAMENTO DE CONSULTAS",
            font=('Arial', 16, 'bold'),
            fg='darkblue'
        )
        titulo.pack(pady=(50, 30))
        
        # Botões de acesso
        botoes_frame = tk.Frame(self.frame)
        botoes_frame.pack(pady=50)
        
        # Botão Paciente
        tk.Button(
            botoes_frame,
            text="👤 ACESSO PACIENTE",
            font=('Arial', 12, 'bold'),
            bg='#4CAF50',
            fg='white',
            width=20,
            height=2,
            command=self.controller.mostrar_login_paciente  # DEVE ESTAR CORRETO
        ).pack(pady=15)
        
        # Botão Médico
        tk.Button(
            botoes_frame,
            text="👨‍⚕️ ACESSO MÉDICO",
            font=('Arial', 12, 'bold'),
            bg='#2196F3',
            fg='white',
            width=20,
            height=2,
            command=self.controller.mostrar_login_medico  # DEVE ESTAR CORRETO
        ).pack(pady=15)
        
        # Botão Admin
        tk.Button(
            botoes_frame,
            text="⚙️ ACESSO ADMIN",
            font=('Arial', 12, 'bold'),
            bg='#FF9800',
            fg='white',
            width=20,
            height=2,
            command=self.controller.mostrar_login_admin  # DEVE ESTAR CORRETO
        ).pack(pady=15)
    
    def mostrar(self):
        self.frame.pack(fill="both", expand=True)
        print("🖥️ MainView mostrada")
    
    def ocultar(self):
        self.frame.pack_forget()