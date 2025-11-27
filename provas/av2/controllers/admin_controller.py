from models.medico import Medico
from models.paciente import Paciente
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk

class AdminController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
    
    def abrir_gerenciamento_medicos(self):
        """Abre a tela de gerenciamento de médicos para o administrador."""
        janela_medicos = tk.Toplevel(self.main_controller.app.root)
        janela_medicos.title("Gerenciar Médicos - Administração")
        janela_medicos.geometry("800x600")
        janela_medicos.configure(bg='#f8f9fa')
        janela_medicos.transient(self.main_controller.app.root)
        janela_medicos.grab_set()

        # Centralizar a janela
        janela_medicos.update_idletasks()
        x = (janela_medicos.winfo_screenwidth() // 2) - (800 // 2)
        y = (janela_medicos.winfo_screenheight() // 2) - (600 // 2)
        janela_medicos.geometry(f"800x600+{x}+{y}")
        
        frame = tk.Frame(janela_medicos, bg='#f8f9fa', padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        # Título
        title_frame = tk.Frame(frame, bg='#2c3e50', pady=15)
        title_frame.pack(fill="x", pady=(0, 20))
        tk.Label(title_frame, text="👨‍⚕️ GERENCIAR MÉDICOS", 
                font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white').pack()

        # Treeview para listar médicos
        tree_frame = tk.Frame(frame, bg='white', relief='solid', bd=1)
        tree_frame.pack(fill="both", expand=True, pady=10)
        
        colunas = ('ID', 'Nome', 'CRM', 'Especialidade', 'Email', 'Telefone', 'Ativo')
        self.tree_medicos = ttk.Treeview(tree_frame, columns=colunas, show='headings', height=15)
        
        for col in colunas:
            self.tree_medicos.heading(col, text=col)
            self.tree_medicos.column(col, width=100, anchor='center')

        self.tree_medicos.column('Nome', width=150, anchor='w')
        self.tree_medicos.column('Email', width=150, anchor='w')
        
        self.carregar_medicos()
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_medicos.yview)
        self.tree_medicos.configure(yscrollcommand=scrollbar.set)
        
        self.tree_medicos.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        # Botões de ação
        botoes_frame = tk.Frame(frame, bg='#f8f9fa', pady=15)
        botoes_frame.pack(fill="x")

        btn_adicionar = tk.Button(botoes_frame, text="➕ Adicionar", 
                                font=('Arial', 10, 'bold'), bg='#28a745', fg='white', 
                                padx=15, pady=8, command=self.abrir_adicionar_medico, cursor="hand2")
        btn_adicionar.pack(side='left', padx=5)

        btn_editar = tk.Button(botoes_frame, text="✏️ Editar", 
                                font=('Arial', 10, 'bold'), bg='#007bff', fg='white', 
                                padx=15, pady=8, command=self.abrir_editar_medico, cursor="hand2")
        btn_editar.pack(side='left', padx=5)

        btn_ativar_desativar = tk.Button(botoes_frame, text="✅/❌ Ativar/Desativar", 
                                font=('Arial', 10, 'bold'), bg='#ffc107', fg='black', 
                                padx=15, pady=8, command=self.ativar_desativar_medico, cursor="hand2")
        btn_ativar_desativar.pack(side='left', padx=5)
        
        btn_fechar = tk.Button(botoes_frame, text="🚪 Fechar", 
                              font=('Arial', 10), bg='#dc3545', fg='white', 
                              padx=15, pady=8, command=janela_medicos.destroy, cursor="hand2")
        btn_fechar.pack(side='right', padx=5)

    def carregar_medicos(self):
        """Carrega e exibe a lista de médicos na treeview."""
        for i in self.tree_medicos.get_children():
            self.tree_medicos.delete(i)
        
        medicos = Medico.listar_todos()
        for medico in medicos:
            self.tree_medicos.insert('', 'end', iid=medico.id, values=(
                medico.id, medico.nome, medico.crm, medico.especialidade, medico.email, medico.telefone, 
                "Ativo" if medico.ativo else "Inativo"
            ))
            
    def abrir_adicionar_medico(self):
        """Abre uma janela para adicionar um novo médico."""
        janela_add_medico = tk.Toplevel(self.main_controller.app.root)
        janela_add_medico.title("Adicionar Médico")
        janela_add_medico.geometry("400x450")
        janela_add_medico.configure(bg='#f8f9fa')
        janela_add_medico.transient(self.main_controller.app.root)
        janela_add_medico.grab_set()

        frame = tk.Frame(janela_add_medico, bg='#f8f9fa', padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Nome:", bg='#f8f9fa').pack(pady=5)
        nome_var = tk.StringVar()
        tk.Entry(frame, textvariable=nome_var).pack(pady=5)

        tk.Label(frame, text="CRM:", bg='#f8f9fa').pack(pady=5)
        crm_var = tk.StringVar()
        tk.Entry(frame, textvariable=crm_var).pack(pady=5)

        tk.Label(frame, text="Especialidade:", bg='#f8f9fa').pack(pady=5)
        especialidade_var = tk.StringVar()
        tk.Entry(frame, textvariable=especialidade_var).pack(pady=5)

        tk.Label(frame, text="Email:", bg='#f8f9fa').pack(pady=5)
        email_var = tk.StringVar()
        tk.Entry(frame, textvariable=email_var).pack(pady=5)

        tk.Label(frame, text="Telefone:", bg='#f8f9fa').pack(pady=5)
        telefone_var = tk.StringVar()
        tk.Entry(frame, textvariable=telefone_var).pack(pady=5)

        tk.Label(frame, text="Senha:", bg='#f8f9fa').pack(pady=5)
        senha_var = tk.StringVar()
        tk.Entry(frame, textvariable=senha_var, show="*").pack(pady=5)

        def salvar_novo_medico():
            novo_medico = Medico(
                nome=nome_var.get(),
                crm=crm_var.get(),
                especialidade=especialidade_var.get(),
                email=email_var.get(),
                telefone=telefone_var.get(),
                senha=senha_var.get()
            )
            if novo_medico.salvar():
                messagebox.showinfo("Sucesso", "Médico adicionado com sucesso!")
                self.carregar_medicos()
                janela_add_medico.destroy()
            else:
                messagebox.showerror("Erro", "Falha ao adicionar médico. Verifique os dados.")

        tk.Button(frame, text="Salvar", command=salvar_novo_medico).pack(pady=10)

    def abrir_editar_medico(self):
        """Abre uma janela para editar o médico selecionado."""
        selecionado = self.tree_medicos.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um médico para editar!")
            return
        
        medico_id = self.tree_medicos.item(selecionado[0], 'iid')
        medico_existente = Medico.buscar_por_id(medico_id)

        if not medico_existente:
            messagebox.showerror("Erro", "Médico não encontrado!")
            return

        janela_edit_medico = tk.Toplevel(self.main_controller.app.root)
        janela_edit_medico.title("Editar Médico")
        janela_edit_medico.geometry("400x450")
        janela_edit_medico.configure(bg='#f8f9fa')
        janela_edit_medico.transient(self.main_controller.app.root)
        janela_edit_medico.grab_set()

        frame = tk.Frame(janela_edit_medico, bg='#f8f9fa', padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Nome:", bg='#f8f9fa').pack(pady=5)
        nome_var = tk.StringVar(value=medico_existente.nome)
        tk.Entry(frame, textvariable=nome_var).pack(pady=5)

        tk.Label(frame, text="CRM:", bg='#f8f9fa').pack(pady=5)
        crm_var = tk.StringVar(value=medico_existente.crm)
        tk.Entry(frame, textvariable=crm_var).pack(pady=5)

        tk.Label(frame, text="Especialidade:", bg='#f8f9fa').pack(pady=5)
        especialidade_var = tk.StringVar(value=medico_existente.especialidade)
        tk.Entry(frame, textvariable=especialidade_var).pack(pady=5)

        tk.Label(frame, text="Email:", bg='#f8f9fa').pack(pady=5)
        email_var = tk.StringVar(value=medico_existente.email)
        tk.Entry(frame, textvariable=email_var).pack(pady=5)

        tk.Label(frame, text="Telefone:", bg='#f8f9fa').pack(pady=5)
        telefone_var = tk.StringVar(value=medico_existente.telefone)
        tk.Entry(frame, textvariable=telefone_var).pack(pady=5)

        tk.Label(frame, text="Senha (deixe em branco para não alterar):", bg='#f8f9fa').pack(pady=5)
        senha_var = tk.StringVar()
        tk.Entry(frame, textvariable=senha_var, show="*").pack(pady=5)

        def salvar_edicao_medico():
            medico_existente.nome = nome_var.get()
            medico_existente.crm = crm_var.get()
            medico_existente.especialidade = especialidade_var.get()
            medico_existente.email = email_var.get()
            medico_existente.telefone = telefone_var.get()
            if senha_var.get(): # Somente atualiza a senha se um novo valor for fornecido
                medico_existente.senha = senha_var.get()
            
            if medico_existente.salvar():
                messagebox.showinfo("Sucesso", "Médico atualizado com sucesso!")
                self.carregar_medicos()
                janela_edit_medico.destroy()
            else:
                messagebox.showerror("Erro", "Falha ao atualizar médico. Verifique os dados.")

        tk.Button(frame, text="Salvar Alterações", command=salvar_edicao_medico).pack(pady=10)

    def ativar_desativar_medico(self):
        """Ativa ou desativa o médico selecionado (exclusão lógica)."""
        selecionado = self.tree_medicos.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um médico para ativar/desativar!")
            return
        
        medico_id = self.tree_medicos.item(selecionado[0], 'iid')
        medico_existente = Medico.buscar_por_id(medico_id)

        if not medico_existente:
            messagebox.showerror("Erro", "Médico não encontrado!")
            return
        
        if medico_existente.ativo:
            resposta = messagebox.askyesno("Desativar Médico", f"Deseja realmente desativar {medico_existente.nome}?")
            if resposta:
                if medico_existente.desativar():
                    messagebox.showinfo("Sucesso", "Médico desativado com sucesso!")
                    self.carregar_medicos()
                else:
                    messagebox.showerror("Erro", "Falha ao desativar médico.")
        else:
            resposta = messagebox.askyesno("Ativar Médico", f"Deseja realmente ativar {medico_existente.nome}?")
            if resposta:
                if medico_existente.ativar():
                    messagebox.showinfo("Sucesso", "Médico ativado com sucesso!")
                    self.carregar_medicos()
                else:
                    messagebox.showerror("Erro", "Falha ao ativar médico.")
    
    def abrir_gerenciamento_pacientes(self):
        """Abre a tela de gerenciamento de pacientes para o administrador."""
        janela_pacientes = tk.Toplevel(self.main_controller.app.root)
        janela_pacientes.title("Gerenciar Pacientes - Administração")
        janela_pacientes.geometry("800x600")
        janela_pacientes.configure(bg='#f8f9fa')
        janela_pacientes.transient(self.main_controller.app.root)
        janela_pacientes.grab_set()

        # Centralizar a janela
        janela_pacientes.update_idletasks()
        x = (janela_pacientes.winfo_screenwidth() // 2) - (800 // 2)
        y = (janela_pacientes.winfo_screenheight() // 2) - (600 // 2)
        janela_pacientes.geometry(f"800x600+{x}+{y}")
        
        frame = tk.Frame(janela_pacientes, bg='#f8f9fa', padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        # Título
        title_frame = tk.Frame(frame, bg='#2c3e50', pady=15)
        title_frame.pack(fill="x", pady=(0, 20))
        tk.Label(title_frame, text="👥 GERENCIAR PACIENTES", 
                font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white').pack()

        # Treeview para listar pacientes
        tree_frame = tk.Frame(frame, bg='white', relief='solid', bd=1)
        tree_frame.pack(fill="both", expand=True, pady=10)
        
        colunas = ('ID', 'Nome', 'Email', 'Telefone', 'Data Nasc.', 'Endereço', 'Ativo')
        self.tree_pacientes = ttk.Treeview(tree_frame, columns=colunas, show='headings', height=15)
        
        for col in colunas:
            self.tree_pacientes.heading(col, text=col)
            self.tree_pacientes.column(col, width=100, anchor='center')

        self.tree_pacientes.column('Nome', width=150, anchor='w')
        self.tree_pacientes.column('Email', width=150, anchor='w')
        
        self.carregar_pacientes()
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_pacientes.yview)
        self.tree_pacientes.configure(yscrollcommand=scrollbar.set)
        
        self.tree_pacientes.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        # Botões de ação
        botoes_frame = tk.Frame(frame, bg='#f8f9fa', pady=15)
        botoes_frame.pack(fill="x")

        btn_adicionar = tk.Button(botoes_frame, text="➕ Adicionar", 
                                font=('Arial', 10, 'bold'), bg='#28a745', fg='white', 
                                padx=15, pady=8, command=self.abrir_adicionar_paciente, cursor="hand2")
        btn_adicionar.pack(side='left', padx=5)

        btn_editar = tk.Button(botoes_frame, text="✏️ Editar", 
                                font=('Arial', 10, 'bold'), bg='#007bff', fg='white', 
                                padx=15, pady=8, command=self.abrir_editar_paciente, cursor="hand2")
        btn_editar.pack(side='left', padx=5)

        btn_ativar_desativar = tk.Button(botoes_frame, text="✅/❌ Ativar/Desativar", 
                                font=('Arial', 10, 'bold'), bg='#ffc107', fg='black', 
                                padx=15, pady=8, command=self.ativar_desativar_paciente, cursor="hand2")
        btn_ativar_desativar.pack(side='left', padx=5)
        
        btn_fechar = tk.Button(botoes_frame, text="🚪 Fechar", 
                              font=('Arial', 10), bg='#dc3545', fg='white', 
                              padx=15, pady=8, command=janela_pacientes.destroy, cursor="hand2")
        btn_fechar.pack(side='right', padx=5)

    def carregar_pacientes(self):
        """Carrega e exibe a lista de pacientes na treeview."""
        for i in self.tree_pacientes.get_children():
            self.tree_pacientes.delete(i)
        
        pacientes = Paciente.listar_todos()
        for paciente in pacientes:
            self.tree_pacientes.insert('', 'end', iid=paciente.id, values=(
                paciente.id, paciente.nome, paciente.email, paciente.telefone, 
                paciente.data_nascimento, paciente.endereco, 
                "Ativo" if paciente.ativo else "Inativo"
            ))
            
    def abrir_adicionar_paciente(self):
        """Abre uma janela para adicionar um novo paciente."""
        janela_add_paciente = tk.Toplevel(self.main_controller.app.root)
        janela_add_paciente.title("Adicionar Paciente")
        janela_add_paciente.geometry("400x500")
        janela_add_paciente.configure(bg='#f8f9fa')
        janela_add_paciente.transient(self.main_controller.app.root)
        janela_add_paciente.grab_set()

        frame = tk.Frame(janela_add_paciente, bg='#f8f9fa', padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Nome:", bg='#f8f9fa').pack(pady=5)
        nome_var = tk.StringVar()
        tk.Entry(frame, textvariable=nome_var).pack(pady=5)

        tk.Label(frame, text="Email:", bg='#f8f9fa').pack(pady=5)
        email_var = tk.StringVar()
        tk.Entry(frame, textvariable=email_var).pack(pady=5)

        tk.Label(frame, text="Telefone:", bg='#f8f9fa').pack(pady=5)
        telefone_var = tk.StringVar()
        tk.Entry(frame, textvariable=telefone_var).pack(pady=5)

        tk.Label(frame, text="Data de Nascimento (DD/MM/AAAA):", bg='#f8f9fa').pack(pady=5)
        data_nascimento_var = tk.StringVar()
        tk.Entry(frame, textvariable=data_nascimento_var).pack(pady=5)

        tk.Label(frame, text="Endereço:", bg='#f8f9fa').pack(pady=5)
        endereco_var = tk.StringVar()
        tk.Entry(frame, textvariable=endereco_var).pack(pady=5)

        tk.Label(frame, text="Senha:", bg='#f8f9fa').pack(pady=5)
        senha_var = tk.StringVar()
        tk.Entry(frame, textvariable=senha_var, show="*").pack(pady=5)

        def salvar_novo_paciente():
            novo_paciente = Paciente(
                nome=nome_var.get(),
                email=email_var.get(),
                telefone=telefone_var.get(),
                data_nascimento=data_nascimento_var.get(),
                endereco=endereco_var.get(),
                senha=senha_var.get()
            )
            if novo_paciente.salvar():
                messagebox.showinfo("Sucesso", "Paciente adicionado com sucesso!")
                self.carregar_pacientes()
                janela_add_paciente.destroy()
            else:
                messagebox.showerror("Erro", "Falha ao adicionar paciente. Verifique os dados.")

        tk.Button(frame, text="Salvar", command=salvar_novo_paciente).pack(pady=10)

    def abrir_editar_paciente(self):
        """Abre uma janela para editar o paciente selecionado."""
        selecionado = self.tree_pacientes.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um paciente para editar!")
            return
        
        paciente_id = self.tree_pacientes.item(selecionado[0], 'iid')
        paciente_existente = Paciente.buscar_por_id(paciente_id)

        if not paciente_existente:
            messagebox.showerror("Erro", "Paciente não encontrado!")
            return

        janela_edit_paciente = tk.Toplevel(self.main_controller.app.root)
        janela_edit_paciente.title("Editar Paciente")
        janela_edit_paciente.geometry("400x500")
        janela_edit_paciente.configure(bg='#f8f9fa')
        janela_edit_paciente.transient(self.main_controller.app.root)
        janela_edit_paciente.grab_set()

        frame = tk.Frame(janela_edit_paciente, bg='#f8f9fa', padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Nome:", bg='#f8f9fa').pack(pady=5)
        nome_var = tk.StringVar(value=paciente_existente.nome)
        tk.Entry(frame, textvariable=nome_var).pack(pady=5)

        tk.Label(frame, text="Email:", bg='#f8f9fa').pack(pady=5)
        email_var = tk.StringVar(value=paciente_existente.email)
        tk.Entry(frame, textvariable=email_var).pack(pady=5)

        tk.Label(frame, text="Telefone:", bg='#f8f9fa').pack(pady=5)
        telefone_var = tk.StringVar(value=paciente_existente.telefone)
        tk.Entry(frame, textvariable=telefone_var).pack(pady=5)

        tk.Label(frame, text="Data de Nascimento (DD/MM/AAAA):", bg='#f8f9fa').pack(pady=5)
        data_nascimento_var = tk.StringVar(value=paciente_existente.data_nascimento)
        tk.Entry(frame, textvariable=data_nascimento_var).pack(pady=5)

        tk.Label(frame, text="Endereço:", bg='#f8f9fa').pack(pady=5)
        endereco_var = tk.StringVar(value=paciente_existente.endereco)
        tk.Entry(frame, textvariable=endereco_var).pack(pady=5)

        tk.Label(frame, text="Senha (deixe em branco para não alterar):", bg='#f8f9fa').pack(pady=5)
        senha_var = tk.StringVar()
        tk.Entry(frame, textvariable=senha_var, show="*").pack(pady=5)

        def salvar_edicao_paciente():
            paciente_existente.nome = nome_var.get()
            paciente_existente.email = email_var.get()
            paciente_existente.telefone = telefone_var.get()
            paciente_existente.data_nascimento = data_nascimento_var.get()
            paciente_existente.endereco = endereco_var.get()
            if senha_var.get(): # Somente atualiza a senha se um novo valor for fornecido
                paciente_existente.senha = senha_var.get()
            
            if paciente_existente.salvar():
                messagebox.showinfo("Sucesso", "Paciente atualizado com sucesso!")
                self.carregar_pacientes()
                janela_edit_paciente.destroy()
            else:
                messagebox.showerror("Erro", "Falha ao atualizar paciente. Verifique os dados.")

        tk.Button(frame, text="Salvar Alterações", command=salvar_edicao_paciente).pack(pady=10)

    def ativar_desativar_paciente(self):
        """Ativa ou desativa o paciente selecionado (exclusão lógica)."""
        selecionado = self.tree_pacientes.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um paciente para ativar/desativar!")
            return
        
        paciente_id = self.tree_pacientes.item(selecionado[0], 'iid')
        paciente_existente = Paciente.buscar_por_id(paciente_id)

        if not paciente_existente:
            messagebox.showerror("Erro", "Paciente não encontrado!")
            return
        
        if paciente_existente.ativo:
            resposta = messagebox.askyesno("Desativar Paciente", f"Deseja realmente desativar {paciente_existente.nome}?")
            if resposta:
                if paciente_existente.desativar():
                    messagebox.showinfo("Sucesso", "Paciente desativado com sucesso!")
                    self.carregar_pacientes()
                else:
                    messagebox.showerror("Erro", "Falha ao desativar paciente.")
        else:
            resposta = messagebox.askyesno("Ativar Paciente", f"Deseja realmente ativar {paciente_existente.nome}?")
            if resposta:
                if paciente_existente.ativar():
                    messagebox.showinfo("Sucesso", "Paciente ativado com sucesso!")
                    self.carregar_pacientes()
                else:
                    messagebox.showerror("Erro", "Falha ao ativar paciente.")
    
    def abrir_agenda_geral(self):
        """Abre a tela de agenda geral para o administrador, mostrando todas as consultas."""
        from models.consulta import Consulta # Importação local para evitar circular

        janela_agenda_geral = tk.Toplevel(self.main_controller.app.root)
        janela_agenda_geral.title("Agenda Geral - Administração")
        janela_agenda_geral.geometry("900x600")
        janela_agenda_geral.configure(bg='#f8f9fa')
        janela_agenda_geral.transient(self.main_controller.app.root)
        janela_agenda_geral.grab_set()

        # Centralizar a janela
        janela_agenda_geral.update_idletasks()
        x = (janela_agenda_geral.winfo_screenwidth() // 2) - (900 // 2)
        y = (janela_agenda_geral.winfo_screenheight() // 2) - (600 // 2)
        janela_agenda_geral.geometry(f"900x600+{x}+{y}")
        
        frame = tk.Frame(janela_agenda_geral, bg='#f8f9fa', padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        # Título
        title_frame = tk.Frame(frame, bg='#2c3e50', pady=15)
        title_frame.pack(fill="x", pady=(0, 20))
        tk.Label(title_frame, text="🗓️ AGENDA GERAL", 
                font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white').pack()

        # Treeview para listar consultas
        tree_frame = tk.Frame(frame, bg='white', relief='solid', bd=1)
        tree_frame.pack(fill="both", expand=True, pady=10)
        
        colunas = ('ID', 'Paciente', 'Médico', 'Especialidade', 'Data', 'Hora', 'Status', 'Motivo')
        self.tree_consultas = ttk.Treeview(tree_frame, columns=colunas, show='headings', height=15)
        
        for col in colunas:
            self.tree_consultas.heading(col, text=col)
            self.tree_consultas.column(col, width=100, anchor='center')

        self.tree_consultas.column('Paciente', width=150, anchor='w')
        self.tree_consultas.column('Médico', width=150, anchor='w')
        
        self.carregar_todas_consultas()
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_consultas.yview)
        self.tree_consultas.configure(yscrollcommand=scrollbar.set)
        
        self.tree_consultas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        # Botões de ação (ex: Cancelar Consulta, Detalhes, etc.)
        botoes_frame = tk.Frame(frame, bg='#f8f9fa', pady=15)
        botoes_frame.pack(fill="x")

        btn_detalhes = tk.Button(botoes_frame, text="📄 Detalhes", 
                                font=('Arial', 10, 'bold'), bg='#007bff', fg='white', 
                                padx=15, pady=8, command=self.abrir_detalhes_consulta_geral, cursor="hand2")
        btn_detalhes.pack(side='left', padx=5)

        btn_fechar = tk.Button(botoes_frame, text="🚪 Fechar", 
                              font=('Arial', 10), bg='#dc3545', fg='white', 
                              padx=15, pady=8, command=janela_agenda_geral.destroy, cursor="hand2")
        btn_fechar.pack(side='right', padx=5)

    def carregar_todas_consultas(self):
        """Carrega e exibe a lista de todas as consultas na treeview."""
        from models.consulta import Consulta # Importação local

        for i in self.tree_consultas.get_children():
            self.tree_consultas.delete(i)
        
        consultas = Consulta.listar_todas() # Será necessário criar este método no model Consulta
        for consulta in consultas:
            self.tree_consultas.insert('', 'end', iid=consulta.id, values=(
                consulta.id, consulta.paciente_nome, consulta.medico_nome, 
                consulta.especialidade, consulta.data_consulta, 
                consulta.hora_consulta, consulta.status, consulta.motivo
            ))
            
    def abrir_detalhes_consulta_geral(self):
        """Abre uma janela de detalhes para a consulta selecionada na agenda geral."""
        selecionado = self.tree_consultas.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma consulta para ver os detalhes!")
            return
        
        consulta_id = self.tree_consultas.item(selecionado[0], 'iid')
        from models.consulta import Consulta # Importação local
        consulta = Consulta.buscar_por_id(consulta_id)

        if not consulta:
            messagebox.showerror("Erro", "Consulta não encontrada!")
            return

        janela_detalhes = tk.Toplevel(self.main_controller.app.root)
        janela_detalhes.title(f"Detalhes da Consulta #{consulta.id}")
        janela_detalhes.geometry("500x400")
        janela_detalhes.configure(bg='#f8f9fa')
        janela_detalhes.transient(self.main_controller.app.root)
        janela_detalhes.grab_set()

        frame = tk.Frame(janela_detalhes, bg='#f8f9fa', padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Detalhes da Consulta", font=('Arial', 14, 'bold'), bg='#f8f9fa').pack(pady=10)
        
        detalhes_text = f"""
ID da Consulta: {consulta.id}
Paciente: {consulta.paciente_nome}
Médico: {consulta.medico_nome} ({consulta.especialidade})
Data: {consulta.data_consulta}
Hora: {consulta.hora_consulta}
Status: {consulta.status}
Motivo: {consulta.motivo if consulta.motivo else 'Não informado'}
Observações: {consulta.observacoes if consulta.observacoes else 'Nenhuma'}
Data de Criação: {consulta.data_criacao}
        """
        tk.Label(frame, text=detalhes_text, justify='left', bg='#f8f9fa', font=('Arial', 10)).pack(pady=10)

        tk.Button(frame, text="Fechar", command=janela_detalhes.destroy).pack(pady=10)

