import os
from veiculo import Veiculo
from locacao import Locacao
from utils import table_format, entrada_segura, limpar_console
from typing import List

LOCACOES_FILE = './arquivos/locacoes.txt'
VEICULOS_FILE = './arquivos/veiculos.txt'

CABECALHO_VEICULOS = 'codigo\tmodelo\tcor\tano\todometro\tcidade\tdisponivel\tvalor_diaria\tvalor_km_rodado'
CABECALHO_LOCACOES = 'veiculo\tcliente\torigem\tdestino\tkm_rodado\tqt_dias_reserva\tqt_dias_realizado'

class Locadora:

    def __init__(self):
        self._veiculos: List[Veiculo] = [] 
        self._locacoes: List[Locacao] = [] 
        
        self.carregar_dados()

    # Métodos públicos
    def carregar_dados(self):
        self._veiculos = self._carregar_veiculos()
        self._locacoes = self._carregar_locacoes(self._veiculos)

    def salvar_dados(self):
        self._salvar_dados(self._veiculos, CABECALHO_VEICULOS, VEICULOS_FILE, 'Veiculos')
        self._salvar_dados(self._locacoes, CABECALHO_LOCACOES, LOCACOES_FILE, 'Locações')

    def consultar_veiculos(self, atributo, valor):
        data = []
         
        for veiculo in self._veiculos:
            if getattr(veiculo, f'_{atributo}') == valor:
                data.append(veiculo.get_row())
        
        if len(data) == 0:
            print("Nenhum veículo encontrado")
        else:
            table_format(CABECALHO_VEICULOS, data)
    
    def realizar_locacao(self, cidade_origem):
        veiculos_disponiveis = []

        for veiculo in self._veiculos:
            if veiculo.get_cidade() == cidade_origem and veiculo.is_disponivel():
                veiculos_disponiveis.append(veiculo)
        
        if len(veiculos_disponiveis) == 0:
            print("Nenhum véiculo disponivel")
            return None

        print(f"Veículos disponíveis para {cidade_origem}: \n")
        table_format(CABECALHO_VEICULOS, [veiculo.get_row() for veiculo in veiculos_disponiveis])

        locacao = self._realiza_locacao(veiculos_disponiveis, cidade_origem)
        if locacao is None:
            return None

        veiculo = locacao.get_veiculo()

        print(f"Valor total díarias: {locacao.valor_diarias():.2f}")
        if entrada_segura("\nDeseja realizar a locacao: (S/N) \n: ", opcoes='SsNn') in 'Nn':
            print("Locação não realizada!")
            return None

        veiculo.set_disponivel(False)
        self._locacoes.append(locacao)
        print("Locação realizada com sucesso!!")

    def consultar_locacoes(self, busca):
        data_veiculos = []
        data_locacao = []

        for locacao in self._locacoes:
            if locacao.get_cliente() == busca or locacao.get_veiculo().get_modelo() == busca:
                data_locacao.append(locacao.get_row())
                data_veiculos.append(locacao.get_veiculo().get_row())
        
        if len(data_locacao) == 0:
            print("Nenhuma locação encontrada")
        else:
            print("Locações: \n")
            table_format(CABECALHO_LOCACOES, data_locacao, width = 20)
            print("\nVeiculos: \n")
            table_format(CABECALHO_VEICULOS, data_veiculos)

    def realizar_devolucao(self, cliente, cidade_devolucao, km_percorrido):
        locacao_cliente = self._consultar_locacao_cliente(cliente)
        veiculo_cliente = locacao_cliente.get_veiculo()

        if locacao_cliente == None:
            print("Cliente informado não possui locação!!")
            return None
        
        print(f"Dias contratados: {locacao_cliente.get_qt_dias_reserva()} dias.")
        resposta = entrada_segura("Foram utilizados apenas esses dias: (S/N) ", opcoes='SsNn')

        if resposta in 'Nn':
            dias = entrada_segura("Quantos dias foram utilizados: \n", int)
            locacao_cliente.set_qt_dias_realizado(dias)
        else:
            locacao_cliente.set_qt_dias_realizado(locacao_cliente.get_qt_dias_reserva())
        
        locacao_cliente.set_km_rodado(km_percorrido)

        limpar_console()

        valor_diarias = locacao_cliente.valor_diarias(True)
        valor_km = locacao_cliente.valor_km_rodado()
        print(f"Valor referente aos KM percorridos: {valor_km:.2f}")
        print(f"Valor total locação: {valor_diarias + valor_km:.2f}")
        input("\nPressione ENTER para continuar")

        limpar_console()
        odometro_atualizado = veiculo_cliente.get_odometro() + km_percorrido
        locacao_cliente.set_destino(cidade_devolucao)
        veiculo_cliente.set_odometro(odometro_atualizado)
        veiculo_cliente.set_disponivel(True)
        print("Devolução concluída com sucesso!!")

    #Getters
    def get_veiculos(self):
        return self._veiculos
    
    def get_locacoes(self):
        return self._locacoes

    # Métodos privados
    def _carregar_veiculos(self):
        if not os.path.isfile(VEICULOS_FILE):
            print("Não existe arquivo com dados do Veículo")
            return []

        lista_veiculo = []
        arquivo = open(VEICULOS_FILE, 'r', encoding='utf-8')
        arquivo.readline()  # Descarta cabeçalho
        for linha in arquivo:
            lista_veiculo.append(Veiculo(linha=linha.strip()))
        arquivo.close()

        return lista_veiculo

    def _carregar_locacoes(self, veiculos):
        if not os.path.isfile(LOCACOES_FILE):
            print("Não existe arquivo com dados de Pessoas")
            return []

        lista_locacoes = []
        arquivo = open(LOCACOES_FILE, 'r', encoding='utf-8')
        arquivo.readline()  # Descarta cabeçalho
        for linha in arquivo:
            lista_locacoes.append(Locacao(linha=linha.strip(), veiculos=veiculos))
        arquivo.close()

        return lista_locacoes

    def _salvar_dados(self, lista, cabecalho, file_name, param):
        arquivo = open(file_name, 'w', encoding='utf-8')
        arquivo.write(cabecalho)
        for valor in lista:
            arquivo.write(valor.serializar())
        arquivo.close()

        print(f'{param} salvos com sucesso!!')
    
    def _realiza_locacao(self, veiculos_disponiveis, cidade_origem):
        veiculo_escolhido = None
        codigos_validos = [veiculo.get_codigo() for veiculo in veiculos_disponiveis]
        codigo_veiculo = entrada_segura('\nInforme o código do veículo: ', int, opcoes=codigos_validos)
        for veiculo in veiculos_disponiveis:
            if codigo_veiculo == veiculo.get_codigo():
                veiculo_escolhido = veiculo
                break
        
        nome_cliente = entrada_segura('Informe o seu nome: ')

        if self._consultar_locacao_cliente(nome_cliente):
            print("Cliente já possui a locação de um véiculo")
            return None

        diarias = entrada_segura('Informe o número de díarias: ', int)

        limpar_console()
        return Locacao(veiculo_escolhido, nome_cliente, cidade_origem, diarias)
 
    def _consultar_locacao_cliente(self, cliente):
        
        for locacao in self._locacoes:
            if locacao.get_cliente() == cliente and not locacao.is_finalizado():
                return locacao

        return None
    
    def resumo(self):
        cont = 0
        print("-- Resumo Locações Finalizadas -- ")
        for locacao in self._locacoes:
            if locacao.is_finalizado() == True:
                cont +=1
                print("Locação Finalizada n°", cont,"- Cód. Veículo", locacao.get_veiculo().get_codigo())
                print("Kms rodados", locacao.get_km_rodado(),"km") 
                print("Dias contratados:", locacao.get_qt_dias_reserva(),"dias") 
                print("Dias realizados:",locacao.get_qt_dias_realizado(), "dias") 
                print('Valor das diárias contratadas: R$ {:.2f}'.format(locacao.diarias_contrat())) 
                print('Valor das diárias extras: R$ {:.2f}'.format(locacao.diarias_extra())) 
                print('Valor dos kms rodados: R$ {:.2f}'.format(locacao.valor_km_rodado()))
                print('Valor Total da locação: R$ {:.2f}'.format(locacao.valor_total()))
                print()
