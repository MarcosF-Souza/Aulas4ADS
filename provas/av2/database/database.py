import sqlite3
import os
import hashlib

class Database:
    def __init__(self, db_name='sistema_agendamento.db'):
        self.db_name = db_name
        self.connection = None
        
    def connect(self):
        """Conecta ao banco de dados SQLite"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.connection.row_factory = sqlite3.Row
            return self.connection
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None
    
    def disconnect(self):
        """Desconecta do banco de dados"""
        if self.connection:
            self.connection.close()
    
    def executar_query(self, query, params=None, fetch_one=False, fetch_all=False, retornar_id=False):
        """
        Executa uma query no banco de dados
        Retorna:
            - Para SELECT: os resultados quando fetch_one ou fetch_all é True
            - Para INSERT: o ID quando retornar_id é True
            - Para outras queries: True em caso de sucesso, False em caso de erro
        """
        conn = self.connect()
        if conn is None:
            return None if fetch_one or fetch_all else False
        
        try:
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Para operações que modificam o banco
            if not query.strip().upper().startswith('SELECT'):
                conn.commit()
                
                if retornar_id and query.strip().upper().startswith('INSERT'):
                    return cursor.lastrowid
                return True
            
            # Para operações SELECT
            if fetch_one:
                result = cursor.fetchone()
                return dict(result) if result else None
            elif fetch_all:
                results = cursor.fetchall()
                return [dict(row) for row in results]
            else:
                return True
                
        except sqlite3.Error as e:
            print(f"Erro ao executar query: {e}")
            print(f"Query: {query}")
            if params:
                print(f"Parâmetros: {params}")
            return None if fetch_one or fetch_all else False
        finally:
            self.disconnect()
    
    def criar_tabelas(self):
        """Cria todas as tabelas do sistema"""
        tabelas = [
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
            # Tabela de administradores (atualizada para compatibilidade com o model)
            """
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
                FOREIGN KEY (id_medico) REFERENCES medicos (id) ON DELETE CASCADE,
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
                FOREIGN KEY (id_paciente) REFERENCES pacientes (id) ON DELETE CASCADE,
                FOREIGN KEY (id_medico) REFERENCES medicos (id) ON DELETE CASCADE
            )
            """,
            # Tabela de prontuários
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
                FOREIGN KEY (id_paciente) REFERENCES pacientes (id) ON DELETE CASCADE,
                FOREIGN KEY (id_medico) REFERENCES medicos (id) ON DELETE CASCADE,
                FOREIGN KEY (id_consulta) REFERENCES consultas (id) ON DELETE CASCADE,
                UNIQUE(id_consulta)
            )
            """
        ]
        
        for tabela_sql in tabelas:
            sucesso = self.executar_query(tabela_sql)
            if not sucesso:
                print(f"Erro ao criar tabela")
                return False
        
        print("Todas as tabelas criadas com sucesso!")
        return True
    
    def _hash_senha(self, senha):
        """Gera hash da senha (para administradores)"""
        return hashlib.sha256(senha.encode()).hexdigest()
    
    def inicializar_dados_teste(self):
        """Inicializa o banco de dados com dados de teste"""
        # Criar tabelas
        if not self.criar_tabelas():
            return False
        
        print("\n" + "="*70)
        print("👥 USUÁRIOS DE TESTE CRIADOS")
        print("="*70)
        
        # ========== ADMINISTRADOR ==========
        admin_existe = self.executar_query(
            "SELECT * FROM administradores WHERE email = ?", 
            ('admin@hospital.com',), 
            fetch_one=True
        )
        if not admin_existe:
            senha_hash = self._hash_senha('admin123')
            admin_id = self.executar_query(
                """INSERT INTO administradores (nome, email, senha_hash, telefone, cargo) 
                VALUES (?, ?, ?, ?, ?)""",
                ('Administrador Principal', 'admin@hospital.com', senha_hash, 
                '(11) 99999-8888', 'Gerente Geral'),
                retornar_id=True
            )
            print("👤 ADMINISTRADOR")
            print(f"   Email: admin@hospital.com")
            print(f"   Senha: admin123")
            print(f"   Nome: Administrador Principal")
        else:
            print("👤 ADMINISTRADOR (já existente)")
            print(f"   Email: admin@hospital.com")
            print(f"   Senha: admin123")
            print(f"   Nome: Administrador Principal")
        
        # ========== MÉDICOS ==========
        medicos = [
            {
                'nome': 'Dra. Letícia de Paiva',
                'crm': 'CRM-SP-12345',
                'especialidade': 'Cardiologia',
                'telefone': '(11) 98888-7777',
                'email': 'leticia.paiva@hospital.com',
                'senha': 'leticia123'
            },
            {
                'nome': 'Dr. Carlos Mendes',
                'crm': 'CRM-SP-67890',
                'especialidade': 'Dermatologia',
                'telefone': '(11) 97777-6666',
                'email': 'carlos.mendes@hospital.com',
                'senha': 'carlos123'
            }
        ]
        
        print("\n👨‍⚕️ MÉDICOS")
        for medico in medicos:
            medico_existe = self.executar_query(
                "SELECT * FROM medicos WHERE crm = ?", 
                (medico['crm'],), 
                fetch_one=True
            )
            if not medico_existe:
                medico_id = self.executar_query(
                    """INSERT INTO medicos (nome, crm, especialidade, telefone, email, senha) 
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (medico['nome'], medico['crm'], medico['especialidade'], 
                    medico['telefone'], medico['email'], medico['senha']),
                    retornar_id=True
                )
                print(f"   {medico['nome']}")
                print(f"   CRM: {medico['crm']}")
                print(f"   Email: {medico['email']}")
                print(f"   Senha: {medico['senha']}")
                print(f"   Especialidade: {medico['especialidade']}\n")
            else:
                print(f"   {medico['nome']} (já existente)")
                print(f"   CRM: {medico['crm']}")
                print(f"   Email: {medico['email']}")
                print(f"   Senha: {medico['senha']}")
                print(f"   Especialidade: {medico['especialidade']}\n")
        
        # ========== PACIENTES ==========
        pacientes = [
            {
                'nome': 'Marcos Ferreira',
                'email': 'marcos.silva@email.com',
                'telefone': '(11) 97777-6666',
                'data_nascimento': '1990-08-15',
                'endereco': 'Rua das Flores, 123 - São Paulo, SP',
                'senha': 'marcos123'
            },
            {
                'nome': 'Ana Santos',
                'email': 'ana.santos@email.com',
                'telefone': '(11) 96666-5555',
                'data_nascimento': '1985-03-22',
                'endereco': 'Av. Paulista, 1000 - São Paulo, SP',
                'senha': 'ana123'
            }
        ]
        
        print("\n👥 PACIENTES")
        for paciente in pacientes:
            paciente_existe = self.executar_query(
                "SELECT * FROM pacientes WHERE email = ?", 
                (paciente['email'],), 
                fetch_one=True
            )
            if not paciente_existe:
                paciente_id = self.executar_query(
                    """INSERT INTO pacientes (nome, email, telefone, data_nascimento, endereco, senha) 
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (paciente['nome'], paciente['email'], paciente['telefone'], 
                    paciente['data_nascimento'], paciente['endereco'], paciente['senha']),
                    retornar_id=True
                )
                print(f"   {paciente['nome']}")
                print(f"   Email: {paciente['email']}")
                print(f"   Senha: {paciente['senha']}")
                print(f"   Telefone: {paciente['telefone']}\n")
            else:
                print(f"   {paciente['nome']} (já existente)")
                print(f"   Email: {paciente['email']}")
                print(f"   Senha: {paciente['senha']}")
                print(f"   Telefone: {paciente['telefone']}\n")
        
        # ========== CONSULTA DE EXEMPLO ==========
        print("\n📅 CONSULTA DE EXEMPLO")
        
        # Obter IDs do paciente e médico
        paciente_result = self.executar_query(
            "SELECT id, nome FROM pacientes WHERE email = ?", 
            ('marcos.silva@email.com',), 
            fetch_one=True
        )
        medico_result = self.executar_query(
            "SELECT id, nome FROM medicos WHERE crm = ?", 
            ('CRM-SP-12345',), 
            fetch_one=True
        )
        
        if paciente_result and medico_result:
            paciente_id = paciente_result['id']
            medico_id = medico_result['id']
            
            # Verificar se a consulta já existe
            consulta_existe = self.executar_query(
                """SELECT * FROM consultas 
                WHERE id_paciente = ? AND id_medico = ? AND data_consulta = ? AND hora_consulta = ?""",
                (paciente_id, medico_id, '2024-12-20', '09:00'),
                fetch_one=True
            )
            
            if not consulta_existe:
                consulta_id = self.executar_query(
                    """INSERT INTO consultas (id_paciente, id_medico, data_consulta, hora_consulta, status, motivo) 
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (paciente_id, medico_id, '2024-12-20', '09:00', 'agendada', 'Check-up cardiológico anual'),
                    retornar_id=True
                )
            else:
                consulta_id = consulta_existe['id']
            
            # Buscar a consulta criada para exibir os dados
            consulta_criada = self.executar_query("""
                SELECT c.*, p.nome as paciente_nome, m.nome as medico_nome 
                FROM consultas c
                JOIN pacientes p ON c.id_paciente = p.id
                JOIN medicos m ON c.id_medico = m.id
                WHERE c.id = ?
            """, (consulta_id,), fetch_one=True)
            
            if consulta_criada:
                print(f"   Paciente: {consulta_criada['paciente_nome']}")
                print(f"   Médico: {consulta_criada['medico_nome']}")
                print(f"   Data: {consulta_criada['data_consulta']} {consulta_criada['hora_consulta']}")
                print(f"   Status: {consulta_criada['status']}")
                print(f"   Motivo: {consulta_criada['motivo']}")
        
        # ========== PRONTUÁRIO DE EXEMPLO ==========
        print("\n📋 PRONTUÁRIO DE EXEMPLO")
        
        if 'consulta_id' in locals() and consulta_id:
            prontuario_existe = self.executar_query(
                "SELECT * FROM prontuarios WHERE id_consulta = ?", 
                (consulta_id,), 
                fetch_one=True
            )
            
            if not prontuario_existe:
                prontuario_id = self.executar_query(
                    """INSERT INTO prontuarios (id_paciente, id_medico, id_consulta, diagnostico, prescricao, exames, observacoes) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (paciente_id, medico_id, consulta_id, 
                    'Paciente com histórico familiar de cardiopatia. Pressão arterial dentro dos limites normais.',
                    'Manter hábitos saudáveis de alimentação e prática regular de exercícios físicos.',
                    'Eletrocardiograma - Normal\nHemograma completo - Dentro dos parâmetros',
                    'Paciente orientado sobre importância do acompanhamento anual.'),
                    retornar_id=True
                )
                
                print(f"   Prontuário criado para: Marcos Ferreira")
                print(f"   Diagnóstico: Paciente com histórico familiar de cardiopatia")
                print(f"   Prescrição: Manter hábitos saudáveis")
            else:
                print(f"   Prontuário já existente para: Marcos Ferreira")
                print(f"   Diagnóstico: {prontuario_existe['diagnostico']}")
                print(f"   Prescrição: {prontuario_existe['prescricao']}")
        
        print("\n" + "="*70)
        print("✅ DADOS DE TESTE INICIALIZADOS COM SUCESSO!")
        print("="*70)
        
        return True

    # MÉTODO DE COMPATIBILIDADE - ADICIONADO PARA RESOLVER O ERRO
    def init_database(self):
        """Método de compatibilidade - chama inicializar_dados_teste()"""
        return self.inicializar_dados_teste()
    
    def obter_dados_login_teste(self):
        """Retorna os dados para login de teste de forma organizada"""
        return {
            'administrador': {
                'tipo': 'Administrador',
                'email': 'admin@hospital.com', 
                'senha': 'admin123',
                'nome': 'Administrador Principal'
            },
            'medicos': [
                {
                    'tipo': 'Médico',
                    'crm': 'CRM-SP-12345',
                    'email': 'leticia.paiva@hospital.com', 
                    'senha': 'leticia123',
                    'nome': 'Dra. Letícia de Paiva',
                    'especialidade': 'Cardiologia'
                },
                {
                    'tipo': 'Médico', 
                    'crm': 'CRM-SP-67890',
                    'email': 'carlos.mendes@hospital.com', 
                    'senha': 'carlos123',
                    'nome': 'Dr. Carlos Mendes',
                    'especialidade': 'Dermatologia'
                }
            ],
            'pacientes': [
                {
                    'tipo': 'Paciente',
                    'email': 'marcos.silva@email.com', 
                    'senha': 'marcos123',
                    'nome': 'Marcos Ferreira'
                },
                {
                    'tipo': 'Paciente',
                    'email': 'ana.santos@email.com', 
                    'senha': 'ana123',
                    'nome': 'Ana Santos'
                }
            ]
        }