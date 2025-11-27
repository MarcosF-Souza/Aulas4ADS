import sqlite3
import os

class Database:
    def __init__(self, db_name='agendamento_consultas.db'):
        self.db_name = db_name
        self.connection = None
        
    def connect(self):
        """Conecta ao banco de dados SQLite3"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.connection.row_factory = sqlite3.Row
            return self.connection
        except sqlite3.Error as e:
            print(f"❌ Erro ao conectar ao SQLite3: {e}")
            return None
    
    def disconnect(self):
        """Desconecta do banco de dados"""
        if self.connection:
            self.connection.close()
    
    def execute_query(self, query, params=None):
        """Executa uma query (INSERT, UPDATE, DELETE)"""
        conn = self.connect()
        if conn is None:
            return False
        
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"❌ Erro ao executar query: {e}")
            return False
        finally:
            self.disconnect()
    
    def fetch_all(self, query, params=None):
        """Executa uma query SELECT e retorna todos os resultados"""
        conn = self.connect()
        if conn is None:
            return None
        
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            return [dict(row) for row in results]
        except sqlite3.Error as e:
            print(f"❌ Erro ao executar query: {e}")
            return None
        finally:
            self.disconnect()
    
    def fetch_one(self, query, params=None):
        """Executa uma query SELECT e retorna um único resultado"""
        conn = self.connect()
        if conn is None:
            return None
        
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            return dict(result) if result else None
        except sqlite3.Error as e:
            print(f"❌ Erro ao executar query: {e}")
            return None
        finally:
            self.disconnect()

    def create_tables(self):
        """Cria todas as tabelas do sistema"""
        tables = [
            # Tabela de pacientes
            """
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
            """,
            # Tabela de médicos
            """
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
            """,
            # Tabela de administradores (ATUALIZADA com coluna ativo)
            """
            CREATE TABLE IF NOT EXISTS administradores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                nome TEXT NOT NULL,
                ativo BOOLEAN DEFAULT 1,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            # Tabela de agenda médica
            """
            CREATE TABLE IF NOT EXISTS agenda_medica (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_medico INTEGER NOT NULL,
                data_agenda TEXT NOT NULL,
                hora_inicio TEXT NOT NULL,
                hora_fim TEXT NOT NULL,
                disponivel BOOLEAN DEFAULT 1,
                motivo_bloqueio TEXT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_medico) REFERENCES medicos (id),
                UNIQUE(id_medico, data_agenda, hora_inicio)
            )
            """,
            # Tabela de consultas
            """
            CREATE TABLE IF NOT EXISTS consultas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_paciente INTEGER NOT NULL,
                id_medico INTEGER NOT NULL,
                data_consulta TEXT NOT NULL,
                hora_consulta TEXT NOT NULL,
                status TEXT DEFAULT 'agendada',
                motivo TEXT,
                observacoes TEXT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_paciente) REFERENCES pacientes (id),
                FOREIGN KEY (id_medico) REFERENCES medicos (id)
            )
            """,
            # NOVA TABELA: Prontuários
            """
            CREATE TABLE IF NOT EXISTS prontuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_paciente INTEGER NOT NULL,
                id_medico INTEGER NOT NULL,
                id_consulta INTEGER NOT NULL,
                diagnostico TEXT,
                prescricao TEXT,
                exames TEXT,
                observacoes TEXT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_paciente) REFERENCES pacientes (id),
                FOREIGN KEY (id_medico) REFERENCES medicos (id),
                FOREIGN KEY (id_consulta) REFERENCES consultas (id)
            )
            """
        ]
        
        for table_sql in tables:
            if not self.execute_query(table_sql):
                print(f"❌ Erro ao criar tabela")
                return False
        
        print("✅ Todas as tabelas criadas com sucesso!")
        return True
    
    def init_database(self):
        """Inicializa o banco de dados com os usuários específicos"""
        self.create_tables()
        
        # ========== ADMINISTRADOR - JOÃO ==========
        admin_existe = self.fetch_one("SELECT * FROM administradores WHERE usuario = 'joao'")
        if not admin_existe:
            self.execute_query(
                "INSERT INTO administradores (usuario, senha, nome) VALUES (?, ?, ?)",
                ('joao', 'joao123', 'João Silva')
            )
            print("✅ Administrador 'João' criado - usuário: joao, senha: joao123")
        
        # ========== MÉDICA - LETÍCIA ==========
        medica_existe = self.fetch_one("SELECT * FROM medicos WHERE crm = 'CRM-SP-12345'")
        if not medica_existe:
            self.execute_query(
                """INSERT INTO medicos (nome, crm, especialidade, telefone, email, senha) 
                VALUES (?, ?, ?, ?, ?, ?)""",
                ('Dra. Letícia de Paiva', 'CRM-SP-12345', 'Cardiologia', '(11) 98888-7777', 'leticia.paiva@hospital.com', 'leticia123')
            )
            print("✅ Médica 'Letícia' criada - CRM: CRM-SP-12345, senha: leticia123")
            
            # Criar alguns horários na agenda da Dra. Letícia
            medico_id = self.fetch_one("SELECT id FROM medicos WHERE crm = 'CRM-SP-12345'")['id']
            
            # Horários de exemplo para a próxima semana
            horarios = [
                ('2024-12-20', '08:00', '09:00'),
                ('2024-12-20', '09:00', '10:00'),
                ('2024-12-20', '10:00', '11:00'),
                ('2024-12-20', '14:00', '15:00'),
                ('2024-12-20', '15:00', '16:00'),
                ('2024-12-21', '08:00', '09:00'),
                ('2024-12-21', '09:00', '10:00'),
            ]
            
            for data, inicio, fim in horarios:
                self.execute_query(
                    "INSERT INTO agenda_medica (id_medico, data_agenda, hora_inicio, hora_fim) VALUES (?, ?, ?, ?)",
                    (medico_id, data, inicio, fim)
                )
            print("✅ Horários na agenda da Dra. Letícia criados")
        
        # ========== PACIENTE - MARCOS ==========
        paciente_existe = self.fetch_one("SELECT * FROM pacientes WHERE email = 'marcos.silva@email.com'")
        if not paciente_existe:
            self.execute_query(
                """INSERT INTO pacientes (nome, email, telefone, data_nascimento, endereco, senha) 
                VALUES (?, ?, ?, ?, ?, ?)""",
                ('Marcos Ferreira', 'marcos.silva@email.com', '(11) 97777-6666', '15/08/1990', 
                 'Rua das Flores, 123 - São Paulo, SP', 'marcos123')
            )
            print("✅ Paciente 'Marcos' criado - email: marcos.silva@email.com, senha: marcos123")
        
        # ========== CONSULTA DE EXEMPLO ==========
        # Criar uma consulta de exemplo entre Marcos e Dra. Letícia
        consulta_existe = self.fetch_one("""
            SELECT * FROM consultas 
            WHERE id_paciente = (SELECT id FROM pacientes WHERE email = 'marcos.silva@email.com')
            AND id_medico = (SELECT id FROM medicos WHERE crm = 'CRM-SP-12345')
        """)
        
        if not consulta_existe:
            paciente_id = self.fetch_one("SELECT id FROM pacientes WHERE email = 'marcos.silva@email.com'")['id']
            medico_id = self.fetch_one("SELECT id FROM medicos WHERE crm = 'CRM-SP-12345'")['id']
            
            self.execute_query(
                """INSERT INTO consultas (id_paciente, id_medico, data_consulta, hora_consulta, status, motivo) 
                VALUES (?, ?, ?, ?, ?, ?)""",
                (paciente_id, medico_id, '2024-12-20', '09:00', 'agendada', 'Check-up cardiológico anual')
            )
            print("✅ Consulta de exemplo criada entre Marcos e Dra. Letícia")
        
        # ========== PRONTUÁRIO DE EXEMPLO ==========
        # Criar um prontuário de exemplo para a consulta entre Marcos e Dra. Letícia
        prontuario_existe = self.fetch_one("""
            SELECT * FROM prontuarios 
            WHERE id_consulta = (
                SELECT id FROM consultas 
                WHERE id_paciente = (SELECT id FROM pacientes WHERE email = 'marcos.silva@email.com')
                AND id_medico = (SELECT id FROM medicos WHERE crm = 'CRM-SP-12345')
            )
        """)

        if not prontuario_existe:
            consulta_id = self.fetch_one("""
                SELECT id FROM consultas 
                WHERE id_paciente = (SELECT id FROM pacientes WHERE email = 'marcos.silva@email.com')
                AND id_medico = (SELECT id FROM medicos WHERE crm = 'CRM-SP-12345')
            """)['id']
            
            paciente_id = self.fetch_one("SELECT id FROM pacientes WHERE email = 'marcos.silva@email.com'")['id']
            medico_id = self.fetch_one("SELECT id FROM medicos WHERE crm = 'CRM-SP-12345'")['id']
            
            self.execute_query(
                """INSERT INTO prontuarios (id_paciente, id_medico, id_consulta, diagnostico, prescricao, exames, observacoes) 
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (paciente_id, medico_id, consulta_id, 
                 'Paciente com histórico familiar de cardiopatia. Pressão arterial dentro dos limites normais.',
                 'Manter hábitos saudáveis de alimentação e prática regular de exercícios físicos.',
                 'Eletrocardiograma - Normal\nHemograma completo - Dentro dos parâmetros',
                 'Paciente orientado sobre importância do acompanhamento anual.')
            )
            print("✅ Prontuário de exemplo criado para a consulta entre Marcos e Dra. Letícia")
        
        print("\n" + "="*50)
        print("👤 USUÁRIOS CRIADOS PARA TESTE:")
        print("="*50)
        print("Administrador:")
        print("  Usuário: joao")
        print("  Senha: joao123")
        print("  Nome: João Silva")
        print("\nMédica:")
        print("  CRM: CRM-SP-12345")
        print("  Senha: leticia123")
        print("  Nome: Dra. Letícia de Paiva")
        print("  Especialidade: Cardiologia")
        print("\nPaciente:")
        print("  E-mail: marcos.silva@email.com")
        print("  Senha: marcos123")
        print("  Nome: Marcos Ferreira")
        print("="*50)

    def get_usuarios_teste(self):
        """Retorna os dados dos usuários de teste para facilitar o login"""
        return {
            'administrador': {'usuario': 'joao', 'senha': 'joao123'},
            'medico': {'crm': 'CRM-SP-12345', 'senha': 'leticia123'},
            'paciente': {'email': 'marcos.silva@email.com', 'senha': 'marcos123'}
        }