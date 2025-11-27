from models.usuario import Usuario
from database.database import Database

class Paciente(Usuario):
    def __init__(self, id=None, nome=None, email=None, telefone=None, data_nascimento=None, 
                 endereco=None, senha=None, ativo=True, data_criacao=None):
        super().__init__(id, nome, email, telefone, senha, ativo, data_criacao)
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.tipo = 'paciente'
    
    def salvar(self):
        """Salva o paciente no banco (CREATE/UPDATE)"""
        db = Database()
        if self.id is None:
            # Novo paciente (CREATE)
            query = """
            INSERT INTO pacientes (nome, email, telefone, data_nascimento, endereco, senha)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            params = (self.nome, self.email, self.telefone, self.data_nascimento, 
                     self.endereco, self.senha)
            self.id = db.execute_query(query, params)
            return self.id is not None
        else:
            # Atualizar paciente (UPDATE)
            query = """
            UPDATE pacientes 
            SET nome=?, email=?, telefone=?, data_nascimento=?, endereco=?, senha=?, ativo=?
            WHERE id=?
            """
            params = (self.nome, self.email, self.telefone, self.data_nascimento,
                     self.endereco, self.senha, self.ativo, self.id)
            return db.execute_query(query, params)
    
    def autenticar(self, email, senha):
        """Autentica o paciente com base no email e senha"""
        return super().autenticar_sistema(email, senha, self.tipo)

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
    
    # O método 'excluir' (desativar) é herdado da classe Usuario
    # def excluir(self):
    #     return self.desativar()