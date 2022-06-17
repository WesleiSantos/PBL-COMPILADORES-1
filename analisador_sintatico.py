from token import Token
VAR_TYPES = ('integer', 'real', 'string', 'boolean', 'char')
CONST_TYPES = ('integer', 'real', 'string', 'boolean', 'char')

class Analisador_sintatico:
    def __init__(self, listTokens) -> None:
        self.tokens_list = listTokens
        self.token_position = -1
        

    def readTokens(self):
        print("\n_________________________\nANALISE SINTÁTICA\n_________________________")            
        self.start()

    def ERROR(self, simb_sinc):
        while(self.nextToken().getLexema() not in tokens_sinc):
                print("ERRO")
        
    def start(self):
        token = self.nextToken() #LER O PRIMEIRO TOKEN
        if(token.getLexema() == "program"):
            print(token.getLexema())
            token = self.nextToken()
        else:
            print("ESPARADO A PALAVRA RESERVADA 'PROGRAM'")
            self.ERROR((';', 'var'))
        if(token.getClass() == 'identificador'):
            print(token.getLexema())
            token = self.nextToken()
        else:
            print("ESPARADO UM IDENTIFICADOR")
            self.ERROR((';', 'var'))
        if(token.getLexema()==';'):
            print(token.getLexema())
            self.globalStatement()
        else:
            print("ESPERADO UM PONTO E VÍRGULA")
            self.globalStatement()            
    

    def globalStatement(self):
        print("GLOBAL STATMENT")
        self.varStatement()
        self.constStatement()
        self.registerStatement()
        #self.procedureStatement()
        #self.functionStatement()
        #self.main()

#################  VAR  #############################   
    def varStatement(self):
        print("VAR STATMENT")
        token = self.nextToken()
        if(token.getLexema() == 'var'):
            print(token.getLexema())
            token = self.nextToken()
        else:
            print("ESPERADO PALAVRA RESERVADA VAR")
            self.ERROR(('}',';'))               
        if(token.getLexema()=='{'):
            print(token.getLexema())
            self.varlist() 
        else:
            print("ESPERADO PALAVRA RESERVADA '{'")

    def varlist(self):
        print("VAR LIST")
        token = self.nextToken()
        if(token.getLexema() in VAR_TYPES):
            self.previousToken()
            self.varDeclaration()
            self.varlist()
        elif(token.getLexema() == '}'):
            print(token.getLexema())
            return    
        else: 
            print("ERRO")
            return ##erro

    def varList1(self):
        token = self.nextToken()
        if(token in ('integer', 'real', 'string','real','boolean', 'char')):
            print(token.getLexema())
            self.varList1()
        elif(self.getLexema()=='}'):
            print(token.getLexema())
            return
        else: 
            print("ERRO")
            return #erro

    def varDeclaration(self):
        print("VAR DLECARATION")
        self.varType()
        token = self.nextToken()
        if(token.getClass() == 'identificador'):
            print(token.getLexema())
            self.varDeclaration1()
            return
        else:
            print("ERRO")
            return #ERROR
        
    def varDeclaration1(self):
        print('VAR DECLARATION 1')
        token = self.nextToken()
        if(token.getLexema()==';'):
            print(token.getLexema())
            return
        elif(token.getLexema()==','):
            print(token.getLexema())
            token = self.nextToken()
            if(token.getClass() == 'identificador'):
                print(token.getLexema())
                self.varDeclaration1()    
            else: 
                print("ERRO")
                return #erro
        else:
           print("ERRO")
           return #ERROR
    
    def varType(self):
        print("VAR TYPE")
        token = self.nextToken()
        if(token.getLexema() in VAR_TYPES):
            print(token.getLexema())
            return
        else:
            print("ERRO")
            return #ERROR

#################  CONST  #############################   
    def constStatement(self):
        print("CONST STATMENT")
        token = self.nextToken()
        if(token.getLexema() == 'const'):
            print(token.getLexema())
            token = self.nextToken()
        else:
            print("ESPERADO PALAVRA RESERVADA CONST")
            self.ERROR(('}',';'))               
        if(token.getLexema()=='{'):
            print(token.getLexema())
            self.constlist() 
        else:
            print("ESPERADO PALAVRA RESERVADA '{'")

    def constlist(self):
        print("CONST LIST")
        token = self.nextToken()
        if(token.getLexema() in CONST_TYPES):
            self.previousToken()
            self.constDeclaration()
            self.constlist()
        elif(token.getLexema() == '}'):
            print(token.getLexema())
            return    
        else: 
            print("ERRO")
            return ##erro
    
    def constList1(self):
        token = self.nextToken()
        if(token in ('integer', 'real', 'string','real','boolean', 'char')):
            print(token.getLexema())
            self.constList1()
        elif(self.getLexema()=='}'):
            print(token.getLexema())
            return
        else: 
            print("ERRO")
            return #erro

    def constDeclaration(self):
        print("CONST DLECARATION")
        self.constType()
        token = self.nextToken()
        if(token.getClass() == 'identificador'):
            print(token.getLexema())
            token = self.nextToken()
        else:
            print("ERRO")
            return #ERROR
        if(token.getLexema()=='='):
            print(token.getLexema())
            self.value()
            self.constDeclaration1()
            return
        else: 
            print("ERRO")
            return #erro
    
    def constDeclaration1(self):
        print('CONST DECLARATION 1')
        token = self.nextToken()
        if(token.getLexema()==';'):
            print(token.getLexema())
            return
        elif(token.getLexema()==','):
            print(token.getLexema())
            token = self.nextToken()
            if(token.getClass() == 'identificador'):
                print(token.getLexema())
                self.value()
                self.constDeclaration1()
                return
            else: 
                print("ERRO")
                return #erro
        else:
           print("ERRO")
           return #ERROR
    
    def constType(self):
        print("CONST TYPE")
        token = self.nextToken()
        if(token.getLexema() in CONST_TYPES):
            print(token.getLexema())
            return
        else:
            print("ERRO")
            return #ERROR
    
    def value(self):
        token = self.nextToken()
        if(token.getClass() in ('inteiro','ponto_flutuante','cadeira de caracteres','caracter','true','false')):
            print(token.getLexema())            
            return
        elif(token.getClass() in 'identificador'):
            self.valueRegister()
            return
        else:
            print("ERRO")
            return #ERROR

    def valueRegister(self):
        token = self.nextToken()
        if(token.getLexema() == '.'):
            print(token.getLexema())
            token = self.nextToken()
            if(token.getClass() in 'identificador'):
                print(token.getLexema())
                return
            else:
                print("ERRO")
                return #ERROR
        else:
            return 



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
        print("localStatement")

    def procedureStatement1(self):
        if(self.nextToken().getLexema()=='}'):
            return 
        elif(self.nextToken().getLexema()=='}'):
            return

  ######################################################################

    # def constStatement():
    # def registerStatement():
    # def procedureStatement():
    # def functionStatement():
    # def main():




    def nextToken(self):
        self.token_position+=1
        return self.tokens_list[self.token_position]
    def previousToken(self):
        self.token_position-=1
        return self.tokens_list[self.token_position]