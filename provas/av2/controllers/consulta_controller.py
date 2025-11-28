# controllers/consulta_controller.py
from models.consulta import Consulta
from models.medico import Medico
from models.paciente import Paciente
from datetime import datetime
import logging

class ConsultaController:
    def __init__(self, main_controller=None):
        self.main_controller = main_controller
        self.logger = logging.getLogger(__name__)

    # === OPERAÇÕES BÁSICAS DE CONSULTA ===
    def agendar_consulta(self, id_paciente, id_medico, data_consulta, hora_consulta, motivo, status='agendada'):
        """
        Agenda uma nova consulta
        Retorna: (success, message, consulta_object)
        """
        try:
            # Validar dados obrigatórios
            if not all([id_paciente, id_medico, data_consulta, hora_consulta]):
                return False, "Todos os campos obrigatórios devem ser preenchidos.", None

            # Verificar se o paciente existe
            paciente = Paciente.buscar_por_id(id_paciente)
            if not paciente:
                return False, "Paciente não encontrado.", None

            # Verificar se o médico existe
            medico = Medico.buscar_por_id(id_medico)
            if not medico:
                return False, "Médico não encontrado.", None

            # Verificar disponibilidade
            if not self.verificar_disponibilidade(id_medico, data_consulta, hora_consulta):
                return False, "Horário não disponível para agendamento.", None

            # Criar e salvar consulta
            consulta = Consulta(
                id_paciente=id_paciente,
                id_medico=id_medico,
                data_consulta=data_consulta,
                hora_consulta=hora_consulta,
                motivo=motivo or "Consulta geral",
                status=status
            )

            if consulta.salvar():
                self.logger.info(f"Consulta agendada: ID {consulta.id}, Paciente {id_paciente}, Médico {id_medico}")
                return True, "Consulta agendada com sucesso!", consulta
            else:
                return False, "Erro ao salvar consulta no banco de dados.", None

        except Exception as e:
            error_msg = f"Erro inesperado ao agendar consulta: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg, None

    def verificar_disponibilidade(self, id_medico, data_consulta, hora_consulta):
        """
        Verifica disponibilidade do médico no horário
        """
        try:
            consultas_existentes = Consulta.buscar_por_medico_e_data(id_medico, data_consulta)
            
            for consulta in consultas_existentes:
                if (consulta.hora_consulta == hora_consulta and 
                    consulta.status in ['agendada', 'confirmada']):
                    return False
            
            return True
            
        except Exception as e:
            self.logger.warning(f"Erro na verificação de disponibilidade: {e}")
            return True  # Em caso de erro, assume disponível

    # === CONSULTAS POR USUÁRIO ===
    def buscar_consultas_por_paciente(self, id_paciente):
        """
        Busca todas as consultas de um paciente
        Retorna: (success, message, consultas_list)
        """
        try:
            consultas = Consulta.buscar_por_paciente(id_paciente)
            return True, "Consultas carregadas com sucesso", consultas
        except Exception as e:
            error_msg = f"Erro ao buscar consultas do paciente: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg, []

    def buscar_consultas_por_medico(self, id_medico):
        """
        Busca todas as consultas de um médico
        Retorna: (success, message, consultas_list)
        """
        try:
            consultas = Consulta.buscar_por_medico(id_medico)
            return True, "Consultas do médico carregadas com sucesso", consultas
        except Exception as e:
            error_msg = f"Erro ao buscar consultas do médico: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg, []

    def buscar_consulta_por_id(self, id_consulta):
        """
        Busca uma consulta específica por ID
        Retorna: (success, message, consulta_object)
        """
        try:
            consulta = Consulta.buscar_por_id(id_consulta)
            if consulta:
                return True, "Consulta encontrada", consulta
            else:
                return False, "Consulta não encontrada", None
        except Exception as e:
            error_msg = f"Erro ao buscar consulta: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg, None

    # === ALTERAÇÕES DE STATUS ===
    def cancelar_consulta(self, id_consulta, motivo="Cancelado pelo paciente"):
        """
        Cancela uma consulta
        Retorna: (success, message)
        """
        try:
            consulta = Consulta.buscar_por_id(id_consulta)
            if not consulta:
                return False, "Consulta não encontrada"

            if consulta.status == 'cancelada':
                return False, "Consulta já está cancelada"

            if consulta.cancelar(motivo):
                self.logger.info(f"Consulta cancelada: ID {id_consulta}")
                return True, "Consulta cancelada com sucesso"
            else:
                return False, "Erro ao cancelar consulta"

        except Exception as e:
            error_msg = f"Erro inesperado ao cancelar consulta: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg

    def confirmar_consulta(self, id_consulta):
        """
        Confirma uma consulta (muda status para 'confirmada')
        Retorna: (success, message)
        """
        try:
            consulta = Consulta.buscar_por_id(id_consulta)
            if not consulta:
                return False, "Consulta não encontrada"

            if consulta.status == 'confirmada':
                return False, "Consulta já está confirmada"

            consulta.status = 'confirmada'
            if consulta.salvar():
                self.logger.info(f"Consulta confirmada: ID {id_consulta}")
                return True, "Consulta confirmada com sucesso"
            else:
                return False, "Erro ao confirmar consulta"

        except Exception as e:
            error_msg = f"Erro inesperado ao confirmar consulta: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg

    def finalizar_consulta(self, id_consulta, observacoes_medicas):
        """
        Finaliza uma consulta (marca como realizada)
        Retorna: (success, message)
        """
        try:
            consulta = Consulta.buscar_por_id(id_consulta)
            if not consulta:
                return False, "Consulta não encontrada"

            if consulta.status == 'realizada':
                return False, "Consulta já foi finalizada"

            if consulta.finalizar(observacoes_medicas):
                self.logger.info(f"Consulta finalizada: ID {id_consulta}")
                return True, "Consulta finalizada com sucesso"
            else:
                return False, "Erro ao finalizar consulta"

        except Exception as e:
            error_msg = f"Erro inesperado ao finalizar consulta: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg

    def remarcar_consulta(self, id_consulta, nova_data, nova_hora, novo_motivo=None):
        """
        Remarca uma consulta
        Retorna: (success, message, consulta_atualizada)
        """
        try:
            consulta = Consulta.buscar_por_id(id_consulta)
            if not consulta:
                return False, "Consulta não encontrada", None

            if consulta.status != 'agendada':
                return False, f"Não é possível remarcar consulta com status: {consulta.status}", None

            # Verificar disponibilidade do novo horário
            if not self.verificar_disponibilidade(consulta.id_medico, nova_data, nova_hora):
                return False, "Novo horário não disponível", None

            # Atualizar consulta
            consulta.data_consulta = nova_data
            consulta.hora_consulta = nova_hora
            if novo_motivo:
                consulta.motivo = novo_motivo

            if consulta.salvar():
                self.logger.info(f"Consulta remarcada: ID {id_consulta}")
                return True, "Consulta remarcada com sucesso", consulta
            else:
                return False, "Erro ao remarcar consulta", None

        except Exception as e:
            error_msg = f"Erro inesperado ao remarcar consulta: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg, None

    # === LISTAGENS E RELATÓRIOS ===
    def listar_todas_consultas(self):
        """
        Lista todas as consultas do sistema
        Retorna: (success, message, consultas_list)
        """
        try:
            consultas = Consulta.listar_todas()
            return True, "Todas as consultas carregadas", consultas
        except Exception as e:
            error_msg = f"Erro ao listar consultas: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg, []

    def listar_consultas_do_dia(self, data=None):
        """
        Lista consultas de um determinado dia
        Retorna: (success, message, consultas_list)
        """
        try:
            if not data:
                data = datetime.now().strftime('%Y-%m-%d')

            consultas = Consulta.buscar_por_data(data)
            return True, f"Consultas do dia {data} carregadas", consultas

        except Exception as e:
            error_msg = f"Erro ao listar consultas do dia: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg, []

    def listar_proximas_consultas(self, id_paciente=None, limite=10):
        """
        Lista as próximas consultas
        Retorna: (success, message, consultas_list)
        """
        try:
            if id_paciente:
                consultas = Consulta.buscar_proximas_por_paciente(id_paciente, limite)
                msg = f"Próximas {limite} consultas do paciente carregadas"
            else:
                consultas = Consulta.buscar_proximas(limite)
                msg = f"Próximas {limite} consultas carregadas"

            return True, msg, consultas

        except Exception as e:
            error_msg = f"Erro ao listar próximas consultas: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg, []

    # === ESTATÍSTICAS E RELATÓRIOS ===
    def obter_estatisticas_consultas(self):
        """
        Obtém estatísticas sobre as consultas
        Retorna: (success, message, estatisticas_dict)
        """
        try:
            todas_consultas = Consulta.listar_todas()
            
            estatisticas = {
                'total': len(todas_consultas),
                'agendadas': len([c for c in todas_consultas if c.status == 'agendada']),
                'confirmadas': len([c for c in todas_consultas if c.status == 'confirmada']),
                'realizadas': len([c for c in todas_consultas if c.status == 'realizada']),
                'canceladas': len([c for c in todas_consultas if c.status == 'cancelada']),
            }

            return True, "Estatísticas carregadas com sucesso", estatisticas

        except Exception as e:
            error_msg = f"Erro ao obter estatísticas: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg, {}

    def obter_consultas_por_periodo(self, data_inicio, data_fim):
        """
        Obtém consultas dentro de um período
        Retorna: (success, message, consultas_list)
        """
        try:
            consultas = Consulta.buscar_por_periodo(data_inicio, data_fim)
            return True, f"Consultas de {data_inicio} a {data_fim} carregadas", consultas
        except Exception as e:
            error_msg = f"Erro ao obter consultas por período: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg, []

    # === EXPORTAÇÃO DE DADOS ===
    def exportar_consultas_para_csv(self, consultas, arquivo_path):
        """
        Exporta consultas para CSV
        Retorna: (success, message)
        """
        try:
            import csv
            
            with open(arquivo_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['ID', 'Paciente', 'Médico', 'Data', 'Hora', 'Status', 'Motivo']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for consulta in consultas:
                    writer.writerow({
                        'ID': consulta.id,
                        'Paciente': consulta.paciente_nome or 'N/A',
                        'Médico': consulta.medico_nome or 'N/A',
                        'Data': consulta.data_consulta,
                        'Hora': consulta.hora_consulta,
                        'Status': consulta.status,
                        'Motivo': consulta.motivo or 'N/A'
                    })
            
            return True, f"Consultas exportadas para {arquivo_path}"

        except Exception as e:
            error_msg = f"Erro ao exportar consultas: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg

    # === VALIDAÇÕES ===
    def validar_dados_consulta(self, id_paciente, id_medico, data_consulta, hora_consulta):
        """
        Valida dados básicos de uma consulta
        Retorna: (success, message)
        """
        try:
            if not all([id_paciente, id_medico, data_consulta, hora_consulta]):
                return False, "Todos os campos obrigatórios devem ser preenchidos"

            # Validar formato da data
            try:
                datetime.strptime(data_consulta, '%Y-%m-%d')
            except ValueError:
                return False, "Formato de data inválido. Use YYYY-MM-DD"

            # Validar formato da hora
            try:
                datetime.strptime(hora_consulta, '%H:%M')
            except ValueError:
                return False, "Formato de hora inválido. Use HH:MM"

            # Verificar se data não é no passado
            data_obj = datetime.strptime(data_consulta, '%Y-%m-%d')
            if data_obj.date() < datetime.now().date():
                return False, "Não é possível agendar consultas para datas passadas"

            return True, "Dados válidos"

        except Exception as e:
            error_msg = f"Erro na validação dos dados: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
        
    def salvar_prontuario(self, consulta_id, diagnostico, prescricao, observacoes_medicas):
        """
        Salva ou atualiza o prontuário de uma consulta
        Retorna: (success, message)
        """
        try:
            consulta = Consulta.buscar_por_id(consulta_id)
            if not consulta:
                return False, "Consulta não encontrada."
            
            # Atualizar campos do prontuário
            consulta.diagnostico = diagnostico
            consulta.prescricao = prescricao
            consulta.observacoes_medicas = observacoes_medicas
            
            if consulta.salvar():
                self.logger.info(f"Prontuário salvo para consulta ID {consulta_id}")
                return True, "Prontuário salvo com sucesso!"
            else:
                return False, "Erro ao salvar prontuário no banco de dados."
                
        except Exception as e:
            error_msg = f"Erro inesperado ao salvar prontuário: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg