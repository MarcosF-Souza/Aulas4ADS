# views/paciente/menu_view.py (atualizado)
import tkinter as tk
from tkinter import ttk, messagebox

class MenuPacienteView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.frame = tk.Frame(root, bg='#f0f0f0')
        
        # Inicialmente não criamos os widgets até saber qual paciente
        self.paciente = None
        
    def _criar_widgets(self):
        if not self.paciente:
            return
            
        print(f"🛠️ Criando menu para: {self.paciente.nome}")
        
        # Limpar widgets existentes
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # Configurar o frame principal
        self.frame.configure(bg='#f0f0f0')
        
        # Título
        titulo = tk.Label(
            self.frame, 
            text=f"BEM-VINDO, {self.paciente.nome.upper()}!",
            font=('Arial', 18, 'bold'),
            fg='#2E7D32',
            bg='#f0f0f0'
        )
        titulo.pack(pady=(50, 20))
        
        # Subtítulo
        subtitulo = tk.Label(
            self.frame,
            text="Sistema de Agendamento de Consultas",
            font=('Arial', 12),
            fg='#555555',
            bg='#f0f0f0'
        )
        subtitulo.pack(pady=(0, 40))
        
        # Container central para os botões
        container_central = tk.Frame(self.frame, bg='#f0f0f0')
        container_central.pack(expand=True)
        
        # Botões do menu
        botoes = [
            ("📅 AGENDAR CONSULTA", self.agendar_consulta, '#4CAF50'),
            ("📋 MINHAS CONSULTAS", self.minhas_consultas, '#2196F3'),
            ("👤 MEUS DADOS", self.meus_dados, '#FF9800'),
            ("📊 MEUS PRONTUÁRIOS", self.meus_prontuarios, '#9C27B0'),
            ("🚪 SAIR", self.sair, '#f44336')
        ]
        
        for texto, comando, cor in botoes:
            btn = tk.Button(
                container_central,
                text=texto,
                font=('Arial', 12, 'bold'),
                bg=cor,
                fg='white',
                width=25,
                height=2,
                command=comando,
                relief='flat',
                bd=0,
                cursor='hand2'
            )
            btn.pack(pady=12, padx=50, fill='x')
        
        # Rodapé
        rodape = tk.Label(
            self.frame,
            text=f"Paciente: {self.paciente.nome} | Email: {self.paciente.email}",
            font=('Arial', 9),
            fg='#777777',
            bg='#f0f0f0'
        )
        rodape.pack(side='bottom', pady=20)
    
    def agendar_consulta(self):
        self.controller.mostrar_agendar_consulta()

    def minhas_consultas(self):
        self.controller.mostrar_minhas_consultas()
    
    def meus_dados(self):
        messagebox.showinfo("Dados", "Funcionalidade de dados em desenvolvimento")
    
    def meus_prontuarios(self):
        messagebox.showinfo("Prontuários", "Funcionalidade de prontuários em desenvolvimento")
    
    def sair(self):
        self.controller.voltar_principal()
    
    def mostrar(self):
        print("🖥️ Mostrando menu do paciente...")
        
        # Obter o paciente logado do controller
        self.paciente = self.controller.usuario_logado
        
        if not self.paciente:
            print("❌ Nenhum paciente logado")
            messagebox.showerror("Erro", "Nenhum paciente logado")
            return
        
        # Criar os widgets com o paciente atual
        self._criar_widgets()
        
        # Mostrar o frame
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        print("✅ Menu do paciente exibido")
    
    def ocultar(self):
        self.frame.pack_forget()