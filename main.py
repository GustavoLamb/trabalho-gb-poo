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
            atributo = entrada_segura('Informe o parâmetro para consulta: (Modelo, Cor, Ano ou Cidade) \n', opcoes=['Modelo', 'Cor', 'Ano', 'Cidade']).lower()
            tipo_atributo = int if atributo == 'ano' else str
            valor_consulta = entrada_segura('Informe o valor para consulta: \n', tipo_atributo)
            
            limpar_console()
            locadora.consultar_veiculos(atributo, valor_consulta)
        elif escolha == '2':
            cidade_origem = entrada_segura('Informe a cidade de origem: ')
            
            limpar_console()
            locadora.realizar_locacao(cidade_origem)
        elif escolha == '3':
            cliente = entrada_segura("Informe seu nome: ")
            cidade_devolucao = entrada_segura("Informe a cidade da devolução: ")
            km_percorrido = entrada_segura("Informe a quilometragem percorrida: ", int)
            
            limpar_console()
            locadora.realizar_devolucao(cliente, cidade_devolucao, km_percorrido)
        elif escolha == '4':
            valor_consulta = entrada_segura("Informe o modelo do veículo ou nome do cliente para consulta: ")
            
            limpar_console()
            locadora.consultar_locacoes(valor_consulta)
        elif escolha == '5':
            locadora.resumo()
        elif escolha == '6':
            locadora.salvar_dados()
            pass
        elif escolha == '7':
            locadora.salvar_dados()
            continue
        else:
            print("Opção não implementada")
        
        input("\nPressione ENTER para continuar")