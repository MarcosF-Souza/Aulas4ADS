class PacienteView:
    """Classe responsável pela visualização das funcionalidades do paciente."""
    
    @staticmethod
    def exibir_menu_paciente():
        """Exibe o menu do paciente."""
        print("\n" + "="*50)
        print("          MENU DO PACIENTE")
        print("="*50)
        print("1. Agendar Consulta")
        print("2. Remarcar Consulta")
        print("3. Cancelar Consulta")
        print("4. Consultar Histórico de Consultas")
        print("5. Alterar Perfil")
        print("0. Voltar ao Menu Principal")
        print("-"*50)
        
        opcao = input("Digite a opção desejada: ")
        return opcao
    
    @staticmethod
    def solicitar_dados_cadastro():
        """Solicita os dados para cadastro do paciente."""
        print("\n--- CADASTRO DE PACIENTE ---")
        nome = input("Nome completo: ")
        email = input("E-mail: ")
        telefone = input("Telefone: ")
        data_nascimento = input("Data de nascimento (DD/MM/AAAA): ")
        endereco = input("Endereço: ")
        senha = input("Senha: ")
        
        return {
            'nome': nome,
            'email': email,
            'telefone': telefone,
            'data_nascimento': data_nascimento,
            'endereco': endereco,
            'senha': senha
        }
    
    @staticmethod
    def solicitar_dados_login():
        """Solicita os dados de login do paciente."""
        print("\n--- LOGIN DO PACIENTE ---")
        email = input("E-mail: ")
        senha = input("Senha: ")
        return email, senha
    
    @staticmethod
    def listar_consultas(consultas):
        """Lista as consultas do paciente."""
        if not consultas:
            print("\nNenhuma consulta encontrada.")
            return
        
        print(f"\n--- SUAS CONSULTAS ({len(consultas)} encontradas) ---")
        for i, consulta in enumerate(consultas, 1):
            print(f"{i}. Data: {consulta['data']} | Médico: {consulta['medico']} | Status: {consulta['status']}")
    
    @staticmethod
    def selecionar_consulta(consultas):
        """Permite ao paciente selecionar uma consulta da lista."""
        if not consultas:
            return None
        
        print("\n--- SELECIONE UMA CONSULTA ---")
        for i, consulta in enumerate(consultas, 1):
            print(f"{i}. Data: {consulta['data']} | Médico: {consulta['medico']}")
        
        try:
            opcao = int(input("\nDigite o número da consulta: ")) - 1
            if 0 <= opcao < len(consultas):
                return consultas[opcao]
            else:
                print("Opção inválida!")
                return None
        except ValueError:
            print("Por favor, digite um número válido!")
            return None
    
    @staticmethod
    def solicitar_nova_data():
        """Solicita nova data para remarcação."""
        print("\n--- REMARCAÇÃO DE CONSULTA ---")
        nova_data = input("Nova data e horário (DD/MM/AAAA HH:MM): ")
        return nova_data
    
    @staticmethod
    def confirmar_cancelamento(consulta):
        """Confirma o cancelamento de uma consulta."""
        print(f"\n--- CONFIRMAR CANCELAMENTO ---")
        print(f"Consulta: {consulta['data']} com Dr. {consulta['medico']}")
        confirmacao = input("Tem certeza que deseja cancelar? (S/N): ")
        return confirmacao.upper() == 'S'