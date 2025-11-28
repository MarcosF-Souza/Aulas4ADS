# views/consulta/agendar_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class AgendarConsultaView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.frame = tk.Frame(root, bg='#f0f0f0')
        
        self._criar_widgets()
    
    def _criar_widgets(self):
        # Título
        titulo = tk.Label(
            self.frame, 
            text="AGENDAR CONSULTA",
            font=('Arial', 18, 'bold'),
            fg='#2E7D32',
            bg='#f0f0f0'
        )
        titulo.pack(pady=(30, 20))
        
        # Container do formulário
        form_frame = tk.Frame(self.frame, bg='#f0f0f0')
        form_frame.pack(pady=20, padx=50, fill='x')
        
        # Médico
        tk.Label(
            form_frame,
            text="Médico:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=0, column=0, sticky='w', pady=10)
        
        self.medico_var = tk.StringVar()
        self.combo_medico = ttk.Combobox(
            form_frame,
            textvariable=self.medico_var,
            font=('Arial', 10),
            state='readonly',
            width=40
        )
        self.combo_medico.grid(row=0, column=1, pady=10, padx=10)

        # Preencher com médicos (vamos simular por enquanto)
        self.carregar_medicos()
        
        # Data
        tk.Label(
            form_frame,
            text="Data:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=1, column=0, sticky='w', pady=10)
        
        self.data_var = tk.StringVar()
        self.entry_data = tk.Entry(
            form_frame,
            textvariable=self.data_var,
            font=('Arial', 10),
            width=42
        )
        self.entry_data.grid(row=1, column=1, pady=10, padx=10)
        # Sugerir data de amanhã
        amanha = (datetime.now() + timedelta(days=1)).strftime('%d/%m/%Y')
        self.entry_data.insert(0, amanha)
        
        # Hora
        tk.Label(
            form_frame,
            text="Hora:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=2, column=0, sticky='w', pady=10)
        
        self.hora_var = tk.StringVar()
        self.combo_hora = ttk.Combobox(
            form_frame,
            textvariable=self.hora_var,
            font=('Arial', 10),
            state='readonly',
            width=40
        )
        self.combo_hora.grid(row=2, column=1, pady=10, padx=10)
        # Preencher horários
        self.combo_hora['values'] = ['08:00', '09:00', '10:00', '11:00', '14:00', '15:00', '16:00', '17:00']
        
        # Motivo
        tk.Label(
            form_frame,
            text="Motivo:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).grid(row=3, column=0, sticky='w', pady=10)
        
        self.motivo_var = tk.StringVar()
        self.entry_motivo = tk.Entry(
            form_frame,
            textvariable=self.motivo_var,
            font=('Arial', 10),
            width=42
        )
        self.entry_motivo.grid(row=3, column=1, pady=10, padx=10)
        
        # Botões
        botoes_frame = tk.Frame(self.frame, bg='#f0f0f0')
        botoes_frame.pack(pady=30)
        
        tk.Button(
            botoes_frame,
            text="✅ AGENDAR",
            font=('Arial', 12, 'bold'),
            bg='#4CAF50',
            fg='white',
            width=15,
            command=self.agendar_consulta
        ).grid(row=0, column=0, padx=10)
        
        tk.Button(
            botoes_frame,
            text="↩️ VOLTAR",
            font=('Arial', 12),
            bg='#757575',
            fg='white',
            width=15,
            command=self.voltar
        ).grid(row=0, column=1, padx=10)
    
    def agendar_consulta(self):
        medico_selecionado = self.medico_var.get()
        data = self.data_var.get()
        hora = self.hora_var.get()
        motivo = self.motivo_var.get()
        
        if not medico_selecionado or not data or not hora or not motivo:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return
        
        try:
            # Converter data de DD/MM/AAAA para AAAA-MM-DD
            data_obj = datetime.strptime(data, '%d/%m/%Y')
            data_formatada = data_obj.strftime('%Y-%m-%d')
            
            # Verificar se data não é no passado
            if data_obj.date() < datetime.now().date():
                messagebox.showerror("Erro", "Não é possível agendar consultas para datas passadas.")
                return
                
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido. Use DD/MM/AAAA.")
            return
        
        # Mapear nome do médico para ID (simulação - na prática viria do controller)
            # ✅ CORREÇÃO: Obter ID do médico através do controller
        id_medico = self.controller.obter_id_medico_por_nome(medico_selecionado)
        if not id_medico:
            messagebox.showerror("Erro", "Médico selecionado inválido.")
            return
        
        # Obter ID do paciente logado
        paciente_logado = self.controller.obter_usuario_logado()
        if not paciente_logado or not hasattr(paciente_logado, 'id'):
            messagebox.showerror("Erro", "Nenhum paciente logado ou sessão inválida.")
            return
        
        id_paciente = paciente_logado.id
        
        # ✅ CORREÇÃO: Chamar o controller para agendar a consulta
        sucesso, mensagem, consulta = self.controller.agendar_consulta(
            id_paciente=id_paciente,
            id_medico=id_medico,
            data_consulta=data_formatada,
            hora_consulta=hora,
            motivo=motivo
        )
        
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.voltar()
        else:
            messagebox.showerror("Erro", mensagem)
    
    def voltar(self):
        self.controller.mostrar_menu_paciente()
    
    def mostrar(self):
        self.frame.pack(fill="both", expand=True)
    
    def ocultar(self):
        self.frame.pack_forget()

    def carregar_medicos(self):
        """Carrega a lista de médicos do controller"""
        try:
            medicos = self.controller.obter_medicos_para_combobox()
            if medicos:
                self.combo_medico['values'] = medicos
                # Selecionar o primeiro médico por padrão
                self.combo_medico.set(medicos[0])
            else:
                self.combo_medico['values'] = ['Nenhum médico disponível']
                messagebox.showwarning("Aviso", "Nenhum médico cadastrado no sistema.")
        except Exception as e:
            print(f"Erro ao carregar médicos: {e}")
            self.combo_medico['values'] = ['Erro ao carregar médicos']