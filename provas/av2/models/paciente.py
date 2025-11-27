from database.database import Database

class Paciente:
    def __init__(self, id=None, nome=None, email=None, telefone=None, data_nascimento=None, 
                 endereco=None, senha=None, ativo=True, data_criacao=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.senha = senha
        self.ativo = ativo
        self.data_criacao = data_criacao
    
    def salvar(self):
        """Salva o paciente no banco (CREATE)"""
        db = Database()
        if self.id is None:
            query = """
            INSERT INTO pacientes (nome, email, telefone, data_nascimento, endereco, senha)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            params = (self.nome, self.email, self.telefone, self.data_nascimento, 
                     self.endereco, self.senha)
            return db.execute_query(query, params)
        else:
            query = """
            UPDATE pacientes 
            SET nome=?, email=?, telefone=?, data_nascimento=?, endereco=?, senha=?, ativo=?
            WHERE id=?
            """
            params = (self.nome, self.email, self.telefone, self.data_nascimento,
                     self.endereco, self.senha, self.ativo, self.id)
            return db.execute_query(query, params)
    
    @staticmethod
    def buscar_por_id(id):
        """Busca paciente por ID (READ)"""
        db = Database()
        query = "SELECT * FROM pacientes WHERE id = ?"
        result = db.fetch_one(query, (id,))
        if result:
            return Paciente(**result)
        return None
    
    @staticmethod
    def buscar_por_email(email):
        """Busca paciente por email"""
        db = Database()
        query = "SELECT * FROM pacientes WHERE email = ?"
        result = db.fetch_one(query, (email,))
        if result:
            return Paciente(**result)
        return None
    
    @staticmethod
    def listar_todos():
        """Lista todos os pacientes (READ)"""
        db = Database()
        query = "SELECT * FROM pacientes WHERE ativo = 1 ORDER BY nome"
        results = db.fetch_all(query)
        pacientes = []
        for result in results:
            pacientes.append(Paciente(**result))
        return pacientes
    
    def excluir(self):
        """Exclui o paciente (DELETE) - exclusão lógica"""
        db = Database()
        query = "UPDATE pacientes SET ativo = 0 WHERE id = ?"
        return db.execute_query(query, (self.id,))