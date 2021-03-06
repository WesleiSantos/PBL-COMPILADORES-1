class Token:
    def __init__(self,posicao,classe,lexema, error=False) -> None:
        self._posicao = posicao
        self._classe = classe
        self.lexema = lexema
        self.error = error 
    
    def hasError(self):
        return self.error

    def get(self):
       return "<"+str(self._posicao)+","+str(self._classe)+","+str(self.lexema)+">"

    def getClass(self):
        return ""+self._classe

    def getLexema(self):
        return ""+self.lexema
    
    def getPosition(self):
        return self._posicao