# views/medico/minha_agenda_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class MinhaAgendaView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.frame = tk.Frame(self.root, bg='white')
        
        # Variáveis para filtros
        self.data_inicio_var = tk.StringVar()
        self.data_fim_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Todos")
        
        self.medico_logado = None
        
        self.criar_widgets()
    
    def criar_widgets(self):
        """Cria os widgets da tela Minha Agenda"""
        # Frame principal
        main_frame = tk.Frame(self.frame, bg='white', padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Título
        titulo = tk.Label(
            main_frame, 
            text="Minha Agenda", 
            font=('Arial', 18, 'bold'),
            bg='white',
            fg='#333333'
        )
        titulo.pack(pady=(0, 20))
        
        # Label para informações do médico (será atualizado no mostrar)
        self.info_medico_label = tk.Label(
            main_frame,
            text="",
            font=('Arial', 12),
            bg='white',
            fg='#666666'
        )
        self.info_medico_label.pack(pady=(0, 10))
        
        # Frame de filtros
        frame_filtros = tk.Frame(main_frame, bg='white')
        frame_filtros.pack(fill="x", pady=(0, 20))
        
        # Filtro por data
        tk.Label(frame_filtros, text="Data Início:", bg='white').grid(row=0, column=0, padx=5, sticky="w")
        entry_data_inicio = tk.Entry(frame_filtros, textvariable=self.data_inicio_var, width=12)
        entry_data_inicio.grid(row=0, column=1, padx=5)
        entry_data_inicio.insert(0, datetime.now().strftime("%d/%m/%Y"))
        
        tk.Label(frame_filtros, text="Data Fim:", bg='white').grid(row=0, column=2, padx=5, sticky="w")
        entry_data_fim = tk.Entry(frame_filtros, textvariable=self.data_fim_var, width=12)
        entry_data_fim.grid(row=0, column=3, padx=5)
        data_fim = datetime.now() + timedelta(days=7)
        entry_data_fim.insert(0, data_fim.strftime("%d/%m/%Y"))
        
        # Filtro por status
        tk.Label(frame_filtros, text="Status:", bg='white').grid(row=0, column=4, padx=5, sticky="w")
        combo_status = ttk.Combobox(
            frame_filtros, 
            textvariable=self.status_var,
            values=["Todos", "Agendada", "Confirmada", "Realizada", "Cancelada"],
            state="readonly",
            width=12
        )
        combo_status.grid(row=0, column=5, padx=5)
        
        # Botão de aplicar filtros
        btn_aplicar = ttk.Button(
            frame_filtros,
            text="Aplicar Filtros",
            command=self.aplicar_filtros,
            style='Accent.TButton'
        )
        btn_aplicar.grid(row=0, column=6, padx=10)
        
        # Treeview para mostrar as consultas
        columns = ('id', 'paciente', 'data', 'hora', 'status', 'motivo')
        self.tree = ttk.Treeview(
            main_frame, 
            columns=columns,
            show='headings',
            height=15
        )
        
        # Definir cabeçalhos
        self.tree.heading('id', text='ID')
        self.tree.heading('paciente', text='Paciente')
        self.tree.heading('data', text='Data')
        self.tree.heading('hora', text='Hora')
        self.tree.heading('status', text='Status')
        self.tree.heading('motivo', text='Motivo')
        
        # Configurar colunas
        self.tree.column('id', width=50)
        self.tree.column('paciente', width=150)
        self.tree.column('data', width=100)
        self.tree.column('hora', width=80)
        self.tree.column('status', width=100)
        self.tree.column('motivo', width=200)
        
        self.tree.pack(fill="both", expand=True, pady=(0, 10))
        
        # Frame de botões de ação
        frame_botoes = tk.Frame(main_frame, bg='white')
        frame_botoes.pack(fill="x", pady=10)
        
        # Botões de ação
        btn_confirmar = ttk.Button(
            frame_botoes,
            text="Confirmar Consulta",
            command=self.confirmar_consulta,
            style='Accent.TButton'
        )
        btn_confirmar.pack(side="left", padx=5)
        
        btn_realizar = ttk.Button(
            frame_botoes,
            text="Marcar como Realizada",
            command=self.marcar_realizada
        )
        btn_realizar.pack(side="left", padx=5)
        
        btn_cancelar = ttk.Button(
            frame_botoes,
            text="Cancelar Consulta",
            command=self.cancelar_consulta
        )
        btn_cancelar.pack(side="left", padx=5)
        
        btn_voltar = ttk.Button(
            frame_botoes,
            text="Voltar",
            command=self.voltar
        )
        btn_voltar.pack(side="right", padx=5)
    
    def mostrar(self):
        """Mostra a view"""
        # Atualizar informações do médico logado sempre que mostrar a view
        self.medico_logado = self.controller.obter_usuario_logado()
        
        if not self.medico_logado or not hasattr(self.medico_logado, 'crm'):
            messagebox.showerror("Erro", "Nenhum médico logado. Faça login novamente.")
            self.controller.voltar_principal()
            return
        
        # Atualizar o label com as informações do médico
        self.info_medico_label.config(text=f"Dr. {self.medico_logado.nome} - {self.medico_logado.especialidade}")
        
        self.frame.pack(fill="both", expand=True)
        self.carregar_consultas()
    
    def ocultar(self):
        """Oculta a view"""
        self.frame.pack_forget()
    
    def carregar_consultas(self):
        """Carrega as consultas do médico"""
        try:
            # Limpar treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Buscar consultas do médico
            if not self.medico_logado:
                return
            
            # Aqui você implementaria a busca real no banco
            # Por enquanto, vamos usar dados de exemplo
            consultas_exemplo = [
                (1, "João Silva", "15/12/2024", "09:00", "Agendada", "Consulta de rotina"),
                (2, "Maria Santos", "15/12/2024", "10:30", "Confirmada", "Acompanhamento"),
                (3, "Pedro Oliveira", "16/12/2024", "14:00", "Agendada", "Exames"),
                (4, "Ana Costa", "17/12/2024", "11:00", "Realizada", "Retorno"),
            ]
            
            for consulta in consultas_exemplo:
                self.tree.insert('', 'end', values=consulta)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar consultas: {str(e)}")
    
    def aplicar_filtros(self):
        """Aplica os filtros selecionados"""
        if not self.medico_logado:
            messagebox.showerror("Erro", "Nenhum médico logado")
            return
        messagebox.showinfo("Info", "Filtros aplicados (funcionalidade em desenvolvimento)")
    
    def confirmar_consulta(self):
        """Confirma a consulta selecionada"""
        if not self.medico_logado:
            messagebox.showerror("Erro", "Nenhum médico logado")
            return
            
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma consulta para confirmar")
            return
        
        consulta_id = self.tree.item(selecionado[0])['values'][0]
        messagebox.showinfo("Info", f"Consulta {consulta_id} confirmada (funcionalidade em desenvolvimento)")
    
    def marcar_realizada(self):
        """Marca a consulta como realizada"""
        if not self.medico_logado:
            messagebox.showerror("Erro", "Nenhum médico logado")
            return
            
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma consulta para marcar como realizada")
            return
        
        consulta_id = self.tree.item(selecionado[0])['values'][0]
        messagebox.showinfo("Info", f"Consulta {consulta_id} marcada como realizada (funcionalidade em desenvolvimento)")
    
    def cancelar_consulta(self):
        """Cancela a consulta selecionada"""
        if not self.medico_logado:
            messagebox.showerror("Erro", "Nenhum médico logado")
            return
            
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma consulta para cancelar")
            return
        
        consulta_id = self.tree.item(selecionado[0])['values'][0]
        messagebox.showinfo("Info", f"Consulta {consulta_id} cancelada (funcionalidade em desenvolvimento)")
    
    def voltar(self):
        """Volta para o menu do médico"""
        self.controller.abrir_menu_medico()