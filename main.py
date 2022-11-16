from locadora import Locadora
from utils import limpar_console, entrada_segura

#Função de menu
def menu():
    limpar_console()

    print(f'{"#" * 8} Bem vindo {"#" * 8}')
    print(f'{"#" * 11} ao {"#" * 12}')
    print(f'{"#" * 8} PyLocadora {"#" * 9}\n')

    print('1. Consultar veículos')
    print('2. Realizar locação')
    print('3. Realizar devolução')
    print('4. Consultar locações')
    print('5. Resumo')
    print('6. Salvar')
    print('7. Sair\n')

    item = entrada_segura("Escolha uma opção: ")
    limpar_console()
    return item


# Função principal
if __name__ == '__main__':
    
    # Inicia locadora
    locadora = Locadora()


    escolha = '0'
    while escolha != '7':
        escolha = menu()
        
        if escolha == '1':
            print("Implementar: Consultar Veículos")
            pass
        elif escolha == '2':
            print("Implementar: Realizar Locação")
            pass
        elif escolha == '3':
            print("Implementar: Realizar Devolução")
            pass
        elif escolha == '4':
            print("Implementar: Consultar Locações")
            pass
        elif escolha == '5':
            print("Implementar: Resumo")
            pass
        elif escolha == '6':
            print("Implementar: Salvar")
            pass
        elif escolha == '7':
            continue
        else:
            print("Opção não implementada")
        
        input("\nPressione ENTER para continuar")






