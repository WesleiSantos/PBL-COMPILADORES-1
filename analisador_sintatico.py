from token import Token

class Analisador_sintatico:
    def __init__(self, listTokens) -> None:
        self.tokens_list = listTokens
        self.token_position = -1

    def readTokens(self):
        self.start()
    
    def start(self):
        token = self.nextToken() #LER O PRIMEIRO TOKEN
        if(token.getLexema()=="program"):
            print("program")
            self.identifier()
            if(token.getLexema()==';'):
                self.globalStatement()
            else:
                print("ESPERADO UM PONTO E VÍRGULA")
                self.globalStatement()
        else: ############# TALVEZ NEM EU SAIBA O QUE FIZ AQUI....
            print("ESPARADO A PALAVRA RESERVADA 'PROGRAM'")
            while(self.nextToken().getLexema()==';'):
                print("ERRO")

    def globalStatement(self):
        #self.varStatement()
        #self.constStatement()
        #self.registerStatement()
        #self.procedureStatement()
        #self.functionStatement()
        #self.main()
        
    ############################ TALVEZ OK
    def procedureStatement(self):
        if(self.nextToken().getLexema()=='procedure'):
            print("PROCEDURE")
            if(self.nextToken().getClass()=='Identifier'):
                if(self.nextToken().getLexema()=='('):
                    parameterProcedure()
                    if(self.nextToken().getLexema()=='{'):
                        localStatement() ####>>>> FALTA A FUNÇÃO
                        procedureStatement1()
                        return
                    
    def parameterProcedure(self):
        token = self.nextToken().getClass
        if(token in ('integer', 'real', 'string','real','boolean', 'char')):
            if(self.nextToken().getClass()=='Identifier'):
                self.parameterListProcedure()
                return
        elif(self.nextToken().getLexema()==')'):
            return

    def parameterListProcedure(self):
        if(self.nextToken().getLexema()==','):
            self.parameterProcedure()
            return
            
            
   
  #########################################
            
    def localStatement(self):

    def procedureStatement1(self):
        if(self.nextToken().getLexema()=='}'):
            return:
        elif(self.nextToken().getLexema()=='}'):
            return
        
        
#################################################### TALVEZ OK        
    def varStatement(self):
        if(self.token.getLexema()=='var'):
            print("palavra_reservada, var")
          if(self.nextToken().getLexema()=='{'):
            self.varlist() 
            return

    def varlist(self):
        token = self.nextToken().getClass
        if(token in ('integer', 'real', 'string','real','boolean', 'char')):
            if(self.nextToken().getClass()=='Identifier'):
                self.varDeclaration()
            self.varlist()
            return
        elif(self.nextToken().getLexema()=='}':
            return
        else:  ##erro

    def varDeclaration(self):
        token = self.nextToken().getClass
        if(token in ('integer', 'real', 'string','real','boolean', 'char')):
            if(self.nextToken().getClass()=='Identifier'):
                self.varDeclaration()
                return
            
    def varList1(self):
        token = self.nextToken().getClass
        if(token in ('integer', 'real', 'string','real','boolean', 'char')):
            self.varList1()
        elif(self.nextToken().getLexema()=='}'):
            return
        else: #erro
        
    def varDeclaration1(self):
        if(self.nextToken().getLexema()==','):
            if(self.nextToken().getClass()=='Identifier'):
                self.varDeclaration1()
        elif(self.nextToken().getLexema()==';'):
            return
        else: #erro
  ######################################################################
            

    # def constStatement():
    # def registerStatement():
    # def procedureStatement():
    # def functionStatement():
    # def main():




    def nextToken(self):
        self.token_position+=1
        return self.tokens_list[self.token_position]