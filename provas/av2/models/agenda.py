from database.database import Database

class Agenda:
    def __init__(self, id=None, id_medico=None, data_agenda=None, hora_inicio=None, 
                 hora_fim=None, disponivel=True, motivo_bloqueio=None):
        self.id = id
        self.id_medico = id_medico
        self.data_agenda = data_agenda
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
        self.disponivel = disponivel
        self.motivo_bloqueio = motivo_bloqueio
    
    def salvar(self):
        """Salva ou atualiza um horário na agenda (CREATE/UPDATE)"""
        db = Database()
        if self.id is None:
            # Inserir novo horário
            query = """
            INSERT INTO agenda_medica (id_medico, data_agenda, hora_inicio, hora_fim, disponivel, motivo_bloqueio)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            params = (self.id_medico, self.data_agenda, self.hora_inicio, 
                     self.hora_fim, self.disponivel, self.motivo_bloqueio)
            return db.execute_query(query, params)
        else:
            # Atualizar horário existente
            query = """
            UPDATE agenda_medica 
            SET id_medico=?, data_agenda=?, hora_inicio=?, hora_fim=?, disponivel=?, motivo_bloqueio=?
            WHERE id=?
            """
            params = (self.id_medico, self.data_agenda, self.hora_inicio, 
                     self.hora_fim, self.disponivel, self.motivo_bloqueio, self.id)
            return db.execute_query(query, params)
    
    @staticmethod
    def buscar_por_id(id):
        """Busca um horário na agenda por ID (READ)"""
        db = Database()
        query = "SELECT * FROM agenda_medica WHERE id = ?"
        result = db.fetch_one(query, (id,))
        if result:
            return Agenda(**result)
        return None
    
    @staticmethod
    def buscar_por_medico_e_data(id_medico, data_agenda):
        """Busca horários de um médico em uma data específica"""
        db = Database()
        query = """
        SELECT * FROM agenda_medica 
        WHERE id_medico = ? AND data_agenda = ? 
        ORDER BY hora_inicio
        """
        results = db.fetch_all(query, (id_medico, data_agenda))
        agendas = []
        for result in results:
            agendas.append(Agenda(**result))
        return agendas
    
    @staticmethod
    def buscar_disponiveis_por_medico_e_data(id_medico, data_agenda):
        """Busca horários disponíveis de um médico em uma data específica"""
        db = Database()
        query = """
        SELECT * FROM agenda_medica 
        WHERE id_medico = ? AND data_agenda = ? AND disponivel = 1
        ORDER BY hora_inicio
        """
        results = db.fetch_all(query, (id_medico, data_agenda))
        agendas = []
        for result in results:
            agendas.append(Agenda(**result))
        return agendas
    
    @staticmethod
    def listar_por_medico(id_medico):
        """Lista todos os horários de um médico"""
        db = Database()
        query = """
        SELECT * FROM agenda_medica 
        WHERE id_medico = ? 
        ORDER BY data_agenda DESC, hora_inicio
        """
        results = db.fetch_all(query, (id_medico,))
        agendas = []
        for result in results:
            agendas.append(Agenda(**result))
        return agendas
    
    def bloquear_horario(self, motivo="Bloqueado pelo médico"):
        """Bloqueia um horário na agenda"""
        db = Database()
        query = "UPDATE agenda_medica SET disponivel = 0, motivo_bloqueio = ? WHERE id = ?"
        return db.execute_query(query, (motivo, self.id))
    
    def liberar_horario(self):
        """Libera um horário bloqueado na agenda"""
        db = Database()
        query = "UPDATE agenda_medica SET disponivel = 1, motivo_bloqueio = NULL WHERE id = ?"
        return db.execute_query(query, (self.id,))
    
    def excluir(self):
        """Exclui um horário da agenda (DELETE)"""
        db = Database()
        query = "DELETE FROM agenda_medica WHERE id = ?"
        return db.execute_query(query, (self.id,))
    
    @staticmethod
    def criar_horarios_padrao(id_medico, data_agenda):
        """Cria horários padrão para um médico em uma data específica"""
        horarios_padrao = [
            ('08:00', '09:00'),
            ('09:00', '10:00'),
            ('10:00', '11:00'),
            ('11:00', '12:00'),
            ('14:00', '15:00'),
            ('15:00', '16:00'),
            ('16:00', '17:00')
        ]
        
        for hora_inicio, hora_fim in horarios_padrao:
            agenda = Agenda(
                id_medico=id_medico,
                data_agenda=data_agenda,
                hora_inicio=hora_inicio,
                hora_fim=hora_fim,
                disponivel=True
            )
            agenda.salvar()
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'id_medico': self.id_medico,
            'data_agenda': self.data_agenda,
            'hora_inicio': self.hora_inicio,
            'hora_fim': self.hora_fim,
            'disponivel': self.disponivel,
            'motivo_bloqueio': self.motivo_bloqueio
        }