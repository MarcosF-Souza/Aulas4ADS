from models.consulta import Consulta
from controllers.consulta_controller import ConsultaController
from models.paciente import Paciente

class PacienteController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.consulta_controller = ConsultaController(main_controller)

    def autenticar_paciente(self, email, senha):
        paciente = Paciente.buscar_por_email(email)
        if paciente and paciente.senha == senha:
            return paciente
        return None
    

    def obter_consultas_paciente(self, paciente_id):
        """Obtém todas as consultas de um paciente"""
        try:
            return Consulta.buscar_por_paciente(paciente_id)
        except Exception as e:
            raise Exception(f"Erro ao obter consultas do paciente: {e}")
        
    def atualizar_consulta(self, consulta_id, dados_consulta):
        """Atualiza os dados de uma consulta"""
        try:
            return self.consulta_controller.atualizar_consulta(consulta_id, dados_consulta)
        except Exception as e:
            raise Exception(f"Erro ao atualizar consulta: {e}")

    def cancelar_consulta(self, consulta_id):
        """Cancela uma consulta"""
        try:
            return self.consulta_controller.cancelar_consulta(consulta_id)
        except Exception as e:
            raise Exception(f"Erro ao cancelar consulta: {e}")

    def obter_dados_usuario_logado(self):
        """Obtém dados do paciente logado"""
        if hasattr(self.main_controller, 'usuario_logado'):
            return {
                'id': self.main_controller.usuario_logado.id,
                'nome': self.main_controller.usuario_logado.nome,
                'cpf': getattr(self.main_controller.usuario_logado, 'cpf', ''),
                'telefone': getattr(self.main_controller.usuario_logado, 'telefone', ''),
                'email': getattr(self.main_controller.usuario_logado, 'email', '')
            }
        return None

    def obter_consultas_futuras(self, paciente_id):
        """Obtém consultas futuras do paciente"""
        try:
            consultas = Consulta.buscar_por_paciente(paciente_id)
            from datetime import datetime
            hoje = datetime.now().date()
            
            consultas_futuras = []
            for consulta in consultas:
                data_consulta = datetime.strptime(consulta.data_consulta, "%Y-%m-%d").date()
                if data_consulta >= hoje and consulta.status == 'agendada':
                    consultas_futuras.append(consulta)
            
            return consultas_futuras
        except Exception as e:
            raise Exception(f"Erro ao obter consultas futuras: {e}")

    def obter_historico_consultas(self, paciente_id):
        """Obtém histórico de consultas realizadas do paciente"""
        try:
            consultas = Consulta.buscar_por_paciente(paciente_id)
            
            historico = []
            for consulta in consultas:
                if consulta.status == 'realizada':
                    historico.append(consulta)
            
            return historico
        except Exception as e:
            raise Exception(f"Erro ao obter histórico de consultas: {e}")

    # Métodos de navegação (delega para o main_controller)
    def abrir_agendamento_consulta(self):
        """Abre a tela de agendamento de consulta"""
        self.main_controller.abrir_agendamento_consulta()

    def abrir_minhas_consultas(self):
        """Abre a tela de minhas consultas"""
        self.main_controller.abrir_minhas_consultas()

    def abrir_meu_perfil(self):
        """Abre a tela de perfil do paciente"""
        self.main_controller.abrir_meu_perfil()