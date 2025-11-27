from models.paciente import Paciente
from models.consulta import Consulta
from models.agenda import Agenda
from models.medico import Medico
from database.database import Database
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

class PacienteController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.db = Database()
        self.consulta_em_agendamento = None
        self.medico_selecionado = None
        self.data_selecionada = None
        self.horario_selecionado = None
        self.passo_atual = 0  # Controlar o passo atual
    
    def abrir_agendamento_consulta(self):
        """Abre a tela de agendamento de consulta com interface moderna"""
        # Criar uma nova janela para agendamento
        self.janela_agendamento = tk.Toplevel(self.main_controller.app.root)
        self.janela_agendamento.title("Agendar Consulta - Sistema Médico")
        self.janela_agendamento.geometry("900x700")  # Aumentei um pouco o tamanho
        self.janela_agendamento.configure(bg='#f0f2f5')
        self.janela_agendamento.transient(self.main_controller.app.root)
        self.janela_agendamento.grab_set()
        
        # Centralizar a janela
        self.janela_agendamento.update_idletasks()
        x = (self.janela_agendamento.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.janela_agendamento.winfo_screenheight() // 2) - (700 // 2)
        self.janela_agendamento.geometry(f"900x700+{x}+{y}")
        
        # Frame principal
        main_frame = tk.Frame(self.janela_agendamento, bg='#f0f2f5', padx=25, pady=25)
        main_frame.pack(fill="both", expand=True)
        
        # Cabeçalho
        header_frame = tk.Frame(main_frame, bg='#2c3e50', pady=20, relief='raised', bd=2)
        header_frame.pack(fill="x", pady=(0, 25))
        
        tk.Label(header_frame, text="🎯 AGENDAR CONSULTA MÉDICA", 
                font=('Arial', 20, 'bold'), bg='#2c3e50', fg='white').pack()
        
        tk.Label(header_frame, text="Siga os passos abaixo para agendar sua consulta", 
                font=('Arial', 11), bg='#2c3e50', fg='#ecf0f1').pack()
        
        # Container dos passos
        self.container_passos = tk.Frame(main_frame, bg='#f0f2f5')
        self.container_passos.pack(fill="both", expand=True)
        
        # Barra de progresso
        self.criar_barra_progresso()
        
        # Iniciar com a seleção do médico
        self.passo_atual = 0
        self.mostrar_passo_1_selecionar_medico()
    
    def criar_barra_progresso(self):
        """Cria a barra de progresso dos passos"""
        progress_frame = tk.Frame(self.container_passos, bg='#f0f2f5', pady=25)
        progress_frame.pack(fill="x")
        
        passos = ["1. Escolher Médico", "2. Escolher Data", "3. Escolher Horário", "4. Confirmar"]
        self.labels_passos = []
        
        for i, passo in enumerate(passos):
            frame_passo = tk.Frame(progress_frame, bg='#f0f2f5')
            frame_passo.pack(side="left", expand=True)
            
            # Círculo do passo
            canvas = tk.Canvas(frame_passo, width=35, height=35, bg='#f0f2f5', highlightthickness=0)
            canvas.pack()
            cor = '#3498db' if i == 0 else '#bdc3c7'
            canvas.create_oval(5, 5, 30, 30, fill=cor, outline=cor, width=2)
            canvas.create_text(17.5, 17.5, text=str(i+1), fill='white', font=('Arial', 11, 'bold'))
            
            # Label do passo
            label = tk.Label(frame_passo, text=passo, font=('Arial', 10, 'bold'), bg='#f0f2f5', 
                           fg=cor if i == 0 else '#95a5a6')
            label.pack(pady=(8, 0))
            self.labels_passos.append((canvas, label))
            
            # Linha conectora (exceto para o último)
            if i < len(passos) - 1:
                linha = tk.Canvas(frame_passo, width=40, height=2, bg='#f0f2f5', highlightthickness=0)
                linha.pack(side="left", padx=5, pady=15)
                linha.create_line(0, 1, 40, 1, fill='#bdc3c7', width=2)
    
    def atualizar_barra_progresso(self, passo_atual):
        """Atualiza a barra de progresso"""
        self.passo_atual = passo_atual
        for i, (canvas, label) in enumerate(self.labels_passos):
            cor_canvas = '#27ae60' if i < passo_atual else ('#3498db' if i == passo_atual else '#bdc3c7')
            cor_texto = '#27ae60' if i < passo_atual else ('#3498db' if i == passo_atual else '#95a5a6')
            
            canvas.delete("all")
            canvas.create_oval(5, 5, 30, 30, fill=cor_canvas, outline=cor_canvas, width=2)
            canvas.create_text(17.5, 17.5, text=str(i+1), fill='white', font=('Arial', 11, 'bold'))
            
            label.configure(fg=cor_texto)
    
    def limpar_container_passos(self):
        """Limpa o container de passos, mantendo apenas a barra de progresso"""
        for widget in self.container_passos.winfo_children()[1:]:  # Mantém a barra de progresso
            widget.destroy()
    
    def criar_botao_estilizado(self, parent, texto, comando, cor='#3498db', lado='right', desabilitado=False):
        """Cria um botão estilizado consistentemente"""
        if desabilitado:
            botao = tk.Button(parent, text=texto, 
                            font=('Arial', 11, 'bold'),
                            bg='#bdc3c7', fg='white', 
                            padx=25, pady=12,
                            state='disabled',
                            cursor="arrow")
        else:
            botao = tk.Button(parent, text=texto, 
                            font=('Arial', 11, 'bold'),
                            bg=cor, fg='white', 
                            padx=25, pady=12,
                            command=comando,
                            cursor="hand2",
                            relief='raised',
                            bd=2)
        
        botao.pack(side=lado, padx=10)
        return botao
    
    def mostrar_passo_1_selecionar_medico(self):
        """Passo 1: Seleção do médico"""
        self.atualizar_barra_progresso(0)
        self.limpar_container_passos()
        
        # Frame do conteúdo
        content_frame = tk.Frame(self.container_passos, bg='#f0f2f5')
        content_frame.pack(fill="both", expand=True, pady=20)
        
        tk.Label(content_frame, text="👨‍⚕️ ESCOLHA SEU MÉDICO", 
                font=('Arial', 18, 'bold'), bg='#f0f2f5', fg='#2c3e50').pack(pady=(0, 20))
        
        # Frame da lista de médicos
        lista_frame = tk.Frame(content_frame, bg='white', relief='solid', bd=1)
        lista_frame.pack(fill="both", expand=True, pady=10)
        
        # Treeview para médicos com estilo melhorado
        style = ttk.Style()
        style.configure("Custom.Treeview", 
                       background="white",
                       foreground="black",
                       rowheight=28,
                       fieldbackground="white",
                       font=('Arial', 10))
        style.configure("Custom.Treeview.Heading", 
                       font=('Arial', 11, 'bold'),
                       background='#34495e',
                       foreground='white')
        style.map("Custom.Treeview", background=[('selected', '#3498db')])
        
        colunas = ('Nome', 'Especialidade', 'CRM', 'Telefone')
        self.tree_medicos = ttk.Treeview(lista_frame, columns=colunas, show='headings', 
                                        style="Custom.Treeview", height=12, selectmode='browse')
        
        # Configurar colunas
        larguras = [200, 180, 120, 150]
        for i, col in enumerate(colunas):
            self.tree_medicos.heading(col, text=col, anchor='w')
            self.tree_medicos.column(col, width=larguras[i], anchor='w')
        
        # Carregar médicos
        medicos = Medico.listar_todos()
        for medico in medicos:
            self.tree_medicos.insert('', 'end', values=(
                medico.nome,
                medico.especialidade,
                medico.crm,
                medico.telefone or '📞 Não informado'
            ), tags=(medico.id,))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=self.tree_medicos.yview)
        self.tree_medicos.configure(yscrollcommand=scrollbar.set)
        
        self.tree_medicos.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        
        # Frame dos botões
        botoes_frame = tk.Frame(content_frame, bg='#f0f2f5', pady=25)
        botoes_frame.pack(fill="x")
        
        # Botão avançar - inicialmente desabilitado
        self.btn_avancar_medico = self.criar_botao_estilizado(
            botoes_frame, "➡️ AVANÇAR PARA DATA", self.avancar_para_data, '#3498db', 'right', True
        )
        
        self.criar_botao_estilizado(
            botoes_frame, "❌ CANCELAR", self.janela_agendamento.destroy, '#e74c3c', 'right'
        )
        
        # Bind para habilitar botão quando selecionar médico
        self.tree_medicos.bind('<<TreeviewSelect>>', self.on_medico_selecionado)
    
    def on_medico_selecionado(self, event):
        """Habilita o botão avançar quando um médico é selecionado"""
        selecionado = self.tree_medicos.selection()
        if selecionado:
            self.btn_avancar_medico.configure(bg='#3498db', state='normal', command=self.avancar_para_data)
        else:
            self.btn_avancar_medico.configure(bg='#bdc3c7', state='disabled')
    
    def avancar_para_data(self):
        """Avança para o passo de seleção de data"""
        selecionado = self.tree_medicos.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Por favor, selecione um médico para continuar!")
            return
        
        # Obter médico selecionado
        item = self.tree_medicos.item(selecionado[0])
        medico_id = item['tags'][0] if item['tags'] else None
        
        if not medico_id:
            messagebox.showerror("Erro", "Médico não encontrado!")
            return
        
        # Buscar médico
        self.medico_selecionado = None
        medicos = Medico.listar_todos()
        for medico in medicos:
            if medico.id == medico_id:
                self.medico_selecionado = medico
                break
        
        if not self.medico_selecionado:
            messagebox.showerror("Erro", "Médico não encontrado!")
            return
        
        self.mostrar_passo_2_selecionar_data()
    
    def mostrar_passo_2_selecionar_data(self):
        """Passo 2: Seleção da data"""
        self.atualizar_barra_progresso(1)
        self.limpar_container_passos()
        
        content_frame = tk.Frame(self.container_passos, bg='#f0f2f5')
        content_frame.pack(fill="both", expand=True, pady=20)
        
        # Informações do médico selecionado
        info_frame = tk.Frame(content_frame, bg='#e8f4f8', relief='solid', bd=1, padx=20, pady=15)
        info_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(info_frame, text="👨‍⚕️ Médico Selecionado:", 
                font=('Arial', 12, 'bold'), bg='#e8f4f8', fg='#2c3e50').pack(anchor='w')
        tk.Label(info_frame, text=f"• {self.medico_selecionado.nome}", 
                font=('Arial', 11), bg='#e8f4f8').pack(anchor='w')
        tk.Label(info_frame, text=f"• Especialidade: {self.medico_selecionado.especialidade}", 
                font=('Arial', 10), bg='#e8f4f8').pack(anchor='w')
        
        tk.Label(content_frame, text="📅 SELECIONE A DATA", 
                font=('Arial', 18, 'bold'), bg='#f0f2f5', fg='#2c3e50').pack(pady=(0, 20))
        
        # Frame do calendário
        calendario_frame = tk.Frame(content_frame, bg='white', relief='solid', bd=1, padx=25, pady=25)
        calendario_frame.pack(fill="both", expand=True, pady=10)
        
        # Criar mini-calendário (próximos 14 dias)
        datas_frame = tk.Frame(calendario_frame, bg='white')
        datas_frame.pack(fill="both", expand=True)
        
        # Dias da semana
        dias_semana = ['DOM', 'SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SÁB']
        for i, dia in enumerate(dias_semana):
            tk.Label(datas_frame, text=dia, font=('Arial', 10, 'bold'), 
                    bg='#3498db', fg='white', width=12, pady=8).grid(row=0, column=i, padx=2, pady=2)
        
        # Gerar datas (próximos 14 dias)
        hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self.botoes_data = []
        self.data_selecionada = None
        
        for i in range(14):
            data = hoje + timedelta(days=i+1)  # Começar de amanhã
            linha = (i // 7) + 1
            coluna = i % 7
            
            btn = tk.Button(datas_frame, 
                          text=f"{data.day:02d}/{data.month:02d}\n{data.strftime('%a').upper()}",
                          font=('Arial', 10, 'bold'),
                          bg='#ecf0f1', fg='#2c3e50',
                          width=12, height=3,
                          command=lambda d=data: self.selecionar_data(d),
                          cursor="hand2",
                          relief='raised',
                          bd=2)
            btn.grid(row=linha, column=coluna, padx=3, pady=3)
            self.botoes_data.append(btn)
        
        # Botões
        botoes_frame = tk.Frame(content_frame, bg='#f0f2f5', pady=25)
        botoes_frame.pack(fill="x")
        
        # Botão avançar - inicialmente desabilitado
        self.btn_avancar_data = self.criar_botao_estilizado(
            botoes_frame, "➡️ VER HORÁRIOS DISPONÍVEIS", self.avancar_para_horarios, '#3498db', 'right', True
        )
        
        self.criar_botao_estilizado(
            botoes_frame, "⬅️ VOLTAR", self.mostrar_passo_1_selecionar_medico, '#95a5a6', 'left'
        )
    
    def selecionar_data(self, data):
        """Seleciona uma data específica"""
        self.data_selecionada = data
        
        # Resetar todos os botões
        for btn in self.botoes_data:
            btn.configure(bg='#ecf0f1', fg='#2c3e50')
        
        # Destacar botão selecionado
        for btn in self.botoes_data:
            if f"{data.day:02d}/{data.month:02d}" in btn.cget('text'):
                btn.configure(bg='#3498db', fg='white')
                break
        
        # Habilitar botão avançar
        self.btn_avancar_data.configure(bg='#3498db', state='normal', command=self.avancar_para_horarios)
    
    def avancar_para_horarios(self):
        """Avança para a seleção de horários"""
        if not self.data_selecionada:
            messagebox.showwarning("Atenção", "Por favor, selecione uma data!")
            return
        
        self.mostrar_passo_3_selecionar_horario()
    
    def mostrar_passo_3_selecionar_horario(self):
        """Passo 3: Seleção do horário"""
        self.atualizar_barra_progresso(2)
        self.limpar_container_passos()
        
        content_frame = tk.Frame(self.container_passos, bg='#f0f2f5')
        content_frame.pack(fill="both", expand=True, pady=20)
        
        # Informações resumo
        info_frame = tk.Frame(content_frame, bg='#e8f4f8', relief='solid', bd=1, padx=20, pady=15)
        info_frame.pack(fill="x", pady=(0, 20))
        
        data_formatada = self.data_selecionada.strftime("%d/%m/%Y")
        tk.Label(info_frame, text="📋 Resumo do Agendamento:", 
                font=('Arial', 12, 'bold'), bg='#e8f4f8', fg='#2c3e50').pack(anchor='w')
        tk.Label(info_frame, text=f"• Médico: {self.medico_selecionado.nome}", 
                font=('Arial', 10), bg='#e8f4f8').pack(anchor='w')
        tk.Label(info_frame, text=f"• Data: {data_formatada}", 
                font=('Arial', 10), bg='#e8f4f8').pack(anchor='w')
        
        tk.Label(content_frame, text="🕒 SELECIONE O HORÁRIO", 
                font=('Arial', 18, 'bold'), bg='#f0f2f5', fg='#2c3e50').pack(pady=(0, 20))
        
        # Buscar horários disponíveis
        data_db = self.data_selecionada.strftime("%Y-%m-%d")
        horarios_disponiveis = Agenda.buscar_disponiveis_por_medico_e_data(
            self.medico_selecionado.id, data_db
        )
        
        # Frame dos horários
        horarios_frame = tk.Frame(content_frame, bg='white', relief='solid', bd=1, padx=25, pady=25)
        horarios_frame.pack(fill="both", expand=True, pady=10)
        
        if not horarios_disponiveis:
            tk.Label(horarios_frame, text="😔 Nenhum horário disponível para esta data.", 
                    font=('Arial', 14), bg='white', fg='#e74c3c').pack(expand=True)
            self.horario_selecionado = None
        else:
            tk.Label(horarios_frame, text="Clique em um horário para selecionar:", 
                    font=('Arial', 12, 'bold'), bg='white').pack(anchor='w', pady=(0, 20))
            
            # Grid de horários
            grid_frame = tk.Frame(horarios_frame, bg='white')
            grid_frame.pack(fill="both", expand=True)
            
            self.botoes_horario = []
            self.horario_selecionado = None
            
            for i, horario in enumerate(horarios_disponiveis):
                btn = tk.Button(grid_frame,
                              text=f"🕒 {horario.hora_inicio} - {horario.hora_fim}",
                              font=('Arial', 11, 'bold'),
                              bg='#ecf0f1', fg='#2c3e50',
                              width=18, height=2,
                              command=lambda h=horario: self.selecionar_horario(h),
                              cursor="hand2",
                              relief='raised',
                              bd=2)
                btn.grid(row=i//3, column=i%3, padx=8, pady=8)
                self.botoes_horario.append(btn)
        
        # Motivo da consulta
        motivo_frame = tk.Frame(content_frame, bg='#f0f2f5', pady=20)
        motivo_frame.pack(fill="x", pady=15)
        
        tk.Label(motivo_frame, text="📝 Motivo da consulta (opcional):", 
                font=('Arial', 12, 'bold'), bg='#f0f2f5').pack(anchor='w')
        
        self.motivo_text = tk.Text(motivo_frame, height=4, font=('Arial', 10),
                                 bg='white', relief='solid', bd=1)
        self.motivo_text.pack(fill="x", pady=(8, 0))
        
        # Botões
        botoes_frame = tk.Frame(content_frame, bg='#f0f2f5', pady=25)
        botoes_frame.pack(fill="x")
        
        # Botão confirmar - inicialmente desabilitado se houver horários
        estado_btn = 'disabled' if horarios_disponiveis else 'normal'
        self.btn_confirmar_agendamento = self.criar_botao_estilizado(
            botoes_frame, "✅ CONFIRMAR AGENDAMENTO", self.mostrar_confirmacao, '#27ae60', 'right', estado_btn
        )
        
        self.criar_botao_estilizado(
            botoes_frame, "⬅️ VOLTAR", self.mostrar_passo_2_selecionar_data, '#95a5a6', 'left'
        )
    
    def selecionar_horario(self, horario):
        """Seleciona um horário específico"""
        self.horario_selecionado = horario
        
        # Resetar todos os botões
        for btn in self.botoes_horario:
            btn.configure(bg='#ecf0f1', fg='#2c3e50')
        
        # Destacar botão selecionado
        for btn in self.botoes_horario:
            if f"{horario.hora_inicio} - {horario.hora_fim}" in btn.cget('text'):
                btn.configure(bg='#27ae60', fg='white')
                break
        
        # Habilitar botão confirmar
        self.btn_confirmar_agendamento.configure(bg='#27ae60', state='normal', command=self.mostrar_confirmacao)
    
    def mostrar_confirmacao(self):
        """Passo 4: Confirmação do agendamento"""
        if not self.horario_selecionado:
            messagebox.showwarning("Atenção", "Por favor, selecione um horário!")
            return
        
        self.atualizar_barra_progresso(3)
        self.limpar_container_passos()
        
        content_frame = tk.Frame(self.container_passos, bg='#f0f2f5')
        content_frame.pack(fill="both", expand=True, pady=20)
        
        tk.Label(content_frame, text="✅ CONFIRMAÇÃO DO AGENDAMENTO", 
                font=('Arial', 20, 'bold'), bg='#f0f2f5', fg='#27ae60').pack(pady=(0, 30))
        
        # Card de confirmação
        card_frame = tk.Frame(content_frame, bg='white', relief='solid', bd=1, padx=35, pady=35)
        card_frame.pack(fill="both", expand=True, pady=10)
        
        data_formatada = self.data_selecionada.strftime("%d/%m/%Y")
        motivo = self.motivo_text.get("1.0", tk.END).strip() or "Consulta geral"
        
        informacoes = [
            ("👨‍⚕️ Médico:", self.medico_selecionado.nome),
            ("🎯 Especialidade:", self.medico_selecionado.especialidade),
            ("📅 Data:", data_formatada),
            ("🕒 Horário:", f"{self.horario_selecionado.hora_inicio} - {self.horario_selecionado.hora_fim}"),
            ("📝 Motivo:", motivo)
        ]
        
        for i, (label, valor) in enumerate(informacoes):
            tk.Label(card_frame, text=label, font=('Arial', 12, 'bold'), 
                    bg='white', fg='#2c3e50').grid(row=i, column=0, sticky='w', pady=12, padx=(0, 15))
            tk.Label(card_frame, text=valor, font=('Arial', 12), 
                    bg='white').grid(row=i, column=1, sticky='w', pady=12)
        
        # Botões de confirmação
        botoes_frame = tk.Frame(content_frame, bg='#f0f2f5', pady=30)
        botoes_frame.pack(fill="x")
        
        self.criar_botao_estilizado(
            botoes_frame, "🚀 CONFIRMAR E AGENDAR", self.confirmar_e_salvar_consulta, '#27ae60', 'right'
        )
        
        self.criar_botao_estilizado(
            botoes_frame, "⬅️ VOLTAR", self.mostrar_passo_3_selecionar_horario, '#95a5a6', 'left'
        )
    
    def confirmar_e_salvar_consulta(self):
        """Confirma e salva a consulta no banco de dados"""
        try:
            # Criar objeto consulta
            data_db = self.data_selecionada.strftime("%Y-%m-%d")
            motivo = self.motivo_text.get("1.0", tk.END).strip() or "Consulta geral"
            
            consulta = Consulta(
                id_paciente=self.main_controller.usuario_logado.id,
                id_medico=self.medico_selecionado.id,
                data_consulta=data_db,
                hora_consulta=self.horario_selecionado.hora_inicio,
                motivo=motivo,
                status='agendada'
            )
            
            # Verificar disponibilidade final
            if not consulta.verificar_disponibilidade():
                messagebox.showerror("Erro", "Este horário não está mais disponível. Por favor, selecione outro.")
                return
            
            # Salvar consulta
            if consulta.salvar():
                # Bloquear horário na agenda
                self.horario_selecionado.disponivel = False
                self.horario_selecionado.salvar()
                
                messagebox.showinfo("✅ Sucesso!", 
                                  "Consulta agendada com sucesso!\n\n"
                                  f"📅 Data: {self.data_selecionada.strftime('%d/%m/%Y')}\n"
                                  f"🕒 Horário: {self.horario_selecionado.hora_inicio}\n"
                                  f"👨‍⚕️ Médico: {self.medico_selecionado.nome}")
                
                self.janela_agendamento.destroy()
                
                # Limpar dados
                self.medico_selecionado = None
                self.data_selecionada = None
                self.horario_selecionado = None
                
            else:
                messagebox.showerror("❌ Erro", "Erro ao salvar consulta no banco de dados!")
                
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Ocorreu um erro inesperado: {str(e)}")

    # ... (os outros métodos permanecem: abrir_minhas_consultas, abrir_meu_perfil, etc.)