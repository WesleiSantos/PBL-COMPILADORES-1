class Erro:
    def __init__(self,posicao, erro) -> None:
        self.posicao = posicao
        self.erro = erro
        
    def getErro(self):
        return self.erro
    
    def getPosition(self):
        return self.posicao
        