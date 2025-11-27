import tkinter as tk
from tkinter import ttk

class MenuPacienteView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.frame = ttk.Frame(root)
        
        self._criar_widgets()
    
    def _criar_widgets(self):
        # Cabeçalho
        cabecalho_frame = tk.Frame(self.frame, bg='#f0f0f0')
        cabecalho_frame.pack(fill="x", pady=(0, 30))
        
        tk.Label(
            cabecalho_frame,
            text="MENU DO PACIENTE",
            font=('Arial', 16, 'bold'),
            fg='darkgreen',
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
        
        # Botões das funcionalidades
        botoes_frame = tk.Frame(self.frame)
        botoes_frame.pack(pady=20)
        
        funcionalidades = [
            ("📅 Agendar Consulta", self.agendar_consulta, "#4CAF50"),
            ("🔄 Remarcar Consulta", self.remarcar_consulta, "#2196F3"),
            ("❌ Cancelar Consulta", self.cancelar_consulta, "#f44336"),
            ("📋 Histórico de Consultas", self.ver_historico, "#9C27B0"),
            ("👤 Meu Perfil", self.ver_perfil, "#FF9800"),
            ("📊 Minhas Estatísticas", self.ver_estatisticas, "#607D8B"),
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
    
    def agendar_consulta(self):
        self.controller.abrir_agendamento_consulta()
    
    def remarcar_consulta(self):
        self.controller.abrir_remarcacao_consulta()
    
    def cancelar_consulta(self):
        self.controller.abrir_cancelamento_consulta()
    
    def ver_historico(self):
        self.controller.abrir_historico_consultas()
    
    def ver_perfil(self):
        self.controller.abrir_perfil_paciente()
    
    def ver_estatisticas(self):
        self.controller.abrir_estatisticas_paciente()
    
    def sair(self):
        self.controller.voltar_principal()
    
    def mostrar(self):
        self.frame.pack(fill="both", expand=True)
    
    def ocultar(self):
        self.frame.pack_forget()