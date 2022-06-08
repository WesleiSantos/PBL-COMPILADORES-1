from token import Token

class Analisador_sintatico:
    def __init__(self, listTokens) -> None:
        self.tokens_list = listTokens
        self.token_position = -1

    def readTokens(self):
        self.start()
    
    def start(self):
        token = self.nextToken() #LER O PRIMEIRO TOKEN
        if(token.getClass()=="palavra_reservada"):
            print("palavra reservada")
            if(token.getLexema()=="program"):
                print("program")
                self.identifier()
                self.delimitador_ponto_virgula()
                self.globalStatement():

    def globalStatement(self):
        #self.varStatement()
        #self.constStatement()
        #self.registerStatement()
        #self.procedureStatement()
        #self.functionStatement()
        #self.main()

    def varStatement(self):
        token = self.nextToken()
        if(token.getLexema()=='var'):
            print("palavra_reservada, var")
            self.delimitador_abre_colchete()
            self.varlist() 

    def varlist(self):
        if(self.varDeclaration() and self.varList1()):
            return
        elif(self.delimitador_fecha_colchete()):
            return
        else:  ##erro

    def varDeclaration(self):
        if(self.varType() and self.identificador() and self.varDeclaration1()):
            return True

    def varList1(self):
        if(self.varDeclaration() and self.varList1()):
        elif(self.delimitador_fecha_colchete()):
        else: #erro
        
    def varDeclaration1(self):
        if(self.delimitador_virgula() and self.identificador() and self.varDeclaration1()):
        elif(self.delimitador_ponto_virgula()):
        else: #erro
            
    def varType(self):
        token = self.nextToken()
        if(token.getClass()=='integer'
          or 'string' or 'real' or 'boolean' or 'char'
          #or Identifier?
        ): return
            

    # def constStatement():
    # def registerStatement():
    # def procedureStatement():
    # def functionStatement():
    # def main():

    def delimitador_ponto_virgula(self):
        token = self.nextToken()
        if(token.getLexema()==";"):
            print("delimitador ;")
            return 
        
    def delimitador_virgula(self):
        token = self.nextToken()
        if(token.getLexema()==","):
            print("delimitador ,")
            return True

    def delimitador_abre_colchete(self):
        token = self.nextToken()
        if(token.getLexema()=="{"):
            print("delimitador {")
            return

    def delimitador_fecha_colchete(self):
        token = self.nextToken()
        if(token.getLexema()=="}"):
            print("delimitador }")
            return

    def identifier(self):
        token = self.nextToken()
        if(token.getClass()=="identificador"): ##verifica se o token é um identificador
            print("identificador, ", token.getLexema())
            return True
    

    def nextToken(self):
        self.token_position+=1
        return self.tokens_list[self.token_position]