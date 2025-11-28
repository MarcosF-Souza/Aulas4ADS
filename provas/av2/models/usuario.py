from database.database import Database
from abc import ABC, abstractmethod

class Usuario(ABC):
    """Classe abstrata base para todos os tipos de usuários do sistema"""
    
    def __init__(self, id=None, nome=None, email=None, telefone=None, senha=None, 
                 ativo=True, data_criacao=None, tipo_usuario=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.senha = senha
        self.ativo = ativo
        self.data_criacao = data_criacao
        self.tipo_usuario = tipo_usuario
    
    @abstractmethod
    def salvar(self):
        """Método abstrato para salvar usuário"""
        pass
    
    @abstractmethod
    def autenticar(self, identificador, senha):
        """Método abstrato para autenticação"""
        pass
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'ativo': self.ativo,
            'data_criacao': self.data_criacao,
            'tipo_usuario': self.tipo_usuario
        }
    
    @abstractmethod
    def ativar(self):
        """Ativa o usuário"""
        pass
    
    @abstractmethod
    def inativar(self):
        """Inativa o usuário"""
        pass
    
    @classmethod
    def criar_tabelas(cls):
        """Cria as tabelas de usuários no banco de dados"""
        from models.paciente import Paciente
        from models.medico import Medico
        from models.administrador import Administrador
        
        Paciente.criar_tabela()
        Medico.criar_tabela()
        Administrador.criar_tabela()
    
    @classmethod
    def buscar_por_credenciais(cls, identificador, senha, tipo_usuario):
        """Busca usuário por credenciais de autenticação"""
        db = Database()
        
        if tipo_usuario == 'paciente':
            query = "SELECT * FROM pacientes WHERE email = ? AND senha = ? AND ativo = 1"
            result = db.executar_query(query, (identificador, senha), fetch_one=True)
            if result:
                from models.paciente import Paciente
                return Paciente(**result)
        
        elif tipo_usuario == 'medico':
            query = "SELECT * FROM medicos WHERE email = ? AND senha = ? AND ativo = 1"
            result = db.executar_query(query, (identificador, senha), fetch_one=True)
            if result:
                from models.medico import Medico
                return Medico(**result)
        
        elif tipo_usuario == 'admin':
            query = "SELECT * FROM administradores WHERE email = ? AND senha_hash = ? AND status = 'ativo'"
            # Note: Para admin, precisaríamos verificar o hash da senha
            result = db.executar_query(query, (identificador, senha), fetch_one=True)
            if result:
                from models.administrador import Administrador
                return Administrador(**result)
        
        return None
    
    @classmethod
    def verificar_email_existente(cls, email, tipo_usuario, exclude_id=None):
        """Verifica se o email já existe para um tipo de usuário"""
        db = Database()
        
        if tipo_usuario == 'paciente':
            if exclude_id:
                query = "SELECT id FROM pacientes WHERE email = ? AND id != ?"
                params = (email, exclude_id)
            else:
                query = "SELECT id FROM pacientes WHERE email = ?"
                params = (email,)
        
        elif tipo_usuario == 'medico':
            if exclude_id:
                query = "SELECT id FROM medicos WHERE email = ? AND id != ?"
                params = (email, exclude_id)
            else:
                query = "SELECT id FROM medicos WHERE email = ?"
                params = (email,)
        
        elif tipo_usuario == 'admin':
            if exclude_id:
                query = "SELECT id FROM administradores WHERE email = ? AND id != ?"
                params = (email, exclude_id)
            else:
                query = "SELECT id FROM administradores WHERE email = ?"
                params = (email,)
        
        else:
            return False
        
        result = db.executar_query(query, params, fetch_one=True)
        return result is not None
    
    @classmethod
    def obter_estatisticas_usuarios(cls):
        """Obtém estatísticas de usuários do sistema"""
        db = Database()
        
        query_pacientes = "SELECT COUNT(*) as total FROM pacientes WHERE ativo = 1"
        query_medicos = "SELECT COUNT(*) as total FROM medicos WHERE ativo = 1"
        query_admins = "SELECT COUNT(*) as total FROM administradores WHERE status = 'ativo'"
        
        pacientes = db.executar_query(query_pacientes, fetch_one=True)
        medicos = db.executar_query(query_medicos, fetch_one=True)
        admins = db.executar_query(query_admins, fetch_one=True)
        
        return {
            'pacientes': pacientes['total'] if pacientes else 0,
            'medicos': medicos['total'] if medicos else 0,
            'administradores': admins['total'] if admins else 0,
            'total': (pacientes['total'] if pacientes else 0) + 
                    (medicos['total'] if medicos else 0) + 
                    (admins['total'] if admins else 0)
        }