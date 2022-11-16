import os

def table_format(cabecalho, dados, width=15):
    headers = cabecalho.split("\t")
    datas = [dado.split('\t') for dado in dados]
    
    for header in headers:
        print(header, end=f"{' ' * (width -(len(header) + 1))}")
    print()

    for row in datas:
        for data in row:
            print(data, end=f"{' ' * (width -(len(data) + 1))}")
        print()

def conversao_segura(tipo, valor, default, parametro: str=None):
    try:
        valor_convertido = tipo(valor)
        return valor_convertido
    except ValueError as E:
        param = parametro if parametro else ''
        print(f"Erro para converter parametro: {param}")
        print(f"Assumindo valor default: {default}")   
    
    return default

def limpar_console():
    os.system("cls" if os.name == "nt" else "clear")


def entrada_segura(dica, tipo=str, opcoes=None):
    seguro = False
    entrada = ''
    while not seguro:
        try:
            entrada = tipo(input(dica))

            if opcoes:
                seguro = entrada in opcoes

                if entrada not in opcoes:
                    print("Valor não é uma opção válida: ", opcoes)
                    input("\nPressione ENTER para continuar")
                    limpar_console()

                continue

            seguro = True
        except ValueError as E:
            print("Erro: Valor inválido")
            input("\nPressione ENTER para continuar")
            limpar_console()

    return entrada
