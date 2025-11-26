class ConsultaView:
    """Classe responsável pela visualização específica de consultas."""
    
    @staticmethod
    def exibir_detalhes_consulta(consulta):
        """Exibe os detalhes completos de uma consulta."""
        if not consulta:
            print("\nConsulta não encontrada.")
            return
        
        print("\n" + "="*50)
        print("          DETALHES DA CONSULTA")
        print("="*50)
        print(f"📅 Data/Horário: {consulta.get('data_hora', 'N/A')}")
        print(f"👨‍⚕️ Médico: {consulta.get('medico_nome', 'N/A')}")
        print(f"🎯 Especialidade: {consulta.get('especialidade', 'N/A')}")
        print(f"👤 Paciente: {consulta.get('paciente_nome', 'N/A')}")
        print(f"📊 Status: {consulta.get('status', 'N/A')}")
        print(f"📝 Motivo: {consulta.get('motivo', 'Não informado')}")
        print(f"💬 Observações: {consulta.get('observacoes', 'Nenhuma')}")
        print("="*50)
    
    @staticmethod
    def listar_consultas_formatado(consultas, titulo="CONSULTAS"):
        """Lista consultas de forma formatada, podendo ser usado por diferentes atores."""
        if not consultas:
            print(f"\nNenhuma consulta encontrada.")
            return
        
        print(f"\n--- {titulo} ({len(consultas)} encontradas) ---")
        for i, consulta in enumerate(consultas, 1):
            status_icon = {
                'agendada': '📅',
                'realizada': '✅',
                'cancelada': '❌',
                'remarcada': '🔄'
            }.get(consulta.get('status', '').lower(), '📋')
            
            print(f"{i}. {status_icon} {consulta['data_hora']} | "
                  f"Paciente: {consulta.get('paciente_nome', 'N/A')} | "
                  f"Médico: {consulta.get('medico_nome', 'N/A')} | "
                  f"Status: {consulta.get('status', 'N/A')}")
    
    @staticmethod
    def solicitar_dados_agendamento(medicos_disponiveis=None):
        """Solicita os dados para agendamento de uma nova consulta."""
        print("\n--- NOVO AGENDAMENTO ---")
        
        # Se a lista de médicos foi fornecida, mostrar opções
        if medicos_disponiveis:
            print("\nMédicos disponíveis:")
            for i, medico in enumerate(medicos_disponiveis, 1):
                print(f"{i}. Dr. {medico['nome']} - {medico['especialidade']} (CRM: {medico['crm']})")
            
            try:
                opcao_medico = int(input("\nSelecione o médico: ")) - 1
                if 0 <= opcao_medico < len(medicos_disponiveis):
                    medico_selecionado = medicos_disponiveis[opcao_medico]
                else:
                    print("Opção inválida!")
                    return None
            except ValueError:
                print("Por favor, digite um número válido!")
                return None
        else:
            # Se não há lista prévia, pedir CRM
            crm_medico = input("CRM do médico: ")
            medico_selecionado = {'crm': crm_medico}
        
        data_consulta = input("Data da consulta (DD/MM/AAAA): ")
        hora_consulta = input("Horário da consulta (HH:MM): ")
        motivo = input("Motivo da consulta (opcional): ")
        
        return {
            'crm_medico': medico_selecionado.get('crm'),
            'data_consulta': data_consulta,
            'hora_consulta': hora_consulta,
            'data_hora': f"{data_consulta} {hora_consulta}",
            'motivo': motivo
        }
    
    @staticmethod
    def exibir_horarios_disponiveis(horarios, medico_nome):
        """Exibe os horários disponíveis para um médico."""
        if not horarios:
            print(f"\nNão há horários disponíveis para Dr. {medico_nome}.")
            return
        
        print(f"\n--- HORÁRIOS DISPONÍVEIS - Dr. {medico_nome} ---")
        for i, horario in enumerate(horarios, 1):
            print(f"{i}. {horario}")
    
    @staticmethod
    def selecionar_horario_disponivel(horarios):
        """Permite selecionar um horário disponível da lista."""
        if not horarios:
            return None
        
        try:
            opcao = int(input("\nSelecione o horário desejado: ")) - 1
            if 0 <= opcao < len(horarios):
                return horarios[opcao]
            else:
                print("Opção inválida!")
                return None
        except ValueError:
            print("Por favor, digite um número válido!")
            return None
    
    @staticmethod
    def confirmar_agendamento(dados_consulta):
        """Confirma os dados do agendamento antes de finalizar."""
        print("\n--- CONFIRMAR AGENDAMENTO ---")
        print(f"📅 Data/Horário: {dados_consulta.get('data_hora')}")
        print(f"👨‍⚕️ Médico: {dados_consulta.get('medico_nome', 'CRM: ' + dados_consulta.get('crm_medico', 'N/A'))}")
        print(f"📝 Motivo: {dados_consulta.get('motivo', 'Não informado')}")
        
        confirmacao = input("\nConfirmar agendamento? (S/N): ")
        return confirmacao.upper() == 'S'
    
    @staticmethod
    def solicitar_observacoes_consulta():
        """Solicita observações médicas após a consulta."""
        print("\n--- REGISTRAR OBSERVAÇÕES ---")
        observacoes = input("Observações da consulta: ")
        return observacoes
    
    @staticmethod
    def exibir_status_agendamento(sucesso, mensagem, dados_consulta=None):
        """Exibe o status do agendamento (sucesso ou erro)."""
        if sucesso:
            print(f"\n✅ AGENDAMENTO REALIZADO COM SUCESSO!")
            if dados_consulta:
                print(f"📅 Data: {dados_consulta.get('data_hora')}")
                print(f"👨‍⚕️ Médico: {dados_consulta.get('medico_nome', 'N/A')}")
        else:
            print(f"\n❌ FALHA NO AGENDAMENTO: {mensagem}")