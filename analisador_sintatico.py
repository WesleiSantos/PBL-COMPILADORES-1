from pickle import NONE
from token import Token
from erro import Erro

VAR_TYPES = ('integer', 'real', 'string', 'boolean', 'char')
CONST_TYPES = ('integer', 'real', 'string', 'boolean', 'char')

class Analisador_sintatico:
    def __init__(self, listTokens) -> None:
        self.tokens_list = listTokens
        self.token_position = -1
        

    def readTokens(self):
        print("\n_________________________\nANALISE SINTÁTICA\n_________________________")            
        self.start()

    def ERROR(self, tokens_sinc):
        token = self.nextToken()
        while(token.getLexema() not in tokens_sinc):
            print("ERRO", token.getLexema())
            token = self.nextToken()
        return token
        
    def start(self):
        token = self.nextToken() #LER O PRIMEIRO TOKEN
        if(token.getLexema() == "program"):
            print(token.getLexema())
            token = self.nextToken()
        else:
            print("ESPERADO A PALAVRA RESERVADA 'PROGRAM'")
           # tk_previous=token #para saber a posição do token anterior (onde esta o erro)
            self.previousToken()
            token = self.ERROR((';', 'var', 'const')) ##se encontrar o um dos token de sicrnz.
            if(token.getLexema() == ';'):
                #erro = Erro(tk_previous.getPosition(), "ESPERADO A PALAVRA RESERVADA 'PROGRAM'")
                #print(tk_previous.getPosition())
                self.globalStatement()
            if(token.getLexema() == 'var'):
                #erro = Erro(tk_previous.getPosition() ", ESPERADO A PALAVRA RESERVADA 'PROGRAM'")
                #print(tk_previous.getPosition())
                
                self.previousToken()
                self.globalStatement()
            if(token.getLexema()== 'const'):
                print("NAO FOI DECLARADO O 'VAR'")
                self.previousToken()
                self.constStatement()
                self.registerStatement()
                
            return
            
        if(token.getClass() == 'identificador'):
            print(token.getLexema())
            token = self.nextToken()
        else:
            print("ESPERADO UM IDENTIFICADOR")
            
            self.previousToken()
            token=self.ERROR((';', 'var'))
            
            if(token.getLexema() == ';'):
                print(tk_previous.getPosition())
            elif(token.getLexema() == 'var'):
                print(tk_previous.getPosition())
                
                self.previousToken()
            self.globalStatement()
            return
            
        if(token.getLexema()==';'):
            print(token.getLexema())
            self.globalStatement()
            return
        else:
            print("ESPERADO UM PONTO E VÍRGULA")
            self.globalStatement()  
            return          
    

    def globalStatement(self):
        print("GLOBAL STATMENT")
        self.varStatement()
        self.constStatement()
        self.registerStatement()
        self.procedureStatement()
        self.functionStatement()
        #self.main()

#################  VAR  #############################   
    def varStatement(self):
        print("VAR STATMENT")
        token = self.nextToken()
        if(token.getLexema() == 'var'):
            print(token.getLexema())
            token = self.nextToken()
        else:
            print("ESPERADO PALAVRA RESERVADA 'VAR'")
                
            self.previousToken()
            token = self.ERROR(('{',';'))
            
            if(token.getLexema()==";"):
                print("ESPERADO VAR '{' ")
                
            ##a continuação é a mesma para caso encontrado o { ou ;
            self.varlist()
            self.constStatement()
            self.registerStatement()
            
            return
                      
        if(token.getLexema()=='{'):
            print(token.getLexema())
            self.varlist() 
        else:
            self.previousToken()
            print("ERROR: ESPERADO O DELIMITADOR '{' ")
            token = self.ERROR(('integer', 'real', 'string', 'boolean', 'char', 'const'))
            if(token.getLexema() in VAR_TYPES):
                self.previousToken()
                self.varlist()
            elif(token.getLexema() == 'const'):
                print("ESPERADO UMA DECLAÇÃO DE VARIAVEL COM SEU TIPO")
                self.previousToken()
        return   
            

    def varlist(self):
        print("VAR LIST")
        token = self.nextToken()
        if(token.getLexema() in VAR_TYPES):
            self.previousToken()
            self.varDeclaration()
            self.varlist()
        elif(token.getLexema() == '}'):
            print(token.getLexema())
            #return    
        else: 
            self.previousToken()
            token = self.ERROR((';','const'))
            if(token.getLexema()==';'):
                print("ESPERADO UM TIPO DE VARIAVEL")
                self.varlist()
            elif(token.getLexema()=='const'):
                print("ESPERADO '}' ")
                self.previousToken()
                self.constStatement()
                self.registerStatement()
            #return ##erro

    def varList1(self):
        token = self.nextToken()
        if(token.getLexema() in VAR_TYPES):
            print(token.getLexema())
            self.varList1()
        elif(token.getLexema()=='}'):
            print(token.getLexema())
            return
        else: 
            print("ESPERADO UM TIPO DE VARIAVEL OU UM }")
            self.ERROR((',',';'))
            #return #erro

    def varDeclaration(self):
        print("VAR DLECARATION")
        self.varType()
        token = self.nextToken()
        if(token.getClass() == 'identificador'):
            print(token.getLexema())
            self.varDeclaration1()
            return
        else:
            print("ESPERADO UM IDENTIFICADOR")
            self.ERROR((',',';'))
            #return #ERROR
        
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
                print("ESPERADO UM IDENTIFICADOR")
                self.ERROR((',',';'))
                #return #erro
        else:
           print("ESPERADO , OU ;")
           self.ERROR((',',';'))
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
            self.previousToken()
            token = self.ERROR(('{','integer', 'real', 'string', 'boolean', 'char', ';'))
            
            if(token.getLexema() in ('integer', 'real', 'string', 'boolean', 'char')):
                print("ESPERADO const '{'")
                self.previousToken()
                
            if(token.getLexema()==";"):
                print("ESPERADO const '{' TYPE VARIABLE ")
                
            ##a continuação é a mesma para caso encontrado o { ou ;
            self.constlist()
            self.registerStatement()
            
            return
                     
        if(token.getLexema()=='{'):
            print(token.getLexema())
            self.constlist() 
        else:
            print("ESPERADO '{'")
            self.previousToken()
            token = self.ERROR((';','register'))
            if(token.getLexema()==";"):
                self.constlist()
                self.registerStatement()
            elif(token.getLexema()=="register"):
                print("HÁ PROBLEMAS NO ESCOPO const")
                self.registerStatement()
            
            return
            

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
           print("ESPERANDO ';' OU ','")
           return #ERROR
    
    def constType(self):
        print("CONST TYPE")
        token = self.nextToken()
        if(token.getLexema() in CONST_TYPES):
            print(token.getLexema())
            return
        else:
            print("ERROR")
            return #ERROR
    
    def value(self):
        token = self.nextToken()
        if(token.getClass() in ('inteiro','ponto_flutuante','cadeira de caracteres','caracter','true','false')):
            print(token.getLexema())            
            return
        elif(token.getClass() in 'identificador'):
            print(token.getLexema())            
            self.valueRegister()
            return
        elif(token.getLexema() in ('true','false')):
            print(token.getLexema())            
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
                print("ERROR")
                return #ERROR
        else:
            self.previousToken()
            return 

#################  REGISTER  #############################   
    def registerStatement(self):
        print('REGISTER STATMENT')
        token = self.nextToken()
        if(token.getLexema() == 'register'):
            print(token.getLexema())
            token = self.nextToken()
        else:
            self.previousToken()
            print("ESPERADO PALAVRA RESERVADA 'register'")
            token = self.ERROR(('{', ';', '}'))
            if(token.getLexema()=="{"):
                self.registerList()
                #procedure etc;;;;
                
            elif(token.getLexema()==";"):
                print("ESPERADO {")
                self.registerDeclaration()
            elif(token.getLexema()=="}"):
                print("EXISTE UM ERRO NO ESCOPO REGISTER")
                self.registerStatementMultiple()
            
            return 
        
        if(token.getClass() == 'identificador'):
            print(token.getLexema())
            token = self.nextToken()
        else:
            print('ESPERADO IDENTIFICADOR')
            return 
        
        if(token.getLexema() == '{'):
            print(token.getLexema())
            self.registerList()
        else:
            print("ESPERADO '{'")
            return
    
    def registerStatementMultiple(self):
        print("REGISTER STATEMENT MULTIPLE")
        token = self.nextToken()
        if(token == None):
            return 
        if(token.getLexema() == 'register'):
            print(token.getLexema())
            self.previousToken()
            self.registerStatement()
        else:
            self.previousToken()
            return 


    def registerList(self):
        print("REGISTER LIST")
        self.registerDeclaration()
        self.registerList1()
    
    def registerList1(self):
        print("REGISTER LIST1")
        token = self.nextToken()
        if(token.getLexema() == '}'):
            print(token.getLexema())
            self.registerStatementMultiple()
        else:
            self.previousToken()
            self.registerDeclaration()
            self.registerList1()
    
    def registerDeclaration(self):
        print("REGISTER DECLARATION")
        self.constType()
        token = self.nextToken()
        if(token.getClass() == 'identificador'):
            print(token.getLexema())
            self.registerDeclaration1()
            return
        else:
            print('ERROR')
            return #ERROR

    def registerDeclaration1(self):
        print("REGISTER DECLARATION1")
        token = self.nextToken()
        if(token.getLexema() == ';'):
            print(token.getLexema())
            return 
        if(token.getLexema() == ','):
            print(token.getLexema())
            token = self.nextToken()
        else:
            print('ERROR')
            return
        if(token.getClass() == 'identificador'):
            print(token.getLexema())
            self.registerDeclaration1()
        else:
            print('ERROR')
            return #ERROR

#################  PROCEDURE  #############################          
    def procedureStatement(self):
        print('PROCEDURE STATMENT')
        token = self.nextToken()
        if(token == None):
            return
        if(token.getLexema()=='procedure'):
            print(token.getLexema())
            token = self.nextToken()
            if(token.getClass()=='identificador'):
                print(token.getLexema())
                token = self.nextToken()
            else:#ERROR
                print("ESPERADO UM IDENTIFICADOR")

            if(token.getLexema()=='('):
                print(token.getLexema())
                self.parameterProcedure()
                token = self.nextToken()
            else:#ERROR
                print("ESPERADO UM (")

            if(token.getLexema()=='{'):
                print(token.getLexema())
                #self.localStatement()
                self.procedureStatement1()
                return
            else:
                #ERROR
                print("ESPERADO UM {")
        else: 
            return
                         
    def parameterProcedure(self):
        print('PARAMETER PROCEDURE')
        token = self.nextToken()
        if(token.getLexema()==')'):
            print(token.getLexema())
            return
        else:
            self.previousToken()
            self.varType()
            token = self.nextToken()
            if(token.getClass()=='identificador'):
                print(token.getLexema())
                self.parameterListProcedure()
                return
            else:#ERROR
                print("ESPERANDO UM IDENTIFICADOR OU ')'")

    def parameterListProcedure(self):
        print('PARAMETER LIST PROCEDURE')
        token = self.nextToken()
        if(token.getLexema()==')'):
            print(token.getLexema())
            return
        else:
            if(token.getLexema()==','):
                print(token.getLexema())
                self.parameterProcedure()
            else:#ERROR
                print("ERROR")
            
    def localStatement(self):
        print("localStatement")

    def procedureStatement1(self):
        print('PROCEDURE STATMENT 1')
        token = self.nextToken()
        if(token.getLexema()=='}'):
            print(token.getLexema())
            self.procedureStatement()
        else:#ERROR
            print("ERROR")

#################  FUNCTION  #############################          
    def functionStatement(self):
        print('FUNCTION STATMENT')
        token = self.nextToken()
        if(token == None):
            return
        if(token.getLexema()=='function'):
            print(token.getLexema())
            token = self.nextToken()
        else:#ERROR
            print("ESPERADO PALAVRA_RESERVADA function")
        if(token.getClass()=='identificador'):
            print(token.getLexema())
            token = self.nextToken()
        else:#ERROR
            print("ESPERADO UM IDENTIFICADOR")
            
        if(token.getLexema()=='('):
            print(token.getLexema())
            self.parameterFunction()
            token = self.nextToken()
        else:#ERROR
            print("ESPERADO UM (")
        
        if(token.getLexema()=='{'):
            print(token.getLexema())
            token = self.nextToken()
            #self.localStatement()
        else:
            #ERROR
            print("ESPERADO UM {")
        
        if(token.getLexema()=='return'):
            print(token.getLexema())
            self.value()
            token = self.nextToken()
        else:
            #ERROR
            print("ESPERADO PALAVRA RESERVADA return")
        
        if(token.getLexema()==';'):
            print(token.getLexema())
            self.functionStatement1()
        else:
            #ERROR
            print("ESPERADO ';'")

        return
    
    def functionStatement1(self):
        print('FUNCTION STATMENT 1')
        token = self.nextToken()
        if(token.getLexema()=='}'):
            print(token.getLexema())
            self.functionStatement()
        else:#ERROR
            print("ERROR")
                         
    def parameterFunction(self):
        print('PARAMETER FUNCTION')
        token = self.nextToken()
        if(token.getLexema()==')'):
            print(token.getLexema())
            token = self.nextToken()
            if(token.getLexema()==':'):
                print(token.getLexema())
                self.varType()
            else:
                print("ESPERANDO ':'")
        else:
            self.previousToken()
            self.varType()
            token = self.nextToken()
            if(token.getClass()=='identificador'):
                print(token.getLexema())
                self.parameterListFunction()
                return
            else:#ERROR
                print("ESPERANDO UM IDENTIFICADOR OU ')'")

    def parameterListFunction(self):
        print('PARAMETER LIST FUNCTION')
        token = self.nextToken()
        if(token.getLexema()==')'):
            print(token.getLexema())
            token = self.nextToken()
            if(token.getLexema()==':'):
                print(token.getLexema())
                self.varType()
            else:
                print("ESPERANDO ':'")
        else:
            if(token.getLexema()==','):
                print(token.getLexema())
                self.parameterFunction()
            else:#ERROR
                print("ERROR")
            
    def localStatement(self):
        print("localStatement")


  ######################################################################

    # def constStatement():
    # def registerStatement():
    # def procedureStatement():
    # def functionStatement():
    # def main():




    def nextToken(self):
        self.token_position+=1
        if self.token_position == len(self.tokens_list):
            return None
        return self.tokens_list[self.token_position]

    def previousToken(self):
        self.token_position-=1
        return self.tokens_list[self.token_position]