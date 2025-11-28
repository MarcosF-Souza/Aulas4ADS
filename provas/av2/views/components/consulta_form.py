# views/componentes/consulta_form.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import re

class ConsultaForm:
    def __init__(self, parent, controller, modo_edicao=False, consulta_data=None):
        """
        Formulário de consulta - reutilizável para criação e edição
        
        Args:
            parent: Widget pai
            controller: Controller para comunicação
            modo_edicao: Se True, modo edição; se False, modo criação
            consulta_data: Dados da consulta para edição (se modo_edicao=True)
        """
        self.parent = parent
        self.controller = controller
        self.modo_edicao = modo_edicao
        self.consulta_data = consulta_data
        
        # Variáveis do formulário
        self.var_paciente_id = tk.StringVar()
        self.var_medico_id = tk.StringVar()
        self.var_data_consulta = tk.StringVar()
        self.var_hora_consulta = tk.StringVar()
        self.var_tipo_consulta = tk.StringVar(value="Rotina")
        self.var_status = tk.StringVar(value="Agendada")
        self.var_motivo = tk.StringVar()
        self.var_observacoes = tk.StringVar()
        
        self.criar_formulario()
        
        if modo_edicao and consulta_data:
            self.preencher_dados_existentes()
    
    def criar_formulario(self):
        """Cria os elementos do formulário"""
        # Frame principal
        self.frame = ttk.Frame(self.parent, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights
        self.frame.columnconfigure(1, weight=1)
        
        # Título
        titulo = "Editar Consulta" if self.modo_edicao else "Nova Consulta"
        ttk.Label(
            self.frame, 
            text=titulo, 
            font=('Arial', 12, 'bold')
        ).grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        linha = 1
        
        # Paciente
        ttk.Label(self.frame, text="Paciente:*").grid(row=linha, column=0, sticky=tk.W, pady=2)
        self.combo_paciente = ttk.Combobox(
            self.frame, 
            textvariable=self.var_paciente_id,
            state="readonly",
            width=30
        )
        self.combo_paciente.grid(row=linha, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        linha += 1
        
        # Médico
        ttk.Label(self.frame, text="Médico:*").grid(row=linha, column=0, sticky=tk.W, pady=2)
        self.combo_medico = ttk.Combobox(
            self.frame, 
            textvariable=self.var_medico_id,
            state="readonly",
            width=30
        )
        self.combo_medico.grid(row=linha, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        linha += 1
        
        # Data da Consulta
        ttk.Label(self.frame, text="Data:*").grid(row=linha, column=0, sticky=tk.W, pady=2)
        frame_data = ttk.Frame(self.frame)
        frame_data.grid(row=linha, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        
        self.entry_data = ttk.Entry(frame_data, textvariable=self.var_data_consulta, width=12)
        self.entry_data.pack(side=tk.LEFT)
        ttk.Button(
            frame_data, 
            text="📅", 
            width=3,
            command=self.selecionar_data
        ).pack(side=tk.LEFT, padx=(5, 0))
        linha += 1
        
        # Hora da Consulta
        ttk.Label(self.frame, text="Hora:*").grid(row=linha, column=0, sticky=tk.W, pady=2)
        self.combo_hora = ttk.Combobox(
            self.frame, 
            textvariable=self.var_hora_consulta,
            values=self.gerar_horarios_disponiveis(),
            state="readonly",
            width=10
        )
        self.combo_hora.grid(row=linha, column=1, sticky=tk.W, pady=2, padx=(5, 0))
        linha += 1
        
        # Tipo de Consulta
        ttk.Label(self.frame, text="Tipo:*").grid(row=linha, column=0, sticky=tk.W, pady=2)
        combo_tipo = ttk.Combobox(
            self.frame, 
            textvariable=self.var_tipo_consulta,
            values=["Rotina", "Retorno", "Emergência", "Exame", "Cirurgia"],
            state="readonly",
            width=15
        )
        combo_tipo.grid(row=linha, column=1, sticky=tk.W, pady=2, padx=(5, 0))
        linha += 1
        
        # Status (apenas em modo edição)
        if self.modo_edicao:
            ttk.Label(self.frame, text="Status:*").grid(row=linha, column=0, sticky=tk.W, pady=2)
            combo_status = ttk.Combobox(
                self.frame, 
                textvariable=self.var_status,
                values=["Agendada", "Confirmada", "Realizada", "Cancelada", "Não Compareceu"],
                state="readonly",
                width=15
            )
            combo_status.grid(row=linha, column=1, sticky=tk.W, pady=2, padx=(5, 0))
            linha += 1
        
        # Motivo da Consulta
        ttk.Label(self.frame, text="Motivo:*").grid(row=linha, column=0, sticky=tk.W, pady=2)
        entry_motivo = ttk.Entry(
            self.frame, 
            textvariable=self.var_motivo,
            width=30
        )
        entry_motivo.grid(row=linha, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        linha += 1
        
        # Observações
        ttk.Label(self.frame, text="Observações:").grid(row=linha, column=0, sticky=tk.NW, pady=2)
        self.text_observacoes = tk.Text(self.frame, width=30, height=4)
        self.text_observacoes.grid(row=linha, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        linha += 1
        
        # Botões
        frame_botoes = ttk.Frame(self.frame)
        frame_botoes.grid(row=linha, column=0, columnspan=2, pady=15)
        
        texto_botao = "Atualizar" if self.modo_edicao else "Agendar"
        ttk.Button(
            frame_botoes, 
            text=texto_botao,
            command=self.submeter_formulario
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            frame_botoes, 
            text="Cancelar",
            command=self.fechar_formulario
        ).pack(side=tk.LEFT)
        
        # Carregar dados iniciais
        self.carregar_pacientes()
        self.carregar_medicos()
        
        # Definir data padrão (amanhã)
        if not self.modo_edicao:
            data_amanha = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
            self.var_data_consulta.set(data_amanha)
    
    def carregar_pacientes(self):
        """Carrega a lista de pacientes no combobox"""
        try:
            pacientes = self.controller.obter_pacientes_ativos()
            opcoes_pacientes = [f"{p['id']} - {p['nome']}" for p in pacientes]
            self.combo_paciente['values'] = opcoes_pacientes
            if opcoes_pacientes:
                self.combo_paciente.current(0)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar pacientes: {str(e)}")
    
def carregar_medicos(self):
    """Carrega a lista de médicos no combobox"""
    try:
        medicos = self.controller.obter_medicos_ativos()
        opcoes_medicos = [f"{m['id']} - {m['nome']} - {m['especialidade']}" for m in medicos]
        self.combo_medico['values'] = opcoes_medicos
        if opcoes_medicos:
            self.combo_medico.current(0)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar médicos: {str(e)}")

def gerar_horarios_disponiveis(self):
    """Gera horários disponíveis para consulta"""
    horarios = []
    for hora in range(8, 18):  # Das 8h às 18h
        for minuto in ['00', '30']:
            horarios.append(f"{hora:02d}:{minuto}")
    return horarios

def selecionar_data(self):
    """Abre um calendário para seleção de data"""
    try:
        from tkcalendar import DateEntry

        # Criar janela popup para calendário
        popup = tk.Toplevel(self.parent)
        popup.title("Selecionar Data")
        popup.transient(self.parent)
        popup.grab_set()

        ttk.Label(popup, text="Selecione a data:").pack(pady=10)

        calendario = DateEntry(
            popup, 
            date_pattern='dd/mm/yyyy',
            mindate=datetime.now()
        )
        calendario.pack(pady=10)

        def confirmar_data():
            data_selecionada = calendario.get_date()
            self.var_data_consulta.set(data_selecionada.strftime("%d/%m/%Y"))
            popup.destroy()

        ttk.Button(popup, text="Confirmar", command=confirmar_data).pack(pady=10)

        # Centralizar popup
        popup.update_idletasks()
        x = self.parent.winfo_rootx() + (self.parent.winfo_width() // 2) - (popup.winfo_width() // 2)
        y = self.parent.winfo_rooty() + (self.parent.winfo_height() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f"+{x}+{y}")

    except ImportError:
        # Fallback se tkcalendar não estiver instalado
        messagebox.showinfo(
            "Selecionar Data", 
            "Digite a data no formato DD/MM/AAAA"
        )
    
    def preencher_dados_existentes(self):
        """Preenche o formulário com dados existentes (modo edição)"""
        if not self.consulta_data:
            return
        
        # Preencher campos
        paciente_str = f"{self.consulta_data['paciente_id']} - {self.consulta_data['paciente_nome']}"
        self.var_paciente_id.set(paciente_str)
        
        medico_str = f"{self.consulta_data['medico_id']} - {self.consulta_data['medico_nome']}"
        self.var_medico_id.set(medico_str)
        
        # Converter data do banco (YYYY-MM-DD) para DD/MM/YYYY
        data_obj = datetime.strptime(self.consulta_data['data_consulta'], "%Y-%m-%d")
        self.var_data_consulta.set(data_obj.strftime("%d/%m/%Y"))
        
        self.var_hora_consulta.set(self.consulta_data['hora_consulta'])
        self.var_tipo_consulta.set(self.consulta_data['tipo_consulta'])
        self.var_status.set(self.consulta_data['status'])
        self.var_motivo.set(self.consulta_data['motivo'])
        
        if self.consulta_data.get('observacoes'):
            self.text_observacoes.insert('1.0', self.consulta_data['observacoes'])
    
    def validar_formulario(self):
        """Valida os dados do formulário"""
        # Validar paciente
        if not self.var_paciente_id.get():
            messagebox.showerror("Erro", "Selecione um paciente")
            return False
        
        # Validar médico
        if not self.var_medico_id.get():
            messagebox.showerror("Erro", "Selecione um médico")
            return False
        
        # Validar data
        data_str = self.var_data_consulta.get()
        try:
            data_obj = datetime.strptime(data_str, "%d/%m/%Y")
            if data_obj.date() < datetime.now().date():
                messagebox.showerror("Erro", "Não é possível agendar consultas para datas passadas")
                return False
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido. Use DD/MM/AAAA")
            return False
        
        # Validar hora
        if not re.match(r'^\d{2}:\d{2}$', self.var_hora_consulta.get()):
            messagebox.showerror("Erro", "Formato de hora inválido. Use HH:MM")
            return False
        
        # Validar motivo
        if not self.var_motivo.get().strip():
            messagebox.showerror("Erro", "Informe o motivo da consulta")
            return False
        
        return True
    
    def extrair_ids(self):
        """Extrai IDs dos comboboxes"""
        paciente_texto = self.var_paciente_id.get()
        medico_texto = self.var_medico_id.get()
        
        paciente_id = int(paciente_texto.split(' - ')[0]) if ' - ' in paciente_texto else None
        medico_id = int(medico_texto.split(' - ')[0]) if ' - ' in medico_texto else None
        
        return paciente_id, medico_id
    
    def submeter_formulario(self):
        """Submete o formulário"""
        if not self.validar_formulario():
            return
        
        try:
            paciente_id, medico_id = self.extrair_ids()
            
            # Preparar dados
            dados_consulta = {
                'paciente_id': paciente_id,
                'medico_id': medico_id,
                'data_consulta': self.var_data_consulta.get(),
                'hora_consulta': self.var_hora_consulta.get(),
                'tipo_consulta': self.var_tipo_consulta.get(),
                'motivo': self.var_motivo.get(),
                'observacoes': self.text_observacoes.get('1.0', tk.END).strip()
            }
            
            if self.modo_edicao:
                dados_consulta['id'] = self.consulta_data['id']
                dados_consulta['status'] = self.var_status.get()
                sucesso = self.controller.atualizar_consulta(dados_consulta)
                mensagem = "Consulta atualizada com sucesso!"
            else:
                sucesso = self.controller.agendar_consulta(dados_consulta)
                mensagem = "Consulta agendada com sucesso!"
            
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.fechar_formulario()
            else:
                messagebox.showerror("Erro", "Erro ao processar consulta")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar formulário: {str(e)}")
    
    def fechar_formulario(self):
        """Fecha o formulário"""
        self.frame.destroy()
    
    def get_frame(self):
        """Retorna o frame principal do formulário"""
        return self.frame