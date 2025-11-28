# views/paciente/meus_prontuarios_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class MeusProntuariosView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.frame = tk.Frame(root, bg='#f0f0f0')
        
        self.prontuarios = []  # Lista para armazenar prontuários reais
        
        self._criar_widgets()
    
    def _criar_widgets(self):
        # Título
        titulo = tk.Label(
            self.frame, 
            text="MEUS PRONTUÁRIOS",
            font=('Arial', 18, 'bold'),
            fg='#2E7D32',
            bg='#f0f0f0'
        )
        titulo.pack(pady=(30, 20))
        
        # Container da lista
        lista_frame = tk.Frame(self.frame, bg='#f0f0f0')
        lista_frame.pack(pady=20, padx=50, fill='both', expand=True)
        
        # Cabeçalho
        cabecalho = tk.Frame(lista_frame, bg='#2E7D32')
        cabecalho.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            cabecalho,
            text="Data",
            font=('Arial', 10, 'bold'),
            bg='#2E7D32',
            fg='white',
            width=12
        ).pack(side='left', padx=5, pady=5)
        
        tk.Label(
            cabecalho,
            text="Médico",
            font=('Arial', 10, 'bold'),
            bg='#2E7D32',
            fg='white',
            width=20
        ).pack(side='left', padx=5, pady=5)
        
        tk.Label(
            cabecalho,
            text="Especialidade",
            font=('Arial', 10, 'bold'),
            bg='#2E7D32',
            fg='white',
            width=20
        ).pack(side='left', padx=5, pady=5)
        
        tk.Label(
            cabecalho,
            text="Status",
            font=('Arial', 10, 'bold'),
            bg='#2E7D32',
            fg='white',
            width=15
        ).pack(side='left', padx=5, pady=5)
        
        tk.Label(
            cabecalho,
            text="Ações",
            font=('Arial', 10, 'bold'),
            bg='#2E7D32',
            fg='white',
            width=15
        ).pack(side='left', padx=5, pady=5)
        
        # Container com scrollbar
        container = tk.Frame(lista_frame)
        container.pack(fill='both', expand=True)
        
        self.canvas = tk.Canvas(container, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#f0f0f0')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botões
        botoes_frame = tk.Frame(self.frame, bg='#f0f0f0')
        botoes_frame.pack(pady=30)
        
        tk.Button(
            botoes_frame,
            text="🔄 ATUALIZAR",
            font=('Arial', 12),
            bg='#2196F3',
            fg='white',
            width=15,
            command=self.carregar_prontuarios
        ).pack(side='left', padx=10)
        
        tk.Button(
            botoes_frame,
            text="↩️ VOLTAR",
            font=('Arial', 12),
            bg='#757575',
            fg='white',
            width=15,
            command=self.voltar
        ).pack(side='left', padx=10)
    
    def carregar_prontuarios(self):
        """Carrega os prontuários reais do paciente do banco de dados"""
        try:
            # Obter paciente logado
            paciente = self.controller.obter_usuario_logado()
            if not paciente:
                messagebox.showerror("Erro", "Nenhum paciente logado")
                return
            
            # Buscar consultas do paciente (vamos filtrar por status depois)
            consultas = self.controller.buscar_consultas_por_paciente(paciente.id)
            
            # Filtrar apenas consultas com prontuário (realizadas)
            consultas_com_prontuario = []
            for consulta in consultas:
                # Verificar se a consulta tem informações de prontuário
                if (hasattr(consulta, 'observacoes_medicas') and consulta.observacoes_medicas) or \
                   (hasattr(consulta, 'diagnostico') and consulta.diagnostico) or \
                   (hasattr(consulta, 'prescricao') and consulta.prescricao) or \
                   consulta.status == 'realizada':
                    consultas_com_prontuario.append(consulta)
            
            # Converter objetos Consulta para o formato esperado pela view
            prontuarios_formatados = []
            for consulta in consultas_com_prontuario:
                # Buscar informações do médico
                medico = self.controller.buscar_medico_por_id(consulta.id_medico)
                medico_nome = medico.nome if medico else "Médico não encontrado"
                especialidade = medico.especialidade if medico else "N/A"
                
                # Formatar dados do prontuário
                prontuario_formatado = {
                    'id': consulta.id,
                    'data': consulta.data_consulta,
                    'medico': medico_nome,
                    'especialidade': especialidade,
                    'status': consulta.status.capitalize(),
                    'observacoes': consulta.observacoes_medicas or "Nenhuma observação registrada",
                    'diagnostico': consulta.diagnostico or "Nenhum diagnóstico registrado",
                    'prescricao': consulta.prescricao or "Nenhuma prescrição registrada"
                }
                prontuarios_formatados.append(prontuario_formatado)
            
            self.prontuarios = prontuarios_formatados
            
            # Atualizar a lista
            self._preencher_lista()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar prontuários: {str(e)}")
    
    def _preencher_lista(self):
        # Limpar o frame (se houver itens anteriores)
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Verificar se há prontuários
        if not self.prontuarios:
            sem_prontuarios_label = tk.Label(
                self.scrollable_frame,
                text="Nenhum prontuário encontrado",
                font=('Arial', 12),
                bg='#f0f0f0',
                fg='#757575'
            )
            sem_prontuarios_label.pack(pady=20)
            return
        
        # Adicionar cada prontuário na lista
        for i, prontuario in enumerate(self.prontuarios):
            linha = tk.Frame(self.scrollable_frame, bg='#ffffff' if i % 2 == 0 else '#f9f9f9')
            linha.pack(fill='x', pady=2)
            
            tk.Label(
                linha,
                text=prontuario['data'],
                font=('Arial', 10),
                bg=linha.cget('bg'),
                width=12
            ).pack(side='left', padx=5, pady=5)
            
            tk.Label(
                linha,
                text=prontuario['medico'],
                font=('Arial', 10),
                bg=linha.cget('bg'),
                width=20
            ).pack(side='left', padx=5, pady=5)
            
            tk.Label(
                linha,
                text=prontuario['especialidade'],
                font=('Arial', 10),
                bg=linha.cget('bg'),
                width=20
            ).pack(side='left', padx=5, pady=5)
            
            # Status com cor
            cor_status = {
                'Realizada': '#4CAF50',
                'Agendada': '#FFA000',
                'Confirmada': '#2196F3',
                'Cancelada': '#F44336'
            }.get(prontuario['status'], '#757575')
            
            tk.Label(
                linha,
                text=prontuario['status'],
                font=('Arial', 10, 'bold'),
                fg=cor_status,
                bg=linha.cget('bg'),
                width=15
            ).pack(side='left', padx=5, pady=5)
            
            # Ações (botões)
            acoes_frame = tk.Frame(linha, bg=linha.cget('bg'))
            acoes_frame.pack(side='left', padx=5, pady=5)
            
            tk.Button(
                acoes_frame,
                text="👁️ VER",
                font=('Arial', 8),
                bg='#2196F3',
                fg='white',
                width=8,
                command=lambda p=prontuario: self.ver_detalhes_prontuario(p)
            ).pack(side='left', padx=2)
    
    def ver_detalhes_prontuario(self, prontuario):
        """Abre uma janela com os detalhes completos do prontuário"""
        # Criar uma nova janela
        detalhes_window = tk.Toplevel(self.frame)
        detalhes_window.title(f"Prontuário - {prontuario['data']}")
        detalhes_window.geometry("600x500")
        detalhes_window.configure(bg='#f0f0f0')
        detalhes_window.transient(self.frame)
        detalhes_window.grab_set()
        
        # Título
        titulo = tk.Label(
            detalhes_window,
            text="DETALHES DO PRONTUÁRIO",
            font=('Arial', 16, 'bold'),
            fg='#2E7D32',
            bg='#f0f0f0'
        )
        titulo.pack(pady=(20, 10))
        
        # Container dos detalhes
        container = tk.Frame(detalhes_window, bg='#f0f0f0')
        container.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Informações básicas
        info_frame = tk.Frame(container, bg='#f0f0f0')
        info_frame.pack(fill='x', pady=10)
        
        # Data
        tk.Label(
            info_frame,
            text="Data da Consulta:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=0, column=0, sticky='w', pady=5)
        
        tk.Label(
            info_frame,
            text=prontuario['data'],
            font=('Arial', 10),
            bg='#f0f0f0'
        ).grid(row=0, column=1, sticky='w', pady=5, padx=10)
        
        # Médico
        tk.Label(
            info_frame,
            text="Médico:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=1, column=0, sticky='w', pady=5)
        
        tk.Label(
            info_frame,
            text=prontuario['medico'],
            font=('Arial', 10),
            bg='#f0f0f0'
        ).grid(row=1, column=1, sticky='w', pady=5, padx=10)
        
        # Especialidade
        tk.Label(
            info_frame,
            text="Especialidade:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=2, column=0, sticky='w', pady=5)
        
        tk.Label(
            info_frame,
            text=prontuario['especialidade'],
            font=('Arial', 10),
            bg='#f0f0f0'
        ).grid(row=2, column=1, sticky='w', pady=5, padx=10)
        
        # Status
        tk.Label(
            info_frame,
            text="Status:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=3, column=0, sticky='w', pady=5)
        
        cor_status = '#4CAF50' if prontuario['status'] == 'Realizada' else '#757575'
        tk.Label(
            info_frame,
            text=prontuario['status'],
            font=('Arial', 10, 'bold'),
            fg=cor_status,
            bg='#f0f0f0'
        ).grid(row=3, column=1, sticky='w', pady=5, padx=10)
        
        # Separador
        separator = ttk.Separator(container, orient='horizontal')
        separator.pack(fill='x', pady=10)
        
        # Observações médicas
        tk.Label(
            container,
            text="Observações Médicas:",
            font=('Arial', 11, 'bold'),
            bg='#f0f0f0'
        ).pack(anchor='w', pady=(10, 5))
        
        observacoes_text = tk.Text(
            container,
            font=('Arial', 10),
            width=60,
            height=4,
            wrap='word',
            bg='#ffffff',
            relief='solid',
            borderwidth=1
        )
        observacoes_text.pack(fill='x', padx=10, pady=5)
        observacoes_text.insert('1.0', prontuario['observacoes'])
        observacoes_text.config(state='disabled')
        
        # Diagnóstico
        tk.Label(
            container,
            text="Diagnóstico:",
            font=('Arial', 11, 'bold'),
            bg='#f0f0f0'
        ).pack(anchor='w', pady=(10, 5))
        
        diagnostico_text = tk.Text(
            container,
            font=('Arial', 10),
            width=60,
            height=3,
            wrap='word',
            bg='#ffffff',
            relief='solid',
            borderwidth=1
        )
        diagnostico_text.pack(fill='x', padx=10, pady=5)
        diagnostico_text.insert('1.0', prontuario['diagnostico'])
        diagnostico_text.config(state='disabled')
        
        # Prescrição médica
        tk.Label(
            container,
            text="Prescrição Médica:",
            font=('Arial', 11, 'bold'),
            bg='#f0f0f0'
        ).pack(anchor='w', pady=(10, 5))
        
        prescricao_text = tk.Text(
            container,
            font=('Arial', 10),
            width=60,
            height=4,
            wrap='word',
            bg='#ffffff',
            relief='solid',
            borderwidth=1
        )
        prescricao_text.pack(fill='x', padx=10, pady=5)
        prescricao_text.insert('1.0', prontuario['prescricao'])
        prescricao_text.config(state='disabled')
        
        # Botão Fechar
        tk.Button(
            detalhes_window,
            text="FECHAR",
            font=('Arial', 12),
            bg='#757575',
            fg='white',
            width=15,
            command=detalhes_window.destroy
        ).pack(pady=20)
    
    def voltar(self):
        self.controller.mostrar_menu_paciente()
    
    def mostrar(self):
        """Mostra a view e carrega os prontuários atualizados"""
        self.carregar_prontuarios()
        self.frame.pack(fill="both", expand=True)
    
    def ocultar(self):
        self.frame.pack_forget()