import os
from veiculo import Veiculo
from locacao import Locacao

LOCACOES_FILE = './arquivos/locacoes.txt'
VEICULO_FILE = './arquivos/veiculos.txt'


class Locadora:

    def __init__(self) -> None:
        self._veiculos = self._carregar_veiculos()
        self._locacoes = self._carregar_locacoes(self._veiculos)
        

    # Métodos públicos
    def consultar_veiculos(self, atributo, valor):
        pass    


    #Getters
    def get_veiculos(self):
        return self._veiculos
    
    def get_locacoes(self):
        return self._locacoes

    # Métodos privados
    def _carregar_veiculos(self):
        if not os.path.isfile(VEICULO_FILE):
            print("Não existe arquivo com dados do Veículo")
            return []

        lista_veiculo = []
        arquivo = open(VEICULO_FILE, 'r')
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
        arquivo = open(LOCACOES_FILE, 'r')
        arquivo.readline()  # Descarta cabeçalho
        for linha in arquivo:
            lista_locacoes.append(Locacao(linha=linha.strip(), veiculos=veiculos))
        arquivo.close()

        return lista_locacoes
