from database.database import Database

class Medico:
    def __init__(self, id=None, nome=None, crm=None, especialidade=None, telefone=None, 
                 email=None, senha=None, ativo=True, data_criacao=None):
        self.id = id
        self.nome = nome
        self.crm = crm
        self.especialidade = especialidade
        self.telefone = telefone
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.data_criacao = data_criacao
    
    def salvar(self):
        """Salva o médico no banco (CREATE)"""
        db = Database()
        if self.id is None:
            query = """
            INSERT INTO medicos (nome, crm, especialidade, telefone, email, senha)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            params = (self.nome, self.crm, self.especialidade, self.telefone, self.email, self.senha)
            return db.execute_query(query, params)
        else:
            query = """
            UPDATE medicos 
            SET nome=?, crm=?, especialidade=?, telefone=?, email=?, senha=?, ativo=?
            WHERE id=?
            """
            params = (self.nome, self.crm, self.especialidade, self.telefone, 
                     self.email, self.senha, self.ativo, self.id)
            return db.execute_query(query, params)
    
    @staticmethod
    def buscar_por_crm(crm):
        """Busca médico por CRM (READ)"""
        db = Database()
        query = "SELECT * FROM medicos WHERE crm = ?"
        result = db.fetch_one(query, (crm,))
        if result:
            return Medico(**result)
        return None
    
    @staticmethod
    def listar_todos():
        """Lista todos os médicos (READ)"""
        db = Database()
        query = "SELECT * FROM medicos WHERE ativo = 1 ORDER BY nome"
        results = db.fetch_all(query)
        medicos = []
        for result in results:
            medicos.append(Medico(**result))
        return medicos