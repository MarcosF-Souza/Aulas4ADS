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
        self.status = status
        self.motivo = motivo
        self.observacoes = observacoes
        self.data_criacao = data_criacao
        # Campos para join
        self.paciente_nome = paciente_nome
        self.medico_nome = medico_nome
        self.especialidade = especialidade
    
    def salvar(self):
        """Salva ou atualiza a consulta"""
        if self.id is None:
            return self._criar()
        else:
            return self._atualizar()
    
    def _criar(self):
        """Cria uma nova consulta"""
        query = """
        INSERT INTO consultas (id_paciente, id_medico, data_consulta, hora_consulta, status, motivo, observacoes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (self.id_paciente, self.id_medico, self.data_consulta, 
                 self.hora_consulta, self.status, self.motivo, self.observacoes)
        
        db = Database()
        self.id = db.executar_query(query, params, retornar_id=True)
        return self.id
    
    def _atualizar(self):
        """Atualiza uma consulta existente"""
        query = """
        UPDATE consultas 
        SET id_paciente=?, id_medico=?, data_consulta=?, hora_consulta=?, status=?, motivo=?, observacoes=?
        WHERE id=?
        """
        params = (self.id_paciente, self.id_medico, self.data_consulta, 
                 self.hora_consulta, self.status, self.motivo, self.observacoes, self.id)
        
        db = Database()
        db.executar_query(query, params)
        return True
    
    @classmethod
    def buscar_por_id(cls, id):
        """Busca uma consulta por ID"""
        query = """
        SELECT c.*, p.nome as paciente_nome, m.nome as medico_nome, m.especialidade
        FROM consultas c
        LEFT JOIN pacientes p ON c.id_paciente = p.id
        LEFT JOIN medicos m ON c.id_medico = m.id
        WHERE c.id = ?
        """
        db = Database()
        result = db.executar_query(query, (id,), fetch_one=True)
        
        if result:
            return cls(**result)
        return None
    
    @classmethod
    def buscar_por_paciente(cls, id_paciente):
        """Busca consultas por ID do paciente"""
        db = Database()
        resultados = db.executar_query(
            "SELECT * FROM consultas WHERE id_paciente = ? ORDER BY data_consulta, hora_consulta",
            (id_paciente,),
            fetch_all=True
        )
        
        consultas = []
        for resultado in resultados:
            consulta = cls(
                id=resultado['id'],
                id_paciente=resultado['id_paciente'],
                id_medico=resultado['id_medico'],
                data_consulta=resultado['data_consulta'],
                hora_consulta=resultado['hora_consulta'],
                motivo=resultado['motivo'],
                status=resultado['status']
            )
            consultas.append(consulta)
        
        return consultas
    
    @classmethod
    def buscar_por_medico(cls, id_medico):
        """Busca todas as consultas de um médico"""
        query = """
        SELECT c.*, p.nome as paciente_nome, m.nome as medico_nome, m.especialidade
        FROM consultas c
        LEFT JOIN pacientes p ON c.id_paciente = p.id
        LEFT JOIN medicos m ON c.id_medico = m.id
        WHERE c.id_medico = ?
        ORDER BY c.data_consulta, c.hora_consulta
        """
        db = Database()
        results = db.executar_query(query, (id_medico,), fetch_all=True)
        
        consultas = []
        for result in results:
            consultas.append(cls(**result))
        return consultas
    
    @classmethod
    def buscar_por_medico_e_data(cls, id_medico, data_consulta):
        """Busca consultas de um médico em uma data específica"""
        query = """
        SELECT c.*, p.nome as paciente_nome, m.nome as medico_nome, m.especialidade
        FROM consultas c
        LEFT JOIN pacientes p ON c.id_paciente = p.id
        LEFT JOIN medicos m ON c.id_medico = m.id
        WHERE c.id_medico = ? AND c.data_consulta = ?
        ORDER BY c.hora_consulta
        """
        db = Database()
        results = db.executar_query(query, (id_medico, data_consulta), fetch_all=True)
        
        consultas = []
        for result in results:
            consultas.append(cls(**result))
        return consultas
    
    @classmethod
    def buscar_por_status(cls, status):
        """Busca consultas por status"""
        query = """
        SELECT c.*, p.nome as paciente_nome, m.nome as medico_nome, m.especialidade
        FROM consultas c
        LEFT JOIN pacientes p ON c.id_paciente = p.id
        LEFT JOIN medicos m ON c.id_medico = m.id
        WHERE c.status = ?
        ORDER BY c.data_consulta, c.hora_consulta
        """
        db = Database()
        results = db.executar_query(query, (status,), fetch_all=True)
        
        consultas = []
        for result in results:
            consultas.append(cls(**result))
        return consultas
    
    @classmethod
    def buscar_proximas_por_paciente(cls, id_paciente, limite=10):
        """Busca as próximas consultas de um paciente"""
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
        db = Database()
        results = db.executar_query(query, (id_paciente, limite), fetch_all=True)
        
        consultas = []
        for result in results:
            consultas.append(cls(**result))
        return consultas
    
    @classmethod
    def buscar_todas(cls):
        """Busca todas as consultas"""
        query = """
        SELECT c.*, p.nome as paciente_nome, m.nome as medico_nome, m.especialidade
        FROM consultas c
        LEFT JOIN pacientes p ON c.id_paciente = p.id
        LEFT JOIN medicos m ON c.id_medico = m.id
        ORDER BY c.data_consulta DESC, c.hora_consulta DESC
        """
        db = Database()
        results = db.executar_query(query, fetch_all=True)
        
        consultas = []
        for result in results:
            consultas.append(cls(**result))
        return consultas
    
    def atualizar_status(self, novo_status, observacoes=None):
        """Atualiza o status da consulta"""
        self.status = novo_status
        if observacoes:
            self.observacoes = f"{self.observacoes or ''}\n{observacoes}"
        return self.salvar()
    
    def confirmar(self):
        """Confirma uma consulta"""
        return self.atualizar_status('confirmada')
    
    def cancelar(self, motivo="Cancelado pelo paciente"):
        """Cancela a consulta"""
        self.status = 'cancelada'
        self.motivo_cancelamento = motivo
        return self.salvar()
    
    def finalizar(self, observacoes_medicas=None):
        """Finaliza uma consulta"""
        observacoes = f"Finalizada: {observacoes_medicas}" if observacoes_medicas else "Consulta finalizada"
        return self.atualizar_status('realizada', observacoes)
    
    def remarcar(self, nova_data, nova_hora):
        """Remarca uma consulta"""
        self.data_consulta = nova_data
        self.hora_consulta = nova_hora
        return self.atualizar_status('remarcada', f"Remarcada para: {nova_data} {nova_hora}")
    
    @classmethod
    def verificar_conflito_horario(cls, id_medico, data_consulta, hora_consulta, exclude_id=None):
        """Verifica se há conflito de horário para o médico"""
        query = """
        SELECT COUNT(*) as count FROM consultas 
        WHERE id_medico = ? AND data_consulta = ? AND hora_consulta = ? 
        AND status IN ('agendada', 'confirmada')
        """
        params = (id_medico, data_consulta, hora_consulta)
        
        if exclude_id:
            query += " AND id != ?"
            params = params + (exclude_id,)
        
        db = Database()
        result = db.executar_query(query, params, fetch_one=True)
        return result['count'] > 0 if result else False
    
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