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
        """Salva ou atualiza o horário na agenda"""
        if self.id is None:
            return self._criar()
        else:
            return self._atualizar()
    
    def _criar(self):
        """Cria um novo horário na agenda"""
        query = """
        INSERT INTO agenda_medica (id_medico, data_agenda, hora_inicio, hora_fim, disponivel, motivo_bloqueio)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (self.id_medico, self.data_agenda, self.hora_inicio, 
                 self.hora_fim, self.disponivel, self.motivo_bloqueio)
        
        db = Database()
        self.id = db.executar_query(query, params, retornar_id=True)
        return self.id
    
    def _atualizar(self):
        """Atualiza um horário existente na agenda"""
        query = """
        UPDATE agenda_medica 
        SET id_medico=?, data_agenda=?, hora_inicio=?, hora_fim=?, disponivel=?, motivo_bloqueio=?
        WHERE id=?
        """
        params = (self.id_medico, self.data_agenda, self.hora_inicio, 
                 self.hora_fim, self.disponivel, self.motivo_bloqueio, self.id)
        
        db = Database()
        db.executar_query(query, params)
        return True
    
    @classmethod
    def buscar_por_id(cls, id):
        """Busca um horário na agenda por ID"""
        query = "SELECT * FROM agenda_medica WHERE id = ?"
        db = Database()
        result = db.executar_query(query, (id,), fetch_one=True)
        
        if result:
            return cls(**result)
        return None
    
    @classmethod
    def buscar_por_medico_e_data(cls, id_medico, data_agenda):
        """Busca horários de um médico em uma data específica"""
        query = """
        SELECT * FROM agenda_medica 
        WHERE id_medico = ? AND data_agenda = ? 
        ORDER BY hora_inicio
        """
        db = Database()
        results = db.executar_query(query, (id_medico, data_agenda), fetch_all=True)
        
        agendas = []
        for result in results:
            agendas.append(cls(**result))
        return agendas
    
    @classmethod
    def buscar_disponiveis_por_medico_e_data(cls, id_medico, data_agenda):
        """Busca horários disponíveis de um médico em uma data específica"""
        query = """
        SELECT * FROM agenda_medica 
        WHERE id_medico = ? AND data_agenda = ? AND disponivel = 1
        ORDER BY hora_inicio
        """
        db = Database()
        results = db.executar_query(query, (id_medico, data_agenda), fetch_all=True)
        
        agendas = []
        for result in results:
            agendas.append(cls(**result))
        return agendas
    
    @classmethod
    def buscar_por_medico(cls, id_medico):
        """Busca todos os horários de um médico"""
        query = """
        SELECT * FROM agenda_medica 
        WHERE id_medico = ? 
        ORDER BY data_agenda DESC, hora_inicio
        """
        db = Database()
        results = db.executar_query(query, (id_medico,), fetch_all=True)
        
        agendas = []
        for result in results:
            agendas.append(cls(**result))
        return agendas
    
    def bloquear(self, motivo="Bloqueado pelo médico"):
        """Bloqueia um horário na agenda"""
        self.disponivel = False
        self.motivo_bloqueio = motivo
        return self.salvar()
    
    def liberar(self):
        """Libera um horário bloqueado na agenda"""
        self.disponivel = True
        self.motivo_bloqueio = None
        return self.salvar()
    
    def excluir(self):
        """Exclui um horário da agenda"""
        query = "DELETE FROM agenda_medica WHERE id = ?"
        db = Database()
        db.executar_query(query, (self.id,))
        return True
    
    @classmethod
    def verificar_disponibilidade(cls, id_medico, data_agenda, hora_inicio, hora_fim=None, exclude_id=None):
        """Verifica se um horário está disponível para agendamento"""
        if hora_fim:
            query = """
            SELECT COUNT(*) as count FROM agenda_medica 
            WHERE id_medico = ? AND data_agenda = ? 
            AND hora_inicio = ? AND hora_fim = ? AND disponivel = 1
            """
            params = (id_medico, data_agenda, hora_inicio, hora_fim)
        else:
            query = """
            SELECT COUNT(*) as count FROM agenda_medica 
            WHERE id_medico = ? AND data_agenda = ? 
            AND hora_inicio = ? AND disponivel = 1
            """
            params = (id_medico, data_agenda, hora_inicio)
        
        if exclude_id:
            query += " AND id != ?"
            params = params + (exclude_id,)
        
        db = Database()
        result = db.executar_query(query, params, fetch_one=True)
        return result['count'] > 0 if result else False
    
    @classmethod
    def criar_horarios_padrao(cls, id_medico, data_agenda):
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
            # Verifica se o horário já existe antes de criar
            if not cls.verificar_disponibilidade(id_medico, data_agenda, hora_inicio, hora_fim):
                agenda = cls(
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