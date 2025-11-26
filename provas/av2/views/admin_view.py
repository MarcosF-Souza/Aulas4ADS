class AdministradorView:
    """Classe responsável pela visualização das funcionalidades do administrador."""
    
    @staticmethod
    def exibir_menu_administrador():
        """Exibe o menu do administrador."""
        print("\n" + "="*50)
        print("         MENU DO ADMINISTRADOR")
        print("="*50)
        print("1. Cadastrar Médico")
        print("2. Gerenciar Pacientes")
        print("3. Gerenciar Agenda Geral")
        print("4. Gerar Relatórios")
        print("5. Gerenciar Políticas do Sistema")
        print("0. Voltar ao Menu Principal")
        print("-"*50)
        
        opcao = input("Digite a opção desejada: ")
        return opcao
    
    @staticmethod
    def solicitar_dados_login():
        """Solicita os dados de login do administrador."""
        print("\n--- LOGIN DO ADMINISTRADOR ---")
        usuario = input("Usuário: ")
        senha = input("Senha: ")
        return usuario, senha
    
    @staticmethod
    def solicitar_dados_medico():
        """Solicita os dados para cadastro de médico."""
        print("\n--- CADASTRO DE MÉDICO ---")
        nome = input("Nome completo: ")
        crm = input("CRM: ")
        especialidade = input("Especialidade: ")
        telefone = input("Telefone: ")
        email = input("E-mail: ")
        senha = input("Senha: ")
        
        return {
            'nome': nome,
            'crm': crm,
            'especialidade': especialidade,
            'telefone': telefone,
            'email': email,
            'senha': senha
        }
    
    @staticmethod
    def exibir_menu_gerenciar_pacientes():
        """Exibe submenu para gerenciar pacientes."""
        print("\n--- GERENCIAR PACIENTES ---")
        print("1. Listar todos os pacientes")
        print("2. Buscar paciente por nome")
        print("3. Editar dados de paciente")
        print("4. Desativar/Ativar paciente")
        print("0. Voltar")
        
        opcao = input("Digite a opção desejada: ")
        return opcao
    
    @staticmethod
    def listar_pacientes(pacientes):
        """Lista todos os pacientes."""
        if not pacientes:
            print("\nNenhum paciente cadastrado.")
            return
        
        print(f"\n--- PACIENTES CADASTRADOS ({len(pacientes)} encontrados) ---")
        for i, paciente in enumerate(pacientes, 1):
            status = "✅ Ativo" if paciente['ativo'] else "❌ Inativo"
            print(f"{i}. {paciente['nome']} | {paciente['email']} | {status}")
    
    @staticmethod
    def solicitar_politicas_sistema():
        """Solicita as configurações das políticas do sistema."""
        print("\n--- CONFIGURAÇÕES DO SISTEMA ---")
        try:
            prazo_cancelamento = int(input("Prazo mínimo para cancelamento (horas): "))
            max_tentativas_login = int(input("Máximo de tentativas de login: "))
            tempo_sessao = int(input("Tempo máximo de sessão (minutos): "))
            
            return {
                'prazo_cancelamento': prazo_cancelamento,
                'max_tentativas_login': max_tentativas_login,
                'tempo_sessao': tempo_sessao
            }
        except ValueError:
            print("Por favor, digite valores numéricos válidos!")
            return None
    
    @staticmethod
    def exibir_relatorios_opcoes():
        """Exibe opções de relatórios disponíveis."""
        print("\n--- GERAR RELATÓRIOS ---")
        print("1. Relatório de Consultas por Período")
        print("2. Relatório de Médicos Mais Demandados")
        print("3. Relatório de Pacientes Ativos")
        print("4. Relatório Financeiro")
        print("0. Voltar")
        
        opcao = input("Digite o tipo de relatório: ")
        return opcao
    
    @staticmethod
    def solicitar_periodo_relatorio():
        """Solicita período para geração de relatório."""
        print("\n--- PERÍODO DO RELATÓRIO ---")
        data_inicio = input("Data de início (DD/MM/AAAA): ")
        data_fim = input("Data de fim (DD/MM/AAAA): ")
        return data_inicio, data_fim