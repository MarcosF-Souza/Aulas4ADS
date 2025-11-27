import tkinter as tk
from tkinter import ttk

class MenuAdminView:
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
            text="MENU DO ADMINISTRADOR",
            font=('Arial', 16, 'bold'),
            fg='darkorange',
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
            ("👨‍⚕️ Gerenciar Médicos", self.gerenciar_medicos, "#FF9800"),
            ("👥 Gerenciar Pacientes", self.gerenciar_pacientes, "#2196F3"),
            ("📅 Agenda Geral", self.ver_agenda_geral, "#4CAF50"),
            ("📊 Relatórios do Sistema", self.gerar_relatorios, "#9C27B0"),
            ("⚙️ Configurações", self.configurar_sistema, "#607D8B"),
            ("🔐 Controle de Acessos", self.controle_acessos, "#795548"),
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
    
    def gerenciar_medicos(self):
        self.controller.abrir_gerenciamento_medicos()
    
    def gerenciar_pacientes(self):
        self.controller.abrir_gerenciamento_pacientes()
    
    def ver_agenda_geral(self):
        self.controller.abrir_agenda_geral()
    
    def gerar_relatorios(self):
        self.controller.abrir_relatorios_admin()
    
    def configurar_sistema(self):
        self.controller.abrir_configuracoes()
    
    def controle_acessos(self):
        self.controller.abrir_controle_acessos()
    
    def sair(self):
        self.controller.voltar_principal()
    
    def mostrar(self):
        self.frame.pack(fill="both", expand=True)
    
    def ocultar(self):
        self.frame.pack_forget()