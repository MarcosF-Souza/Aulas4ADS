# controllers/main_controller.py
from models.paciente import Paciente
from models.medico import Medico
from models.administrador import Administrador
from database.database import Database
from .paciente_controller import PacienteController
from .medico_controller import MedicoController
from .admin_controller import AdminController
from .consulta_controller import ConsultaController
from tkinter import messagebox

class MainController:
    def __init__(self, app):
        self.app = app
        self.db = Database()
        self.db.init_database()
        self.usuario_logado = None
        
        # Inicializar controllers específicos
        self.paciente_controller = PacienteController(self)
        self.medico_controller = MedicoController(self)
        self.admin_controller = AdminController(self)
        self.consulta_controller = ConsultaController(self)

    # === NAVEGAÇÃO PRINCIPAL ===
    def mostrar_tela_principal(self):
        """Mostra a tela principal do sistema"""
        self.app.mostrar_view("MainView")

    def mostrar_menu_paciente(self):
        """Mostra o menu do paciente após login bem-sucedido"""
        print("🎯 Navegando para MenuPaciente")
    
        # Verificar se há um paciente logado
        if not self.usuario_logado:
            print("❌ Nenhum usuário logado")
            return
    
        # Atualizar o título da janela
        self.app.root.title(f"Sistema de Agendamento - Paciente: {self.usuario_logado.nome}")
    
        # Navegar para o menu do paciente
        self.app.mostrar_view("MenuPaciente")

    def mostrar_login_paciente(self):
        """Navega para tela de login do paciente"""
        self.app.mostrar_view("LoginPaciente")

    def mostrar_cadastro_paciente(self):
        """Navega para tela de cadastro do paciente"""
        self.app.mostrar_view("CadastroPaciente")

    def mostrar_login_medico(self):
        """Navega para tela de login do médico"""
        self.app.mostrar_view("LoginMedico")

    def mostrar_login_admin(self):
        """Navega para tela de login do administrador"""
        self.app.mostrar_view("LoginAdmin")

    def fazer_logout(self):
        """Realiza logout do usuário atual"""
        self.usuario_logado = None
        self.mostrar_tela_principal()

    def sair_sistema(self):
        """Encerra o sistema"""
        self.app.root.quit()

    # === AUTENTICAÇÃO ===
    def autenticar_paciente(self, email, senha):
        """
        Autentica um paciente
        Retorna: (success, message, paciente_object)
        """
        try:
            paciente = Paciente.buscar_por_email(email)
            if not paciente:
                return False, "Paciente não encontrado.", None
            
            if not paciente.ativo:
                return False, "Paciente inativo.", None
            
            # Verificar senha (simplificado - em produção usar hash)
            if paciente.senha != senha:
                return False, "Senha incorreta.", None
            
            self.usuario_logado = paciente
            return True, f"Login realizado com sucesso. Bem-vindo(a), {paciente.nome}!", paciente
            
        except Exception as e:
            error_msg = f"Erro na autenticação: {str(e)}"
            return False, error_msg, None

    def autenticar_medico(self, crm, senha):
        """
        Autentica um médico
        Retorna: (success, message, medico_object)
        """
        try:
            medico = Medico.buscar_por_crm(crm)
            if not medico:
                return False, "Médico não encontrado.", None
            
            if not medico.ativo:
                return False, "Médico inativo.", None
            
            # Verificar senha (simplificado - em produção usar hash)
            if medico.senha != senha:
                return False, "Senha incorreta.", None
            
            self.usuario_logado = medico
            return True, f"Login realizado com sucesso. Bem-vindo(a), Dr. {medico.nome}!", medico
            
        except Exception as e:
            error_msg = f"Erro na autenticação: {str(e)}"
            return False, error_msg, None

    def autenticar_admin(self, email, senha):
        """
        Autentica um administrador
        Retorna: (success, message, admin_object)
        """
        try:
            admin = Administrador.buscar_por_email(email)
            if not admin:
                return False, "Administrador não encontrado.", None
            
            if admin.status != 'ativo':
                return False, "Administrador inativo.", None
            
            if not admin.verificar_senha(senha):
                return False, "Senha incorreta.", None
            
            self.usuario_logado = admin
            return True, f"Login realizado com sucesso. Bem-vindo(a), {admin.nome}!", admin
            
        except Exception as e:
            error_msg = f"Erro na autenticação: {str(e)}"
            return False, error_msg, None

    # === CADASTRO DE USUÁRIOS ===
    def cadastrar_paciente(self, dados_paciente):
        """
        Cadastra um novo paciente
        Retorna: (success, message, paciente_object)
        """
        try:
            # Validar dados obrigatórios
            campos_obrigatorios = ['nome', 'email', 'senha']
            for campo in campos_obrigatorios:
                if not dados_paciente.get(campo):
                    return False, f"Campo {campo} é obrigatório.", None

            # Verificar se email já existe
            if Paciente.buscar_por_email(dados_paciente['email']):
                return False, "Este e-mail já está cadastrado.", None

            # Verificar confirmação de senha
            if dados_paciente.get('senha') != dados_paciente.get('confirmar_senha'):
                return False, "As senhas não coincidem.", None

            # Criar paciente
            paciente = Paciente(
                nome=dados_paciente['nome'],
                email=dados_paciente['email'],
                telefone=dados_paciente.get('telefone'),
                data_nascimento=dados_paciente.get('data_nascimento'),
                endereco=dados_paciente.get('endereco'),
                senha=dados_paciente['senha']
            )

            if paciente.salvar():
                return True, "Paciente cadastrado com sucesso!", paciente
            else:
                return False, "Erro ao cadastrar paciente no banco de dados.", None

        except Exception as e:
            error_msg = f"Erro no cadastro: {str(e)}"
            return False, error_msg, None

    # === MÉTODOS PARA AS VIEWS EXISTENTES ===
    
    def fazer_login_paciente(self, email, senha):
        """Método usado pela view de login do paciente"""
        print(f"🔐 Tentando login do paciente: {email}")
        
        sucesso, mensagem, paciente = self.autenticar_paciente(email, senha)
        
        if sucesso:
            print(f"✅ Login bem-sucedido: {paciente.nome}")
            # Usar o sistema de navegação do app para mostrar o menu
            self.usuario_logado = paciente
            self.mostrar_menu_paciente()
        else:
            print(f"❌ Falha no login: {mensagem}")
            messagebox.showerror("Erro", mensagem)

    def fazer_login_medico(self, crm, senha):
        """Método usado pela view de login do médico"""
        print(f"🔐 Tentando login do médico: {crm}")
        
        sucesso, mensagem, medico = self.autenticar_medico(crm, senha)
        
        if sucesso:
            print(f"✅ Login bem-sucedido: Dr. {medico.nome}")
            # Garantir que o usuário logado está definido
            self.usuario_logado = medico
            # Atualizar o título da janela
            self.app.root.title(f"Sistema de Agendamento - Médico: Dr. {medico.nome}")
            # Navegar para o menu do médico
            self.app.mostrar_view("MenuMedico")
        else:
            print(f"❌ Falha no login: {mensagem}")
            from tkinter import messagebox
            messagebox.showerror("Erro", mensagem)

    def verificar_medico_logado(self):
        """Verifica se há um médico logado"""
        if not self.usuario_logado:
            return False
        
        # Verificar se o usuário logado é realmente um médico
        if hasattr(self.usuario_logado, 'crm'):
            return True
        
        return False

    def fazer_login_admin(self, email, senha):
        """Método usado pela view de login do administrador"""
        print(f"🔐 Tentando login do admin: {email}")
        
        sucesso, mensagem, admin = self.autenticar_admin(email, senha)
        
        if sucesso:
            print(f"✅ Login bem-sucedido: Admin {admin.nome}")
            # Atualizar o título da janela
            self.app.root.title(f"Sistema de Agendamento - Administrador: {admin.nome}")
            # Navegar para o menu do admin
            self.app.mostrar_view("MenuAdmin")
        else:
            print(f"❌ Falha no login: {mensagem}")
            from tkinter import messagebox
            messagebox.showerror("Erro", mensagem)

    def abrir_cadastro_paciente(self):
        """Abre o cadastro de paciente"""
        self.mostrar_cadastro_paciente()

    def voltar_principal(self):
        """Volta para a tela principal"""
        self.usuario_logado = None
        self.mostrar_tela_principal()

    def mostrar_menu_paciente(self):
        """Mostra o menu do paciente após login bem-sucedido"""
        print("🎯 Navegando para MenuPaciente")
        self.app.mostrar_view("MenuPaciente")

    # === DELEGAÇÃO PARA CONTROLLERS ESPECÍFICOS ===
    
    # --- PACIENTE ---
    def abrir_menu_paciente(self, paciente_id=None):
        """Abre o menu do paciente"""
        if not paciente_id and self.usuario_logado:
            paciente_id = self.usuario_logado.id
        self.mostrar_menu_paciente()

    def abrir_agendamento_consulta(self):
        """Delega para paciente controller"""
        return self.paciente_controller.abrir_agendamento_consulta()

    def abrir_minhas_consultas(self):
        """Delega para paciente controller"""
        return self.paciente_controller.abrir_minhas_consultas()

    def abrir_meu_perfil(self):
        """Delega para paciente controller"""
        return self.paciente_controller.abrir_meu_perfil()

    # --- MÉDICO ---
    def abrir_menu_medico(self, medico_id=None):
        """Abre o menu do médico"""
        if not medico_id and self.usuario_logado:
            medico_id = self.usuario_logado.id
        self.app.mostrar_view("MenuMedico")

    def abrir_minha_agenda(self):
        """Delega para médico controller"""
        return self.medico_controller.abrir_minha_agenda()

    def abrir_consultas_do_dia(self):
        """Delega para médico controller"""
        return self.medico_controller.abrir_consultas_do_dia()

    def abrir_prontuarios(self):
        """Delega para médico controller"""
        return self.medico_controller.abrir_prontuarios()

    def abrir_gerenciamento_agenda(self):
        """Delega para médico controller"""
        return self.medico_controller.abrir_gerenciamento_agenda()

    def abrir_relatorios_medico(self):
        """Delega para médico controller"""
        return self.medico_controller.abrir_relatorios_medico()

    # --- ADMINISTRADOR ---
    def abrir_menu_admin(self, admin_id=None):
        """Abre o menu do administrador"""
        if not admin_id and self.usuario_logado:
            admin_id = self.usuario_logado.id
        self.app.mostrar_view("MenuAdmin")

    def abrir_gerenciamento_medicos(self):
        """Delega para admin controller"""
        return self.admin_controller.abrir_gerenciamento_medicos()

    def abrir_gerenciamento_pacientes(self):
        """Delega para admin controller"""
        return self.admin_controller.abrir_gerenciamento_pacientes()

    def abrir_agenda_geral(self):
        """Delega para admin controller"""
        return self.admin_controller.abrir_agenda_geral()

    def abrir_relatorios_admin(self):
        """Delega para admin controller"""
        return self.admin_controller.abrir_relatorios_admin()

    # --- CONSULTAS (ACESSO DIRETO) ---
    def agendar_consulta(self, id_paciente, id_medico, data_consulta, hora_consulta, motivo):
        """Delega para consulta controller"""
        return self.consulta_controller.agendar_consulta(
            id_paciente, id_medico, data_consulta, hora_consulta, motivo
        )

    def cancelar_consulta(self, consulta_id, motivo=None):
        """Delega para consulta controller"""
        return self.consulta_controller.cancelar_consulta(consulta_id, motivo)

    def remarcar_consulta(self, consulta_id, nova_data, nova_hora, novo_motivo=None):
        """Delega para consulta controller"""
        return self.consulta_controller.remarcar_consulta(
            consulta_id, nova_data, nova_hora, novo_motivo
        )

    # === UTILITÁRIOS ===
    def obter_usuario_logado(self):
        """Retorna o usuário atualmente logado"""
        return self.usuario_logado

    def obter_tipo_usuario_logado(self):
        """Retorna o tipo do usuário logado"""
        if not self.usuario_logado:
            return None
        
        if hasattr(self.usuario_logado, 'crm'):
            return 'medico'
        elif hasattr(self.usuario_logado, 'tipo_usuario') and self.usuario_logado.tipo_usuario == 'admin':
            return 'admin'
        else:
            return 'paciente'

    def verificar_sessao_ativa(self):
        """Verifica se há uma sessão ativa"""
        return self.usuario_logado is not None

    def obter_estatisticas_sistema(self):
        """Obtém estatísticas gerais do sistema"""
        try:
            total_pacientes = len(Paciente.buscar_todos())
            total_medicos = len(Medico.buscar_todos())
            total_admins = len(Administrador.buscar_todos())
            
            # Usar consulta controller para estatísticas de consultas
            estatisticas = self.consulta_controller.obter_estatisticas_consultas()
            
            if estatisticas:
                return {
                    'pacientes': total_pacientes,
                    'medicos': total_medicos,
                    'administradores': total_admins,
                    'consultas_total': estatisticas.get('total', 0),
                    'consultas_agendadas': estatisticas.get('agendadas', 0),
                    'consultas_realizadas': estatisticas.get('realizadas', 0),
                    'consultas_canceladas': estatisticas.get('canceladas', 0)
                }
            else:
                return {
                    'pacientes': total_pacientes,
                    'medicos': total_medicos,
                    'administradores': total_admins,
                    'consultas_total': 0,
                    'consultas_agendadas': 0,
                    'consultas_realizadas': 0,
                    'consultas_canceladas': 0
                }
                
        except Exception as e:
            print(f"Erro ao obter estatísticas do sistema: {e}")
            return {}
        
    def mostrar_agendar_consulta(self):
        """Mostra a tela de agendar consulta"""
        print("🎯 Navegando para AgendarConsulta")
        self.app.mostrar_view("AgendarConsulta")

    def mostrar_minhas_consultas(self):
        """Mostra a tela de minhas consultas"""
        print("🎯 Navegando para MinhasConsultas")
        self.app.mostrar_view("MinhasConsultas")

    def mostrar_meus_dados(self):
        """Mostra a tela de meus dados"""
        print("🎯 Navegando para MeusDados")
        self.app.mostrar_view("MeusDados")
        
    def abrir_minha_agenda(self):
        """Abre a tela Minha Agenda do médico"""
        print("🎯 Navegando para MinhaAgenda")
        self.app.mostrar_view("MinhaAgenda")

    def abrir_prescricoes(self):
        """Abre a tela de prescrições do médico"""
        print("🎯 Navegando para tela de prescrições (em desenvolvimento)")
        # Por enquanto, vamos mostrar uma mensagem
        from tkinter import messagebox
        messagebox.showinfo("Em desenvolvimento", "Funcionalidade de prescrições em desenvolvimento")

    def buscar_consultas_por_paciente(self, paciente_id):
        """Busca consultas de um paciente específico"""
        sucesso, mensagem, consultas = self.consulta_controller.buscar_consultas_por_paciente(paciente_id)
        if sucesso:
            return consultas
        else:
            print(f"❌ Erro ao buscar consultas: {mensagem}")
            return []
        
    def obter_lista_medicos(self):
        """Retorna lista de médicos para preencher combobox"""
        medicos = Medico.buscar_todos()
        return [f"Dr. {medico.nome} - {medico.especialidade}" for medico in medicos]
    
    def obter_medicos_para_combobox(self):
        """Obtém lista de médicos para preencher combobox na view de agendamento"""
        try:
            medicos = Medico.buscar_todos()
            if not medicos:
                return []
            
            # Formatar: "Dr. Nome - Especialidade"
            medicos_formatados = []
            self.mapeamento_medicos = {}  # Para uso posterior
            
            for medico in medicos:
                if medico.ativo:  # Só médicos ativos
                    texto_medico = f"Dr. {medico.nome} - {medico.especialidade}"
                    medicos_formatados.append(texto_medico)
                    self.mapeamento_medicos[texto_medico] = medico.id
            
            return medicos_formatados
            
        except Exception as e:
            print(f"Erro ao obter médicos: {e}")
            return []
        
    def obter_id_medico_por_nome(self, texto_medico):
        """Obtém o ID do médico a partir do texto do combobox"""
        try:
            # Usar o mapeamento criado anteriormente
            if hasattr(self, 'mapeamento_medicos'):
                return self.mapeamento_medicos.get(texto_medico)
            
            # Fallback: buscar no banco se não tiver mapeamento
            medicos = Medico.buscar_todos()
            for medico in medicos:
                texto_formatado = f"Dr. {medico.nome} - {medico.especialidade}"
                if texto_formatado == texto_medico:
                    return medico.id
                    
            return None
            
        except Exception as e:
            print(f"Erro ao obter ID do médico: {e}")
            return None