class Token:
    def __init__(self,posicao,classe,lexema) -> None:
        self._posicao = posicao
        self._classe = classe
        self.lexema = lexema
    

    def get(self):
        print("<",self._posicao,",",self._classe,",",self.lexema,">")