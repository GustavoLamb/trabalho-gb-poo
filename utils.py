import os


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
                    input("Pressione ENTER para continuar")
                    limpar_console()

                continue

            seguro = True
        except ValueError as E:
            print("Erro: Valor inválido")
            input("Pressione ENTER para continuar")
            limpar_console()

    return entrada
