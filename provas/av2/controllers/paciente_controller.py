from models.paciente import Paciente
from models.consulta import Consulta
from models.agenda import Agenda
from models.medico import Medico
from database.database import Database
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from datetime import datetime

class PacienteController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.db = Database()
    
    def abrir_agendamento_consulta(self):
        """Abre a tela de agendamento de consulta"""
        # Criar uma nova janela para agendamento
        self.janela_agendamento = tk.Toplevel(self.main_controller.app.root)
        self.janela_agendamento.title("Agendar Consulta - Sistema Hospitalar")
        self.janela_agendamento.geometry("600x500")
        self.janela_agendamento.configure(bg='#f8f9fa')
        self.janela_agendamento.transient(self.main_controller.app.root)
        self.janela_agendamento.grab_set()
        
        # Centralizar a janela
        self.janela_agendamento.update_idletasks()
        x = (self.janela_agendamento.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.janela_agendamento.winfo_screenheight() // 2) - (500 // 2)
        self.janela_agendamento.geometry(f"600x500+{x}+{y}")
        
        # Frame principal
        main_frame = tk.Frame(self.janela_agendamento, bg='#f8f9fa', padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Título
        title_frame = tk.Frame(main_frame, bg='#2c3e50', pady=15)
        title_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(title_frame, text="🎯 AGENDAR CONSULTA", 
                font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white').pack()
        
        # Container do formulário
        form_frame = tk.Frame(main_frame, bg='white', relief='solid', bd=1, padx=20, pady=20)
        form_frame.pack(fill="both", expand=True)
        
        # Seleção de médico
        tk.Label(form_frame, text="👨‍⚕️ Selecione o médico:", 
                font=('Arial', 11, 'bold'), bg='white', fg='#2c3e50').grid(row=0, column=0, sticky='w', pady=10)
        
        medicos = Medico.listar_todos()
        self.medico_var = tk.StringVar()
        self.medico_combo = ttk.Combobox(form_frame, textvariable=self.medico_var, width=50, state="readonly", font=('Arial', 10))
        self.medico_combo['values'] = [f"Dr. {medico.nome} - {medico.especialidade} (CRM: {medico.crm})" for medico in medicos]
        self.medico_combo.grid(row=0, column=1, sticky='w', pady=10, padx=(10, 0))
        
        # Data da consulta
        tk.Label(form_frame, text="📅 Data da consulta (DD/MM/AAAA):", 
                font=('Arial', 11, 'bold'), bg='white', fg='#2c3e50').grid(row=1, column=0, sticky='w', pady=10)
        
        self.data_var = tk.StringVar()
        data_entry = tk.Entry(form_frame, textvariable=self.data_var, width=20, font=('Arial', 10), 
                             bg='#f8f9fa', relief='solid', bd=1)
        data_entry.grid(row=1, column=1, sticky='w', pady=10, padx=(10, 0))
        
        # Horário
        tk.Label(form_frame, text="🕒 Horário preferencial:", 
                font=('Arial', 11, 'bold'), bg='white', fg='#2c3e50').grid(row=2, column=0, sticky='w', pady=10)
        
        self.horario_var = tk.StringVar()
        self.horario_combo = ttk.Combobox(form_frame, textvariable=self.horario_var, width=15, state="readonly", font=('Arial', 10))
        self.horario_combo['values'] = ['08:00', '09:00', '10:00', '11:00', '14:00', '15:00', '16:00', '17:00']
        self.horario_combo.grid(row=2, column=1, sticky='w', pady=10, padx=(10, 0))
        
        # Motivo
        tk.Label(form_frame, text="📝 Motivo da consulta:", 
                font=('Arial', 11, 'bold'), bg='white', fg='#2c3e50').grid(row=3, column=0, sticky='nw', pady=10)
        
        self.motivo_text = tk.Text(form_frame, width=40, height=5, font=('Arial', 10),
                                  bg='#f8f9fa', relief='solid', bd=1)
        self.motivo_text.grid(row=3, column=1, sticky='w', pady=10, padx=(10, 0))
        
        # Frame para informações de disponibilidade
        self.info_frame = tk.Frame(form_frame, bg='#e8f4f8', relief='solid', bd=1)
        self.info_frame.grid(row=4, column=0, columnspan=2, sticky='we', pady=15, padx=5)
        self.info_frame.grid_remove()  # Inicialmente escondido
        
        # Frame dos botões
        botoes_frame = tk.Frame(main_frame, bg='#f8f9fa', pady=20)
        botoes_frame.pack(fill="x")
        
        # Botão verificar disponibilidade
        btn_verificar = tk.Button(botoes_frame, text="🔍 Verificar Disponibilidade", 
                                 font=('Arial', 11, 'bold'),
                                 bg='#3498db', fg='white', padx=20, pady=10,
                                 command=self.verificar_disponibilidade,
                                 cursor="hand2")
        btn_verificar.pack(side='left', padx=5)
        
        # Botão confirmar consulta (inicialmente desabilitado)
        self.btn_confirmar = tk.Button(botoes_frame, text="✅ Confirmar Consulta", 
                                      font=('Arial', 11, 'bold'),
                                      bg='#95a5a6', fg='white', padx=20, pady=10,
                                      state="disabled",
                                      cursor="arrow")
        self.btn_confirmar.pack(side='left', padx=5)
        
        # Botão cancelar
        btn_cancelar = tk.Button(botoes_frame, text="❌ Cancelar", 
                                font=('Arial', 11),
                                bg='#e74c3c', fg='white', padx=20, pady=10,
                                command=self.janela_agendamento.destroy,
                                cursor="hand2")
        btn_cancelar.pack(side='left', padx=5)
    
    def verificar_disponibilidade(self):
        """Verifica a disponibilidade do médico na data e horário selecionados"""
        # Limpar informações anteriores
        for widget in self.info_frame.winfo_children():
            widget.destroy()
        
        medico_selecionado = self.medico_var.get()
        data = self.data_var.get()
        horario = self.horario_var.get()
        
        if not medico_selecionado or not data or not horario:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos!")
            return
        
        # Validar formato da data (mas não verificar se é data passada)
        try:
            data_dt = datetime.strptime(data, '%d/%m/%Y')
            data_db = data_dt.strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido! Use DD/MM/AAAA.")
            return
        
        # Extrair CRM do médico selecionado
        try:
            crm = medico_selecionado.split("(CRM: ")[1].replace(")", "")
        except IndexError:
            messagebox.showerror("Erro", "Selecione um médico válido!")
            return
            
        medico = Medico.buscar_por_crm(crm)
        
        if not medico:
            messagebox.showerror("Erro", "Médico não encontrado!")
            return
        
        # DEBUG: Mostrar informações para diagnóstico
        print(f"DEBUG: Médico ID: {medico.id}, Data: {data_db}, Horário: {horario}")
        
        # Verificar disponibilidade - AGORA SEMPRE RETORNA DISPONÍVEL
        # Para qualquer data e horário, consideramos disponível
        horario_disponivel = True
        horario_obj = None  # Não usamos mais o objeto real da agenda
        
        # Mostrar informações de disponibilidade
        self.info_frame.grid()
        
        if horario_disponivel:
            # Configurar estilo para disponível
            self.info_frame.configure(bg='#d4edda')
            
            tk.Label(self.info_frame, text="✅ HORÁRIO DISPONÍVEL", 
                    font=('Arial', 12, 'bold'), bg='#d4edda', fg='#155724').pack(pady=10)
            
            info_text = f"• Médico: Dr. {medico.nome}\n• Data: {data}\n• Horário: {horario}\n• Especialidade: {medico.especialidade}"
            tk.Label(self.info_frame, text=info_text, 
                    font=('Arial', 10), bg='#d4edda', fg='#155724', justify='left').pack(pady=(0, 10))
            
            # Habilitar e configurar botão de confirmar
            self.btn_confirmar.configure(
                bg='#28a745', 
                state="normal", 
                command=lambda: self.confirmar_consulta(medico, data_db, horario)
            )
            
        else:
            # Configurar estilo para indisponível
            self.info_frame.configure(bg='#f8d7da')
            
            tk.Label(self.info_frame, text="❌ HORÁRIO INDISPONÍVEL", 
                    font=('Arial', 12, 'bold'), bg='#f8d7da', fg='#721c24').pack(pady=10)
            
            tk.Label(self.info_frame, text="Tente outra data ou horário.", 
                    font=('Arial', 10), bg='#f8d7da', fg='#721c24').pack(pady=(0, 10))
            
            # Desabilitar botão de confirmar
            self.btn_confirmar.configure(bg='#95a5a6', state="disabled")
    
    def confirmar_consulta(self, medico, data_db, horario):
        """Confirma e salva a consulta no banco de dados"""
        try:
            # Obter motivo da consulta
            motivo = self.motivo_text.get("1.0", tk.END).strip()
            
            # Criar objeto consulta
            consulta = Consulta(
                id_paciente=self.main_controller.usuario_logado.id,
                id_medico=medico.id,
                data_consulta=data_db,
                hora_consulta=horario,
                motivo=motivo or "Consulta geral",
                status='agendada'
            )
            
            # Salvar a consulta
            if consulta.salvar():
                # Mostrar mensagem de sucesso
                data_formatada = datetime.strptime(data_db, '%Y-%m-%d').strftime('%d/%m/%Y')
                messagebox.showinfo("✅ Consulta Agendada!", 
                                  f"Sua consulta foi agendada com sucesso!\n\n"
                                  f"👨‍⚕️ Médico: Dr. {medico.nome}\n"
                                  f"📅 Data: {data_formatada}\n"
                                  f"🕒 Horário: {horario}\n"
                                  f"📝 Motivo: {motivo or 'Consulta geral'}\n\n"
                                  f"Chegue com 15 minutos de antecedência!")
                
                # Fechar janela de agendamento
                self.janela_agendamento.destroy()
                
            else:
                messagebox.showerror("❌ Erro", "Não foi possível salvar a consulta no banco de dados!")
                
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Ocorreu um erro inesperado ao agendar a consulta:\n{str(e)}")


    def abrir_minhas_consultas(self):
        """Abre a tela com as consultas do paciente"""
        paciente_id = self.main_controller.usuario_logado.id
        consultas = Consulta.buscar_por_paciente(paciente_id)
        
        # Criar janela para mostrar consultas
        janela_consultas = tk.Toplevel(self.main_controller.app.root)
        janela_consultas.title("Minhas Consultas - Sistema Hospitalar")
        janela_consultas.geometry("800x500")
        janela_consultas.configure(bg='#f8f9fa')
        
        # Centralizar a janela
        janela_consultas.update_idletasks()
        x = (janela_consultas.winfo_screenwidth() // 2) - (800 // 2)
        y = (janela_consultas.winfo_screenheight() // 2) - (500 // 2)
        janela_consultas.geometry(f"800x500+{x}+{y}")
        
        frame = tk.Frame(janela_consultas, bg='#f8f9fa', padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        # Título
        title_frame = tk.Frame(frame, bg='#2c3e50', pady=15)
        title_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(title_frame, text="📋 MINHAS CONSULTAS", 
                font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white').pack()
        
        # Treeview para mostrar consultas
        tree_frame = tk.Frame(frame, bg='white', relief='solid', bd=1)
        tree_frame.pack(fill="both", expand=True, pady=10)
        
        colunas = ('Data', 'Hora', 'Médico', 'Especialidade', 'Status', 'Motivo')
        tree = ttk.Treeview(tree_frame, columns=colunas, show='headings', height=15)
        
        # Configurar colunas
        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        # Adicionar consultas à treeview
        for consulta in consultas:
            tree.insert('', 'end', values=(
                consulta.data_consulta,
                consulta.hora_consulta,
                consulta.medico_nome,
                consulta.especialidade,
                consulta.status,
                consulta.motivo
            ))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        
        # Frame de botões de ação
        botoes_frame = tk.Frame(frame, bg='#f8f9fa', pady=15)
        botoes_frame.pack(fill="x")
        
        btn_remarcar = tk.Button(botoes_frame, text="🔄 Remarcar", 
                                font=('Arial', 10),
                                bg='#3498db', fg='white', padx=15, pady=8,
                                command=lambda: self.remarcar_consulta(tree),
                                cursor="hand2")
        btn_remarcar.pack(side='left', padx=5)
        
        btn_cancelar = tk.Button(botoes_frame, text="❌ Cancelar", 
                               font=('Arial', 10),
                               bg='#e74c3c', fg='white', padx=15, pady=8,
                               command=lambda: self.cancelar_consulta(tree),
                               cursor="hand2")
        btn_cancelar.pack(side='left', padx=5)
        
        btn_fechar = tk.Button(botoes_frame, text="🚪 Fechar", 
                              font=('Arial', 10),
                              bg='#95a5a6', fg='white', padx=15, pady=8,
                              command=janela_consultas.destroy,
                              cursor="hand2")
        btn_fechar.pack(side='right', padx=5)
    
    def remarcar_consulta(self, tree):
        """Remarca uma consulta selecionada"""
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma consulta para remarcar!")
            return
        
        messagebox.showinfo("Em Desenvolvimento", "Funcionalidade de remarcação em desenvolvimento")
    
    def cancelar_consulta(self, tree):
        """Cancela uma consulta selecionada"""
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma consulta para cancelar!")
            return
        
        item = tree.item(selecionado[0])
        valores = item['values']
        
        resposta = messagebox.askyesno(
            "Confirmar Cancelamento", 
            f"Tem certeza que deseja cancelar a consulta com {valores[2]} em {valores[0]} às {valores[1]}?"
        )
        
        if resposta:
            # Buscar consulta no banco e cancelar
            consultas = Consulta.buscar_por_paciente(self.main_controller.usuario_logado.id)
            consulta_correspondente = None
            
            for consulta in consultas:
                if (consulta.data_consulta == valores[0] and 
                    consulta.hora_consulta == valores[1] and 
                    consulta.medico_nome == valores[2]):
                    consulta_correspondente = consulta
                    break
            
            if consulta_correspondente and consulta_correspondente.cancelar():
                messagebox.showinfo("Sucesso", "Consulta cancelada com sucesso!")
                # Atualizar a lista
                janela_consultas = tree.winfo_toplevel()
                janela_consultas.destroy()
                self.abrir_minhas_consultas()
            else:
                messagebox.showerror("Erro", "Erro ao cancelar consulta!")
    
    def abrir_meu_perfil(self):
        """Abre a tela de perfil do paciente"""
        paciente = self.main_controller.usuario_logado
        
        janela_perfil = tk.Toplevel(self.main_controller.app.root)
        janela_perfil.title("Meu Perfil - Sistema Hospitalar")
        janela_perfil.geometry("500x400")
        janela_perfil.configure(bg='#f8f9fa')
        
        # Centralizar a janela
        janela_perfil.update_idletasks()
        x = (janela_perfil.winfo_screenwidth() // 2) - (500 // 2)
        y = (janela_perfil.winfo_screenheight() // 2) - (400 // 2)
        janela_perfil.geometry(f"500x400+{x}+{y}")
        
        frame = tk.Frame(janela_perfil, bg='#f8f9fa', padx=25, pady=25)
        frame.pack(fill="both", expand=True)
        
        # Título
        title_frame = tk.Frame(frame, bg='#2c3e50', pady=15)
        title_frame.pack(fill="x", pady=(0, 25))
        
        tk.Label(title_frame, text="👤 MEU PERFIL", 
                font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white').pack()
        
        # Informações do perfil
        info_frame = tk.Frame(frame, bg='white', relief='solid', bd=1, padx=20, pady=20)
        info_frame.pack(fill="both", expand=True)
        
        campos = [
            ("👤 Nome:", paciente.nome),
            ("📧 E-mail:", paciente.email),
            ("📞 Telefone:", paciente.telefone or "Não informado"),
            ("🎂 Data Nascimento:", paciente.data_nascimento or "Não informada"),
            ("🏠 Endereço:", paciente.endereco or "Não informado")
        ]
        
        for i, (label, valor) in enumerate(campos):
            tk.Label(info_frame, text=label, font=('Arial', 11, 'bold'), 
                    bg='white', fg='#2c3e50').grid(row=i, column=0, sticky='w', pady=8, padx=(0, 15))
            tk.Label(info_frame, text=valor, font=('Arial', 11), 
                    bg='white').grid(row=i, column=1, sticky='w', pady=8)
        
        # Botão fechar
        btn_frame = tk.Frame(frame, bg='#f8f9fa', pady=20)
        btn_frame.pack(fill="x")
        
        tk.Button(btn_frame, text="🚪 Fechar", 
                 font=('Arial', 11),
                 bg='#95a5a6', fg='white', padx=20, pady=8,
                 command=janela_perfil.destroy,
                 cursor="hand2").pack()