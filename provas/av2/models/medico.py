# models/medico.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.usuario import Usuario
from database import Database

class Medico(Usuario):
    def __init__(self, id=None, nome=None, email=None, telefone=None, senha=None, 
                 ativo=True, data_criacao=None, crm=None, especialidade=None):
        super().__init__(id, nome, email, telefone, senha, ativo, data_criacao, 'medico')
        self.crm = crm
        self.especialidade = especialidade

    def salvar(self):
        """Salva o médico no banco de dados"""
        db = Database()
        if self.id is None:
            # Inserir novo médico
            query = """
                INSERT INTO medicos (nome, email, telefone, senha, crm, especialidade, ativo)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            params = (self.nome, self.email, self.telefone, self.senha, 
                     self.crm, self.especialidade, self.ativo)
            result = db.executar_query(query, params, retornar_id=True)
            if result:
                self.id = result
                return True
            return False
        else:
            # Atualizar médico existente
            query = """
                UPDATE medicos 
                SET nome=?, email=?, telefone=?, senha=?, crm=?, especialidade=?, ativo=?
                WHERE id=?
            """
            params = (self.nome, self.email, self.telefone, self.senha, 
                     self.crm, self.especialidade, self.ativo, self.id)
            return db.executar_query(query, params)

    def autenticar(self, identificador, senha):
        """Autentica o médico por email e senha"""
        return self.email == identificador and self.senha == senha

    def ativar(self):
        """Ativa o médico"""
        self.ativo = True
        if self.id is not None:
            db = Database()
            query = "UPDATE medicos SET ativo = 1 WHERE id = ?"
            return db.executar_query(query, (self.id,))
        return False

    def inativar(self):
        """Inativa o médico"""
        self.ativo = False
        if self.id is not None:
            db = Database()
            query = "UPDATE medicos SET ativo = 0 WHERE id = ?"
            return db.executar_query(query, (self.id,))
        return False

    @classmethod
    def buscar_por_email(cls, email):
        """Busca um médico pelo email"""
        db = Database()
        resultado = db.executar_query(
            "SELECT * FROM medicos WHERE email = ? AND ativo = 1",
            (email,),
            fetch_one=True
        )
        if resultado:
            return cls(
                id=resultado['id'],
                nome=resultado['nome'],
                email=resultado['email'],
                telefone=resultado['telefone'],
                senha=resultado['senha'],
                ativo=resultado['ativo'],
                data_criacao=resultado['data_criacao'],
                crm=resultado['crm'],
                especialidade=resultado['especialidade']
            )
        return None
    
    @classmethod
    def buscar_por_crm(cls, crm):
        """Busca um médico pelo CRM"""
        db = Database()
        resultado = db.executar_query(
            "SELECT * FROM medicos WHERE crm = ? AND ativo = 1",
            (crm,),
            fetch_one=True
        )
        if resultado:
            return cls(
                id=resultado['id'],
                nome=resultado['nome'],
                email=resultado['email'],
                telefone=resultado['telefone'],
                senha=resultado['senha'],
                ativo=resultado['ativo'],
                data_criacao=resultado['data_criacao'],
                crm=resultado['crm'],
                especialidade=resultado['especialidade']
            )
        return None

    @classmethod
    def criar_tabela(cls):
        """Cria a tabela de médicos no banco de dados"""
        db = Database()
        tabela_sql = """
            CREATE TABLE IF NOT EXISTS medicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                crm TEXT UNIQUE NOT NULL,
                especialidade TEXT NOT NULL,
                telefone TEXT,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                ativo BOOLEAN DEFAULT 1,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        return db.executar_query(tabela_sql)

    def to_dict(self):
        """Converte o objeto para dicionário, incluindo campos específicos do médico"""
        data = super().to_dict()
        data.update({
            'crm': self.crm,
            'especialidade': self.especialidade
        })
        return data