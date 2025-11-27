from database.database import Database
from abc import ABC, abstractmethod

class Usuario(ABC):
    """Classe abstrata base para todos os tipos de usuários do sistema"""
    
    def __init__(self, id=None, nome=None, email=None, telefone=None, senha=None, ativo=True, data_criacao=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.senha = senha
        self.ativo = ativo
        self.data_criacao = data_criacao
    
    @abstractmethod
    def salvar(self):
        """Método abstrato para salvar usuário (deve ser implementado pelas subclasses)"""
        pass
    
    @abstractmethod
    def autenticar(self, identificador, senha):
        """Método abstrato para autenticação (deve ser implementado pelas subclasses)"""
        pass
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'ativo': self.ativo,
            'data_criacao': self.data_criacao
        }
    
    def desativar(self):
        """Desativa o usuário (exclusão lógica)"""
        db = Database()
        # Esta é uma implementação genérica, as subclasses podem sobrescrever
        if hasattr(self, 'tipo'):
            if self.tipo == 'paciente':
                query = "UPDATE pacientes SET ativo = 0 WHERE id = ?"
            elif self.tipo == 'medico':
                query = "UPDATE medicos SET ativo = 0 WHERE id = ?"
            elif self.tipo == 'administrador':
                query = "UPDATE administradores SET ativo = 0 WHERE id = ?"
            else:
                return False
        else:
            return False
        
        return db.execute_query(query, (self.id,))
    
    def ativar(self):
        """Ativa o usuário"""
        db = Database()
        if hasattr(self, 'tipo'):
            if self.tipo == 'paciente':
                query = "UPDATE pacientes SET ativo = 1 WHERE id = ?"
            elif self.tipo == 'medico':
                query = "UPDATE medicos SET ativo = 1 WHERE id = ?"
            elif self.tipo == 'administrador':
                query = "UPDATE administradores SET ativo = 1 WHERE id = ?"
            else:
                return False
        else:
            return False
        
        return db.execute_query(query, (self.id,))
    
    @staticmethod
    def buscar_por_email(email):
        """Busca qualquer tipo de usuário por email"""
        db = Database()
        
        # Buscar em pacientes
        query_paciente = "SELECT *, 'paciente' as tipo FROM pacientes WHERE email = ?"
        paciente = db.fetch_one(query_paciente, (email,))
        if paciente:
            return paciente
        
        # Buscar em médicos
        query_medico = "SELECT *, 'medico' as tipo FROM medicos WHERE email = ?"
        medico = db.fetch_one(query_medico, (email,))
        if medico:
            return medico
        
        return None
    
    @staticmethod
    def autenticar_sistema(identificador, senha, tipo_usuario):
        """
        Autentica um usuário no sistema baseado no tipo
        Retorna o usuário autenticado ou None
        """
        db = Database()
        
        if tipo_usuario == 'paciente':
            query = "SELECT *, 'paciente' as tipo FROM pacientes WHERE email = ? AND senha = ? AND ativo = 1"
            usuario = db.fetch_one(query, (identificador, senha))
        
        elif tipo_usuario == 'medico':
            query = "SELECT *, 'medico' as tipo FROM medicos WHERE crm = ? AND senha = ? AND ativo = 1"
            usuario = db.fetch_one(query, (identificador, senha))
        
        elif tipo_usuario == 'administrador':
            query = "SELECT *, 'administrador' as tipo FROM administradores WHERE usuario = ? AND senha = ?"
            usuario = db.fetch_one(query, (identificador, senha))
        
        else:
            return None
        
        return usuario
    
    @staticmethod
    def contar_usuarios_ativos():
        """Retorna estatísticas de usuários ativos no sistema"""
        db = Database()
        
        pacientes_ativos = db.fetch_one("SELECT COUNT(*) as total FROM pacientes WHERE ativo = 1")['total']
        medicos_ativos = db.fetch_one("SELECT COUNT(*) as total FROM medicos WHERE ativo = 1")['total']
        administradores_ativos = db.fetch_one("SELECT COUNT(*) as total FROM administradores")['total']
        
        return {
            'pacientes': pacientes_ativos,
            'medicos': medicos_ativos,
            'administradores': administradores_ativos,
            'total': pacientes_ativos + medicos_ativos + administradores_ativos
        }