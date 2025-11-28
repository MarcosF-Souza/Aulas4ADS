# controllers/admin_controller.py
from models.medico import Medico
from models.paciente import Paciente
from models.consulta import Consulta
from models.administrador import Administrador

class AdminController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
    
    # === MÉDICOS ===
    def listar_medicos(self):
        """Retorna lista de todos os médicos"""
        try:
            return Medico.listar_todos()
        except Exception as e:
            print(f"Erro ao listar médicos: {e}")
            return []
    
    def obter_medico_por_id(self, medico_id):
        """Retorna um médico específico pelo ID"""
        try:
            return Medico.buscar_por_id(medico_id)
        except Exception as e:
            print(f"Erro ao buscar médico: {e}")
            return None
    
    def criar_medico(self, dados_medico):
        """Cria um novo médico"""
        try:
            medico = Medico(
                nome=dados_medico['nome'],
                crm=dados_medico['crm'],
                especialidade=dados_medico['especialidade'],
                email=dados_medico['email'],
                telefone=dados_medico.get('telefone'),
                senha=dados_medico['senha']
            )
            return medico.criar()
        except Exception as e:
            print(f"Erro ao criar médico: {e}")
            return False
    
    def atualizar_medico(self, medico_id, dados_medico):
        """Atualiza os dados de um médico"""
        try:
            medico = Medico.buscar_por_id(medico_id)
            if not medico:
                return False
            
            medico.nome = dados_medico['nome']
            medico.crm = dados_medico['crm']
            medico.especialidade = dados_medico['especialidade']
            medico.email = dados_medico['email']
            medico.telefone = dados_medico.get('telefone')
            
            if dados_medico.get('senha'):
                medico.senha = dados_medico['senha']
            
            return medico.atualizar()
        except Exception as e:
            print(f"Erro ao atualizar médico: {e}")
            return False
    
    def alterar_status_medico(self, medico_id, ativo):
        """Ativa ou desativa um médico"""
        try:
            medico = Medico.buscar_por_id(medico_id)
            if not medico:
                return False
            
            if ativo:
                return medico.ativar()
            else:
                return medico.desativar()
        except Exception as e:
            print(f"Erro ao alterar status do médico: {e}")
            return False
    
    # === PACIENTES ===
    def listar_pacientes(self):
        """Retorna lista de todos os pacientes"""
        try:
            return Paciente.listar_todos()
        except Exception as e:
            print(f"Erro ao listar pacientes: {e}")
            return []
    
    def obter_paciente_por_id(self, paciente_id):
        """Retorna um paciente específico pelo ID"""
        try:
            return Paciente.buscar_por_id(paciente_id)
        except Exception as e:
            print(f"Erro ao buscar paciente: {e}")
            return None
    
    def criar_paciente(self, dados_paciente):
        """Cria um novo paciente"""
        try:
            paciente = Paciente(
                nome=dados_paciente['nome'],
                email=dados_paciente['email'],
                telefone=dados_paciente.get('telefone'),
                data_nascimento=dados_paciente.get('data_nascimento'),
                endereco=dados_paciente.get('endereco'),
                senha=dados_paciente['senha']
            )
            return paciente.criar()
        except Exception as e:
            print(f"Erro ao criar paciente: {e}")
            return False
    
    def atualizar_paciente(self, paciente_id, dados_paciente):
        """Atualiza os dados de um paciente"""
        try:
            paciente = Paciente.buscar_por_id(paciente_id)
            if not paciente:
                return False
            
            paciente.nome = dados_paciente['nome']
            paciente.email = dados_paciente['email']
            paciente.telefone = dados_paciente.get('telefone')
            paciente.data_nascimento = dados_paciente.get('data_nascimento')
            paciente.endereco = dados_paciente.get('endereco')
            
            if dados_paciente.get('senha'):
                paciente.senha = dados_paciente['senha']
            
            return paciente.atualizar()
        except Exception as e:
            print(f"Erro ao atualizar paciente: {e}")
            return False
    
    def alterar_status_paciente(self, paciente_id, ativo):
        """Ativa ou desativa um paciente"""
        try:
            paciente = Paciente.buscar_por_id(paciente_id)
            if not paciente:
                return False
            
            if ativo:
                return paciente.ativar()
            else:
                return paciente.desativar()
        except Exception as e:
            print(f"Erro ao alterar status do paciente: {e}")
            return False
    
    # === CONSULTAS ===
    def listar_todas_consultas(self):
        """Retorna lista de todas as consultas"""
        try:
            return Consulta.listar_todas()
        except Exception as e:
            print(f"Erro ao listar consultas: {e}")
            return []
    
    def obter_consulta_por_id(self, consulta_id):
        """Retorna uma consulta específica pelo ID"""
        try:
            return Consulta.buscar_por_id(consulta_id)
        except Exception as e:
            print(f"Erro ao buscar consulta: {e}")
            return None
    
    def cancelar_consulta_admin(self, consulta_id):
        """Cancela uma consulta (admin)"""
        try:
            consulta = Consulta.buscar_por_id(consulta_id)
            if not consulta:
                return False
            
            consulta.status = "Cancelada"
            return consulta.atualizar()
        except Exception as e:
            print(f"Erro ao cancelar consulta: {e}")
            return False
    
    # === ADMINISTRADORES ===
    def listar_administradores(self):
        """Retorna lista de todos os administradores"""
        try:
            return Administrador.listar_todos()
        except Exception as e:
            print(f"Erro ao listar administradores: {e}")
            return []
    
    def criar_administrador(self, dados_admin):
        """Cria um novo administrador"""
        try:
            admin = Administrador(
                nome=dados_admin['nome'],
                email=dados_admin['email'],
                senha=dados_admin['senha'],
                telefone=dados_admin.get('telefone'),
                cargo=dados_admin.get('cargo', 'Administrador'),
                nivel_acesso=dados_admin.get('nivel_acesso', 'total')
            )
            return admin.criar()
        except Exception as e:
            print(f"Erro ao criar administrador: {e}")
            return False
    
    def atualizar_administrador(self, admin_id, dados_admin):
        """Atualiza os dados de um administrador"""
        try:
            admin = Administrador.buscar_por_id(admin_id)
            if not admin:
                return False
            
            admin.nome = dados_admin['nome']
            admin.email = dados_admin['email']
            admin.telefone = dados_admin.get('telefone')
            admin.cargo = dados_admin.get('cargo')
            admin.nivel_acesso = dados_admin.get('nivel_acesso')
            
            if dados_admin.get('senha'):
                admin.redefinir_senha(dados_admin['senha'])
            
            return admin.atualizar()
        except Exception as e:
            print(f"Erro ao atualizar administrador: {e}")
            return False
    
    def alterar_status_administrador(self, admin_id, status):
        """Altera o status de um administrador"""
        try:
            admin = Administrador.buscar_por_id(admin_id)
            if not admin:
                return False
            
            return admin.alterar_status(status)
        except Exception as e:
            print(f"Erro ao alterar status do administrador: {e}")
            return False
    
    # === RELATÓRIOS E ESTATÍSTICAS ===
    def obter_estatisticas_gerais(self):
        """Retorna estatísticas gerais do sistema"""
        try:
            total_medicos = len(Medico.listar_todos())
            total_pacientes = len(Paciente.listar_todos())
            total_consultas = len(Consulta.listar_todas())
            
            consultas_agendadas = len([c for c in Consulta.listar_todas() if c.status == 'Agendada'])
            consultas_realizadas = len([c for c in Consulta.listar_todas() if c.status == 'Realizada'])
            consultas_canceladas = len([c for c in Consulta.listar_todas() if c.status == 'Cancelada'])
            
            return {
                'total_medicos': total_medicos,
                'total_pacientes': total_pacientes,
                'total_consultas': total_consultas,
                'consultas_agendadas': consultas_agendadas,
                'consultas_realizadas': consultas_realizadas,
                'consultas_canceladas': consultas_canceladas
            }
        except Exception as e:
            print(f"Erro ao obter estatísticas: {e}")
            return {}
    
    def obter_consultas_por_periodo(self, data_inicio, data_fim):
        """Retorna consultas em um período específico"""
        try:
            # Implementar lógica para filtrar por período
            todas_consultas = Consulta.listar_todas()
            # Filtro simplificado - você pode implementar lógica mais robusta
            consultas_filtradas = [
                c for c in todas_consultas 
                if data_inicio <= c.data_consulta <= data_fim
            ]
            return consultas_filtradas
        except Exception as e:
            print(f"Erro ao obter consultas por período: {e}")
            return []