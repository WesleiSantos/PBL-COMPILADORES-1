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

msg = read.arquiv.read_lines("example.txt")

print(msg, "\n")

# mensagem = input()
estado = 0
pos = 0
listTokens = []
Arraylist = []
linha_atual = ''

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


def nextToken(count):
    global estado
    global pos
    global listTokens
    inicio_lexema = 0

    while True:
        if estado == 0:
            # ler o proximo, e muda o estado e sai.
            char = readNext()

            print("lookhead: ", char)

            if(char.isspace()):
                print("É UM ESPAÇO")
                estado = 0

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
                # fechar o token

            elif char == '-':
                print("É o '+' ")
                estado = 6
                inicio_lexema = pos-1
                # fechar o token

            elif char in ('/', '*'):
                print("É o ", char)
                estado = 7
                inicio_lexema = pos-1  # aqui poderíamos fechar o token , pós nao pode vim outra / ou *

            elif char in ('=', '<', '>'):
                print("É o ", char)
                estado = 8
                inicio_lexema = pos-1

            elif char == '!':
                print("É o ", char)
                estado = 9
                inicio_lexema = pos-1

            elif char == '&':
                print("É o ", char)
                estado = 11
                inicio_lexema = pos-1

            elif char == '|':
                print("É o ", char)
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

            elif char in ('.', ',', ':', ';'):  # delimitadores
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

            # se chegou ao fim
            if(pos==len(linha_atual)):
                listTokens = linha_atual[inicio_lexema:pos]
                print("token: ", listTokens)
                return
        elif estado == 2:
            
            # ler o proximo, e muda o estado e sai.
            char = readNext()

            print("lookhead: ", char)

            if(char.isspace() or char in ('.', ',', ':', ';')):
                print("É DELIMITADOR")
                lexema = linha_atual[inicio_lexema:pos]
                token = Token(count,'digito',lexema)
                estado = 0
                return token
                
            if(char.isnumeric()):
                print("É UM DIGITO")
                estado = 2
                inicio_lexema = pos-1
        
        elif estado == 5:
            # ler o proximo, e muda o estado e sai.
            char = readNext()

            print("lookhead: ", char)

            if(char.isspace()):
                print("É DELIMITADOR")
                lexema = linha_atual[inicio_lexema:pos]
                token = Token(count,'operador_adicao',lexema)
                estado = 0
                pos = pos-1
                return token
                
            elif char == '+':
                print("É o '+' ")
                estado = 7
                inicio_lexema = pos-1
                # fechar o token
        elif estado == 8:
             # ler o proximo, e muda o estado e sai.
            char = readNext()

            print("lookhead: ", char)

            if(char.isspace()):
                print("É DELIMITADOR")
                lexema = linha_atual[inicio_lexema:pos]
                token = Token(count,'operador_adicao',lexema)
                estado = 0
                pos = pos-1
                return token
            elif(char == '\n'):
                print("FIM DE LINHA")
git                 estado = 0
                pass

        
            
        
            


        
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
    char = linha_atual[pos]
    pos+=1
    return char

# verificar um token
count = 1
for linha in msg:
    linha_atual = linha
    for letra in linha:
        token = nextToken(count)
        if token is not None:
            print(token.get())
        else:
            break
    count += 1 
