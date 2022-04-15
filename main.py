# myfile = open('c:/Users/dhoml/Desktop/example.txt')
# file = open('example.txt', 'r')
# print("meu arquivo: ", myfile.read)

# from turtle import pos
# from unicodedata import combining
# import numpy;
# from unicodedata import normalize

# from nbformat import read
import read
from token import Token


# retorna true se o caracter é sem acento
def semAcento(char):
    if char in ('á', 'à', 'â', 'ã', 'ç', 'í', 'ì', 'î', 'ñ', 'û', 'ú', 'ù', 'ó', 'ô', 'õ'):
        print("Caracter com acento!")
        return False
    elif char in ('á'.upper(), 'à'.upper(), 'â'.upper(), 'ã'.upoer(), 'ç'.upper(), 'ì'.upper(),
    'í'.upper(), 'î'.upper(), 'û'.upper(), 'ú'.upper(), 'ù'.upper(), 'ó'.upper(), 'ô'.upper(), 'õ'.upper()):
        print("Caracter com acento!")
        return False
    return True


def listToken():
    global estado
    global pos
    global listTokens
    global count_line
    inicio_lexema = 0
    caracter_anterior=''

    while True:
        if estado == 0: #estado inicial
             # ler o proximo, e muda o estado e sai.
            print("\nESTADO 0")
            char = readNext()
            print("lookhead: ", char)

            if not char:
                break

            if(char.isspace()):
                print("É UM ESPAÇO")
                estado = 0
                inicio_lexema = pos-1

            if(char.isnumeric()):
                print("É UM DIGITO")
                estado = 2
                inicio_lexema = pos-1

            # é uma letra, exceto ç - falta colocar exececoes nas letras com acentos.
            elif char.isalpha() and semAcento(char):
                print("É UMA LETRA")
                estado = 1

                inicio_lexema = pos-1  # como a posicao foi para 1 precisa-se usar a posicao anterior caso forme um token
            elif char == '+':
                print("É o '+' ")
                estado = 5
                inicio_lexema = pos-1
                
            elif char == '-':
                print("É o '-' ")
                estado = 6
                inicio_lexema = pos-1
                
            elif char in ('/', '*'):
                print("É o ", char)
                estado = 7
                caracter_anterior=char
                inicio_lexema = pos-1  # aqui poderíamos fechar o token , pós nao pode vim outra / ou *

            elif char in ('=', '<', '>'):
                print("É o ", char)
                estado = 8
                caracter_anterior=char
                inicio_lexema = pos-1
            
            elif char == '!':
                print("É o ", char)
                estado = 9
                inicio_lexema = pos-1

            elif char == '&':
                print("É o ", char)
                caracter_anterior = char;
                estado = 11
                inicio_lexema = pos-1

            elif char == '|':
                print("É o ", char)
                caracter_anterior = char;
                estado = 12
                inicio_lexema = pos-1

            elif char == '!':
                print("É o ", char)
                estado = 13
                inicio_lexema = pos-1

            elif char == '%':
                print("É o ", char)
                estado = 14
                inicio_lexema = pos-1

            elif char == '/':
                print("É o ", char)
                estado = 14
                inicio_lexema = pos-1

            elif char == '/':
                print("É o ", char)
                estado = 15
                inicio_lexema = pos-1

            elif(char in (',', ':', ';')): # delimitadores
                print("É o ", char)
                estado = 19
                inicio_lexema = pos-1

            elif char == "\"":  # CADEIRA DE CARACTEREs
                print("É o ", char)
                estado = 20
                inicio_lexema = pos-1

            elif char == "'":  # caracter
                print("É o ", char)
                estado = 23
                inicio_lexema = pos-1

            elif(char == '\n'):
                print("FIM DE LINHA")
                count_line+=1
                estado = 0
                inicio_lexema = pos-1
  
        elif estado == 2: #estado de digito
            
            # ler o proximo, e muda o estado e sai.
            char = readNext()
            print("\nESTADO 2")
            print("lookhead: ", char)

            if char == None:
                print("none")
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line,'delimitador',lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
                break
            elif(char.isspace() or char in (',', ':', ';')):
                print("É DELIMITADOR")
                print("SALVA TOKEN")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line,'inteiro',lexema)
                listTokens.append(token)
                estado = 0
                pos = pos-1
            
            elif (char.isnumeric()): ##depois de um dígito pode ter outro 
                print("É UM DIGITO")
                estado = 2
                #inicio_lexema = pos-1

            elif(char == '.'): ## ou ter um limitador(float)
                print("É DELIMITADOR . ")
                estado = 3

            elif(char == '\n'):
                print("FIM DE LINHA")
                estado = 0
            
            else:
                print("É OUTRO CARACTER")
                print("SALVA TOKEN")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line,'inteiro',lexema)
                listTokens.append(token)
                estado = 0
                pos = pos-1

        elif estado == 3: #estado do ponto "flutuante"
            char = readNext()
            print("\nESTADO 3")
            print("lookhead: ", char)

            if(char.isnumeric()): ##depois de um . tem um digito 
                print("É UM DIGITO")
                estado = 4
                #inicio_lexema = pos-1

            #encontra outro delimitador -> (ex.: 123.,) digito mal formado? marca até o 123.
            if(char.isspace() or char in ('.', ',', ':', ';')): 
                lexema = codigo[inicio_lexema:pos-1] 
                estado = 0
            
            elif(char == '\n'):
                print("FIM DE LINHA")
                estado = 0
        
        elif estado == 4: #estado dos decimais
            char = readNext()
            print("\nESTADO 4")
            print("lookhead: ", char)

            if char == None:
                print("none")
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line,'delimitador',lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
                break

            elif(char.isnumeric()): ##depois de um . tem um digito 
                print("É UM DIGITO")
                estado = 4

            elif(char.isspace() or char in ('.', ',', ':', ';') ):
                print("É DELIMITADOR")
                print("SALVA TOKEN")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line,'ponto flutuante',lexema)
                estado = 0
                pos = pos-1
                listTokens.append(token)
            elif(char == '\n'):
                print("FIM DE LINHA")
                estado = 0
            else:
                print("É OUTRO CARACTER")
                print("SALVA TOKEN")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line,'ponto flutuante',lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1

        elif estado == 5: #estado sinal de adição
            # ler o proximo, e muda o estado e sai.
            char = readNext()
            print("\nESTADO 5")
            print("lookhead: ", char)

            if char == None:
                print("none")
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line,'delimitador',lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
                break

            elif(char.isspace() or char in ('.', ',', ':', ';')):
                print("É DELIMITADOR")
                print("SALVA TOKEN")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line,'operador_adicao',lexema)
                estado = 0
                pos = pos-1
                listTokens.append(token)
                
            elif char == '+':
                print("É o '+' ")
                estado = 7
                inicio_lexema = pos-1
            elif(char == '\n'):
                print("FIM DE LINHA")
                estado = 0
            else:
                print("É OUTRO CARACTER")
                print("SALVA TOKEN")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line,'operador_adicao',lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1

        elif estado == 6: #estado sinal de subtração
            # ler o proximo, e muda o estado e sai.
            char = readNext()
            print("\nESTADO 6")
            print("lookhead: ", char)

            if char == None:
                print("none")
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line,'delimitador',lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
                break

            elif(char.isspace() or char in ('.', ',', ':', ';')):
                print("É DELIMITADOR")
                print("SALVA TOKEN")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line,'operador_subtração',lexema)
                estado = 0
                pos = pos-1
                listTokens.append(token)
                
            elif char == '-':
                print("É o '-' ")
                estado = 7
                inicio_lexema = pos-1
            
            elif(char == '\n'):
                print("FIM DE LINHA")
                estado = 0

        elif estado == 7: #estado de incremento, deremento, multiplicação ou divisão
            char = readNext()
            print("\nESTADO 7")
            print("lookhead: ", char)

            if char == None:
                print("none")
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line,'delimitador',lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
                break
            
            elif(char == '-'):
                print("operador de subtração")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line,'operador_decremento',lexema)
                estado = 0
                pos = pos-1
                listTokens.append(token)

            elif(char == '+'):
                print("operador de adicao")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line,'operador_incremento',lexema)
                estado = 0
                pos = pos-1
                listTokens.append(token)

            #se o caracter anterior foi o / ou *
            #if(char.isspace() or char in ('.', ',', ':', ';', '/', '*', )): 

            #READ ME----->>>>> acho que nem precisa desse if, pois o que vem antes é 
            # um dos operadores e depois qualquer outra coisa q aí vai ter que jogar
            #  pro estado 0 (SUGESTAO) posso ta falando besteira... 
            print("É o ", caracter_anterior)
            lexema = codigo[inicio_lexema:pos-1]

            if(caracter_anterior=='*'):
                token = Token(count_line,'operador_multiplicacao',lexema)
            if(caracter_anterior=='/'):
                token = Token(count_line,'operador_divisao',lexema)
                estado = 0
                pos = pos-1
                caracter_anterior=''
                listTokens.append(token)
            if(char == '\n'):
                print("FIM DE LINHA")
                estado = 0

        elif estado == 8: #estado de igual, maior ou menor
             # ler o proximo, e muda o estado e sai.
            char = readNext()
            print("\nESTADO 8")
            print("lookhead: ", char)

            if char == None:
                print("none")
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line,'delimitador',lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
                break

            elif(char.isspace() or char in ('.', ',', ':', ';')):
                print("É DELIMITADOR")
                print("SALVA TOKEN")
                lexema = codigo[inicio_lexema:pos-1]
                if(caracter_anterior=="="):
                    token = Token(count_line,'operador_atribuicao',lexema)
                elif(caracter_anterior=="<"):
                    token = Token(count_line,'operador_menorque',lexema)
                elif(caracter_anterior==">"):
                    token = Token(count_line,'operador_maiorque',lexema)
                estado = 0
                pos = pos-1
                caracter_anterior=''
                listTokens.append(token)

            elif char == '=':
                print("É o ", char)
                estado = 10 ##poderíamos fechar o lexama aqui? nem precisaria do estado 10
                if(caracter_anterior=="="): 
                    token = Token(count_line,'operador_igualdade',lexema)
                elif(caracter_anterior=="<"):
                    token = Token(count_line,'operador_menor_igual',lexema)
                elif(caracter_anterior==">"):
                    token = Token(count_line,'operador_maior_igual',lexema)
                lexema = codigo[inicio_lexema:pos-1]
                estado = 0
                listTokens.append(token)
                pos = pos-1

            elif(char == '\n'):
                print("FIM DE LINHA")
                estado = 0
            else:
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line,'operador_adicao',lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
        
        elif estado == 9: #estado de sinal de exclamação
             # ler o proximo, e muda o estado e sai.
            char = readNext()
            print("\nESTADO 9")
            print("lookhead: ", char)
            if char == '=':
                print("É o ", char)
                estado = 10 ##poderíamos fechar o lexama aqui? nem precisaria do estado 10
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line,'operador_diferente_de',lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
            elif(char == '\n'):
                print("FIM DE LINHA")
                estado = 0

        elif estado == 13:
            char = readNext()
            print("\nESTADO ", estado)
            ##aqui tem-se um erro - operador lógico incompleto.
            if char == None:
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line,'delimitador',lexema)
                estado = 0
                listTokens .append(token)
                pos = pos-1
                break
            elif char in ('.', ',', ':', ';') or char == '\n' or char.isspace():
                print("delimitador")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line,'delimitador',lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
            elif char == '&' and caracter_anterior == '&':
                print("operador lógico E")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line,'operador lógico &&',lexema)
                estado = 0
                listTokens.append(token)
                #pos = pos-1
            elif char == '&' and caracter_anterior == '|':
                print("&| error")
                #ERROR
            elif char == '|' and caracter_anterior == '&':
                print("|& error")
            elif char == '|' and caracter_anterior == '|':
                print("operador lógico OU")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line,'operador lógico ||',lexema)
                estado = 0
                listTokens.append(token)
                #pos = pos-1
            else:
                print ("outher", char)
                #ERRO
            
                
                

        elif estado == 19: #estado de delimitadores
            # ler o proximo, e muda o estado e sai.
            char = readNext()
            print("\nESTADO 19")
            print("lookhead: ", char)
            if char == None:
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line,'delimitador',lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
                break
            elif char in ('.', ',', ':', ';') or char == '\n' or char.isspace():
                print("delimitador")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line,'delimitador',lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
                
            


        
            
        
            


        
            '''print("I = ", i)
            print("POSITION= ", pos)
        elif estado == 1:
            print("POSICAO", pos)
            char = readNext()
            if(char.isalpha() or char.isnumeric() or char=='_'):
                if(char.isalpha() and semAcento(char)):
                    print("CARACTER SEM ACENTO")
                    estado = 1
                    

                estado = 1
            else: #o proximo caracter nao é nem L, D ou _
                pos-=1
                estado=0
                
            i+=1
            if(pos==len(msg)):
                listTokens = msg[inicio_lexema-1:pos]
                print("token: ", listTokens)'''
            
def readNext():
    global pos
    global file
    global codigo
    if pos == len(codigo):
        return None
    char = codigo[pos]
    pos+=1
    return char



# mensagem = input()
estado = 0
pos = 0
listTokens = []
Arraylist = []
count_line = 0

file = open("digito.txt", "r")
codigo = file.read()

listToken()
for token in listTokens:
    print(token.get())



file.close()