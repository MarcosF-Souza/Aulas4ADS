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
        # Campos para join (não existem na tabela, mas são úteis para exibição)
        self.paciente_nome = paciente_nome
        self.medico_nome = medico_nome
        self.especialidade = especialidade
    
    def salvar(self):
        """Salva ou atualiza um prontuário (CREATE/UPDATE)"""
        db = Database()
        if self.id is None:
            # Novo prontuário
            query = """
            INSERT INTO prontuarios (id_paciente, id_medico, id_consulta, diagnostico, prescricao, exames, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            params = (self.id_paciente, self.id_medico, self.id_consulta, self.diagnostico, 
                     self.prescricao, self.exames, self.observacoes)
            return db.execute_query(query, params)
        else:
            # Atualizar prontuário existente
            query = """
            UPDATE prontuarios 
            SET id_paciente=?, id_medico=?, id_consulta=?, diagnostico=?, prescricao=?, exames=?, observacoes=?
            WHERE id=?
            """
            params = (self.id_paciente, self.id_medico, self.id_consulta, self.diagnostico, 
                     self.prescricao, self.exames, self.observacoes, self.id)
            return db.execute_query(query, params)
    
    @staticmethod
    def buscar_por_id(id):
        """Busca um prontuário por ID (READ)"""
        db = Database()
        query = """
        SELECT p.*, pac.nome as paciente_nome, med.nome as medico_nome, med.especialidade
        FROM prontuarios p
        LEFT JOIN pacientes pac ON p.id_paciente = pac.id
        LEFT JOIN medicos med ON p.id_medico = med.id
        WHERE p.id = ?
        """
        result = db.fetch_one(query, (id,))
        if result:
            return Prontuario(**result)
        return None
    
    @staticmethod
    def buscar_por_paciente(id_paciente):
        """Busca todos os prontuários de um paciente"""
        db = Database()
        query = """
        SELECT p.*, pac.nome as paciente_nome, med.nome as medico_nome, med.especialidade
        FROM prontuarios p
        LEFT JOIN pacientes pac ON p.id_paciente = pac.id
        LEFT JOIN medicos med ON p.id_medico = med.id
        WHERE p.id_paciente = ?
        ORDER BY p.data_criacao DESC
        """
        results = db.fetch_all(query, (id_paciente,))
        prontuarios = []
        for result in results:
            prontuarios.append(Prontuario(**result))
        return prontuarios
    
    @staticmethod
    def buscar_por_medico(id_medico):
        """Busca todos os prontuários preenchidos por um médico"""
        db = Database()
        query = """
        SELECT p.*, pac.nome as paciente_nome, med.nome as medico_nome, med.especialidade
        FROM prontuarios p
        LEFT JOIN pacientes pac ON p.id_paciente = pac.id
        LEFT JOIN medicos med ON p.id_medico = med.id
        WHERE p.id_medico = ?
        ORDER BY p.data_criacao DESC
        """
        results = db.fetch_all(query, (id_medico,))
        prontuarios = []
        for result in results:
            prontuarios.append(Prontuario(**result))
        return prontuarios
    
    @staticmethod
    def buscar_por_consulta(id_consulta):
        """Busca um prontuário por consulta"""
        db = Database()
        query = """
        SELECT p.*, pac.nome as paciente_nome, med.nome as medico_nome, med.especialidade
        FROM prontuarios p
        LEFT JOIN pacientes pac ON p.id_paciente = pac.id
        LEFT JOIN medicos med ON p.id_medico = med.id
        WHERE p.id_consulta = ?
        """
        result = db.fetch_one(query, (id_consulta,))
        if result:
            return Prontuario(**result)
        return None
    
    @staticmethod
    def listar_todos():
        """Lista todos os prontuários (para administrador)"""
        db = Database()
        query = """
        SELECT p.*, pac.nome as paciente_nome, med.nome as medico_nome, med.especialidade
        FROM prontuarios p
        LEFT JOIN pacientes pac ON p.id_paciente = pac.id
        LEFT JOIN medicos med ON p.id_medico = med.id
        ORDER BY p.data_criacao DESC
        """
        results = db.fetch_all(query)
        prontuarios = []
        for result in results:
            prontuarios.append(Prontuario(**result))
        return prontuarios
    
    def excluir(self):
        """Exclui um prontuário (DELETE)"""
        db = Database()
        query = "DELETE FROM prontuarios WHERE id = ?"
        return db.execute_query(query, (self.id,))
    
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