from utils import conversao_segura

class Veiculo:

    # Construtor
    def __init__(self, linha=''):
        self._codigo = 0
        self._modelo = ''
        self._cor = ''
        self._ano = 0
        self._odometro = 0
        self._cidade = ''
        self._disponivel = False
        self._valor_diaria = 0.0
        self._valor_km_rodado = 0.0
        
        if linha != '':
            self.deserializar(linha)
    

    # Métodos especias
    def serializar(self):
        disponivel_str = 'S' if self._disponivel else 'N'

        return f'\n{self._codigo}\t{self._modelo}\t{self._cor}\t{self._ano}\t{self._odometro}' + \
            f'\t{self._cidade}\t{disponivel_str}\t{self._valor_diaria}\t{self._valor_km_rodado}'
    
    def deserializar(self, linha):
        dados = linha.split("\t")
        self.set_codigo(conversao_segura(int, dados[0], 0, 'codigo'))
        self.set_modelo(conversao_segura(str, dados[1], '', 'modelo'))
        self.set_cor(conversao_segura(str, dados[2], '', 'cor'))
        self.set_ano(conversao_segura(int, dados[3], 0, 'ano'))
        self.set_odometro(conversao_segura(int, dados[4], 0, 'odometro'))
        self.set_cidade(conversao_segura(str, dados[5], '', 'cidade'))
        self.set_disponivel(conversao_segura(str, dados[6], 'N', 'disponivel'))
        self.set_valor_diaria(conversao_segura(float, dados[7], 0.0, 'valor_diaria'))
        self.set_valor_km_rodado(conversao_segura(float, dados[8], 0.0, 'valor_km_rodado'))


    # Getters and Setters
    def get_codigo(self):
        return self._codigo

    def set_codigo(self, codigo):
        if not isinstance(codigo, int):
            return None

        self._codigo = codigo
    
    def get_modelo(self):
        return self._modelo

    def set_modelo(self, modelo):
        if not isinstance(modelo, str):
            return None

        self._modelo = modelo.capitalize()
    
    def get_cor(self):
        return self._cor

    def set_cor(self, cor):
        if not isinstance(cor, str):
            return None

        self._cor = cor.capitalize()
    
    def get_ano(self):
        return self._ano

    def set_ano(self, ano):
        if not isinstance(ano, int):
            return None
        
        self._ano = ano
    
    def get_odometro(self):
        return self._odometro

    def set_odometro(self, odometro):
        if not isinstance(odometro, int):
            return None

        self._odometro = odometro
    
    def get_cidade(self):
        return self._cidade

    def set_cidade(self, cidade):
        if not isinstance(cidade, str):
            return None
        
        self._cidade = cidade
    
    def is_disponivel(self):
        return self._disponivel

    def set_disponivel(self, disponivel):
        if isinstance(disponivel, str):
            disponivel = True if disponivel == 'S' else False

        if not isinstance(disponivel, bool):
            return None
        
        self._disponivel = disponivel
    
    def get_valor_diaria(self):
        return self._valor_diaria

    def set_valor_diaria(self, valor_diaria):
        if not isinstance(valor_diaria, float):
            return None

        self._valor_diaria = valor_diaria
    
    def get_valor_km_rodado(self):
        return self._valor_km_rodado

    def set_valor_km_rodado(self, valor_km_rodado):
        if not isinstance(valor_km_rodado, float):
            return None

        self._valor_km_rodado = valor_km_rodado
    
    def get_row(self):
      return self.serializar().replace('\n', '')  

