import tkinter as tk
from tkinter import ttk

class MenuMedicoView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.frame = ttk.Frame(root)
        
        self._criar_widgets()
    
    def _criar_widgets(self):
        # Configurar o frame principal
        self.frame.configure(style='TFrame')
        
        # Cabeçalho
        cabecalho_frame = tk.Frame(self.frame, bg='#2E7D32')
        cabecalho_frame.pack(fill="x", pady=(0, 40))
        
        tk.Label(
            cabecalho_frame,
            text="MENU DO MÉDICO",
            font=('Arial', 20, 'bold'),
            fg='white',
            bg='#2E7D32'
        ).pack(side="left", padx=30, pady=20)
        
        # Botão Sair no cabeçalho
        tk.Button(
            cabecalho_frame,
            text="🚪 SAIR",
            font=('Arial', 10, 'bold'),
            bg='#D32F2F',
            fg='white',
            width=10,
            command=self.sair
        ).pack(side="right", padx=20, pady=10)
        
        # Container central para os botões principais
        container_central = tk.Frame(self.frame, bg='#f0f0f0')
        container_central.pack(expand=True, pady=50)
        
        # ✅ APENAS 2 FUNCIONALIDADES PRINCIPAIS
        funcionalidades = [
            ("📅 MINHA AGENDA", self.ver_minha_agenda, "#2196F3"),
            ("📋 PRONTUÁRIOS", self.ver_prontuarios, "#9C27B0"),
        ]
        
        # Criar botões principais (maiores e mais destacados)
        for texto, comando, cor in funcionalidades:
            btn = tk.Button(
                container_central,
                text=texto,
                font=('Arial', 14, 'bold'),
                bg=cor,
                fg='white',
                width=25,
                height=3,
                relief='flat',
                bd=0,
                cursor='hand2',
                command=comando
            )
            btn.pack(pady=20, padx=50)
        
        # Rodapé com informações do médico
        rodape_frame = tk.Frame(self.frame, bg='#f0f0f0')
        rodape_frame.pack(side='bottom', fill='x', pady=20)
        
        # Aqui você pode adicionar informações do médico logado se quiser
        medico_logado = self.controller.obter_usuario_logado()
        if medico_logado:
            info_texto = f"Dr. {medico_logado.nome} - {medico_logado.especialidade}"
            tk.Label(
                rodape_frame,
                text=info_texto,
                font=('Arial', 10),
                fg='#666666',
                bg='#f0f0f0'
            ).pack()
    
    def ver_minha_agenda(self):
        """Abre a tela de Minha Agenda"""
        self.controller.abrir_minha_agenda()
    
    def ver_prontuarios(self):
        """Abre a tela de Prontuários"""
        self.controller.abrir_prontuarios()
    
    def sair(self):
        """Volta para a tela principal"""
        self.controller.voltar_principal()
    
    def mostrar(self):
        """Mostra o menu do médico"""
        self.frame.pack(fill="both", expand=True)
    
    def ocultar(self):
        """Oculta o menu do médico"""
        self.frame.pack_forget()