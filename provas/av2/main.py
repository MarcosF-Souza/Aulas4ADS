import tkinter as tk
from tkinter import ttk
from views.main_view import MainView
from views.paciente.login_view import LoginPacienteView
from views.paciente.cadastro_view import CadastroPacienteView
from views.paciente.menu_view import MenuPacienteView
from views.medico.login_view import LoginMedicoView
from views.medico.menu_view import MenuMedicoView
from views.admin.login_view import LoginAdminView
from views.admin.menu_view import MenuAdminView
from controllers.main_controller import MainController

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
        self.views["MainView"] = MainView(self.root, self.controller)
        
        # Views do paciente
        self.views["LoginPaciente"] = LoginPacienteView(self.root, self.controller)
        self.views["CadastroPaciente"] = CadastroPacienteView(self.root, self.controller)
        self.views["MenuPaciente"] = MenuPacienteView(self.root, self.controller)
        
        # Views do médico
        self.views["LoginMedico"] = LoginMedicoView(self.root, self.controller)
        self.views["MenuMedico"] = MenuMedicoView(self.root, self.controller)
        
        # Views do administrador
        self.views["LoginAdmin"] = LoginAdminView(self.root, self.controller)
        self.views["MenuAdmin"] = MenuAdminView(self.root, self.controller)
    
    def mostrar_view(self, nome_view):
        """Mostra a view especificada e oculta as outras"""
        for nome, view in self.views.items():
            if nome == nome_view:
                view.mostrar()
            else:
                if hasattr(view, 'ocultar'):
                    view.ocultar()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()