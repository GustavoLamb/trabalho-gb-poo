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

        print(f"Valor total díarias: {locacao.valor_diarias():.2f}")
        if entrada_segura("\nDeseja realizar a locacao: ", opcoes='SsNn') in 'Nn':
            print("Locação não realizada!")
            return None

        self._atualizar_disponibilidade_veiculo(locacao.get_veiculo().get_codigo(), False)
        self._locacoes.append(locacao)
        print("Locação realizado com sucesso!!")

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
        diarias = entrada_segura('Informe o número de díarias: ', int)

        limpar_console()
        return Locacao(veiculo_escolhido, nome_cliente, cidade_origem, diarias)
    
    def _atualizar_disponibilidade_veiculo(self, cod_veiculo, disponivel):
        for veiculo in self._veiculos:
            if veiculo.get_codigo() == cod_veiculo:
                veiculo.set_disponivel(disponivel)
                break