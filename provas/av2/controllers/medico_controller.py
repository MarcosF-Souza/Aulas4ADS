from models.medico import Medico
from models.consulta import Consulta
from models.agenda import Agenda
from models.prontuario import Prontuario
from database.database import Database
from datetime import datetime

class MedicoController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.db = Database()
    
    def obter_agenda_medico(self, medico_id, data_filtro=None):
        """Obtém a agenda do médico, com filtro opcional por data"""
        if data_filtro:
            return Consulta.buscar_por_medico_e_data(medico_id, data_filtro)
        return Consulta.buscar_por_medico(medico_id)
    
    def abrir_minha_agenda(self):
        """Abre a agenda do médico"""
        return self.main_controller.abrir_minha_agenda()
    
    def abrir_prescricoes(self):
        """Abre a tela de prescrições"""
        return self.main_controller.abrir_prescricoes()
    
    def obter_prontuario_consulta(self, consulta_id):
        """Obtém o prontuário de uma consulta específica"""
        return Prontuario.buscar_por_consulta(consulta_id)
    
    def criar_prontuario(self, consulta_id, dados_prontuario):
        """
        Cria um novo prontuário
        dados_prontuario: dict com diagnostico, prescricao, exames, observacoes
        """
        consulta = Consulta.buscar_por_id(consulta_id)
        if not consulta:
            return False, "Consulta não encontrada"
        
        prontuario = Prontuario(
            paciente_id=consulta.paciente_id,
            medico_id=consulta.medico_id,
            consulta_id=consulta_id,
            diagnostico=dados_prontuario.get('diagnostico', ''),
            prescricao=dados_prontuario.get('prescricao', ''),
            exames=dados_prontuario.get('exames', ''),
            observacoes=dados_prontuario.get('observacoes', '')
        )
        
        if prontuario.salvar():
            return True, "Prontuário criado com sucesso"
        return False, "Erro ao criar prontuário"
    
    def editar_prontuario(self, prontuario_id, dados_prontuario):
        """Edita um prontuário existente"""
        prontuario = Prontuario.buscar_por_id(prontuario_id)
        if not prontuario:
            return False, "Prontuário não encontrado"
        
        prontuario.diagnostico = dados_prontuario.get('diagnostico', prontuario.diagnostico)
        prontuario.prescricao = dados_prontuario.get('prescricao', prontuario.prescricao)
        prontuario.exames = dados_prontuario.get('exames', prontuario.exames)
        prontuario.observacoes = dados_prontuario.get('observacoes', prontuario.observacoes)
        
        if prontuario.atualizar():
            return True, "Prontuário atualizado com sucesso"
        return False, "Erro ao atualizar prontuário"
    
    def finalizar_consulta(self, consulta_id, observacao="Consulta finalizada pelo médico"):
        """Finaliza uma consulta"""
        consulta = Consulta.buscar_por_id(consulta_id)
        if not consulta:
            return False, "Consulta não encontrada"
        
        if consulta.finalizar(observacao):
            return True, "Consulta finalizada com sucesso"
        return False, "Erro ao finalizar consulta"
    
    def obter_consultas_do_dia(self, medico_id):
        """Obtém as consultas do médico para o dia atual"""
        data_hoje = datetime.now().strftime("%Y-%m-%d")
        return Consulta.buscar_por_medico_e_data(medico_id, data_hoje)
    
    def obter_relatorios_medico(self, medico_id):
        """Obtém relatórios e estatísticas do médico"""
        consultas = Consulta.buscar_por_medico(medico_id)
        
        consultas_realizadas = len([c for c in consultas if c.status == 'realizada'])
        consultas_agendadas = len([c for c in consultas if c.status == 'agendada'])
        consultas_canceladas = len([c for c in consultas if c.status == 'cancelada'])
        
        return {
            'total_consultas': len(consultas),
            'consultas_realizadas': consultas_realizadas,
            'consultas_agendadas': consultas_agendadas,
            'consultas_canceladas': consultas_canceladas
        }
    
    def buscar_consulta_por_dados(self, medico_id, data_consulta, hora_consulta, paciente_nome):
        """Busca uma consulta específica pelos dados"""
        consultas = Consulta.buscar_por_medico(medico_id)
        for consulta in consultas:
            if (consulta.data_consulta == data_consulta and 
                consulta.hora_consulta == hora_consulta and 
                consulta.paciente_nome == paciente_nome):
                return consulta
        return None
    
    def obter_dados_usuario_logado(self):
        """Obtém dados do médico logado"""
        if hasattr(self.main_controller, 'usuario_logado'):
            return {
                'id': self.main_controller.usuario_logado.id,
                'nome': self.main_controller.usuario_logado.nome,
                'crm': getattr(self.main_controller.usuario_logado, 'crm', ''),
                'especialidade': getattr(self.main_controller.usuario_logado, 'especialidade', '')
            }
        return None