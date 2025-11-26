class MainView:
    """Classe responsável pela visualização do menu principal do sistema."""
    
    @staticmethod
    def exibir_menu_principal():
        """Exibe o menu principal do sistema de agendamento médico."""
        print("\n" + "="*50)
        print("    SISTEMA DE AGENDAMENTO DE CONSULTAS MÉDICAS")
        print("="*50)
        print("1. Acesso Paciente")
        print("2. Acesso Médico") 
        print("3. Acesso Administrador")
        print("0. Sair")
        print("-"*50)
        
        opcao = input("Digite a opção desejada: ")
        return opcao
    
    @staticmethod
    def exibir_mensagem(mensagem):
        """Exibe uma mensagem para o usuário."""
        print(f"\n{mensagem}")
    
    @staticmethod
    def exibir_erro(mensagem):
        """Exibe uma mensagem de erro."""
        print(f"\n⚠️  ERRO: {mensagem}")
    
    @staticmethod
    def exibir_sucesso(mensagem):
        """Exibe uma mensagem de sucesso."""
        print(f"\n✅ {mensagem}")
    
    @staticmethod
    def limpar_tela():
        """Limpa a tela do console (funciona em Windows e Unix)."""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def aguardar_enter():
        """Aguarda o usuário pressionar Enter para continuar."""
        input("\nPressione Enter para continuar...")
    
    @staticmethod
    def cabecalho(titulo):
        """Exibe um cabeçalho formatado."""
        print("\n" + "="*50)
        print(f"    {titulo}")
        print("="*50)