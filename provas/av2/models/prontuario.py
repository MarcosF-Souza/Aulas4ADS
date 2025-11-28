from database.database import Database

class Prontuario:
    def __init__(self, id=None, id_paciente=None, id_medico=None, id_consulta=None, 
                 diagnostico=None, prescricao=None, exames=None, observacoes=None, 
                 data_criacao=None, paciente_nome=None, medico_nome=None, especialidade=None):
        self.id = id
        self.id_paciente = id_paciente
        self.id_medico = id_medico
        self.id_consulta = id_consulta
        self.diagnostico = diagnostico
        self.prescricao = prescricao
        self.exames = exames
        self.observacoes = observacoes
        self.data_criacao = data_criacao
        # Campos para join
        self.paciente_nome = paciente_nome
        self.medico_nome = medico_nome
        self.especialidade = especialidade
    
    def salvar(self):
        """Salva ou atualiza o prontuário"""
        if self.id is None:
            return self._criar()
        else:
            return self._atualizar()
    
    def _criar(self):
        """Cria um novo prontuário"""
        query = """
        INSERT INTO prontuarios (id_paciente, id_medico, id_consulta, diagnostico, prescricao, exames, observacoes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (self.id_paciente, self.id_medico, self.id_consulta, self.diagnostico, 
                 self.prescricao, self.exames, self.observacoes)
        
        db = Database()
        self.id = db.executar_query(query, params, retornar_id=True)
        return self.id
    
    def _atualizar(self):
        """Atualiza um prontuário existente"""
        query = """
        UPDATE prontuarios 
        SET id_paciente=?, id_medico=?, id_consulta=?, diagnostico=?, prescricao=?, exames=?, observacoes=?
        WHERE id=?
        """
        params = (self.id_paciente, self.id_medico, self.id_consulta, self.diagnostico, 
                 self.prescricao, self.exames, self.observacoes, self.id)
        
        db = Database()
        db.executar_query(query, params)
        return True
    
    @classmethod
    def buscar_por_id(cls, id):
        """Busca um prontuário por ID"""
        query = """
        SELECT p.*, pac.nome as paciente_nome, med.nome as medico_nome, med.especialidade
        FROM prontuarios p
        LEFT JOIN pacientes pac ON p.id_paciente = pac.id
        LEFT JOIN medicos med ON p.id_medico = med.id
        WHERE p.id = ?
        """
        db = Database()
        result = db.executar_query(query, (id,), fetch_one=True)
        
        if result:
            return cls(**result)
        return None
    
    @classmethod
    def buscar_por_consulta(cls, id_consulta):
        """Busca um prontuário por consulta"""
        query = """
        SELECT p.*, pac.nome as paciente_nome, med.nome as medico_nome, med.especialidade
        FROM prontuarios p
        LEFT JOIN pacientes pac ON p.id_paciente = pac.id
        LEFT JOIN medicos med ON p.id_medico = med.id
        WHERE p.id_consulta = ?
        """
        db = Database()
        result = db.executar_query(query, (id_consulta,), fetch_one=True)
        
        if result:
            return cls(**result)
        return None
    
    @classmethod
    def buscar_por_paciente(cls, id_paciente):
        """Busca todos os prontuários de um paciente"""
        query = """
        SELECT p.*, pac.nome as paciente_nome, med.nome as medico_nome, med.especialidade
        FROM prontuarios p
        LEFT JOIN pacientes pac ON p.id_paciente = pac.id
        LEFT JOIN medicos med ON p.id_medico = med.id
        WHERE p.id_paciente = ?
        ORDER BY p.data_criacao DESC
        """
        db = Database()
        results = db.executar_query(query, (id_paciente,), fetch_all=True)
        
        prontuarios = []
        for result in results:
            prontuarios.append(cls(**result))
        return prontuarios
    
    @classmethod
    def buscar_por_medico(cls, id_medico):
        """Busca todos os prontuários preenchidos por um médico"""
        query = """
        SELECT p.*, pac.nome as paciente_nome, med.nome as medico_nome, med.especialidade
        FROM prontuarios p
        LEFT JOIN pacientes pac ON p.id_paciente = pac.id
        LEFT JOIN medicos med ON p.id_medico = med.id
        WHERE p.id_medico = ?
        ORDER BY p.data_criacao DESC
        """
        db = Database()
        results = db.executar_query(query, (id_medico,), fetch_all=True)
        
        prontuarios = []
        for result in results:
            prontuarios.append(cls(**result))
        return prontuarios
    
    @classmethod
    def buscar_todos(cls):
        """Busca todos os prontuários"""
        query = """
        SELECT p.*, pac.nome as paciente_nome, med.nome as medico_nome, med.especialidade
        FROM prontuarios p
        LEFT JOIN pacientes pac ON p.id_paciente = pac.id
        LEFT JOIN medicos med ON p.id_medico = med.id
        ORDER BY p.data_criacao DESC
        """
        db = Database()
        results = db.executar_query(query, fetch_all=True)
        
        prontuarios = []
        for result in results:
            prontuarios.append(cls(**result))
        return prontuarios
    
    @classmethod
    def buscar_por_periodo(cls, data_inicio, data_fim):
        """Busca prontuários por período de criação"""
        query = """
        SELECT p.*, pac.nome as paciente_nome, med.nome as medico_nome, med.especialidade
        FROM prontuarios p
        LEFT JOIN pacientes pac ON p.id_paciente = pac.id
        LEFT JOIN medicos med ON p.id_medico = med.id
        WHERE p.data_criacao BETWEEN ? AND ?
        ORDER BY p.data_criacao DESC
        """
        db = Database()
        results = db.executar_query(query, (data_inicio, data_fim), fetch_all=True)
        
        prontuarios = []
        for result in results:
            prontuarios.append(cls(**result))
        return prontuarios
    
    def excluir(self):
        """Exclui um prontuário"""
        query = "DELETE FROM prontuarios WHERE id = ?"
        db = Database()
        db.executar_query(query, (self.id,))
        return True
    
    def atualizar_dados_medicos(self, diagnostico=None, prescricao=None, exames=None, observacoes=None):
        """Atualiza os dados médicos do prontuário"""
        if diagnostico is not None:
            self.diagnostico = diagnostico
        if prescricao is not None:
            self.prescricao = prescricao
        if exames is not None:
            self.exames = exames
        if observacoes is not None:
            self.observacoes = observacoes
        
        return self.salvar()
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'id_paciente': self.id_paciente,
            'id_medico': self.id_medico,
            'id_consulta': self.id_consulta,
            'diagnostico': self.diagnostico,
            'prescricao': self.prescricao,
            'exames': self.exames,
            'observacoes': self.observacoes,
            'data_criacao': self.data_criacao,
            'paciente_nome': self.paciente_nome,
            'medico_nome': self.medico_nome,
            'especialidade': self.especialidade
        }