# models/administrador.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.usuario import Usuario
from database import Database
import hashlib

class Administrador(Usuario):
    def __init__(self, id=None, nome=None, email=None, telefone=None, senha=None, 
                 data_cadastro=None, cargo=None, nivel_acesso=None, status=None):
        super().__init__(id, nome, email, telefone, senha, True, data_cadastro, 'admin')
        self.cargo = cargo
        self.nivel_acesso = nivel_acesso
        self.status = status

    def _hash_senha(self, senha):
        """Gera hash da senha"""
        return hashlib.sha256(senha.encode()).hexdigest()

    def salvar(self):
        """Salva o administrador no banco de dados"""
        db = Database()
        senha_hash = self._hash_senha(self.senha) if self.senha else None
        
        if self.id is None:
            # Inserir novo administrador
            query = """
                INSERT INTO administradores (nome, email, senha_hash, telefone, cargo, nivel_acesso, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            params = (self.nome, self.email, senha_hash, self.telefone, 
                     self.cargo, self.nivel_acesso, self.status or 'ativo')
            result = db.executar_query(query, params, retornar_id=True)
            if result:
                self.id = result
                return True
            return False
        else:
            # Atualizar administrador existente
            query = """
                UPDATE administradores 
                SET nome=?, email=?, telefone=?, cargo=?, nivel_acesso=?, status=?
                WHERE id=?
            """
            params = (self.nome, self.email, self.telefone, self.cargo, 
                     self.nivel_acesso, self.status, self.id)
            return db.executar_query(query, params)

    def autenticar(self, identificador, senha):
        """Autentica o administrador por email e senha (com hash)"""
        if self.email != identificador:
            return False
        
        # Verificar senha com hash
        senha_hash = self._hash_senha(senha)
        db = Database()
        resultado = db.executar_query(
            "SELECT * FROM administradores WHERE email = ? AND senha_hash = ? AND status = 'ativo'",
            (identificador, senha_hash),
            fetch_one=True
        )
        return resultado is not None

    def ativar(self):
        """Ativa o administrador"""
        self.status = 'ativo'
        if self.id is not None:
            db = Database()
            query = "UPDATE administradores SET status = 'ativo' WHERE id = ?"
            return db.executar_query(query, (self.id,))
        return False

    def inativar(self):
        """Inativa o administrador"""
        self.status = 'inativo'
        if self.id is not None:
            db = Database()
            query = "UPDATE administradores SET status = 'inativo' WHERE id = ?"
            return db.executar_query(query, (self.id,))
        return False

    @classmethod
    def buscar_por_email(cls, email):
        """Busca um administrador pelo email"""
        db = Database()
        resultado = db.executar_query(
            "SELECT * FROM administradores WHERE email = ? AND status = 'ativo'",
            (email,),
            fetch_one=True
        )
        if resultado:
            return cls(
                id=resultado['id'],
                nome=resultado['nome'],
                email=resultado['email'],
                telefone=resultado['telefone'],
                senha='',  # Não retornamos a senha por segurança
                data_cadastro=resultado['data_cadastro'],
                cargo=resultado['cargo'],
                nivel_acesso=resultado['nivel_acesso'],
                status=resultado['status']
            )
        return None

    @classmethod
    def criar_tabela(cls):
        """Cria a tabela de administradores no banco de dados"""
        db = Database()
        tabela_sql = """
            CREATE TABLE IF NOT EXISTS administradores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha_hash TEXT NOT NULL,
                telefone TEXT,
                cargo TEXT DEFAULT 'Administrador',
                nivel_acesso TEXT DEFAULT 'total',
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'ativo'
            )
        """
        return db.executar_query(tabela_sql)

    def to_dict(self):
        """Converte o objeto para dicionário, incluindo campos específicos do administrador"""
        data = super().to_dict()
        data.update({
            'cargo': self.cargo,
            'nivel_acesso': self.nivel_acesso,
            'status': self.status
        })
        return data