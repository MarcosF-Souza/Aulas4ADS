class MedicoView:
    """Classe responsável pela visualização das funcionalidades do médico."""
    
    @staticmethod
    def exibir_menu_medico():
        """Exibe o menu do médico."""
        print("\n" + "="*50)
        print("            MENU DO MÉDICO")
        print("="*50)
        print("1. Visualizar Agenda")
        print("2. Gerenciar Agenda Pessoal")
        print("3. Visualizar Prontuário do Paciente")
        print("4. Consultar Histórico de Atendimentos")
        print("0. Voltar ao Menu Principal")
        print("-"*50)
        
        opcao = input("Digite a opção desejada: ")
        return opcao
    
    @staticmethod
    def solicitar_dados_login():
        """Solicita os dados de login do médico."""
        print("\n--- LOGIN DO MÉDICO ---")
        crm = input("CRM: ")
        senha = input("Senha: ")
        return crm, senha
    
    @staticmethod
    def exibir_agenda(agenda):
        """Exibe a agenda do médico."""
        if not agenda:
            print("\nNenhum compromisso agendado.")
            return
        
        print("\n--- SUA AGENDA ---")
        for compromisso in agenda:
            status = "👥 COM PACIENTE" if compromisso['ocupado'] else "✅ LIVRE"
            paciente = compromisso.get('paciente', 'Disponível')
            print(f"📅 {compromisso['data']} - {status} - {paciente}")
    
    @staticmethod
    def solicitar_periodo_bloqueio():
        """Solicita o período para bloquear/desbloquear na agenda."""
        print("\n--- GERENCIAR DISPONIBILIDADE ---")
        data_inicio = input("Data e hora de início (DD/MM/AAAA HH:MM): ")
        data_fim = input("Data e hora de fim (DD/MM/AAAA HH:MM): ")
        acao = input("Bloquear (B) ou Desbloquear (D): ").upper()
        
        return {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'acao': acao
        }
    
    @staticmethod
    def selecionar_paciente_para_prontuario(pacientes):
        """Permite ao médico selecionar um paciente para ver o prontuário."""
        if not pacientes:
            print("\nNenhum paciente com consulta agendada.")
            return None
        
        print("\n--- SELECIONE UM PACIENTE ---")
        for i, paciente in enumerate(pacientes, 1):
            print(f"{i}. {paciente['nome']} - Consulta: {paciente['data_consulta']}")
        
        try:
            opcao = int(input("\nDigite o número do paciente: ")) - 1
            if 0 <= opcao < len(pacientes):
                return pacientes[opcao]
            else:
                print("Opção inválida!")
                return None
        except ValueError:
            print("Por favor, digite um número válido!")
            return None
    
    @staticmethod
    def exibir_prontuario(prontuario):
        """Exibe o prontuário de um paciente."""
        if not prontuario:
            print("\nProntuário não encontrado ou vazio.")
            return
        
        print(f"\n--- PRONTUÁRIO DE {prontuario['paciente_nome'].upper()} ---")
        print(f"📋 Histórico de consultas: {prontuario['total_consultas']}")
        print(f"📝 Observações médicas: {prontuario['observacoes']}")
        print(f"💊 Medicações: {prontuario['medicacoes']}")
        print(f"🔍 Exames realizados: {prontuario['exames']}")