from models.usuario import Usuario
from database.database import Database

class Medico(Usuario):
    def __init__(self, id=None, nome=None, crm=None, especialidade=None, telefone=None, 
                 email=None, senha=None, ativo=True, data_criacao=None):
        super().__init__(id, nome, email, telefone, senha, ativo, data_criacao)
        self.crm = crm
        self.especialidade = especialidade
        self.tipo = 'medico'

    def salvar(self):
        """Salva o médico no banco (CREATE/UPDATE)"""
        db = Database()
        if self.id is None:
            # Novo médico (CREATE)
            query = """
            INSERT INTO medicos (nome, crm, especialidade, telefone, email, senha)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            params = (self.nome, self.crm, self.especialidade, self.telefone, self.email, self.senha)
            self.id = db.execute_query(query, params)
            return self.id is not None
        else:
            # Atualizar médico (UPDATE)
            query = """
            UPDATE medicos 
            SET nome=?, crm=?, especialidade=?, telefone=?, email=?, senha=?, ativo=?
            WHERE id=?
            """
            params = (self.nome, self.crm, self.especialidade, self.telefone, 
                     self.email, self.senha, self.ativo, self.id)
            return db.execute_query(query, params)

    def autenticar(self, crm, senha):
        """Autentica o médico com base no CRM e senha"""
        return super().autenticar_sistema(crm, senha, self.tipo)

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
    def buscar_por_id(id):
        """Busca médico por ID (READ)"""
        db = Database()
        query = "SELECT * FROM medicos WHERE id = ?"
        result = db.fetch_one(query, (id,))
        if result:
            return Medico(**result)
        return None

    @staticmethod
    def buscar_por_nome(nome):
        """Busca médico por nome (READ)"""
        db = Database()
        query = "SELECT * FROM medicos WHERE nome = ?"
        result = db.fetch_one(query, (nome,))
        if result:
            return Medico(**result)
        return None