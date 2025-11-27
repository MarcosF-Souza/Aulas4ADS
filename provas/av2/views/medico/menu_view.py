import tkinter as tk
from tkinter import ttk

class MenuMedicoView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.frame = ttk.Frame(root)
        
        self._criar_widgets()
    
    def _criar_widgets(self):
        cabecalho_frame = tk.Frame(self.frame, bg='#f0f0f0')
        cabecalho_frame.pack(fill="x", pady=(0, 30))
        
        tk.Label(
            cabecalho_frame,
            text="MENU DO MÉDICO",
            font=('Arial', 16, 'bold'),
            fg='darkblue',
            bg='#f0f0f0'
        ).pack(side="left", padx=20, pady=15)
        
        tk.Button(
            cabecalho_frame,
            text="🚪 Sair",
            font=('Arial', 9),
            bg='#f44336',
            fg='white',
            command=self.sair
        ).pack(side="right", padx=20, pady=10)
        
        botoes_frame = tk.Frame(self.frame)
        botoes_frame.pack(pady=20)
        
        funcionalidades = [
            ("📅 Minha Agenda", self.ver_agenda, "#2196F3"),
            ("👥 Consultas do Dia", self.ver_consultas_dia, "#4CAF50"),
            ("📋 Prontuários", self.ver_prontuarios, "#9C27B0"),
            ("⚙️ Gerenciar Agenda", self.gerenciar_agenda, "#FF9800"),
            ("📊 Relatórios", self.ver_relatorios, "#607D8B"),
            ("💊 Prescrições", self.gerenciar_prescricoes, "#795548"),
        ]
        
        for i, (texto, comando, cor) in enumerate(funcionalidades):
            btn = tk.Button(
                botoes_frame,
                text=texto,
                font=('Arial', 11),
                bg=cor,
                fg='white',
                width=25,
                height=2,
                relief='raised',
                bd=2,
                command=comando
            )
            btn.grid(row=i//2, column=i%2, padx=15, pady=10)
    
    def ver_agenda(self):
        self.controller.abrir_agenda_medico()
    
    def ver_consultas_dia(self):
        self.controller.abrir_consultas_dia()
    
    def ver_prontuarios(self):
        self.controller.abrir_prontuarios()
    
    def gerenciar_agenda(self):
        self.controller.abrir_gerenciamento_agenda()
    
    def ver_relatorios(self):
        self.controller.abrir_relatorios_medico()
    
    def gerenciar_prescricoes(self):
        self.controller.abrir_prescricoes()
    
    def sair(self):
        self.controller.voltar_principal()
    
    def mostrar(self):
        self.frame.pack(fill="both", expand=True)
    
    def ocultar(self):
        self.frame.pack_forget()