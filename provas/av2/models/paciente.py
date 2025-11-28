# models/paciente.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.usuario import Usuario
from database import Database

class Paciente(Usuario):
    def __init__(self, id=None, nome=None, email=None, telefone=None, senha=None, 
                 ativo=True, data_criacao=None, data_nascimento=None, endereco=None):
        super().__init__(id, nome, email, telefone, senha, ativo, data_criacao, 'paciente')
        self.data_nascimento = data_nascimento
        self.endereco = endereco

    def salvar(self):
        """Salva o paciente no banco de dados"""
        db = Database()
        if self.id is None:
            # Inserir novo paciente
            query = """
                INSERT INTO pacientes (nome, email, telefone, senha, data_nascimento, endereco, ativo)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            params = (self.nome, self.email, self.telefone, self.senha, 
                     self.data_nascimento, self.endereco, self.ativo)
            result = db.executar_query(query, params, retornar_id=True)
            if result:
                self.id = result
                return True
            return False
        else:
            # Atualizar paciente existente
            query = """
                UPDATE pacientes 
                SET nome=?, email=?, telefone=?, senha=?, data_nascimento=?, endereco=?, ativo=?
                WHERE id=?
            """
            params = (self.nome, self.email, self.telefone, self.senha, 
                     self.data_nascimento, self.endereco, self.ativo, self.id)
            return db.executar_query(query, params)

    def autenticar(self, identificador, senha):
        """Autentica o paciente por email e senha"""
        # Para pacientes, o identificador é o email
        return self.email == identificador and self.senha == senha

    def ativar(self):
        """Ativa o paciente"""
        self.ativo = True
        if self.id is not None:
            db = Database()
            query = "UPDATE pacientes SET ativo = 1 WHERE id = ?"
            return db.executar_query(query, (self.id,))
        return False

    def inativar(self):
        """Inativa o paciente"""
        self.ativo = False
        if self.id is not None:
            db = Database()
            query = "UPDATE pacientes SET ativo = 0 WHERE id = ?"
            return db.executar_query(query, (self.id,))
        return False

    @classmethod
    def buscar_por_email(cls, email):
        """Busca um paciente pelo email"""
        db = Database()
        resultado = db.executar_query(
            "SELECT * FROM pacientes WHERE email = ? AND ativo = 1",
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
                data_nascimento=resultado['data_nascimento'],
                endereco=resultado['endereco']
            )
        return None

    @classmethod
    def criar_tabela(cls):
        """Cria a tabela de pacientes no banco de dados"""
        db = Database()
        tabela_sql = """
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                telefone TEXT,
                data_nascimento TEXT,
                endereco TEXT,
                senha TEXT NOT NULL,
                ativo BOOLEAN DEFAULT 1,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        return db.executar_query(tabela_sql)

    def to_dict(self):
        """Converte o objeto para dicionário, incluindo campos específicos do paciente"""
        data = super().to_dict()
        data.update({
            'data_nascimento': self.data_nascimento,
            'endereco': self.endereco
        })
        return data