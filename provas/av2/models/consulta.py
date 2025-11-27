from database.database import Database

class Consulta:
    def __init__(self, id=None, id_paciente=None, id_medico=None, data_consulta=None, 
                 hora_consulta=None, status='agendada', motivo=None, observacoes=None, 
                 data_criacao=None, paciente_nome=None, medico_nome=None, especialidade=None):
        self.id = id
        self.id_paciente = id_paciente
        self.id_medico = id_medico
        self.data_consulta = data_consulta
        self.hora_consulta = hora_consulta
        self.status = status  # 'agendada', 'confirmada', 'realizada', 'cancelada', 'remarcada'
        self.motivo = motivo
        self.observacoes = observacoes
        self.data_criacao = data_criacao
        # Campos para join (não existem na tabela, mas são úteis para exibição)
        self.paciente_nome = paciente_nome
        self.medico_nome = medico_nome
        self.especialidade = especialidade
    
    def salvar(self):
        """Salva ou atualiza uma consulta (CREATE/UPDATE)"""
        db = Database()
        if self.id is None:
            # Nova consulta
            query = """
            INSERT INTO consultas (id_paciente, id_medico, data_consulta, hora_consulta, status, motivo, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            params = (self.id_paciente, self.id_medico, self.data_consulta, 
                     self.hora_consulta, self.status, self.motivo, self.observacoes)
            return db.execute_query(query, params)
        else:
            # Atualizar consulta existente
            query = """
            UPDATE consultas 
            SET id_paciente=?, id_medico=?, data_consulta=?, hora_consulta=?, status=?, motivo=?, observacoes=?
            WHERE id=?
            """
            params = (self.id_paciente, self.id_medico, self.data_consulta, 
                     self.hora_consulta, self.status, self.motivo, self.observacoes, self.id)
            return db.execute_query(query, params)
    
    @staticmethod
    def buscar_por_id(id):
        """Busca uma consulta por ID (READ)"""
        db = Database()
        query = """
        SELECT c.*, p.nome as paciente_nome, m.nome as medico_nome, m.especialidade
        FROM consultas c
        LEFT JOIN pacientes p ON c.id_paciente = p.id
        LEFT JOIN medicos m ON c.id_medico = m.id
        WHERE c.id = ?
        """
        result = db.fetch_one(query, (id,))
        if result:
            return Consulta(**result)
        return None
    
    @staticmethod
    def buscar_por_paciente(id_paciente):
        """Busca todas as consultas de um paciente"""
        db = Database()
        query = """
        SELECT c.*, p.nome as paciente_nome, m.nome as medico_nome, m.especialidade
        FROM consultas c
        LEFT JOIN pacientes p ON c.id_paciente = p.id
        LEFT JOIN medicos m ON c.id_medico = m.id
        WHERE c.id_paciente = ?
        ORDER BY c.data_consulta DESC, c.hora_consulta DESC
        """
        results = db.fetch_all(query, (id_paciente,))
        consultas = []
        for result in results:
            consultas.append(Consulta(**result))
        return consultas
    
    @staticmethod
    def buscar_por_medico(id_medico):
        """Busca todas as consultas de um médico"""
        db = Database()
        query = """
        SELECT c.*, p.nome as paciente_nome, m.nome as medico_nome, m.especialidade
        FROM consultas c
        LEFT JOIN pacientes p ON c.id_paciente = p.id
        LEFT JOIN medicos m ON c.id_medico = m.id
        WHERE c.id_medico = ?
        ORDER BY c.data_consulta, c.hora_consulta
        """
        results = db.fetch_all(query, (id_medico,))
        consultas = []
        for result in results:
            consultas.append(Consulta(**result))
        return consultas
    
    @staticmethod
    def buscar_por_medico_e_data(id_medico, data_consulta):
        """Busca consultas de um médico em uma data específica"""
        db = Database()
        query = """
        SELECT c.*, p.nome as paciente_nome, m.nome as medico_nome, m.especialidade
        FROM consultas c
        LEFT JOIN pacientes p ON c.id_paciente = p.id
        LEFT JOIN medicos m ON c.id_medico = m.id
        WHERE c.id_medico = ? AND c.data_consulta = ?
        ORDER BY c.hora_consulta
        """
        results = db.fetch_all(query, (id_medico, data_consulta))
        consultas = []
        for result in results:
            consultas.append(Consulta(**result))
        return consultas
    
    @staticmethod
    def buscar_proximas_por_paciente(id_paciente, limite=10):
        """Busca as próximas consultas de um paciente"""
        db = Database()
        query = """
        SELECT c.*, p.nome as paciente_nome, m.nome as medico_nome, m.especialidade
        FROM consultas c
        LEFT JOIN pacientes p ON c.id_paciente = p.id
        LEFT JOIN medicos m ON c.id_medico = m.id
        WHERE c.id_paciente = ? AND c.data_consulta >= date('now') 
        AND c.status IN ('agendada', 'confirmada')
        ORDER BY c.data_consulta, c.hora_consulta
        LIMIT ?
        """
        results = db.fetch_all(query, (id_paciente, limite))
        consultas = []
        for result in results:
            consultas.append(Consulta(**result))
        return consultas
    
    def confirmar(self):
        """Confirma uma consulta"""
        self.status = 'confirmada'
        return self.salvar()
    
    def cancelar(self, motivo="Cancelado pelo paciente"):
        """Cancela uma consulta"""
        self.status = 'cancelada'
        self.observacoes = f"{self.observacoes or ''}\nCancelamento: {motivo}"
        return self.salvar()
    
    def remarcar(self, nova_data, nova_hora):
        """Remarca uma consulta"""
        self.data_consulta = nova_data
        self.hora_consulta = nova_hora
        self.status = 'remarcada'
        self.observacoes = f"{self.observacoes or ''}\nRemarcada para: {nova_data} {nova_hora}"
        return self.salvar()
    
    def finalizar(self, observacoes_medicas):
        """Finaliza uma consulta (marcar como realizada)"""
        self.status = 'realizada'
        self.observacoes = f"{self.observacoes or ''}\nFinalizada: {observacoes_medicas}"
        return self.salvar()
    
    def verificar_disponibilidade(self):
        """Verifica se o horário da consulta está disponível"""
        from .agenda import Agenda
        
        horarios_disponiveis = Agenda.buscar_disponiveis_por_medico_e_data(
            self.id_medico, self.data_consulta
        )
        
        for horario in horarios_disponiveis:
            if (horario.hora_inicio <= self.hora_consulta < horario.hora_fim and 
                horario.disponivel):
                return True
        return False
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'id_paciente': self.id_paciente,
            'id_medico': self.id_medico,
            'data_consulta': self.data_consulta,
            'hora_consulta': self.hora_consulta,
            'status': self.status,
            'motivo': self.motivo,
            'observacoes': self.observacoes,
            'data_criacao': self.data_criacao,
            'paciente_nome': self.paciente_nome,
            'medico_nome': self.medico_nome,
            'especialidade': self.especialidade
        }