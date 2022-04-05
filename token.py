class Token:
    def __init__(self,posicao,classe,lexema) -> None:
        self._posicao = posicao
        self._classe = classe
        self.lexema = lexema
    

    def get(self):
       return "<"+str(self._posicao)+","+str(self._classe)+","+str(self.lexema)+">"