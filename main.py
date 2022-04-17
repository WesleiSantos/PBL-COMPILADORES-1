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
    elif char in ('á'.upper(), 'à'.upper(), 'â'.upper(), 'ã'.upper(), 'ç'.upper(), 'ì'.upper(),
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
    caracter_anterior = ''
    delimitadores = ('.', ',', ':', ';', '(', ')', '[', ']', '{', '}')
    reservation_words = ("program", "var", "const","register","function", "procedure","return", "main", "if", "else", "while","read","write", "integer", "real","boolean","char", "string", "true", "false")
    while True:

        if estado == 0:  # estado inicial
            # ler o proximo, e muda o estado e sai.
            print("\nESTADO 0")
            char = readNext()
            print("lookhead: ", char)

            if char == None:
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

                # como a posicao foi para 1 precisa-se usar a posicao anterior caso forme um token
                inicio_lexema = pos-1
            elif char == '+':
                print("É o '+' ")
                caracter_anterior = char
                estado = 5
                inicio_lexema = pos-1

            elif char == '-':
                print("É o '-' ")
                caracter_anterior = char
                estado = 6
                inicio_lexema = pos-1

            elif char in ('/', '*'):
                print("É o Veio", char)
                estado = 7
                caracter_anterior = char
                inicio_lexema = pos-1  # aqui poderíamos fechar o token , pós nao pode vim outra / ou *

            elif char in ('=', '<', '>'):
                print("É o ", char)
                estado = 8
                caracter_anterior = char
                inicio_lexema = pos-1

            elif char == '!':
                print("É o ", char)
                estado = 9
                caracter_anterior = char
                inicio_lexema = pos-1

            elif char == '&':
                print("É o ", char)
                caracter_anterior = char
                estado = 11
                inicio_lexema = pos-1

            elif char == '|':
                print("É o ", char)
                caracter_anterior = char
                estado = 12
                inicio_lexema = pos-1

            elif char == '%':
                print("É o ", char)
                estado = 14
                inicio_lexema = pos-1

            elif(char in delimitadores):  # delimitadores
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
                count_line += 1
                estado = 0
                inicio_lexema = pos-1
    
        elif estado == 1:  # estado de identificador
            # ler o proximo, e muda o estado e sai.
            char = readNext()
            print("\nESTADO 1")
            print("lookhead: ", char)

            if char == None:
                print("none")
                lexema = codigo[inicio_lexema:pos]
                if(lexema in reservation_words):
                    token = Token(count_line, 'palavra reservada', lexema)
                else:
                    token = Token(count_line, 'identificador', lexema)
                estado = 0
                listTokens.append(token)
                break
            elif(char.isspace() or char in delimitadores or char == "\n"):
                print("identificador")
                print("SALVA TOKEN")
                lexema = codigo[inicio_lexema:pos-1]
                if(lexema in reservation_words):
                    token = Token(count_line, 'palavra reservada', lexema)
                else:
                    token = Token(count_line, 'identificador', lexema)
                listTokens.append(token)
                estado = 0
                pos=pos-1
            elif ((char.isalpha() and semAcento(char)) or char.isnumeric() or char == "_"):
                print("É UMA LETRA")
                estado = 1
            else:
                lexema = codigo[inicio_lexema:pos-1]
                if(lexema in reservation_words):
                    token = Token(count_line, 'palavra reservada', lexema)
                else:
                    token = Token(count_line, 'identificador', lexema)
                listTokens.append(token)
                estado = 0
                pos = pos-1

        elif estado == 2:  # estado de digito

            # ler o proximo, e muda o estado e sai.
            char = readNext()
            print("\nESTADO 2")
            print("lookhead: ", char)

            if char == None:
                print("none")
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line, 'inteiro', lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
                break
            
            elif(char == '.'):  # ou ter um limitador(float)
                print("É DELIMITADOR . ")
                estado = 3

            elif(char.isspace() or char in delimitadores):
                print("É DELIMITADOR")
                print("SALVA TOKEN")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'inteiro', lexema)
                listTokens.append(token)
                estado = 0
                pos = pos-1

            elif (char.isnumeric()):  # depois de um dígito pode ter outro
                print("É UM DIGITO")
                estado = 2
                #inicio_lexema = pos-1

            elif(char == '\n'):
                print("FIM DE LINHA")
                estado = 0

            else:
                print("É OUTRO CARACTER")
                print("SALVA TOKEN")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'inteiro', lexema)
                listTokens.append(token)
                estado = 0
                pos = pos-1

        elif estado == 3:  # estado do ponto "flutuante"
            char = readNext()
            print("\nESTADO 3")
            print("lookhead: ", char)

            if(char.isnumeric()):  # depois de um . tem um digito
                print("É UM DIGITO")
                estado = 4
                #inicio_lexema = pos-1

            # encontra outro delimitador -> (ex.: 123.,) digito mal formado? marca até o 123.
            if(char.isspace() or char in delimitadores):
                lexema = codigo[inicio_lexema:pos-1]
                estado = 0

            elif(char == '\n'):
                print("FIM DE LINHA")
                estado = 0

        elif estado == 4:  # estado dos decimais
            char = readNext()
            print("\nESTADO 4")
            print("lookhead: ", char)

            if char == None:
                print("none")
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line, 'ponto_flutuante', lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
                break

            elif(char.isnumeric()):  # depois de um . tem um digito
                print("É UM DIGITO")
                estado = 4

            elif(char.isspace() or char in delimitadores):
                print("É DELIMITADOR")
                print("SALVA TOKEN")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'ponto_flutuante', lexema)
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
                token = Token(count_line, 'ponto_flutuante', lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1

        elif estado == 5:  # estado sinal de adição
            # ler o proximo, e muda o estado e sai.
            char = readNext()
            print("\nESTADO 5")
            print("lookhead: ", char)

            if char == None:
                print("none")
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line, 'delimitador', lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
                break

            elif(char.isspace() or char in delimitadores):
                print("É DELIMITADOR")
                print("SALVA TOKEN")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'operador_adicao', lexema)
                estado = 0
                pos = pos-1
                listTokens.append(token)

            elif char == '+':
                print("É o '+' ")
                estado = 7
            elif(char == '\n'):
                print("FIM DE LINHA")
                estado = 0
            else:
                print("É OUTRO CARACTER")
                print("SALVA TOKEN")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'operador_adicao', lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1

        elif estado == 6:  # estado sinal de subtração
            # ler o proximo, e muda o estado e sai.
            char = readNext()
            print("\nESTADO 6")
            print("lookhead: ", char)

            if char == None:
                print("none")
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line, 'delimitador', lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
                break

            elif(char.isspace() or char in delimitadores):
                print("É DELIMITADOR")
                print("SALVA TOKEN")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'operador_subtração', lexema)
                estado = 0
                pos = pos-1
                listTokens.append(token)

            elif char == '-':
                print("É o '-' ")
                estado = 7

            elif(char == '\n'):
                print("FIM DE LINHA")
                estado = 0

        elif estado == 7:  # estado de incremento, deremento, multiplicação ou divisão
            char = readNext()
            print("\nESTADO 7")
            print("lookhead: ", char)
            print(caracter_anterior)
            if char == None:
                print("none")
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line, 'delimitador', lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
                break
            elif(caracter_anterior == '-'):
                print("operador de subtração")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'operador_decremento', lexema)
                estado = 0
                pos = pos-1
                listTokens.append(token)
                caracter_anterior=''
            elif(caracter_anterior == '+'):
                print("operador de adicao")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'operador_incremento', lexema)
                estado = 0
                pos = pos-1
                listTokens.append(token)
                caracter_anterior=''
            elif(caracter_anterior == '*'):
                print("operador de multiplicação")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'operador_multiplicacao', lexema)
                estado = 0
                pos = pos-1
                listTokens.append(token)
                caracter_anterior=''
            elif(caracter_anterior == '/' and char == '#'):
                estado = 15
            elif(caracter_anterior == '/'):
                print("operador de divisão")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'operador_divisao', lexema)
                estado = 0
                pos = pos-1
                caracter_anterior = ''
                listTokens.append(token)
            elif(char == '\n'):
                print("FIM DE LINHA")
                estado = 0
        
        elif estado == 8:  # estado de igual, maior ou menor
            # ler o proximo, e muda o estado e sai.
            char = readNext()
            print("\nESTADO 8")
            print("lookhead: ", char)
            if char == None:
                print("É um operador relacional")
                lexema = codigo[inicio_lexema:pos]
                if(caracter_anterior == "="):
                    token = Token(count_line, 'operador_atribuicao', lexema)
                elif(caracter_anterior == "<"):
                    token = Token(count_line, 'operador_menorque', lexema)
                elif(caracter_anterior == ">"):
                    token = Token(count_line, 'operador_maiorque', lexema)
                listTokens.append(token)
                break
            elif char.isspace() or char in delimitadores:
                print("É um operador relacional")
                lexema = codigo[inicio_lexema:pos-1]
                if(caracter_anterior == "="):
                    token = Token(count_line, 'operador_atribuicao', lexema)
                elif(caracter_anterior == "<"):
                    token = Token(count_line, 'operador_menorque', lexema)
                elif(caracter_anterior == ">"):
                    token = Token(count_line, 'operador_maiorque', lexema)
                estado = 0
                pos = pos-1
                caracter_anterior = ''
                listTokens.append(token)
            elif char == '=':
                print("É o ", char)
                estado = 10  # poderíamos fechar o lexama aqui? nem precisaria do estado 10
            elif(char == '\n'):
                print("FIM DE LINHA")
                estado = 0
            else:
                lexema = codigo[inicio_lexema:pos-1]
                if(caracter_anterior=="="):
                    token = Token(count_line,'operador_atribuicao',lexema)
                elif(caracter_anterior=="<"):
                    token = Token(count_line,'operador_menorque',lexema)
                elif(caracter_anterior==">"):
                    token = Token(count_line,'operador_maiorque',lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
                  
        elif estado == 9:  # estado de sinal de exclamação
            # ler o proximo, e muda o estado e sai.
            char = readNext()
            print("\nESTADO 9")
            print("lookhead: ", char)
            if char == None:
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line,'operador_de_negacao',lexema)
                listTokens.append(token)
                break
            elif char == '=':
                print("É o ", char)
                estado = 10  # poderíamos fechar o lexama aqui? nem precisaria do estado 10
            elif char in delimitadores or char.isspace():
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line,'operador_de_negacao',lexema)
                listTokens.append(token)
                pos = pos-1
                caracter_anterior = ''
                estado = 0
            else:
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line,'operador_de_negacao',lexema)
                listTokens.append(token)
                pos = pos-1
                caracter_anterior = ''
                estado = 0

        elif estado == 10:  # estado de igual, maior ou menor
            # ler o proximo, e muda o estado e sai.
            char = readNext()
            print("\nESTADO 10")
            print("lookhead: ", char)
            print("Caracter anteriror", caracter_anterior)
            if(caracter_anterior == "="):
                    print("É o ", char)
                    estado = 0 ##poderíamos fechar o lexama aqui? nem precisaria do estado 10
                    lexema = codigo[inicio_lexema:pos-1]
                    estado = 0
                    token = Token(count_line,'operador_igualdade',lexema)
                    listTokens.append(token)
                    pos = pos-1
                    caracter_anterior = ''
            elif(caracter_anterior=="<"):
                    print("É o ", char)
                    estado = 0 ##poderíamos fechar o lexama aqui? nem precisaria do estado 10
                    lexema = codigo[inicio_lexema:pos-1]
                    estado = 0
                    token = Token(count_line,'operador_menor_igual',lexema)
                    listTokens.append(token)
                    pos = pos-1
                    caracter_anterior = ''
            elif(caracter_anterior==">"):
                    print("É o ", char)
                    estado = 0 ##poderíamos fechar o lexama aqui? nem precisaria do estado 10
                    lexema = codigo[inicio_lexema:pos-1]
                    estado = 0
                    token = Token(count_line,'operador_maior_igual',lexema)
                    listTokens.append(token)
                    pos = pos-1
                    caracter_anterior = ''
            elif(caracter_anterior=="!"):
                    print("É o ", char)
                    estado = 0 ##poderíamos fechar o lexama aqui? nem precisaria do estado 10
                    lexema = codigo[inicio_lexema:pos-1]
                    estado = 0
                    token = Token(count_line,'operador_diferenca',lexema)
                    listTokens.append(token)
                    pos = pos-1
                    caracter_anterior = ''
            elif(char == '\n'):
                print("FIM DE LINHA")
                estado = 0
            elif(char.isspace() or char in delimitadores):
                print("É DELIMITADOR")
                print("SALVA TOKEN")
                lexema = codigo[inicio_lexema:pos-1]
                estado = 0
                pos = pos-1
                caracter_anterior=''
                listTokens.append(token)
            else:
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'operador_logico', lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
            if char == None:
                break

        elif estado == 11:  # estado sinal de &
            # ler o proximo, e muda o estado e sai.
            char = readNext()
            print("\nESTADO 11")
            print("lookhead: ", char)

            if char == None:
                print("none")
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line, 'operador_logico_mal_formado', lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
                break
            elif(char.isspace() or char in delimitadores):
                print("É DELIMITADOR")
                print("SALVA TOKEN")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'error', lexema)
                estado = 0
                pos = pos-1
                listTokens.append(token)
            elif char == '&':
                print("É o", char)
                estado = 13
            else:
                print("ERROR")
                print("SALVA TOKEN")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'operador_logico_mal_formado', lexema)
                estado = 0
                pos = pos-1
                listTokens.append(token)
        
        elif estado == 12:  # estado sinal de |
            # ler o proximo, e muda o estado e sai.
            char = readNext()
            print("\nESTADO 12")
            print("lookhead: ", char)

            if char == None:
                print("none")
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line, 'operador_logico_mal_formado', lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
                break
            elif char == '|':
                print("É o", char)
                estado = 13
            elif(char.isspace() or char in delimitadores):
                print("É DELIMITADOR")
                print("SALVA TOKEN")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'operador_logico_mal_formado', lexema)
                estado = 0
                pos = pos-1
                listTokens.append(token)
            else:
                print("ERROR")
                print("SALVA TOKEN")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'operador_logico_mal_formado', lexema)
                estado = 0
                pos = pos-1
                listTokens.append(token)

        elif estado == 13:  # estado de operadores relacionais
            char = readNext()
            print("\nESTADO ", estado)
            # aqui tem-se um erro - operador lógico incompleto.
            print(caracter_anterior)
            if char == None :
                lexema = codigo[inicio_lexema:pos]
                if caracter_anterior == '&':
                    print("operador lógico E")
                    token = Token(count_line, 'operador_logico_and', lexema)
                elif caracter_anterior == '|':
                    print("operador lógico OU")
                    lexema = codigo[inicio_lexema:pos]
                    token = Token(count_line, 'operador_logico_or', lexema)
                listTokens.append(token)
                break
            if caracter_anterior == '&':
                print("operador lógico E")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'operador_logico_and', lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
            elif caracter_anterior == '|':
                print("operador lógico OU")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'operador_logico_or', lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
            elif char == '&' and caracter_anterior == '|':
                print("&| error")
                # ERROR
            elif char == '|' and caracter_anterior == '&':
                print("|& error")
            elif char in delimitadores or char.isspace():
                print("delimitador")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'operador_relacional', lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
            else:
                print ("outher", char)

        elif estado == 14:  # Comentário de linha
            char = readNext()
            print("\nESTADO ", estado)
            # aqui tem-se um erro - operador lógico incompleto.
            if char == None :
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line, 'comentario_de_linha', lexema)
                listTokens.append(token)
                break
            elif char == '\n':
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'comentario_de_linha', lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
            else:
                estado=14

        elif estado == 15:  # Comentário de bloco #
            char = readNext()
            print("\nESTADO ", estado)
            # aqui tem-se um erro - operador lógico incompleto.
            if char == None :
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line, 'comentario_de_bloco_mal_formado', lexema)
                listTokens.append(token)
                break
            elif char == '#':
                estado = 16
            else:
                estado=15
        
        elif estado == 16:  # Comentário de bloco #
            char = readNext()
            print("\nESTADO ", estado)
            # aqui tem-se um erro - operador lógico incompleto.
            if char == None :
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line, 'comentario_de_bloco_mal_formado', lexema)
                listTokens.append(token)
                break
            elif char == '/':
                estado=17
            else:
                estado=15
        
        elif estado == 17:  # Comentário de bloco
            char = readNext()
            print("\nESTADO ", estado)
            # aqui tem-se um erro - operador lógico incompleto.
            if char == None :
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line, 'comentario_de_bloco', lexema)
                listTokens.append(token)
                break
            else:
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line, 'comentario_de_bloco', lexema)
                listTokens.append(token)
                estado = 0

        elif estado == 19:  # estado de delimitadores
            # ler o proximo, e muda o estado e sai.
            char = readNext()
            print("\nESTADO 19")
            print("lookhead: ", char)
            if char == None:
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line, 'delimitador', lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
                break
            elif char in delimitadores or char == '\n' or char.isspace():
                print("delimitador")
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'delimitador', lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1
            else:
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'delimitador', lexema)
                estado = 0
                listTokens.append(token)
                pos = pos-1

        elif estado in (20, 21):  # estados para a cadeia de catacteres
            # ler o proximo, e muda o estado e sai.
            char = readNext()
            print("\nESTADO", estado)
            print("lookhead: ", char)

            if(char == '"'):
                estado = 22
            elif(char == None):  # ERRO
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line, 'cadeira de caracteres mal formado', lexema)
                estado = 0
                listTokens.append(token)
                break
            elif(char == "\n"):
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'cadeira de caracteres mal formado', lexema)
                estado = 0
                listTokens.append(token)
                pos=pos-1
            else:
                estado = 21

        elif estado == 22:  # estado de cadeia de caracters
             # ler o proximo, e muda o estado e sai.
            char = readNext()
            print("\nESTADO 22")
            print("lookhead: ", char)
        
            if char == None:
                lexema = codigo[inicio_lexema:pos]
            else:
                lexema = codigo[inicio_lexema:pos-1]
                pos=pos-1;
            token = Token(count_line, 'cadeira de caracteres', lexema)
            estado = 0
            listTokens.append(token)
            
        elif estado == 23:  # estado para caracter
            # ler o proximo, e muda o estado e sai.
            char = readNext()
            print("\nESTADO 23")
            print("lookhead: ", char)

            if(char == "'"):
                estado = 25
            elif(char == None):  # ERRO
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line, 'caracter invalido', lexema)
                estado = 0
                listTokens.append(token)
                break
            elif(char == "\n"):
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'caracter invalido', lexema)
                estado = 0
                listTokens.append(token)
                pos=pos-1
            else:
                estado = 24  

        elif estado == 24:  
            # ler o proximo, e muda o estado e sai.
            char = readNext()
            print("\nESTADO 23")
            print("lookhead: ", char)

            if(char == "'"):
                estado = 25
            elif(char == None):  # ERRO
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line, 'caracter invalido', lexema)
                estado = 0
                listTokens.append(token)
                break
            elif(char == "\n"):
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'caracter invalido', lexema)
                estado = 0
                listTokens.append(token)
                pos=pos-1
            else:
                estado = 555 #AQUI ENTRA UM CASSO DE ERRO. EX: 'ab;
        
        elif estado == 25:
            # ler o proximo, e muda o estado e sai.
            char = readNext()
            print("\nESTADO ", estado)
            print("lookhead: ", char)

            if char == None:
                lexema = codigo[inicio_lexema:pos]
            else:
                lexema = codigo[inicio_lexema:pos-1]
                pos=pos-1;
            token = Token(count_line, 'caracter', lexema)
            estado = 0
            listTokens.append(token)
            
        elif estado == 555:
            char = readNext()
            print("\nESTADO DE ERRO ", estado)
            print("lookhead: ", char)

            if(char == None):  # ERRO
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line, 'caracter invalido', lexema)
                estado = 0
                listTokens.append(token)
                break
            elif(char == "\n" or char in delimitadores or char.isspace()):
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'caracter invalido', lexema)
                estado = 0
                listTokens.append(token)
                pos=pos-1
            elif(char == "'"):
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'caracter invalido', lexema)
                estado = 0
                listTokens.append(token)
                pos=pos-1
            else: 
                estado = 555

        elif estado == 556: ##ERRO DE INDETIFICADOR MAL FORMADO
            char = readNext()
            print("\nESTADO DE ERRO ", estado)
            print("lookhead: ", char)

            if(char == None):  # ERRO
                lexema = codigo[inicio_lexema:pos]
                token = Token(count_line, 'identificador mal formado', lexema)
                estado = 0
                listTokens.append(token)
                break
            elif(char == "\n" or char in delimitadores or char.isspace()):
                lexema = codigo[inicio_lexema:pos-1]
                token = Token(count_line, 'identificador mal formado', lexema)
                estado = 0
                listTokens.append(token)
                pos=pos-1
            else: 
                estado = 556


def readNext():
    global pos
    global file
    global codigo
    if pos == len(codigo):
        return None
    char = codigo[pos]
    pos += 1
    return char


# mensagem = input()
estado = 0
pos = 0
listTokens = []
Arraylist = []
count_line = 0

file = open("Exemplo1.txt", "r")
codigo = file.read()

listToken()
for token in listTokens:
    print(token.get())


file.close()
