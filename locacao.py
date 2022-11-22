from typing import List
from utils import conversao_segura
from veiculo import Veiculo

class Locacao:

    # Construtor
    def __init__(self, veiculo=None, cliente='', origem='', qt_dias_reserva=0, linha='', veiculos=[]):
        self._veiculo: Veiculo = veiculo
        self._cliente = cliente
        self._origem = origem
        self._destino = ''
        self._km_rodado = 0
        self._qt_dias_reserva = qt_dias_reserva
        self._qt_dias_realizado = 0

        if linha != '' and len(veiculos) != 0:
            self.deserializar(linha, veiculos)

    # Métodos publicos 
    def valor_diarias(self, utilizado=False):
        valor_veiculo = self._veiculo.get_valor_diaria()
        valor = valor_veiculo * self._qt_dias_reserva

        if utilizado:
            if self._qt_dias_reserva > self._qt_dias_realizado:
                return valor - (valor * 0.2)
            elif self._qt_dias_reserva < self._qt_dias_realizado:
                return valor + valor * 0.3
            else:
                return valor

        return valor 
    
    def diarias_contrat(self):
        valor_veiculo = self._veiculo.get_valor_diaria()
        valor = valor_veiculo * self._qt_dias_reserva
        return valor
    
    def diarias_extra(self):
        extra = self._qt_dias_realizado - self._qt_dias_reserva
        if extra > 0:
            valor_extra = self._veiculo.get_valor_diaria() + (self._veiculo.get_valor_diaria() * 0.3)
            return extra * valor_extra
        else:
            return 0
    
    def valor_total(self):
        if self._qt_dias_realizado < self._qt_dias_reserva:
            dias_desconto = self._qt_dias_reserva - self._qt_dias_realizado
            return self.diarias_contrat() + dias_desconto * (self._veiculo.get_valor_diaria() * 0.2)
        else:
            return self.diarias_extra() + self.diarias_contrat()
    
    def valor_km_rodado(self):
        valor_veiculo = self._veiculo.get_valor_km_rodado()

        return valor_veiculo * self._km_rodado
    
    def is_finalizado(self):
        return self._qt_dias_realizado !=0 and self._km_rodado != 0

    # Métodos especiais
    def serializar(self):
        id_veiculo = self._veiculo.get_codigo()
        km_rodado = self._km_rodado if self._qt_dias_realizado !=0 else ''
        dias_realizados = self._qt_dias_realizado if self._qt_dias_realizado !=0 else ''

        return f'\n{id_veiculo}\t{self._cliente}\t{self._origem}\t{self._destino}\t{km_rodado}' + \
            f'\t{self._qt_dias_reserva}\t{dias_realizados}'
    
    def deserializar(self, linha, veiculos: List[Veiculo]):
        dados = linha.split('\t')
        self.set_cliente(conversao_segura(str, dados[1], '', 'cliente'))
        self.set_origem(conversao_segura(str, dados[2], '', 'origem'))
        self.set_destino(conversao_segura(str, dados[3], '', 'destino'))
        self.set_km_rodado(conversao_segura(int, dados[4], 0, 'km_rodado'))
        self.set_qt_dias_reserva(conversao_segura(int, dados[5], '', 'qt_dias_reserva'))
        try:
            self.set_qt_dias_realizado(conversao_segura(int, dados[6], 0, 'qt_dias_realizado'))
        except IndexError as e:
            print("Sem informação de dias realizados locação")
        
        id_veiculo_locacao = conversao_segura(int, dados[0], 0, 'veiculo')

        for veiculo in veiculos:
            if veiculo.get_codigo() == id_veiculo_locacao:
                self.set_veiculo(veiculo)
                break
       

    # Getters e Setters
    def get_veiculo(self):
        return self._veiculo

    def set_veiculo(self, veiculo):
        if not isinstance(veiculo, Veiculo):
            return None
        
        self._veiculo = veiculo

    def get_cliente(self):
        return self._cliente

    def set_cliente(self, cliente):
        if not isinstance(cliente, str):
            return None
        
        self._cliente = cliente

    def get_origem(self):
        return self._origem

    def set_origem(self, origem):
        if not isinstance(origem, str):
            return None
        
        self._origem = origem

    def get_destino(self):
        return self._destino

    def set_destino(self, destino):
        if not isinstance(destino, str):
            return None
        
        self._destino = destino
    
    def get_km_rodado(self):
        return self._km_rodado

    def set_km_rodado(self, km_rodado):
        if not isinstance(km_rodado, int):
            return None
        
        self._km_rodado = km_rodado
    
    def get_qt_dias_reserva(self):
        return self._qt_dias_reserva

    def set_qt_dias_reserva(self, qt_dias_reserva):
        if not isinstance(qt_dias_reserva, int):
            return None
        
        self._qt_dias_reserva = qt_dias_reserva

    def get_qt_dias_realizado(self):
        return self._qt_dias_realizado

    def set_qt_dias_realizado(self, qt_dias_realizado):
        if not isinstance(qt_dias_realizado, int):
            return None
        
        self._qt_dias_realizado = qt_dias_realizado

    def get_row(self):
      return self.serializar().replace('\n', '')