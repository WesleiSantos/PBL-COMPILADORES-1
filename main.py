#myfile = open('c:/Users/dhoml/Desktop/example.txt')
#file = open('example.txt', 'r')
#print("meu arquivo: ", myfile.read)

#from turtle import pos
#from unicodedata import combining
#import numpy;
#from unicodedata import normalize

from nbformat import read
import read

msg= read.arquiv.read_lines("example.txt")

print("Tamanho: A", len(msg))
print(msg)


#mensagem = input()
estado = 0
pos = 0
listTokens = ""
Arraylist = []

#retorna true se o caracter é sem acento
def semAcento(char):
    if char in ('á','à','â','ã', 'ç', 'í', 'ì','î', 'ñ', 'û','ú', 'ù', 'ó', 'ô', 'õ'):
        print("Caracter com acento!")
        return False
    elif char in ('á'.upper(), 'à'.upper(),'â'.upper(), 'ã'.upoer(),'ç'.upper(), 'ì'.upper(),  
    'í'.upper(),'î'.upper(),'û'.upper(), 'ú'.upper(), 'ù'.upper(),'ó'.upper(), 'ô'.upper(), 'õ'.upper()):
        print("Caracter com acento!")
        return False
    return True

def nextToken():
    global estado
    global pos
    global listTokens
    pos2 = 0;

    i = 0
    print("TAMANHO DA MENSAGEM: ", len(msg))
    while i < len(msg):
        if estado == 0:
            # ler o proximo, e muda o estado e sai.
            char = readNext()

            print("CHAR: ", char)
            if(char.isnumeric()):
                print("É UM DIGITO")
                estado = 2
                pos2 = pos-1

            # é uma letra, exceto ç - falta colocar exececoes nas letras com acentos.
            elif char.isalpha() and semAcento(char):
                print("É UMA LETRA")
                estado = 1

                pos2 = pos-1 #como a posicao foi para 1 precisa-se usar a posicao anterior caso forme um token
            elif char=='+':
                print("É o '+' ")
                estado = 5
                pos2 = pos-1
                ##fechar o token

            elif char=='-':
                print("É o '+' ")
                estado = 6
                pos2 = pos-1
                ##fechar o token

            elif char in('/', '*') :
                print("É o ", char)
                estado = 7
                pos2 = pos-1 ##aqui poderíamos fechar o token , pós nao pode vim outra / ou *
            
            elif char in ('=', '<', '>'):
                print("É o ", char)
                estado = 8
                pos2 = pos-1
                
            elif char =='!':
                print("É o ", char)
                estado = 9
                pos2 = pos-1

            elif char =='&':
                print("É o ", char)
                estado = 11
                pos2 = pos-1

            elif char =='|':
                print("É o ", char)
                estado = 12
                pos2 = pos-1

            elif char =='!':
                print("É o ", char)
                estado = 13
                pos2 = pos-1

            elif char =='%':
                print("É o ", char)
                estado = 14
                pos2 = pos-1

            elif char =='/':
                print("É o ", char)
                estado = 14
                pos2 = pos-1

            elif char =='/':
                print("É o ", char)
                estado = 15
                pos2 = pos-1

            elif char in('.', ',', ':', ';'): #delimitadores
                print("É o ", char)
                estado = 19
                pos2 = pos-1

            elif char =="\"": #CADEIRA DE CARACTEREs
                print("É o ", char)
                estado = 20
                pos2 = pos-1

            elif char =="'": #caracter
                print("É o ", char)
                estado = 23
                pos2 = pos-1

            else: ##tratar o resto
                print("NEM LETRA, NEM DIGITO")
            
            #se chegou ao fim
            if(pos==len(msg)):
                listTokens = msg[pos2:pos]
                print("token: ", listTokens)
                
            i+=1
            print("I = ", i)
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
                listTokens = msg[pos2-1:pos]
                print("token: ", listTokens)
            
            
            

def readNext():
    global pos

    char = msg[pos]
    pos+=1
    return char

#verificar um token
nextToken()
