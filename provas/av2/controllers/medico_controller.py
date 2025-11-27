from models.medico import Medico
from models.consulta import Consulta
from models.agenda import Agenda
from models.prontuario import Prontuario
from database.database import Database
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from datetime import datetime

class MedicoController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.db = Database()
    
    def abrir_minha_agenda(self):
        """Abre a tela com a agenda do médico"""
        medico_id = self.main_controller.usuario_logado.id
        consultas = Consulta.buscar_por_medico(medico_id)
        
        janela_agenda = tk.Toplevel(self.main_controller.app.root)
        janela_agenda.title("Minha Agenda")
        janela_agenda.geometry("800x500")
        
        frame = ttk.Frame(janela_agenda, padding="20")
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="MINHA AGENDA", font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Filtro por data
        filtro_frame = ttk.Frame(frame)
        filtro_frame.pack(fill='x', pady=10)
        
        ttk.Label(filtro_frame, text="Filtrar por data:").pack(side='left', padx=5)
        self.data_filtro_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        data_entry = ttk.Entry(filtro_frame, textvariable=self.data_filtro_var, width=12)
        data_entry.pack(side='left', padx=5)
        ttk.Button(filtro_frame, text="Aplicar Filtro", 
                  command=lambda: self.filtrar_agenda(tree, medico_id)).pack(side='left', padx=5)
        
        # Treeview para agenda
        colunas = ('Data', 'Hora', 'Paciente', 'Status', 'Motivo')
        tree = ttk.Treeview(frame, columns=colunas, show='headings', height=20)
        
        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        # Carregar consultas
        self.carregar_consultas_na_treeview(tree, consultas)
        
        tree.pack(pady=10, fill='both', expand=True)
        
        # Botões de ação
        botoes_frame = ttk.Frame(frame)
        botoes_frame.pack(pady=10)
        
        ttk.Button(botoes_frame, text="Ver Prontuário", 
                  command=lambda: self.ver_prontuario(tree)).pack(side='left', padx=5)
        ttk.Button(botoes_frame, text="Finalizar Consulta", 
                  command=lambda: self.finalizar_consulta(tree)).pack(side='left', padx=5)
        ttk.Button(botoes_frame, text="Fechar", 
                  command=janela_agenda.destroy).pack(side='left', padx=5)
    
    def carregar_consultas_na_treeview(self, tree, consultas):
        """Carrega as consultas na treeview"""
        for item in tree.get_children():
            tree.delete(item)
        
        for consulta in consultas:
            tree.insert('', 'end', values=(
                consulta.data_consulta,
                consulta.hora_consulta,
                consulta.paciente_nome,
                consulta.status,
                consulta.motivo or "Não informado"
            ))
    
    def filtrar_agenda(self, tree, medico_id):
        """Filtra a agenda por data"""
        data_filtro = self.data_filtro_var.get()
        if data_filtro:
            consultas_filtradas = Consulta.buscar_por_medico_e_data(medico_id, data_filtro)
            self.carregar_consultas_na_treeview(tree, consultas_filtradas)
    
    def ver_prontuario(self, tree):
        """Abre o prontuário do paciente selecionado"""
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma consulta para ver o prontuário!")
            return
        
        item = tree.item(selecionado[0])
        valores = item['values']
        
        # Buscar prontuário
        consultas = Consulta.buscar_por_medico(self.main_controller.usuario_logado.id)
        consulta_correspondente = None
        
        for consulta in consultas:
            if (consulta.data_consulta == valores[0] and 
                consulta.hora_consulta == valores[1] and 
                consulta.paciente_nome == valores[2]):
                consulta_correspondente = consulta
                break
        
        if not consulta_correspondente:
            messagebox.showerror("Erro", "Consulta não encontrada!")
            return
        
        prontuario = Prontuario.buscar_por_consulta(consulta_correspondente.id)
        
        janela_prontuario = tk.Toplevel(self.main_controller.app.root)
        janela_prontuario.title(f"Prontuário - {valores[2]}")
        janela_prontuario.geometry("600x500")
        
        frame = ttk.Frame(janela_prontuario, padding="20")
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text=f"PRONTUÁRIO - {valores[2]}", font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Área de texto para o prontuário
        texto_frame = ttk.Frame(frame)
        texto_frame.pack(fill="both", expand=True)
        
        text_area = tk.Text(texto_frame, wrap=tk.WORD, width=60, height=20)
        scrollbar = ttk.Scrollbar(texto_frame, orient="vertical", command=text_area.yview)
        text_area.configure(yscrollcommand=scrollbar.set)
        
        if prontuario:
            conteudo = f"""PACIENTE: {prontuario.paciente_nome}
DATA: {valores[0]} {valores[1]}
MÉDICO: {prontuario.medico_nome}

DIAGNÓSTICO:
{prontuario.diagnostico or 'Não informado'}

PRESCRIÇÃO:
{prontuario.prescricao or 'Não informado'}

EXAMES:
{prontuario.exames or 'Não informado'}

OBSERVAÇÕES:
{prontuario.observacoes or 'Não informado'}
"""
        else:
            conteudo = f"""PACIENTE: {valores[2]}
DATA: {valores[0]} {valores[1]}
MÉDICO: {self.main_controller.usuario_logado.nome}

DIAGNÓSTICO:
[Preencher diagnóstico]

PRESCRIÇÃO:
[Preencher prescrição]

EXAMES:
[Preencher exames]

OBSERVAÇÕES:
[Preencher observações]
"""
        
        text_area.insert("1.0", conteudo)
        text_area.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botões
        botoes_frame = ttk.Frame(frame)
        botoes_frame.pack(pady=10)
        
        if prontuario:
            ttk.Button(botoes_frame, text="Editar", 
                      command=lambda: self.editar_prontuario(consulta_correspondente.id, text_area)).pack(side='left', padx=5)
        else:
            ttk.Button(botoes_frame, text="Criar Prontuário", 
                      command=lambda: self.criar_prontuario(consulta_correspondente.id, text_area)).pack(side='left', padx=5)
        
        ttk.Button(botoes_frame, text="Fechar", 
                  command=janela_prontuario.destroy).pack(side='left', padx=5)
    
    def editar_prontuario(self, consulta_id, text_area):
        """Edita o prontuário"""
        conteudo = text_area.get("1.0", tk.END)
        # Implementar lógica de edição do prontuário
        messagebox.showinfo("Em Desenvolvimento", "Funcionalidade de edição de prontuário em desenvolvimento")
    
    def criar_prontuario(self, consulta_id, text_area):
        """Cria um novo prontuário"""
        conteudo = text_area.get("1.0", tk.END)
        # Implementar lógica de criação do prontuário
        messagebox.showinfo("Em Desenvolvimento", "Funcionalidade de criação de prontuário em desenvolvimento")
    
    def finalizar_consulta(self, tree):
        """Finaliza uma consulta selecionada"""
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma consulta para finalizar!")
            return
        
        item = tree.item(selecionado[0])
        valores = item['values']
        
        # Buscar consulta
        consultas = Consulta.buscar_por_medico(self.main_controller.usuario_logado.id)
        consulta_correspondente = None
        
        for consulta in consultas:
            if (consulta.data_consulta == valores[0] and 
                consulta.hora_consulta == valores[1] and 
                consulta.paciente_nome == valores[2]):
                consulta_correspondente = consulta
                break
        
        if consulta_correspondente and consulta_correspondente.finalizar("Consulta finalizada pelo médico"):
            messagebox.showinfo("Sucesso", "Consulta finalizada com sucesso!")
            # Atualizar a lista
            self.abrir_minha_agenda()
        else:
            messagebox.showerror("Erro", "Erro ao finalizar consulta!")
    
    def abrir_consultas_do_dia(self):
        """Mostra as consultas agendadas para o dia atual"""
        medico_id = self.main_controller.usuario_logado.id
        data_hoje = datetime.now().strftime("%Y-%m-%d")
        consultas_hoje = Consulta.buscar_por_medico_e_data(medico_id, data_hoje)
        
        if not consultas_hoje:
            messagebox.showinfo("Consultas de Hoje", "Nenhuma consulta agendada para hoje.")
            return
        
        janela_consultas = tk.Toplevel(self.main_controller.app.root)
        janela_consultas.title("Consultas de Hoje")
        janela_consultas.geometry("500x300")
        
        frame = ttk.Frame(janela_consultas, padding="20")
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text=f"CONSULTAS DE HOJE ({data_hoje})", font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        for consulta in consultas_hoje:
            consulta_frame = ttk.Frame(frame, relief='solid', padding=10)
            consulta_frame.pack(fill='x', pady=5)
            
            ttk.Label(consulta_frame, text=f"⏰ {consulta.hora_consulta} - {consulta.paciente_nome}", 
                     font=('Arial', 10, 'bold')).pack(anchor='w')
            ttk.Label(consulta_frame, text=f"Motivo: {consulta.motivo}", 
                     font=('Arial', 9)).pack(anchor='w')
            ttk.Label(consulta_frame, text=f"Status: {consulta.status}", 
                     font=('Arial', 9)).pack(anchor='w')
        
        ttk.Button(frame, text="Fechar", 
                  command=janela_consultas.destroy).pack(pady=10)
    
    def abrir_gerenciar_agenda(self):
        """Abre a tela para gerenciar a agenda (bloquear/liberar horários)"""
        messagebox.showinfo("Em Desenvolvimento", "Funcionalidade de gerenciamento de agenda em desenvolvimento")
    
    def abrir_relatorios(self):
        """Abre a tela de relatórios do médico"""
        medico_id = self.main_controller.usuario_logado.id
        consultas = Consulta.buscar_por_medico(medico_id)
        
        consultas_realizadas = len([c for c in consultas if c.status == 'realizada'])
        consultas_agendadas = len([c for c in consultas if c.status == 'agendada'])
        consultas_canceladas = len([c for c in consultas if c.status == 'cancelada'])
        
        janela_relatorios = tk.Toplevel(self.main_controller.app.root)
        janela_relatorios.title("Meus Relatórios")
        janela_relatorios.geometry("400x300")
        
        frame = ttk.Frame(janela_relatorios, padding="20")
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="MEUS RELATÓRIOS", font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Estatísticas
        stats = [
            ("Total de Consultas:", len(consultas)),
            ("Consultas Realizadas:", consultas_realizadas),
            ("Consultas Agendadas:", consultas_agendadas),
            ("Consultas Canceladas:", consultas_canceladas),
        ]
        
        for i, (label, valor) in enumerate(stats):
            ttk.Label(frame, text=label, font=('Arial', 10, 'bold')).grid(row=i, column=0, sticky='w', pady=5, padx=5)
            ttk.Label(frame, text=str(valor)).grid(row=i, column=1, sticky='w', pady=5, padx=5)
        
        ttk.Button(frame, text="Fechar", 
                  command=janela_relatorios.destroy).grid(row=len(stats), column=0, columnspan=2, pady=20)