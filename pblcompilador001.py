#myfile = open('c:/Users/dhoml/Desktop/example.txt')
#file = open('example.txt', 'r')
#print("meu arquivo: ", myfile.read)

#from turtle import pos
#from unicodedata import combining
#import numpy;
#from unicodedata import normalize

print("digite o quiser")

mensagem = input()
estado = 0
pos = 0
listTokens = ""


#retorna true se o caracter é sem acento
def semAcento(char):
    if char in ('á','à', 'ç', 'ç'.upper(), 'í', 'í'.upper(), 'ì', 'ñ', 'û', 'û'.upper(), 'ú', 'ú'.upper(), 'ù'):
        print("Caracter com acento!")
        return False
    elif char in ('á'.upper(), 'à'.upper(), 'ì'.upper()):
        print("Caracter com acento!")
        return False
    return True

def nextToken():
    global estado
    global pos
    global listTokens
    pos2 = 0;

    i = 0
    print("TAMANHO DA MENSAGEM: ", len(mensagem))
    while i < len(mensagem):
        if estado == 0:
            # ler o proximo, e muda o estado e sai.
            char = readNext()

            print("CHAR: ", char)
            if(char.isnumeric()):
                print("É UM DIGITO")
                estado = 2
            # é uma letra, exceto ç - falta colocar exececoes nas letras com acentos.
            elif char.isalpha() and semAcento(char):
                print("É UMA LETRA")
                estado = 1

                pos2 = pos;

            else:
                print("NEM LETRA, NEM DIGITO")
            
            #se chegou ao fim
            if(pos==len(mensagem)):
                listTokens = mensagem[pos2-1:pos]
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
            if(pos==len(mensagem)):
                listTokens = mensagem[pos2-1:pos]
                print("token: ", listTokens)
            
            
            

def readNext():
    global pos

    char = mensagem[pos]
    pos+=1
    return char

#verificar um token
nextToken()
