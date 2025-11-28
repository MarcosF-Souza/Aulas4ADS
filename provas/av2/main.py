# main.py
import tkinter as tk
from tkinter import ttk
from views.main_view import MainView
from views.paciente.login_view import LoginPacienteView
from views.paciente.cadastro_view import CadastroPacienteView
from views.paciente.menu_view import MenuPacienteView
from views.paciente.agendar_consulta_view import AgendarConsultaView
from views.paciente.minhas_consultas_view import MinhasConsultasView
from views.medico.login_view import LoginMedicoView
from views.medico.menu_view import MenuMedicoView
from views.admin.login_view import LoginAdminView
from views.admin.menu_view import MenuAdminView
from controllers.main_controller import MainController
from views.medico.minha_agenda_view import MinhaAgendaView
from views.paciente.meus_dados_view import MeusDadosView  

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Agendamento de Consultas Médicas")
        self.root.geometry("900x700")
        self.root.configure(bg='white')
        
        # Configurar estilo para botões de destaque
        self.configurar_estilos()
        
        # Inicializar controller
        self.controller = MainController(self)
        
        # Dicionário para armazenar as views
        self.views = {}
        
        # Inicializar todas as views
        self._inicializar_views()
        
        # Mostrar a view principal
        self.mostrar_view("MainView")
        
    def configurar_estilos(self):
        """Configura estilos personalizados para a aplicação"""
        style = ttk.Style()
        
        # Estilo para botão de destaque (accent)
        style.configure('Accent.TButton', 
                       foreground='white',
                       background='#007acc',
                       font=('Arial', 10, 'bold'))
        
        style.map('Accent.TButton',
                 background=[('active', '#005a9e'),
                           ('pressed', '#004a7c')])
    
    def _inicializar_views(self):
        """Inicializa todas as views do sistema"""
        print("🔄 Inicializando views...")
        
        # View principal
        self.views["MainView"] = MainView(self.root, self.controller)
        print("✅ MainView inicializada")
        
        # Views do paciente
        self.views["LoginPaciente"] = LoginPacienteView(self.root, self.controller)
        self.views["CadastroPaciente"] = CadastroPacienteView(self.root, self.controller)
        self.views["MenuPaciente"] = MenuPacienteView(self.root, self.controller)
        self.views["AgendarConsulta"] = AgendarConsultaView(self.root, self.controller)
        self.views["MinhasConsultas"] = MinhasConsultasView(self.root, self.controller)
        print("✅ Views do paciente inicializadas")
        
        # Views do médico
        self.views["LoginMedico"] = LoginMedicoView(self.root, self.controller)
        self.views["MenuMedico"] = MenuMedicoView(self.root, self.controller)
        self.views["MinhaAgenda"] = MinhaAgendaView(self.root, self.controller)
        print("✅ Views do médico inicializadas")
        
        # Views do administrador
        self.views["LoginAdmin"] = LoginAdminView(self.root, self.controller)
        self.views["MenuAdmin"] = MenuAdminView(self.root, self.controller)
        print("✅ Views do admin inicializadas")
        
        print("🎉 Todas as views foram inicializadas com sucesso!")
    
    def mostrar_view(self, nome_view):
        """Mostra a view especificada e oculta as outras"""
        print(f"🔄 Navegando para: {nome_view}")
        
        # Verificar se a view existe
        if nome_view not in self.views:
            print(f"❌ View não encontrada: {nome_view}")
            return
        
        # Ocultar todas as views
        for nome, view in self.views.items():
            try:
                if hasattr(view, 'ocultar') and callable(view.ocultar):
                    view.ocultar()
                elif hasattr(view, 'frame'):
                    view.frame.pack_forget()
            except Exception as e:
                print(f"⚠️ Erro ao ocultar view {nome}: {e}")
        
        # Mostrar a view solicitada
        view = self.views[nome_view]
        try:
            if hasattr(view, 'mostrar') and callable(view.mostrar):
                view.mostrar()
            elif hasattr(view, 'frame'):
                view.frame.pack(fill="both", expand=True)
            print(f"✅ View {nome_view} mostrada com sucesso")
        except Exception as e:
            print(f"❌ Erro ao mostrar view {nome_view}: {e}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()