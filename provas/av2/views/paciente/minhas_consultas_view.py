# views/paciente/minhas_consultas_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class MinhasConsultasView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.frame = tk.Frame(root, bg='#f0f0f0')
        
        self._criar_widgets()
    
    def _criar_widgets(self):
        # Título
        titulo = tk.Label(
            self.frame, 
            text="MINHAS CONSULTAS",
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
            width=10
        ).pack(side='left', padx=5, pady=5)
        
        tk.Label(
            cabecalho,
            text="Hora",
            font=('Arial', 10, 'bold'),
            bg='#2E7D32',
            fg='white',
            width=10
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
        
        # Lista de consultas (vamos simular por enquanto)
        self.lista_consultas = [
            {
                'data': '20/12/2024',
                'hora': '09:00',
                'medico': 'Dra. Letícia de Paiva',
                'status': 'Agendada'
            },
            {
                'data': '15/12/2024',
                'hora': '14:00',
                'medico': 'Dr. Carlos Mendes',
                'status': 'Realizada'
            }
        ]
        
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
        
        # Preencher a lista
        self._preencher_lista()
        
        # Botões
        botoes_frame = tk.Frame(self.frame, bg='#f0f0f0')
        botoes_frame.pack(pady=30)
        
        tk.Button(
            botoes_frame,
            text="↩️ VOLTAR",
            font=('Arial', 12),
            bg='#757575',
            fg='white',
            width=15,
            command=self.voltar
        ).pack(side='left', padx=10)
    
    def _preencher_lista(self):
        # Limpar o frame (se houver itens anteriores)
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Adicionar cada consulta na lista
        for i, consulta in enumerate(self.lista_consultas):
            linha = tk.Frame(self.scrollable_frame, bg='#ffffff' if i % 2 == 0 else '#f9f9f9')
            linha.pack(fill='x', pady=2)
            
            tk.Label(
                linha,
                text=consulta['data'],
                font=('Arial', 10),
                bg=linha.cget('bg'),
                width=10
            ).pack(side='left', padx=5, pady=5)
            
            tk.Label(
                linha,
                text=consulta['hora'],
                font=('Arial', 10),
                bg=linha.cget('bg'),
                width=10
            ).pack(side='left', padx=5, pady=5)
            
            tk.Label(
                linha,
                text=consulta['medico'],
                font=('Arial', 10),
                bg=linha.cget('bg'),
                width=20
            ).pack(side='left', padx=5, pady=5)
            
            # Status com cor
            cor_status = {
                'Agendada': '#FFA000',
                'Realizada': '#4CAF50',
                'Cancelada': '#F44336'
            }.get(consulta['status'], '#757575')
            
            tk.Label(
                linha,
                text=consulta['status'],
                font=('Arial', 10, 'bold'),
                fg=cor_status,
                bg=linha.cget('bg'),
                width=15
            ).pack(side='left', padx=5, pady=5)
            
            # Ações (botões)
            acoes_frame = tk.Frame(linha, bg=linha.cget('bg'))
            acoes_frame.pack(side='left', padx=5, pady=5)
            
            if consulta['status'] == 'Agendada':
                tk.Button(
                    acoes_frame,
                    text="❌",
                    font=('Arial', 8),
                    bg='#F44336',
                    fg='white',
                    width=3,
                    command=lambda c=consulta: self.cancelar_consulta(c)
                ).pack(side='left', padx=2)
                
                tk.Button(
                    acoes_frame,
                    text="✏️",
                    font=('Arial', 8),
                    bg='#2196F3',
                    fg='white',
                    width=3,
                    command=lambda c=consulta: self.remarcar_consulta(c)
                ).pack(side='left', padx=2)
            else:
                tk.Label(
                    acoes_frame,
                    text="---",
                    font=('Arial', 10),
                    bg=linha.cget('bg'),
                    width=15
                ).pack(side='left', padx=5, pady=5)
    
    def cancelar_consulta(self, consulta):
        resposta = messagebox.askyesno(
            "Cancelar Consulta",
            f"Tem certeza que deseja cancelar a consulta com {consulta['medico']} no dia {consulta['data']} às {consulta['hora']}?"
        )
        if resposta:
            # Aqui você chamaria o controller para cancelar a consulta
            messagebox.showinfo("Sucesso", "Consulta cancelada com sucesso.")
            # Atualizar a lista (por enquanto, vamos recarregar a view)
            self._preencher_lista()
    
    def remarcar_consulta(self, consulta):
        messagebox.showinfo("Remarcar", "Funcionalidade de remarcação em desenvolvimento.")
        # Aqui você poderia abrir a tela de agendamento com os dados preenchidos
    
    def voltar(self):
        self.controller.mostrar_menu_paciente()
    
    def mostrar(self):
        self.frame.pack(fill="both", expand=True)
    
    def ocultar(self):
        self.frame.pack_forget()