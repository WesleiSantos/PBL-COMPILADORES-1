from pickle import NONE
from token import Token
from erro import Erro
import os

VAR_TYPES = ('integer', 'real', 'string', 'boolean', 'char')
CONST_TYPES = ('integer', 'real', 'string', 'boolean', 'char')
ADDEND_OPERATOR = ('inteiro','ponto_flutuante','booleano')
REL_LOG_Expression = ('<', '>', '!=', '<=', '>=', '==', '||', '&&')

class Analisador_sintatico:
    def __init__(self, listTokens) -> None:
        self.tokens_list = listTokens
        self.token_position = -1
        cwd = os.getcwd()
        self.file_exit = open(cwd+"/output"+'/sintatico.txt', 'w+')
        
        
    def readTokens(self):
        print("\n_________________________\nANALISE SINTÁTICA\n_________________________")            
        self.start()
        self.file_exit.close()
        
    def ERROR(self, tokens_sinc):
        token = self.nextToken()
        while(token.getLexema() not in tokens_sinc):
            print("ERRO", token.getLexema())
            token = self.nextToken()
        return token
        
    def start(self):
        token = self.nextToken() #LER O PRIMEIRO TOKEN
        tokError = token.getPosition()
        if(token == None):
            print("ERROR - ARQUIVO VAZIO")
            self.file_exit.write("ERRO: AQUIVO VAZIO\n")
            return
        elif(token.getLexema() == "program"):
            print(token.getLexema())
            tokError = token.getPosition()
            token = self.nextToken()
        else:
            #print("ESPERADO A PALAVRA RESERVADA 'PROGRAM'")
            #self.file_exit.write("ERRO: ESPERADO A PALAVRA RESERVADA 'program' - linha "+ str(tokError))
            if(token.getClass()=='identificador'):
                tokError = token.getPosition()
                token = self.nextToken()
                if(not(token.getLexema()==';')):
                    self.previousToken()
                    token = self.ERROR((';', 'var', 'const')) ##se encontrar o um dos token de sicrnz.
                    if(token.getLexema() == ';'):
                        self.file_exit.write("ERRO: ESPERADO A PALAVRA RESERVADA 'program' - linha "+ str(tokError)+"\n")
                        self.globalStatement()
                    if(token.getLexema() == 'var'):
                        self.file_exit.write("ERRO: ESPERADO 'program ;' - linha "+ str(tokError)+"\n")
                        self.previousToken()
                        self.globalStatement()
                    if(token.getLexema()== 'const'):
                        print("NAO FOI DECLARADO O 'VAR'")
                        self.file_exit.write("ERRO: ESPERADO 'program ; <varStatement>' - linha "+ str(tokError)+"\n")
                        self.previousToken()
                        self.constStatement()
                        self.registerStatement()  
                else:
                    self.file_exit.write("ERRO: ESPERADO 'program' - linha "+ str(tokError)+"\n")
                return                 
                
            self.previousToken()
            tokError = token.getPosition()
            token = self.ERROR((';', 'var', 'const')) ##se encontrar o um dos token de sicrnz.
            if(token.getLexema() == ';'):
                self.file_exit.write("ERRO: ESPERADO 'program identifier' - linha "+ str(tokError)+"\n")
                self.globalStatement()
            if(token.getLexema() == 'var'):
                self.file_exit.write("ERRO: ESPERADO 'program identifier;' - linha "+ str(tokError)+"\n")
                self.previousToken()
                self.globalStatement()
            if(token.getLexema()== 'const'):
                print("NAO FOI DECLARADO O 'VAR'")
                self.file_exit.write("ERRO: ESPERADO 'program identifier; <varStatement>' - linha "+ str(tokError)+"\n")
                self.previousToken()
                self.constStatement()
                self.registerStatement()
            return
            
        if(token.getClass() == 'identificador'):
            print(token.getLexema())
            token = self.nextToken()
        else:
            print("ESPERADO UM IDENTIFICADOR")
            #self.file_exit.write("ERRO: ESPERADO 'identifier' - linha "+ str(tokError)+"\n")
            self.previousToken()
            token=self.ERROR((';', 'var'))
            if(token.getLexema() == ';'):
                self.file_exit.write("ERRO: ESPERADO 'identifier' - linha "+ str(tokError)+"\n")
                self.globalStatement()
            elif(token.getLexema() == 'var'):
                self.file_exit.write("ERRO: ESPERADO 'identifier;' - linha "+ str(tokError)+"\n")
                self.previousToken()
                self.globalStatement()
            return
        
        if(token.getLexema()==';'):
            print(token.getLexema())
            self.globalStatement()
            return
        else:
            print("ESPERADO UM PONTO E VÍRGULA")
            self.file_exit.write("ERRO: ESPERADO ';' - linha "+ str(tokError)+"\n")
            self.previousToken()
            self.globalStatement()  
            return          
    
    def globalStatement(self):
        print("GLOBAL STATMENT")
        self.varStatement()
        self.constStatement()
        self.registerStatement()
        self.procedureStatement()
        self.functionStatement()
        self.main()

#################  VAR  #############################   
    def varStatement(self):
        print("VAR STATMENT")
        token = self.nextToken()
        tokError = token.getPosition()
        if(token.getLexema() == 'var'):
            print(token.getLexema())
            token = self.nextToken()
        else:
            self.previousToken()
            token = self.ERROR(('{','integer', 'real', 'string', 'boolean', 'char',';'))
            
            if(token.getLexema()=="{"):
                print("ESPERADO PALAVRA RESERVADA 'var' ")
                self.file_exit.write("ERRO: ESPERADO 'var' - linha "+ str(tokError)+"\n")
            elif(token.getLexema()==";"):
                print("ESPERADO ESPERADO 'var { variable_type' ")
                self.file_exit.write("ERRO: ESPERADO 'var { variable_type' - linha "+ str(tokError)+"\n")
            elif(token.getLexema() in VAR_TYPES):
                print("ESPERADO 'var {' ")
                self.file_exit.write("ERRO: ESPERADO 'var {' - linha "+ str(tokError)+"\n")
                self.previousToken()
                
            ##a continuação é a mesma para caso encontrado o { ou ;
            self.varlist()
            return
                      
        if(token.getLexema()=='{'):
            print(token.getLexema())
            self.varlist() 
        else:
            self.previousToken()
            print("ERROR: ESPERADO O DELIMITADOR '{' ")
            
            token = self.ERROR(('integer', 'real', 'string', 'boolean', 'char', 'const'))
            if(token.getLexema() in VAR_TYPES):
                self.file_exit.write("ERRO: ESPERADO '{' - linha "+ str(tokError)+"\n")
                self.previousToken()
                self.varlist()
            elif(token.getLexema() == 'const'):
                print("ESPERADO UMA DECLAÇÃO DE VARIAVEL COM SEU TIPO")
                self.file_exit.write("ERRO: ESTRUTURA DE DECLARAÇÃO DE VARIÁVEL INVALIDA - linha "+ str(tokError)+"\n")
                self.previousToken()
        return   
            

    def varlist(self):
        print("VAR LIST")
        token = self.nextToken()
        tokError = token.getPosition()
        if(token.getLexema() in VAR_TYPES or token.getClass()=='identificador'):
            self.previousToken()
            self.varDeclaration()
            self.varList1()
        elif(token.getLexema() == '}'):
            print(token.getLexema())
            #return    
        else: 
            
            if(token.getClass()=="identificador"):
                print("ESPERADO DECLARAÇÃO DE UM TIPO DE VARIÁVEL")
                self.varDeclaration1()
                self.varList1()
                return
            self.previousToken()
            token = self.ERROR(('integer', 'real', 'string', 'boolean', 'char', ';', ',' ,'const'))
            if(token.getLexema() in VAR_TYPES):
                self.file_exit.write("ERRO: DECLARAÇÃO DE VÁRIÁVEL INVALIDA - linha "+ str(tokError)+"\n")
                self.previousToken()
                self.varlist()
            if(token.getLexema()==";"):
                print("ESPERADO DECLARAÇÃO DE UM TIPO DE VARIÁVEL e 'identificador(es)'")
                self.varlist()
            elif(token.getLexema()==','):
                print("ESPERADO 'type_var identifier")
                self.previousToken()
                self.varDeclaration1()
                self.varList1()
            elif(token.getLexema()=="const"):
                print("ESPERADO }")
                self.previousToken()
            return 

    def varList1(self):
        print("VAR LIST 1")
        token = self.nextToken()
        if(token.getLexema() in VAR_TYPES):
            print(token.getLexema())
            self.previousToken()
            self.varDeclaration()
            self.varList1()
        elif(token.getLexema()=='}'):
            print(token.getLexema())
            return
        else:
            
            if(token.getClass()=="identificador"):
                print("ESPERADO DECLARAÇÃO DE UM TIPO DE VARIÁVEL")
                self.varDeclaration1()
                return
            self.previousToken()
            tokError = token.getPosition()
            token = self.ERROR((';', ',' ,'}','const'))
            if(token.getLexema()==";"):
                print("ESPERADO DECLARAÇÃO DE UM TIPO DE VARIÁVEL e 'identificador(es)'")
                self.varlist()
            elif(token.getLexema()==','):
                print("ESPERADO 'type_var identifier")
                self.previousToken()
                self.varDeclaration1()
            if(token.getLexema()=="}"):
                self.file_exit.write("ERRO: DECLARAÇÃO DE VÁRIÁVEL INVALIDA - linha "+ str(tokError)+"\n")
                return
            elif(token.getLexema()=="const"):
                print("ESPERADO }")
                self.previousToken()
            return 
        
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
            self.previousToken()
            self.varDeclaration1()
            #self.ERROR((',',';'))
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
                print("ERROR")
                print("ESPERADO UM IDENTIFICADOR")
                self.previousToken()
                self.varDeclaration1()
                #self.ERROR((',',';'))
                return
        else:
            if(token.getClass()=='identificador'):
               print(token.getLexema())
               print("ESPERADO UMA VÍRGULA")
               self.varDeclaration1()
            else:
                self.previousToken()
                print("ESPERADO ';'")
            return 
    
    def varType(self):
        print("VAR TYPE")
        token = self.nextToken()
        if(token.getLexema() in VAR_TYPES or token.getClass() == 'identificador'):
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
            self.previousToken()
            token = self.ERROR(('=',';','register'))
            if(token.getLexema()=="register"):
                print("ESPERADO }")
                self.previousToken()
            elif(token.getLexema()==";"):
                print("ESPERADO UM TIPO DE constante E UMA ATRIBUIÇÃO ")
                self.constList1()
            elif(token.getLexema()=="="):
                print("ESPERADO UM TIPO DE CONSTANTE")
                self.value()
                self.constDeclaration1()
                self.constList1()
            return
        
        
    def constList1(self):
        print("CONST LIST 1")
        token = self.nextToken()
        if(token.getLexema() in ('integer', 'real', 'string','real','boolean', 'char')):
            print(token.getLexema())
            self.previousToken()
            self.constDeclaration()
            self.constList1()
        elif(token.getLexema()=='}'):
            print(token.getLexema())
            return
        else: 
            self.previousToken()
            token = self.ERROR(('=',';','register'))
            if(token.getLexema()=="register"):
                print("ESPERADO }")
                self.previousToken()
            elif(token.getLexema()==";"):
                print("ESPERADO UM TIPO DE constante E UMA ATRIBUIÇÃO ")
                self.constList1()
            elif(token.getLexema()=="="):
                print("ESPERADO UM TIPO DE CONSTANTE")
                self.value()
                self.constDeclaration1()
                self.constList1()
            return

    def constDeclaration(self):
        print("CONST DLECARATION")
        self.constType()
        token = self.nextToken()
        if(token.getClass() == 'identificador'):
            print(token.getLexema())
            token = self.nextToken()
        else:
            token = self.ERROR(('=', ';'))
            if(token.getLexema() == '='):
                print("ESPERADO UM TIPO DE CONSTANTE")
                self.value()
                self.ConstDeclaration1()
            elif(token.getLexema() == ';'):
                print("ESPERADO UM TIPO DE constante E UMA ATRIBUIÇÃO ")
                self.constList1()
            return
        
        if(token.getLexema()=='='):
            print(token.getLexema())
            self.value()
            self.constDeclaration1()
            return
        else: 
            token = self.ERROR((';'))
            
            if(token.getLexema() == ';'):
                print("ESPERADO UM TIPO DE constante E UMA ATRIBUIÇÃO ")
                self.constList1()
            
            return
    
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
                token = self.nextToken()    
                if(token.getLexema()=='='):
                    print(token.getLexema())
                    self.value()
                    self.constDeclaration1()
                return
            else: 
                self.previousToken()
                token = self.ERROR(('=', ',', ';'))
                if(token.getLexema() == '='):
                    print("ESPERADO UM IDENTIFICADOR ")
                    self.value()
                    self.ConstDeclaration1()
                elif(token.getLexema() == ','):
                    print("ESPERADO UM IDENTIFICADOR E UMA ATRIBUIÇÃO ")
                    self.previousToken()
                    self.constDeclaration1()
                elif(token.getLexema() == ';'):
                    print("ESPERADO UM IDENTIFICADOR E UMA ATRIBUIÇÃO ")
                return 
        else:
            print("ERRO")
            self.previousToken()
            token = self.nextToken()
            if(token.getClass()=='identificador'):
               print("ESPERADO UMA VÍRGULA")
            ##teria que haver uma forma de mostrar o erro "esperado ;"
            self.previousToken()
            token = self.ERROR((';'))
            if(token.getLexema() == ';'):
                print("ESPERADO UMA ',' ou ';' ")
            return #ERROR
    
    def constType(self):
        print("CONST TYPE")
        token = self.nextToken()
        if(token.getLexema() in CONST_TYPES):
            print(token.getLexema())
            return
        else:
            print("ESPERADO UM TIPO DE CONSTANTE")
            return
    
    def value(self):
        token = self.nextToken()
        if(token.getClass() in ('inteiro','ponto_flutuante','cadeia de caracteres','caracter')):
            print(token.getLexema())
        elif(token.getClass() == 'identificador'):
            print(token.getLexema())            
            self.valueRegister()
        elif(token.getLexema() in ('true','false')):
            print(token.getLexema())
        else:
            print("ESPERADO UM VALOR PARA A ATRIBUIÇÃO")
        return

    def valueRegister(self):
        token = self.nextToken()
        if(token.getLexema() == '.'):
            print(token.getLexema())
            token = self.nextToken()
            if(token.getClass() in 'identificador'):
                print(token.getLexema())
                return
            else:
                print("ESPERADO UM IDENTIFICADOR DO REGISTER")
                return
        else:##vazio
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
            token = self.ERROR(('{', ';', '}'))
            if(token.getLexema()=="{"):
                print("ESPERADO PALAVRA RESERVADA 'register'")
                self.registerList()
            elif(token.getLexema()==";"):
                print("ESPERADO {")
                self.registerDeclaration1()
            elif(token.getLexema()=="}"):
                print("EXISTE UM ERRO NO ESCOPO REGISTER")
                self.registerStatementMultiple()
            
            return 
        
        if(token.getClass() == 'identificador'):
            print(token.getLexema())
            token = self.nextToken()
        else:
            self.previousToken()
            token = self.ERROR(('{', ';', '}'))
            if(token.getLexema()=="{"):
                print("ESPERADO UM IDENTIFICADOR")
                self.registerList()
            elif(token.getLexema()==";"):
                print("ESPERADO 'identifier {'")
                self.registerList()
            elif(token.getLexema()=="}"):
                print("EXISTE UM ERRO NO ESCOPO REGISTER (ESPERADO identifier { e ;)")
                self.registerStatementMultiple()
            return 
        
        if(token.getLexema() == '{'):
            print(token.getLexema())
            self.registerList()
        else:
            self.previousToken()
            token = self.ERROR((';', '}'))
            if(token.getLexema()==";"):
                print("ESPERADO '{'")
                self.registerList()
            elif(token.getLexema()=="}"):
                print("EXISTE UM ERRO NO ESCOPO REGISTER (ESPERADO { e ;)")
                self.registerStatementMultiple()
            return
    
    def registerStatementMultiple(self):
        print("REGISTER STATEMENT MULTIPLE")
        token = self.nextToken()
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
            self.previousToken()
            token = self.ERROR((',',';'))
            if(token.getLexema()==','):
                print("ESPERADO UM IDENTIFICADOR")
                self.previousToken()
                self.registerDeclaration1()
            elif(token.getLexema()==';'):
                print("ESPERADO UM IDENTIFICADOR")
            return 

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
            if(token.getClass()=='identificador'):
                print("ESPERADO ',' ")
                print(token.getLexema())
                self.registerDeclaration1()
            else:
                self.previousToken()
                print("ESPERADO ';' ")
            return
        if(token.getClass() == 'identificador'):
            print(token.getLexema())
            self.registerDeclaration1()
        else:
            print('ESPERADO UM IDENTIFICADOR')
            return

#################  PROCEDURE  #############################          
    def procedureStatement(self): ##>>>>>>>>>>>>>>>>> FALTA TESTAR OS ERROS
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
            else: ##ok segue para '('
                print("ESPERADO UM IDENTIFICADOR")
                
            if(token.getLexema()=='('):
                print(token.getLexema())
                self.parameterProcedure()
                token = self.nextToken()
            else:
                print("ESPERADO UM (")
                self.previousToken()
                self.parameterProcedure()
                token = self.nextToken()
                ##segue para o '{'

            if(token.getLexema()=='{'):
                print(token.getLexema())
                self.localStatement()
                self.procedureStatement1()
                return
            else:
                self.previousToken()
                print("ESPERADO UM {")
                self.localStatement()
                self.procedureStatement1()
                return   
        else: ##vazio
            self.previousToken()
            return
        
    def parameterProcedure(self):
        print('PARAMETER PROCEDURE')
        token = self.nextToken()
        if(token.getLexema()==')'):
            print(token.getLexema())
            return
        elif(token.getLexema() in VAR_TYPES): ##verificar entre os primeros de <VarType>
            print(token.getLexema())
            token = self.nextToken()
            if(token.getClass()=='identificador'):
                print(token.getLexema())
                self.parameterListProcedure()
            else:
                print("ESPERADO UM IDENTIFICADOR")
                self.parameterListProcedure()
            return
        else:
            if(token.getClass()=='identificador'):
                 print("ESPERADO UM TIPO DE VARIÁVEL NO PARAMETER PROCEDURE")
                 self.parameterListProcedure()
            else:
                print("ESPERANDO UM ')'")
                self.previousToken()
            return
            
    '''                    
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
            else:
                print("ESPERANDO UM IDENTIFICADOR OU ')'")
                '''

    def parameterListProcedure(self):
        print('PARAMETER LIST PROCEDURE')
        token = self.nextToken()
        if(token.getLexema()==')'):
            print(token.getLexema())
            return
        elif(token.getLexema()==','):
            print(token.getLexema())
            self.parameterProcedure()
        else:
            if(token.getLexema() in VAR_TYPES):
                print("ESPERADO UMA ',' ")
                self.previousToken()
                self.parameterProcedure()
            elif(token.getClass()=='identificador'):
                print("ESPERADO UMA ',' E UM TIPO DE VARIAVEL EM PARAMETER PROCEDURE")
                self.parameterListProcedure()
            else:
                self.previousToken()
                print("ESPERADO ')' EM PROCEDURE")   
                
    def procedureStatement1(self):
        print('PROCEDURE STATMENT 1')
        token = self.nextToken()
        if(token.getLexema()=='}'):
            print(token.getLexema())
            self.procedureStatement()
        else:
            print("ESPERADO '}'")

#################  FUNCTION  #############################          
    def functionStatement(self):
        print('FUNCTION STATMENT')
        token = self.nextToken()
        if(token == None):
            return
        if(token.getLexema()=='function'):
            print(token.getLexema())
            token = self.nextToken()
                    
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
                self.previousToken()
                print("ESPERADO UM '('")
                self.parameterFunction()
                token = self.nextToken()
            
            if(token.getLexema()=='{'):
                print(token.getLexema())
                self.localStatement()
                token = self.nextToken()
            else:#ERROR
                print("ESPERADO UM '{'")
                self.localStatement()
            
            tokError= token.getPosition()
            if(token.getLexema()=='return'):
                print(token.getLexema())
                self.value()
                token = self.nextToken()
            else:
                #ERROR
                print("ESPERADO PALAVRA RESERVADA 'return' - linha ", tokError)
                self.value()
            
            if(token.getLexema()==';'):
                print(token.getLexema())
                self.functionStatement1()
            else:
                #ERROR
                print("ESPERADO ';' - linha ", tokError)
                self.previousToken()
                self.functionStatement1()
        else:#vazio
            self.previousToken()
        return
    
    def functionStatement1(self):
        print('FUNCTION STATMENT 1')
        token = self.nextToken()
        if(token.getLexema()=='}'):
            print(token.getLexema())
            self.functionStatement()
        else:#ERROR
            print("ESPERADO UM '}'")
            
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
                self.varType()
            return
        elif(token.getLexema() in VAR_TYPES):##verificar entre os primeros de <VarType>
            print(token.getLexema())
            token = self.nextToken()
            if(token.getClass()=='identificador'):
                print(token.getLexema())
                self.parameterListFunction()
            else:#ERROR
                print("ESPERANDO UM IDENTIFICADOR")
                self.previousToken()
                self.parameterListFunction()
            return
        else:
            if(token.getClass()=='identificador'):
                print("ESPERADO UM TIPO DE VARIÁVEL NO PARAMETER PROCEDURE")
                self.parameterListFunction()
            elif(token.getLexema()==':'):
                print("ESPERADO ')' EM FUNCTION")
                self.varType()
            elif(token.getLexema()=='{'):
                print("ESPERANDO UM '): type_var_return")
                self.previousToken()
            return
    
    def parameterListFunction(self):
        print('PARAMETER LIST FUNCTION')
        token = self.nextToken()
        if(token.getLexema()==')'):
            print(token.getLexema())
            token = self.nextToken()
            if(token.getLexema()==':'):
                print(token.getLexema())
                tokError = token.getPosition()
                token = self.nextToken()
                if(token.getLexema() in VAR_TYPES):
                    print(token.getLexema())
                    return
                else:
                    print("ESPERADO UM TIPO DE VÁRIÁVEL DE RETORNO - linha ", tokError)
                    self.previousToken()
            else:
                print("ESPERANDO ':'")
        elif(token.getLexema()==','):
            print(token.getLexema())
            self.parameterFunction()
        else:
            if(token.getLexema() in VAR_TYPES):
                print("ESPERADO UMA ',' ")
                self.previousToken()
                self.parameterFuction()
            elif(token.getClass()=='identificador'):
                print("ESPERADO UMA ',' E UM TIPO DE VARIAVEL EM PARAMETER PROCEDURE")
                self.parameterListFuction()
            elif(token.getLexema()==':'):
                print("ESPERADO ')' EM FUNCTION")
                self.varType()
            elif(token.getLexema()=='{'):
                print("ESPERANDO UM '): type_var_return")
                self.previousToken()
            return

  ########################## MAIN e LOCAL STATEMENTS #########################################
    def main(self):
        token = self.nextToken()
        tokError = token.getPosition()
        if(token.getLexema()=='main'):
            print(token.getLexema())
            tokError = token.getPosition()
            token = self.nextToken()
            if(token.getLexema()=='{'):
                print(token.getLexema())
                self.localStatement()
                tokError = token.getPosition()
                token = self.nextToken()
                if(token == None):
                    print("ESPERADO '}' (FIM DE ARQUIVO NAO ESPERADO) - linha ", tokError)
                    return
                
                if(token.getLexema()=='}'):
                    print(token.getLexema())
                else:
                    print("ESPERADO '}' - linha ", tokError)
                    token = self.ERROR(('}'))
                    tokError = token.getPosition()
                    if(token == None):
                        print("ESPERADO '}' (FIM DE ARQUIVO NAO ESPERADO) - linha ", tokError)
                        return
                    if(token.getLexema()=='{'):
                        print(token.getLexema())
                        print("EXISTE ERROS ANTES DO '}' - linha ", tokError)
            
            else:
                print("ESPERADO '{' - linha", tokError)   
                self.previousToken()
                self.localCommands()
                token = self.nextToken()
                tokError = token.getPosition()
                if(token.getLexema()=='}'):
                    print(token.getLexema())
                else:
                    print("ESPERADO '}' - linha ", tokError)
                    token = self.ERROR(('}'))
                    tokError = token.getPosition()
                    if(token == None):
                        print("ESPERADO '}' (FIM DE ARQUIVO NAO ESPERADO) - linha ", tokError)
                        return
                    if(token.getLexema()=='{'):
                        print(token.getLexema())
                        print("EXISTE ERROS ANTES DO '}' - linha ", tokError)
        else: ##ERRROR
            print("ESPERADO A 'main' - linha ", tokError)
            self.previousToken()
            token = self.ERROR(('{','}'))
            
            if(token.getLexema()=='{'):
                print(token.getLexema())
                self.localStatement()
                tokError = token.getPosition()
                token = self.nextToken()
                if(token == None):
                    print("ESPERADO '}' (FIM DE ARQUIVO NAO ESPERADO) - linha ", tokError)
                    return
                
                if(token.getLexema()=='}'):
                    print(token.getLexema())
                else:
                    print("ESPERADO '}' - linha ", tokError)
                    token = self.ERROR(('}'))
                    tokError = token.getPosition()
                    if(token == None):
                        print("ESPERADO '}' (FIM DE ARQUIVO NAO ESPERADO) - linha ", tokError)
                        return
                    if(token.getLexema()=='{'):
                        print(token.getLexema())
                        print("EXISTE ERROS ANTES DO '}' - linha ", tokError)
            
            if(token.getLexema()=='}'):
                print(token.getLexema())
            else:
                print("ESPERADO '}' - linha ", tokError)
                token = self.ERROR(('}'))
                tokError = token.getPosition()
                if(token == None):
                    print("ESPERADO '}' (FIM DE ARQUIVO NAO ESPERADO) - linha ", tokError)
                    return
                if(token.getLexema()=='{'):
                    print(token.getLexema())
                    print("EXISTE ERROS ANTES DO '}' - linha ", tokError)
                        
                    
    def localStatement(self):
        print("LOCAL STATEMENT")
        token = self.nextToken()
        if(token.getLexema()=='var'):
            print(token.getLexema())
            self.previousToken()    
            self.varStatement()
        else:    
            self.previousToken()    
        self.localCommands()
        return
        
    def localCommands(self):
        print('LOCAL COMMANDS')
        token = self.nextToken()
        print(token.getLexema())
        if(token.getLexema()=='if'):
            self.previousToken()
            self.ifDecs()
            self.localCommands()
        elif(token.getLexema()=='write'):
            self.previousToken()
            self.writeDecs()
            self.localCommands()
        elif(token.getLexema()=='read'):
            self.previousToken()
            self.readDecs()
            self.localCommands()
        elif(token.getLexema()=='while'):
            self.previousToken()
            self.whileDecs()
            self.localCommands()
        elif(token.getClass()=='identificador'):
            print(token.getLexema())
            self.call()
            self.localCommands()
        else:#vazio
            self.previousToken()
        return

######################### READ / WRITE #######################
    def writeDecs(self):
        token = self.nextToken()
        if(token.getLexema()=='write'):
            print(token.getLexema())
            token = self.nextToken()
            if(token == None):
                print("2 ERROS - ESPERADO '(<parameter>);' e FIM DE ARQUIVO NAO ESPERADO")
                return
            if(token.getLexema()=='('):
                print(token.getLexema())
                self.argumentsWrite()
            else:
                print("ESPERADO '('")
                self.previousToken()
                self.argumentsWrite()
        else:
            if(token.getLexema()=='('):
                print("ESPERADO UMA PALAVRA RESERVADA 'write'")
            else:
                print("ESPERADO 'read ('")
            self.previousToken()
            self.argumentsWrite()
            
    def argumentsWrite(self):
        token = self.nextToken()
        if(token == None):
            print("2 ERROS - ESPERADO <parameter>); e FIM DE ARQUIVO NAO ESPERADO")
            return
        if(token.getClass()=='identificador'):
            print(token.getLexema())
            self.registerReadWrite()
            self.listArgumentsWrite()
        elif(self.writeContent(token)):
            print(token.getLexema())
            self.listArgumentsWrite()
        else:
            self.previousToken()
            token = self.ERROR(('.', ',', ')', ';'))
            if(token.getLexema()=='.'):
                self.previousToken()
                self.registerReadWrite()
                self.listArgumentsWrite()
            elif(token.getLexema()==','):
                print(token.getLexema())
                print("ESPERADO UM IDENTIFICADOR, DIGITO, PONTO FLUTUANTE OU STRING")
                self.argumentsWrite()
            elif(token.getLexema()==')'):
                print(token.getLexema())
                print("ESPERADO UM PARAMETRO EM WRITE")
                token = self.nextToken()
                if(token.getLexema()==';'):
                    print(token.getLexema())
                else:
                    print("ESPERADO UM ';'")
                    self.previousToken()
                    return
            elif(token.getLexema()==';'):
                print("ESPERADO '<parameter>)'")
            else:
                self.previousToken()
                return
            
    def writeContent(self, token):
        if(token.getClass() in ('inteiro','ponto_flutuante','cadeira de caracteres')):
            return True
    
    def readDecs(self):
        token = self.nextToken()
        if(token.getLexema()=='read'):
            print(token.getLexema())
            token = self.nextToken()
            if(token == None):
                return
            if(token.getLexema()=='('):
                print(token.getLexema())
                self.argumentsRead()
            else:
                ("ESPERADO '('")
                self.previousToken()
                self.argumentsRead()
        else:
            if(token.getLexema()=='('):
                print("ESPERADO UMA PALAVRA RESERVADA 'read'")
            else:
                print("ESPERADO 'read ('")
            self.previousToken()
            self.argumentsRead()
    
    def argumentsRead(self):
        token = self.nextToken()
        if(token == None):
            return
        if(token.getClass()=='identificador'):
            print(token.getLexema())
            self.registerReadWrite()
            self.listArgumentsRead()
        else:
            print("ESPERADO UM IDENTIFICADOR")   
            self.previousToken()
            self.registerReadWrite()
            token = self.ERROR((',',')',';'))
            if(token.getLexema()==','):
                print(token.getLexema())
                self.previousToken()
                self.listArgumentsRead()
            elif(token.getLexema()==')'):
                print(token.getLexema())
                token = self.nextToken()
                if(token.getLexema()==';'):
                    print(token.getLexema())
                else:
                    self.previousToken()
                    print("ESPERADO UM ';'")
            elif(token.getLexema()==';'):
                    print(token.getLexema())
            else:
                self.previousToken()
                print("ESPERADO UM ');'")
            
    
    def registerReadWrite(self):
        token = self.nextToken()
        if(token == None):
            self.previousToken()
            return
        if(token.getLexema()=='.'):
            print(token.getLexema())
            token = self.nextToken()
            if(token.getClass()=='identificador'):
                print(token.getLexema())
            else:
                self.previousToken()
                print("ESPERADO UM IDENTIFICADOR APOS '.'")
        else:
            self.previousToken()

    def listArgumentsRead(self):
        token = self.nextToken()
        if(token == None):
            print("ESPERADO ',' OU ';' - ERRO FIM DE ARQUIVO NAO ESPERADO")
            return
        if(token.getLexema()==','):
            print(token.getLexema())
            self.argumentsRead()
        elif(token.getLexema()==')'):
            print(token.getLexema())
            token = self.nextToken()
            if(token == None):
                print("2 ERROS: ESPERADO ; E FIM DE ARQUIVO NAO ESPERADO")
                return
            if(token.getLexema()==';'):
                print(token.getLexema())
            else:
                self.previousToken()
                print("ESPERADO UM ';'")
        else:
            if(token.getClass()=='identificador'):
                print("ESPERADO UMA ','")
                self.previousToken()
                self.argumentsRead()
                return
            if(token.getLexema()==';'):
                print("ESPERADO UM ')'")
            else:
                print("ESPERADO ');' NO FIM DE READ")
                self.previousToken()      

    def listArgumentsWrite(self):
        token = self.nextToken()
        if(token == None):
            print("ERRO - FIM DE ARQUIVO NAO ESPERADO")
            return
        if(token.getLexema()==','):
            print(token.getLexema())
            self.argumentsWrite()
        elif(token.getLexema()==')'):
            
            print(token.getLexema())
            token = self.nextToken()
            if(token == None):
                print("ESPERADO ';'")
                return
            if(token.getLexema()==';'):
                print(token.getLexema())
            else:
                self.previousToken()
                print("ESPERADO UM ';'")
        else:
            if(token.getClass()=='identificador'):
                print("ESPERADO UM ','")
                self.previousToken()
                self.argumentsWrite()
                return
            elif(self.writeContent(token)):
                print("ESPERADO UMA ','")
                self.previousToken()
                self.argumentsWrite()
                return
                
            if(token.getLexema()==';'):
                print("ESPERADO UM ')'")
            else:
                print("ESPERADO ');' NO FIM DE WRITE")
                self.previousToken()      

######################### if, else, while, assignExpr ############################
    def ifDecs(self):
        token = self.nextToken()
        if(token.getLexema()=='if'):
            print(token.getLexema())
            token = self.nextToken()
            
            if(token == None):
                print("ESPERADO '(){}' APOS O 'if' - FIM DE ARQUIVO NAO ESPERADO")
                return
            
            if(token.getLexema()=='('):
                print(token.getLexema())
                self.assignExpr()
                token = self.nextToken()
            else:#ERROR
                print("ESPERADO '('")
                self.previousToken()
                self.assignExpr()
                token = self.nextToken()
                
            if(token == None):
                print("ESPERADO '){}' APOS O 'if(<assignExpr>' - FIM DE ARQUIVO NAO ESPERADO")
                return
                
            if(token.getLexema()==')'):
                print(token.getLexema())
                token = self.nextToken()
            else:#ERRO
                print("ESPERADO ')'")
                token = self.nextToken()
                
            if(token == None):
                print("ESPERADO '{}' APOS O 'if(<assignExpr>)' - FIM DE ARQUIVO NAO ESPERADO")
                return
                
            if(token.getLexema()=='{'):
                print(token.getLexema())
                self.localCommands()
                token = self.nextToken()
            else:#ERROR
                print("ESPERADO '{'")
                self.previousToken()
                self.localCommands()
                token = self.nextToken()
                
            if(token == None):
                print("ESPERADO '}' APOS O 'if(assignExpr>){' - FIM DE ARQUIVO NAO ESPERADO")
                return
                
            if(token.getLexema()=='}'):
                print(token.getLexema())
                self.elseDecs()
            else:
                print("ESPERADO '}'")
                self.previousToken()
                self.elseDecs()
            
    def elseDecs(self):
        token = self.nextToken()
        if(token == None):
            return
        if(token.getLexema()=='else'):
            print(token.getLexema())
            token = self.nextToken()
            
            if(token == None):
                print("ESPERADO '{}' APOS O 'else' - FIM DE ARQUIVO NAO ESPERADO")
                return
            
            if(token.getLexema()=='{'):
                print(token.getLexema())
                self.localCommands()
                token = self.nextToken()
            else:#ERROR
                print("ESPERADO '{'")
                self.previousToken()
                self.localCommands()
                token = self.nextToken()
                
            if(token == None):
                print("ESPERADO '}' APOS O 'else{<localComands>' - FIM DE ARQUIVO NAO ESPERADO")
                return
                
            if(token.getLexema()=='}'):
                print(token.getLexema())
                self.elseDecs()
            else:
                print("ESPERADO '}'")
                self.previousToken()
                self.elseDecs()
        else: ##vazio
            self.previousToken()
            
    def whileDecs(self):
        token = self.nextToken()
        if(token.getLexema()=='while'):
            print(token.getLexema())
            token = self.nextToken()
            
            if(token == None):
                print("ESPERADO '(){}' APOS O 'while' - FIM DE ARQUIVO NAO ESPERADO")
                return
            
            if(token.getLexema()=='('):
                print(token.getLexema())
                self.assignExpr()
                token = self.nextToken()
            else:#ERROR
                print("ESPERADO '('")
                self.previousToken()
                self.assignExpr()
                token = self.nextToken()
                
            if(token == None):
                print("ESPERADO '){}' APOS O 'while(assignExpr>' - FIM DE ARQUIVO NAO ESPERADO")
                return
                
            if(token.getLexema()==')'):
                print(token.getLexema())
                token = self.nextToken()
            else:#ERRO
                print("ESPERADO ')'")
                token = self.nextToken()
                
            if(token == None):
                print("ESPERADO '{}' APOS O 'while(assignExpr>)' - FIM DE ARQUIVO NAO ESPERADO")
                return
                
            if(token.getLexema()=='{'):
                print(token.getLexema())
                self.localCommands()
                token = self.nextToken()
            else:#ERROR
                print("ESPERADO '{'")
                self.previousToken()
                self.localCommands()
                token = self.nextToken()
                
            if(token == None):
                print("ESPERADO '}' APOS O 'while(assignExpr>){' - FIM DE ARQUIVO NAO ESPERADO")
                return
                
            if(token.getLexema()=='}'):
                print(token.getLexema())
            else:
                print("ESPERADO '}'")
                self.previousToken()
                
    #<AssignExpr> ::= <LogicalOrExpression> |    
    def assignExpr(self):
        print("ASSIGN EXPR")
        token = self.nextToken()
        
        if(token == None):
            print("ESPERADO UM TERMINAL - FIM DE ARQUIVO NAO ESPERADO")
            self.previousToken()
            return
        
        if(token.getClass() in ADDEND_OPERATOR or token.getClass()=="identificador"):
            self.previousToken()
            self.logicalOrExpression()
            # self.conditionContin()
            # self.logicalAndExpression1()
            # self.logicalOrExpression1()
        else: ##vazio
            self.previousToken()
            
    #<LogicalOrExpression> ::= <LogicalAndExpression> <LogicalOrExpression1>               
    def logicalOrExpression(self):
        self.logicalAndExpression()
        self.logicalOrExpression1()
    
    #<LogicalAndExpression> ::= <Condition> <LogicalAndExpression1>            
    def logicalAndExpression(self):
        self.condition()
        self.logicalAndExpression1()
    
    #<LogicalOrExpression1> ::= '||' <LogicalAndExpression> <LogicalOrExpression1> | 
    def logicalOrExpression1(self):
        token = self.nextToken()
        if(token == None): 
            self.previousToken()
            return
        if(token.getLexema()=='||'):
            print(token.getLexema())
            self.logicalAndExpression()
            self.logicalOrExpression1()
        else:##vazio
            self.previousToken()
                        
    #<LogicalAndExpression1> ::= '&&' <Condition> <LogicalAndExpression1> |        
    def logicalAndExpression1(self):
        token = self.nextToken()
        if(token == None): 
            self.previousToken()
            return
        if(token.getLexema()=='&&'):
            print(token.getLexema())
            self.condition()
            self.logicalAndExpression1()
        else:##vazio
            self.previousToken()
            
    #<Condition> ::= <AddendIdent> <ConditionContin>                    
    def condition(self):
        self.addentIdent()
        self.conditionContin()
    
    #<ConditionContin> ::= <RelationalExpression> | <LogicalExpression>    
    def conditionContin(self):
        # <RelationalExpression> | <LogicalExpression>
        token = self.nextToken()
        
        if(token == None): 
            print("ESPERADO UM OPERADOR RELACIONAL OU LÓGICO - FIM DE ARQUIVO NAO ESPERADO")
            self.previousToken()
            return
        
        if(token.getLexema() in REL_LOG_Expression):
            print(token.getLexema())
            self.addentIdent()
        else: ##ERROR
            self.previousToken()
            print("ESPERADO UM OPERADOR RELACIONAL OU LOGICO")
            self.addentIdent()
            
    #<AddendIdent>::= <AddendOperator> | Identifier        
    def addentIdent(self):
        print("ADDENT_IDENT")
        token = self.nextToken()
        tokError = token.getPosition()
        if(token.getClass() in ADDEND_OPERATOR or token.getClass()=="identificador" or token.getLexema() in ('false', 'true')):
            print(token.getLexema())
        else:#ERROR
            self.previousToken()
            print("ESPERADO UM TERMINAL - linha ", tokError)
            
            
################ CHAMADAS DE FUNÇÕES ###############
    #<Call> ::= <ProcedureCall> | '=' <FAcall> | '.' Identifier '=' <FAcall> | '++' ';' | '--' ';'
    def call(self):
        token = self.nextToken()
        tokError = token.getPosition()
        
        if(token == None):
            print("ESPERADO UM ATRIBUIÇÃO OU CHAMADA DE PROCEDURA APÓS O IDENTIFICAR - FIM DE ARQUIVO NAO ESPERADO")
            self.previousToken()
            return
        
        if(token.getLexema()=="("): #Primeiro de procedureCall
            print("PROCEDURE CALL")
            print(token.getLexema())
            self.procedureCall()
        elif(token.getLexema() == "="):
            print(token.getLexema())
            self.faCall()
        elif(token.getLexema() == "."):
            print(token.getLexema())
            token = self.nextToken()
            
            if(token.getClass()=="identificador"):
                print(token.getLexema())
                token = self.nextToken()  
            else:
                print("ESPERADO UM IDENTIFICADOR")
            
            if(token.getLexema() == "="):
                print(token.getLexema())
                self.faCall()
            else:
                self.previousToken()
                print("ESPERADO UM '='")
                
        elif(token.getLexema() in ('++', '--')):
            print(token.getLexema())
            tokError = token.getPosition()
            token = self.nextToken()
            if(token.getLexema()==';'):
                print(token.getLexema())
            else:
                self.previousToken()
                print("ESPERADO UM ';' - linha", tokError)
        else: ###ERRO
            if(token.getClass()=='identificador'):
                t = token
                token = self.nextToken()
                tokError2 = token.getPosition()
                if(token.getLexema()=='='):
                    print("ESPERADO UM '.' APOS O IDENTIFICADOR - linha", tokError)
                    print(t.getLexema())
                    print(token.getLexema())
                    self.faCall()
                    return
                else:
                    print("ESPERADO UM '.' - linha", tokError)
                    print(t.getLexema())
                    print("ESPERADO UM '=' - linha", tokError2)
                    self.previousToken()
                    self.faCall()
                return  
                
            self.previousToken()
            token = self.ERROR((',',')',';'))
            
            if(token.getLexema()==','):
                print("ESPERADO UM '('")
                self.previousToken()
                self.argumentList()
                token = self.nextToken()
                if(token.getLexema()==')'):
                    print(token.getLexema())
                    self.previousToken()
                else:
                    print("ESPERADO UM ')'")
                
                if(token.getLexema()==';'):
                    print(token.getLexema())
                else:
                    self.previousToken()
                    print("ESPERADO UM ';'")
                return
            
            if(token.getLexema()==')'):
                print("ESPERADO 'identifier ('")  
                print(token.getLexema())
                token = self.nextToken()
                if(token.getLexema()== ';'):
                    print(token.getLexema())
                else:
                    self.previousToken()
                    print("ESPERADO UM ';'")
                return
                
            if(token.getLexema()==';'):
                print(token.getLexema()) 
                print("ESPERADO UM CHAMADA DE PROCEDURE OU '.' OU '=' OU '++' OU '--'")    
                return

            
    #<FAcall>::= Identifier <FAcall1> | <ValueBinary> | <UnaryExpression>        
    def faCall(self):
        print("FA_CALL")
        token = self.nextToken()
        tokError = token.getPosition()
        if(token.getClass()=='identificador'):
            print(token.getLexema())
            self.faCall1()
        elif(token.getClass() in ('cadeira de caracteres','caracter','inteiro','ponto_flutuante') or token.getLexema() in ('false', 'true')): ##primeiros de value Binary|
            self.previousToken()
            self.valueBinary()
        elif(token.getLexema()=='!'):
            self.previousToken()
            self.unaryExpression()
        else:
            self.previousToken()
            token = self.ERROR(('(',')', ',' , '+', '-', '*',
                                '/','++', '--', ';','<', '>', 
                                '!=', '<=', '>=', '==', '||', 
                                '&&','.',';'))
            
            if(token.getLexema()==';'):
                print(token.getLexema()) 
                print("ESPERADO UM IDENTIFICADOR OU OPERADOR - linha ", tokError)    
                return
            
            if(token.getLexema()=='('):
                print("ESPERADO UM IDENTIFICADOR")
                self.previousToken()
                self.functionCall()
                return
                
            if(token.getLexema()==')'):
                print("ESPERADO 'identifier ('")  
                print(token.getLexema())
                token = self.nextToken()
                if(token.getLexema()== ';'):
                    print(token.getLexema())
                else:
                    self.previousToken()
                    print("ESPERADO UM ';'")
                return
                
            if(token.getLexema()==','):
                print("ESPERADO UM 'identifier ('")
                self.previousToken()
                self.argumentList()
                token = self.nextToken()
                if(token.getLexema()==')'):
                    print(token.getLexema())
                    self.previousToken()
                else:
                    print("ESPERADO UM ')'")
                
                if(token.getLexema()==';'):
                    print(token.getLexema())
                else:
                    self.previousToken()
                    print("ESPERADO UM ';'")
                return 
            
            if(token.getLexema() in ('+', '-', '*',
                                '/','++', '--', ';','<', '>', 
                                '!=', '<=', '>=', '==', '||', 
                                '&&','.')):
                self.previousToken()
                self.faCall1()
                return
    
    # <FAcall1> ::= <FunctionCall> | <BinaryExpressionContin> | '.' Identifier ';'           
    def faCall1(self):
        print("FA_CALL1")
        token = self.nextToken()
        tokError = token.getPosition()
        if(token.getLexema()=='('):
            self.previousToken()
            self.functionCall()
        elif(token.getLexema() in ('+', '-', '*',
                                '/','++', '--', ';','<', '>', 
                                '!=', '<=', '>=', '==', '||', 
                                '&&',';')):
            self.previousToken()
            self.binaryExpressionContin()
        elif(token.getLexema()=='.'):
            print(token.getLexema())
            token = self.nextToken()
            if(token.getClass()=='identificador'):
                print(token.getLexema())
                token = self.nextToken()
            else:
                print("ESPERADO UM IDENTIFICADOR")
                
            if(token.getLexema()==';'):
                print(token.getLexema())
            else:
                self.previousToken()
                print("ESPERADO UM ';'")
        else:
            
            if(token.getClass()=='identificador'):
                print("ESPERADO UM OPERADOR - linha ", tokError)
                print(token.getLexema())
                token = self.nextToken()
                tokError = token.getPosition()
                if(token.getLexema()==';'):
                    print(token.getLexema())
                else:
                    print("ESPERADO UM ';'- linha ", tokError)
                return
            
            self.previousToken()
            token = self.ERROR((',',')',';'))
            
            if(token.getLexema()==','):
                print("ESPERADO UM 'identifier ('")
                self.previousToken()
                self.argumentList()
                token = self.nextToken()
                if(token.getLexema()==')'):
                    print(token.getLexema())
                    self.previousToken()
                else:
                    print("ESPERADO UM ')'")
                
                if(token.getLexema()==';'):
                    print(token.getLexema())
                else:
                    self.previousToken()
                    print("ESPERADO UM ';'")
                return 
                
            if(token.getLexema()==')'):
                print("ESPERADO 'identifier ('")  
                print(token.getLexema())
                token = self.nextToken()
                if(token.getLexema()== ';'):
                    print(token.getLexema())
                else:
                    self.previousToken()
                    print("ESPERADO UM ';'")
                return
                    
            if(token.getLexema()==';'):
                print(token.getLexema())
                print("ESPERADO UM '.' OU OPERADOR OU COMPLEMENTO DE UMA CHAMADA DE FUNÇÃO ")    
                return

    #<ValueBinary>::= StringLiteral ';' | Char ';' | <AddendOperator> <BinaryExpressionContin>       
    def valueBinary(self):
        token = self.nextToken()
        if(token.getClass() in  ('cadeira de caracteres','caracter')):
            print(token.getLexema())
            token = self.nextToken()
            if(token.getLexema()==';'):
                print(token.getLexema())
            else:
                self.previousToken()
                print("ESPERADO UM ';'")       
        elif(token.getClass() in ('inteiro','ponto_flutuante') or token.getLexema() in ('false', 'true')):
            self.binaryExpressionContin()
        else:
            self.previousToken()
            print("ESPERADO UM VALOR APÓS '='")

    #<UnaryExpression> ::= '!' <AddendOperatorUnary> ';'
    def unaryExpression(self):
        token = self.nextToken()
        if(token.getLexema() == '!'):
            print(token.getLexema())
            self.addendOperatorUnary() 
            token = self.nextToken()
            if(token.getLexema()==';'):
                print(token.getLexema())          
        else:
            self.previousToken()
            print("ESPERADO '!'")

    #<AddendOperatorUnary> ::= Identifier | Boolean     
    def addendOperatorUnary(self):
        token = self.nextToken()
        if(token.getClass() in ('identificador') or token.getLexema() in ('true', 'false')):
            print(token.getLexema())            
        else:
            self.previousToken()
            print("ESPERADO UM IDENTIFICADOR OU UM BOLEANO")
                
    def binaryExpressionContin(self):
        print("BINARY_EXPRESSION_CONTIN")
        token = self.nextToken()
        tokError = token.getPosition()
        if(token == None):
            print("ESPERARO ';' - FIM DE ARQUIVO NAO ESPERADO - linha ", tokError)
            return
        if((token.getLexema() in ('+', '-', '*', '/')) or (token.getLexema() in REL_LOG_Expression)):
            print(token.getLexema())
            self.addentIdent()
            token = self.nextToken()
            if(token.getLexema()==';'):
                print(token.getLexema())
            else:
                self.previousToken()
                print("ESPERADO UM ';'")
                
        elif(token.getLexema() in ('++', '--')):
            print(token.getLexema())
            token = self.nextToken()
            if(token.getLexema()==';'):
                print(token.getLexema())
            else:
                self.previousToken()
                print("ESPERADO UM ';'")
        elif(token.getLexema() ==';'):
            print(token.getLexema())
            return
        else:
            self.previousToken()
            print("ESPERADO UM OPERADOR ARITMÉTICO, LÓGICO OU RELACIONAL")                            
    
    def procedureCall(self):
        self.argument()
        token = self.nextToken()
        if(token.getLexema()==")"):
            print(token.getLexema()) 
            token = self.nextToken()
        else:
            print("ESPERADO UM ')'")
        
        if(token.getLexema()==";"):
            print(token.getLexema()) 
        else:
            self.previousToken()
            print("ESPERADO UM ';'")

    #<FunctionCall> ::= '(' <Argument> ')' ';'
    def functionCall(self):
        token = self.nextToken()
        if(token.getLexema()=='('):
            print(token.getLexema())
            self.argument()
            token = self.nextToken()
            if(token.getLexema()==')'):
                print(token.getLexema())
                token = self.nextToken()
            else:
                print("ESPERADO UM ')'")
                
            if(token.getLexema()==';'):
                print(token.getLexema())
            else:
                self.previousToken()
                print("ESPERADO UM ';'")
        else:
            self.previousToken()
            token = self.ERROR((',',';'))
            
            if(token.getLexema()==','):
                print("ESPERADO UM '('")
                self.previousToken()
                self.argumentList()
                token = self.nextToken()
                if(token.getLexema()==')'):
                    print(token.getLexema())
                    self.previousToken()
                else:
                    print("ESPERADO UM ')'")
                
                if(token.getLexema()==';'):
                    print(token.getLexema())
                else:
                    self.previousToken()
                    print("ESPERADO UM ';'")
                return   
                    
            if(token.getLExema()==';'):
                print(token.getLexema())
                print("ESPERADO '(' e ')'")    
                return
                
    #<Argument> ::= <Value> <ArgumentList> |
    def argument(self):
        token = self.nextToken()
        if(token.getLexema() in ('false','true') 
        or token.getClass() in ('inteiro','ponto_flutuante','cadeia de caracteres','caracter', 'identificador')):
            self.previousToken()
            self.value()
            self.argumentList()
        else:##vazio 
            self.previousToken()
            
    #<ArgumentList> ::= ',' <Argument> |       
    def argumentList(self):
        print("ARGUMENT_LIST")
        token = self.nextToken()
        tokError = token.getPosition()
        if(token.getLexema()==','):
            print(token.getLexema())
            self.argument()
        else: #vazio
            if(token.getClass()=='identificador'):
                print("ESPERADO UMA ',' - linha ", tokError)
                self.previousToken()
                self.argument()
                return
                
            self.previousToken()
#########################################################################################    
    
    def nextToken(self):
        self.token_position+=1
        if self.token_position == len(self.tokens_list):
            return None
        return self.tokens_list[self.token_position]

    def previousToken(self):
        self.token_position-=1
        return self.tokens_list[self.token_position]