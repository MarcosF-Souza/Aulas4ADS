from models.paciente import Paciente
from models.medico import Medico
from database.database import Database
from tkinter import messagebox
from .paciente_controller import PacienteController
from .medico_controller import MedicoController
from .admin_controller import AdminController # Importar AdminController

class MainController:
    def __init__(self, app):
        self.app = app
        self.db = Database()
        self.db.init_database()
        self.usuario_logado = None
        
        # Inicializar controllers específicos
        self.paciente_controller = PacienteController(self)
        self.medico_controller = MedicoController(self)
        self.admin_controller = AdminController(self) # Instanciar AdminController
    
    # Métodos de navegação
    def abrir_login_paciente(self):
        self.app.mostrar_view("LoginPaciente")
    
    def abrir_cadastro_paciente(self):
        self.app.mostrar_view("CadastroPaciente")
    
    def abrir_login_medico(self):
        self.app.mostrar_view("LoginMedico")
    
    def abrir_login_admin(self):
        self.app.mostrar_view("LoginAdmin")
    
    def voltar_principal(self):
        self.app.mostrar_view("MainView")
        self.usuario_logado = None
    
    def voltar_login_paciente(self):
        self.app.mostrar_view("LoginPaciente")
    
    def sair_sistema(self):
        if messagebox.askyesno("Sair", "Deseja realmente sair do sistema?"):
            self.app.root.quit()
    
    # Métodos de autenticação
    def fazer_login_paciente(self, email, senha):
        paciente = Paciente.buscar_por_email(email)
        if paciente and paciente.senha == senha and paciente.ativo:
            self.usuario_logado = paciente
            self.app.mostrar_view("MenuPaciente")
            # Limpar campos da tela de login
            self.app.views["LoginPaciente"].limpar_campos()
            return True
        else:
            messagebox.showerror("Erro", "E-mail ou senha inválidos!")
            return False
    
    def cadastrar_paciente(self, dados):
        # Verificar se as senhas coincidem
        if dados['senha'] != dados['confirmar_senha']:
            messagebox.showerror("Erro", "As senhas não coincidem!")
            return False
        
        # Verificar se email já existe
        if Paciente.buscar_por_email(dados['email']):
            messagebox.showerror("Erro", "Este e-mail já está cadastrado!")
            return False
        
        paciente = Paciente(
            nome=dados['nome'],
            email=dados['email'],
            telefone=dados['telefone'],
            data_nascimento=dados['data_nascimento'],
            endereco=dados['endereco'],
            senha=dados['senha']
        )
        
        if paciente.salvar():
            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
            self.app.views["CadastroPaciente"].limpar_campos()
            self.app.mostrar_view("LoginPaciente")
            return True
        else:
            messagebox.showerror("Erro", "Erro ao cadastrar paciente!")
            return False
    
    def fazer_login_medico(self, crm, senha):
        medico = Medico.buscar_por_crm(crm)
        if medico and medico.senha == senha and medico.ativo:
            self.usuario_logado = medico
            self.app.mostrar_view("MenuMedico")
            self.app.views["LoginMedico"].limpar_campos()
            return True
        else:
            messagebox.showerror("Erro", "CRM ou senha inválidos!")
            return False
    
    def fazer_login_admin(self, usuario, senha):
        """Buscar administrador no banco de dados"""
        admin = self.db.fetch_one("SELECT * FROM administradores WHERE usuario = ? AND senha = ?", (usuario, senha))
        
        if admin:
            self.usuario_logado = admin
            self.app.mostrar_view("MenuAdmin")
            self.app.views["LoginAdmin"].limpar_campos()
            return True
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")
            return False
    
    # Métodos delegados para os controllers específicos
    
    # Paciente
    def abrir_agendamento_consulta(self):
        self.paciente_controller.abrir_agendamento_consulta()
    
    def abrir_minhas_consultas(self):
        self.paciente_controller.abrir_minhas_consultas()
    
    def abrir_meu_perfil(self):
        self.paciente_controller.abrir_meu_perfil()
    
    # Médico
    def abrir_minha_agenda(self):
        self.medico_controller.abrir_minha_agenda()
    
    def abrir_consultas_do_dia(self):
        self.medico_controller.abrir_consultas_do_dia()
    
    def abrir_prontuarios(self):
        self.medico_controller.ver_prontuario(None)  # Será chamado com treeview específica
    
    def abrir_gerenciamento_agenda(self):
        self.medico_controller.abrir_gerenciar_agenda()
    
    def abrir_relatorios_medico(self):
        self.medico_controller.abrir_relatorios()
    
    # Administrador
    def abrir_gerenciamento_medicos(self):
        self.admin_controller.abrir_gerenciamento_medicos()
    
    def abrir_gerenciamento_pacientes(self):
        self.admin_controller.abrir_gerenciamento_pacientes()
    
    def abrir_agenda_geral(self):
        self.admin_controller.abrir_agenda_geral()
    
    def abrir_relatorios_admin(self):
        self.admin_controller.abrir_relatorios_admin()
    
    # Placeholders para outras funcionalidades
    def abrir_remarcacao_consulta(self):
        messagebox.showinfo("Em Desenvolvimento", "Funcionalidade de remarcação em desenvolvimento")
    
    def abrir_configuracoes(self):
        messagebox.showinfo("Em Desenvolvimento", "Funcionalidade de configurações em desenvolvimento")
    
    def abrir_controle_acessos(self):
        messagebox.showinfo("Em Desenvolvimento", "Funcionalidade de controle de acessos em desenvolvimento")