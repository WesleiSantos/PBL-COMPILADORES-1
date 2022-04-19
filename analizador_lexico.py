from token import Token

class analizador_lexico:
    def __init__(self) -> None:
        self.estado = 0
        self.pos = 0
        self.Arraylist = []
        self.count_line = 1
        self.codigo = ''
        self.reservation_words = ("program", "var", "const","register","function", "procedure","return", "main", "if", "else", "while","read","write", "integer", "real","boolean","char", "string", "true", "false","for")

    # Ler arquivo de texto com o código a ser analizado
    def readArchive(self,path):
        file = open(path, "r")
        self.codigo = file.read()
        file.close()

    # retorna true se o caracter é sem acento
    def semAcento(self,char):
        if char in ('á', 'à', 'â', 'ã', 'ç', 'í', 'ì', 'î', 'ñ', 'û', 'ú', 'ù', 'ó', 'ô', 'õ'):
            print("Caracter com acento!")
            return False
        elif char in ('á'.upper(), 'à'.upper(), 'â'.upper(), 'ã'.upper(), 'ç'.upper(), 'ì'.upper(),
                      'í'.upper(), 'î'.upper(), 'û'.upper(), 'ú'.upper(), 'ù'.upper(), 'ó'.upper(), 'ô'.upper(), 'õ'.upper()):
            print("Caracter com acento!")
            return False
        return True

    #lista tokens
    def listToken(self):
        inicio_lexema = 0
        caracter_anterior = ''
        delimitadores = ('.', ',', ':', ';', '(', ')', '[', ']', '{', '}')
        listTokens = []
        while True:
            if self.estado == 0:  # estado inicial
                # ler o proximo, e muda o estado e sai.
                print("\nESTADO 0")
                char = self.readNext()
                print("lookhead: ", char)

                if char == None:
                    break

                if(char.isspace()):
                    print("É UM ESPAÇO")
                    self.estado = 0
                    inicio_lexema = self.pos-1

                elif(char.isnumeric()):
                    print("É UM DIGITO")
                    self.estado = 2
                    inicio_lexema = self.pos-1

                # é uma letra, exceto ç - falta colocar exececoes nas letras com acentos.
                elif char.isalpha() and self.semAcento(char):
                    print("É UMA LETRA")
                    self.estado = 1

                    # como a posicao foi para 1 precisa-se usar a posicao anterior caso forme um token
                    inicio_lexema = self.pos-1
                elif char == '+':
                    print("É o '+' ")
                    caracter_anterior = char
                    self.estado = 5
                    inicio_lexema = self.pos-1

                elif char == '-':
                    print("É o '-' ")
                    caracter_anterior = char
                    self.estado = 6
                    inicio_lexema = self.pos-1

                elif char in ('/', '*'):
                    print("É o Veio", char)
                    self.estado = 7
                    caracter_anterior = char
                    inicio_lexema = self.pos-1  # aqui poderíamos fechar o token , pós nao pode vim outra / ou *

                elif char in ('=', '<', '>'):
                    print("É o ", char)
                    self.estado = 8
                    caracter_anterior = char
                    inicio_lexema = self.pos-1

                elif char == '!':
                    print("É o ", char)
                    self.estado = 9
                    caracter_anterior = char
                    inicio_lexema = self.pos-1

                elif char == '&':
                    print("É o ", char)
                    caracter_anterior = char
                    self.estado = 11
                    inicio_lexema = self.pos-1

                elif char == '|':
                    print("É o ", char)
                    caracter_anterior = char
                    self.estado = 12
                    inicio_lexema = self.pos-1

                elif char == '%':
                    print("É o ", char)
                    self.estado = 14
                    inicio_lexema = self.pos-1

                elif(char in delimitadores):  # delimitadores
                    print("É o ", char)
                    self.estado = 19
                    inicio_lexema = self.pos-1

                elif char == "\"":  # CADEIRA DE CARACTEREs
                    print("É o ", char)
                    self.estado = 20
                    inicio_lexema = self.pos-1

                elif char == "'":  # caracter
                    print("É o ", char)
                    self.estado = 23
                    inicio_lexema = self.pos-1

                elif(char == '\n'):
                    print("FIM DE LINHA")
                    self.count_line += 1
                    self.estado = 0
                    inicio_lexema = self.pos-1
                else:
                    print("SIMBOLO INVÁLIDO")
                    inicio_lexema = self.pos-1
                    self.pos = self.pos-1 
                    self.estado = 559

            elif self.estado == 1:  # estado de identificador
                # ler o proximo, e muda o estado e sai.
                char = self.readNext()
                print("\nESTADO 1")
                print("lookhead: ", char)

                if char == None:
                    print("none")
                    lexema = self.codigo[inicio_lexema:self.pos]
                    if(lexema in self.reservation_words):
                        token = Token(self.count_line, 'palavra reservada', lexema)
                    else:
                        token = Token(self.count_line, 'identificador', lexema)
                    self.estado = 0
                    listTokens.append(token)
                    break
                elif(char.isspace() or char in delimitadores or char == "\n"):
                    print("identificador")
                    print("SALVA TOKEN")
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    if(lexema in self.reservation_words):
                        token = Token(self.count_line, 'palavra reservada', lexema)
                    else:
                        token = Token(self.count_line, 'identificador', lexema)
                    listTokens.append(token)
                    self.estado = 0
                    self.pos=self.pos-1
                elif char in ['+','-','/', '*','=', '<', '>','!','&','|','%',"\"","'"]:
                    print("identificador")
                    print("SALVA TOKEN")
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    if(lexema in self.reservation_words):
                        token = Token(self.count_line, 'palavra reservada', lexema)
                    else:
                        token = Token(self.count_line, 'identificador', lexema)
                    listTokens.append(token)
                    self.estado = 0
                    self.pos=self.pos-1
                elif ((char.isalpha() and self.semAcento(char)) or char.isnumeric() or char == "_"):
                    print("É UMA LETRA")
                    self.estado = 1
                else:
                    self.estado = 556

            elif self.estado == 2:  # estado de digito

                # ler o proximo, e muda o estado e sai.
                char = self.readNext()
                print("\nESTADO 2")
                print("lookhead: ", char)

                if char == None:
                    print("none")
                    lexema = self.codigo[inicio_lexema:self.pos]
                    token = Token(self.count_line, 'inteiro', lexema)
                    self.estado = 0
                    listTokens.append(token)
                    self.pos = self.pos-1
                    break
                
                elif(char == '.'):  # ou ter um limitador(float)
                    print("É DELIMITADOR . ")
                    self.estado = 3

                elif(char.isspace() or char in delimitadores):
                    print("É DELIMITADOR")
                    print("SALVA TOKEN")
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'inteiro', lexema)
                    listTokens.append(token)
                    self.estado = 0
                    self.pos = self.pos-1

                elif (char.isnumeric()):  # depois de um dígito pode ter outro
                    print("É UM DIGITO")
                    self.estado = 2
                    #inicio_lexema = self.pos-1

                elif(char == '\n'):
                    print("FIM DE LINHA")
                    self.estado = 0

                else:
                    print("É OUTRO CARACTER")
                    print("SALVA TOKEN")
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'inteiro', lexema)
                    listTokens.append(token)
                    self.estado = 0
                    self.pos = self.pos-1

            elif self.estado == 3:  # estado do ponto "flutuante"
                char = self.readNext()
                print("\nESTADO 3")
                print("lookhead: ", char)

                if char.isnumeric():  # depois de um . tem um digito
                    print("É UM DIGITO")
                    self.estado = 4
                else:
                    self.pos = self.pos-1
                    self.estado = 560

            elif self.estado == 4:  # estado dos decimais
                char = self.readNext()
                print("\nESTADO 4")
                print("lookhead: ", char)

                if char == None:
                    print("none")
                    lexema = self.codigo[inicio_lexema:self.pos]
                    token = Token(self.count_line, 'ponto_flutuante', lexema)
                    self.estado = 0
                    listTokens.append(token)
                    self.pos = self.pos-1
                    break

                elif(char.isnumeric()):  # depois de um . tem um digito
                    print("É UM DIGITO")
                    self.estado = 4

                elif(char.isspace() or char in delimitadores):
                    print("É DELIMITADOR")
                    print("SALVA TOKEN")
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'ponto_flutuante', lexema)
                    self.estado = 0
                    self.pos = self.pos-1
                    listTokens.append(token)
                elif(char == '\n'):
                    print("FIM DE LINHA")
                    self.estado = 0
                else:
                    print("É OUTRO CARACTER")
                    print("SALVA TOKEN")
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'ponto_flutuante', lexema)
                    self.estado = 0
                    listTokens.append(token)
                    self.pos = self.pos-1

            elif self.estado == 5:  # estado sinal de adição
                # ler o proximo, e muda o estado e sai.
                char = self.readNext()
                print("\nESTADO 5")
                print("lookhead: ", char)

                if char == None:
                    print("none")
                    lexema = self.codigo[inicio_lexema:self.pos]
                    token = Token(self.count_line, 'delimitador', lexema)
                    self.estado = 0
                    listTokens.append(token)
                    self.pos = self.pos-1
                    break

                elif(char.isspace() or char in delimitadores):
                    print("É DELIMITADOR")
                    print("SALVA TOKEN")
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'operador_adicao', lexema)
                    self.estado = 0
                    self.pos = self.pos-1
                    listTokens.append(token)

                elif char == '+':
                    print("É o '+' ")
                    self.estado = 7
                elif(char == '\n'):
                    print("FIM DE LINHA")
                    self.estado = 0
                else:
                    print("É OUTRO CARACTER")
                    print("SALVA TOKEN")
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'operador_adicao', lexema)
                    self.estado = 0
                    listTokens.append(token)
                    self.pos = self.pos-1

            elif self.estado == 6:  # estado sinal de subtração
                # ler o proximo, e muda o estado e sai.
                char = self.readNext()
                print("\nESTADO 6")
                print("lookhead: ", char)

                if char == None:
                    print("none")
                    lexema = self.codigo[inicio_lexema:self.pos]
                    token = Token(self.count_line, 'delimitador', lexema)
                    self.estado = 0
                    listTokens.append(token)
                    self.pos = self.pos-1
                    break

                elif(char.isspace() or char in delimitadores):
                    print("É DELIMITADOR")
                    print("SALVA TOKEN")
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'operador_subtração', lexema)
                    self.estado = 0
                    self.pos = self.pos-1
                    listTokens.append(token)

                elif char == '-':
                    print("É o '-' ")
                    self.estado = 7

                elif(char == '\n'):
                    print("FIM DE LINHA")
                    self.estado = 0
                else:
                    print("SALVA TOKEN")
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'operador_subtração', lexema)
                    self.estado = 0
                    self.pos = self.pos-1
                    listTokens.append(token)

            elif self.estado == 7:  # estado de incremento, deremento, multiplicação ou divisão
                char = self.readNext()
                print("\nESTADO 7")
                print("lookhead: ", char)
                print(caracter_anterior)
                if char == None:
                    print("none")
                    lexema = self.codigo[inicio_lexema:self.pos]
                    token = Token(self.count_line, 'delimitador', lexema)
                    self.estado = 0
                    listTokens.append(token)
                    self.pos = self.pos-1
                    break
                elif(caracter_anterior == '-'):
                    print("operador de subtração")
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'operador_decremento', lexema)
                    self.estado = 0
                    self.pos = self.pos-1
                    listTokens.append(token)
                    caracter_anterior=''
                elif(caracter_anterior == '+'):
                    print("operador de adicao")
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'operador_incremento', lexema)
                    self.estado = 0
                    self.pos = self.pos-1
                    listTokens.append(token)
                    caracter_anterior=''
                elif(caracter_anterior == '*'):
                    print("operador de multiplicação")
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'operador_multiplicacao', lexema)
                    self.estado = 0
                    self.pos = self.pos-1
                    listTokens.append(token)
                    caracter_anterior=''
                elif(caracter_anterior == '/' and char == '#'):
                    self.estado = 15
                elif(caracter_anterior == '/'):
                    print("operador de divisão")
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'operador_divisao', lexema)
                    self.estado = 0
                    self.pos = self.pos-1
                    caracter_anterior = ''
                    listTokens.append(token)
                elif(char == '\n'):
                    print("FIM DE LINHA")
                    self.estado = 0

            elif self.estado == 8:  # estado de igual, maior ou menor
                # ler o proximo, e muda o estado e sai.
                char = self.readNext()
                print("\nESTADO 8")
                print("lookhead: ", char)
                if char == None:
                    print("É um operador relacional")
                    lexema = self.codigo[inicio_lexema:self.pos]
                    if(caracter_anterior == "="):
                        token = Token(self.count_line, 'operador_atribuicao', lexema)
                    elif(caracter_anterior == "<"):
                        token = Token(self.count_line, 'operador_menorque', lexema)
                    elif(caracter_anterior == ">"):
                        token = Token(self.count_line, 'operador_maiorque', lexema)
                    listTokens.append(token)
                    break
                elif char.isspace() or char in delimitadores:
                    print("É um operador relacional")
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    if(caracter_anterior == "="):
                        token = Token(self.count_line, 'operador_atribuicao', lexema)
                    elif(caracter_anterior == "<"):
                        token = Token(self.count_line, 'operador_menorque', lexema)
                    elif(caracter_anterior == ">"):
                        token = Token(self.count_line, 'operador_maiorque', lexema)
                    self.estado = 0
                    self.pos = self.pos-1
                    caracter_anterior = ''
                    listTokens.append(token)
                elif char == '=':
                    print("É o ", char)
                    self.estado = 10  # poderíamos fechar o lexama aqui? nem precisaria do estado 10
                elif(char == '\n'):
                    print("FIM DE LINHA")
                    self.estado = 0
                else:
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    if(caracter_anterior=="="):
                        token = Token(self.count_line,'operador_atribuicao',lexema)
                    elif(caracter_anterior=="<"):
                        token = Token(self.count_line,'operador_menorque',lexema)
                    elif(caracter_anterior==">"):
                        token = Token(self.count_line,'operador_maiorque',lexema)
                    self.estado = 0
                    listTokens.append(token)
                    self.pos = self.pos-1

            elif self.estado == 9:  # estado de sinal de exclamação
                # ler o proximo, e muda o estado e sai.
                char = self.readNext()
                print("\nESTADO 9")
                print("lookhead: ", char)
                if char == None:
                    lexema = self.codigo[inicio_lexema:self.pos]
                    token = Token(self.count_line,'operador_de_negacao',lexema)
                    listTokens.append(token)
                    break
                elif char == '=':
                    print("É o ", char)
                    estado = 10  # poderíamos fechar o lexama aqui? nem precisaria do estado 10
                elif char in delimitadores or char.isspace():
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line,'operador_de_negacao',lexema)
                    listTokens.append(token)
                    self.pos = self.pos-1
                    caracter_anterior = ''
                    self.estado = 0
                else:
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line,'operador_de_negacao',lexema)
                    listTokens.append(token)
                    self.pos = self.pos-1
                    caracter_anterior = ''
                    self.estado = 0

            elif self.estado == 10:  # estado de igual, maior ou menor
                # ler o proximo, e muda o estado e sai.
                char = self.readNext()
                print("\nESTADO 10")
                print("lookhead: ", char)
                print("Caracter anteriror", caracter_anterior)
                if(caracter_anterior == "="):
                        print("É o ", char)
                        lexema = self.codigo[inicio_lexema:self.pos-1]
                        self.estado = 0
                        token = Token(self.count_line,'operador_igualdade',lexema)
                        listTokens.append(token)
                        self.pos = self.pos-1
                        caracter_anterior = ''
                elif(caracter_anterior=="<"):
                        print("É o ", char)
                        lexema = self.codigo[inicio_lexema:self.pos-1]
                        self.estado = 0
                        token = Token(self.count_line,'operador_menor_igual',lexema)
                        listTokens.append(token)
                        self.pos = self.pos-1
                        caracter_anterior = ''
                elif(caracter_anterior==">"):
                        print("É o ", char)
                        lexema = self.codigo[inicio_lexema:self.pos-1]
                        self.estado = 0
                        token = Token(self.count_line,'operador_maior_igual',lexema)
                        listTokens.append(token)
                        self.pos = self.pos-1
                        caracter_anterior = ''
                elif(caracter_anterior=="!"):
                        print("É o ", char)
                        lexema = self.codigo[inicio_lexema:self.pos-1]
                        self.estado = 0
                        token = Token(self.count_line,'operador_diferenca',lexema)
                        listTokens.append(token)
                        self.pos = self.pos-1
                        caracter_anterior = ''
                elif(char == '\n'):
                    print("FIM DE LINHA")
                    self.estado = 0
                elif(char.isspace() or char in delimitadores):
                    print("É DELIMITADOR")
                    print("SALVA TOKEN")
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    self.estado = 0
                    self.pos = self.pos-1
                    caracter_anterior=''
                    listTokens.append(token)
                else:
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'operador_logico', lexema)
                    self.estado = 0
                    listTokens.append(token)
                    self.pos = self.pos-1
                if char == None:
                    break

            elif self.estado == 11:  # estado sinal de &
                # ler o proximo, e muda o estado e sai.
                char = self.readNext()
                print("\nESTADO 11")
                print("lookhead: ", char)

                if char == None:
                    self.estado = 561
                elif char == '&':
                    print("É o", char)
                    self.estado = 13
                else:
                    self.estado = 561
                    self.pos = self.pos-1

            elif self.estado == 12:  # estado sinal de |
                # ler o proximo, e muda o estado e sai.
                char = self.readNext()
                print("\nESTADO 12")
                print("lookhead: ", char)

                if char == None:
                    self.estado = 561
                    self.pos = self.pos-1
                elif char == '|':
                    print("É o", char)
                    self.estado = 13
                else:
                    self.estado = 561
                    self.pos = self.pos-1

            elif self.estado == 13:  # estado de operadores relacionais
                char = self.readNext()
                print("\nESTADO ", self.estado)
                # aqui tem-se um erro - operador lógico incompleto.
                print(caracter_anterior)
                if char == None :
                    lexema = self.codigo[inicio_lexema:self.pos]
                    if caracter_anterior == '&':
                        print("operador lógico E")
                        token = Token(self.count_line, 'operador_logico_and', lexema)
                    elif caracter_anterior == '|':
                        print("operador lógico OU")
                        lexema = self.codigo[inicio_lexema:self.pos]
                        token = Token(self.count_line, 'operador_logico_or', lexema)
                    listTokens.append(token)
                    break
                if caracter_anterior == '&':
                    print("operador lógico E")
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'operador_logico_and', lexema)
                    self.estado = 0
                    listTokens.append(token)
                    self.pos = self.pos-1
                elif caracter_anterior == '|':
                    print("operador lógico OU")
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'operador_logico_or', lexema)
                    self.estado = 0
                    listTokens.append(token)
                    self.pos = self.pos-1
                elif char == '&' and caracter_anterior == '|':
                    print("&| error")
                    # ERROR
                elif char == '|' and caracter_anterior == '&':
                    print("|& error")
                elif char in delimitadores or char.isspace():
                    print("delimitador")
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'operador_relacional', lexema)
                    self.estado = 0
                    listTokens.append(token)
                    self.pos = self.pos-1
                else:
                    print ("outher", char)

            elif self.estado == 14:  # Comentário de linha
                char = self.readNext()
                print("\nESTADO ", self.estado)
                # aqui tem-se um erro - operador lógico incompleto.
                if char == None :
                    lexema = self.codigo[inicio_lexema:self.pos]
                    token = Token(self.count_line, 'comentario_de_linha', lexema)
                    listTokens.append(token)
                    break
                elif char == '\n':
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'comentario_de_linha', lexema)
                    self.estado = 0
                    listTokens.append(token)
                    self.pos = self.pos-1
                else:
                    self.estado=14

            elif self.estado == 15:  # Comentário de bloco #
                char = self.readNext()
                print("\nESTADO ", self.estado)
                # aqui tem-se um erro - operador lógico incompleto.
                if char == None :
                    self.estado = 558
                elif char == '#':
                    self.estado = 16
                else:
                    self.estado=15

            elif self.estado == 16:  # Comentário de bloco #
                char = self.readNext()
                print("\nESTADO ", self.estado)
                # aqui tem-se um erro - operador lógico incompleto.
                if char == None :
                    self.estado = 558
                elif char == '/':
                    self.estado=17
                else:
                    self.estado=15

            elif self.estado == 17:  # Comentário de bloco
                char = self.readNext()
                print("\nESTADO ", self.estado)
                # aqui tem-se um erro - operador lógico incompleto.
                if char == None :
                    lexema = self.codigo[inicio_lexema:self.pos]
                    token = Token(self.count_line, 'comentario_de_bloco', lexema)
                    listTokens.append(token)
                    break
                else:
                    lexema = self.codigo[inicio_lexema:self.pos]
                    token = Token(self.count_line, 'comentario_de_bloco', lexema)
                    listTokens.append(token)
                    self.estado = 0

            elif self.estado == 19:  # estado de delimitadores
                # ler o proximo, e muda o estado e sai.
                char = self.readNext()
                print("\nESTADO 19")
                print("lookhead: ", char)
                if char == None:
                    lexema = self.codigo[inicio_lexema:self.pos]
                    token = Token(self.count_line, 'delimitador', lexema)
                    estado = 0
                    listTokens.append(token)
                    self.pos = self.pos-1
                    break
                elif char in delimitadores or char == '\n' or char.isspace():
                    print("delimitador")
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'delimitador', lexema)
                    self.estado = 0
                    listTokens.append(token)
                    self.pos = self.pos-1
                else:
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'delimitador', lexema)
                    self.estado = 0
                    listTokens.append(token)
                    self.pos = self.pos-1

            elif self.estado in (20, 21):  # estados para a cadeia de catacteres
                # ler o proximo, e muda o estado e sai.
                char = self.readNext()
                print("\nESTADO", self.estado)
                print("lookhead: ", char)

                if(char == '"'):
                    self.estado = 22
                elif(char == None):  # ERRO
                    lexema = self.codigo[inicio_lexema:self.pos]
                    token = Token(self.count_line, 'cadeira de caracteres mal formado', lexema)
                    self.estado = 0
                    listTokens.append(token)
                    break
                elif(char == "\n"):
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'cadeira de caracteres mal formado', lexema)
                    self.estado = 0
                    listTokens.append(token)
                    self.pos=self.pos-1
                else:
                    self.estado = 21

            elif self.estado == 22:  # estado de cadeia de caracters
                 # ler o proximo, e muda o estado e sai.
                char = self.readNext()
                print("\nESTADO 22")
                print("lookhead: ", char)

                if char == None:
                    lexema = self.codigo[inicio_lexema:self.pos]
                else:
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    self.pos=self.pos-1;
                token = Token(self.count_line, 'cadeira de caracteres', lexema)
                self.estado = 0
                listTokens.append(token)

            elif self.estado == 23:  # estado para caracter
                # ler o proximo, e muda o estado e sai.
                char = self.readNext()
                print("\nESTADO 23")
                print("lookhead: ", char)

                if(char == "'"):
                    self.estado = 25
                elif(char == None):  # ERRO
                    lexema = self.codigo[inicio_lexema:self.pos]
                    token = Token(self.count_line, 'caracter_mal_formado', lexema)
                    self.estado = 0
                    listTokens.append(token)
                    break
                elif(char == "\n"):
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'caracter_mal_formado', lexema)
                    self.estado = 0
                    listTokens.append(token)
                    self.pos=self.pos-1
                else:
                    self.estado = 24  

            elif self.estado == 24:  # estado para caracter
                # ler o proximo, e muda o estado e sai.
                char = self.readNext()
                print("\nESTADO 23")
                print("lookhead: ", char)

                if(char == "'"):
                    self.estado = 25
                else:
                    self.pos = self.pos-1
                    self.estado = 555 #AQUI ENTRA UM CASSO DE ERRO. EX: 'ab;

            elif self.estado == 25: # estado para caracter
                # ler o proximo, e muda o estado e sai.
                char = self.readNext()
                print("\nESTADO ", self.estado)
                print("lookhead: ", char)

                if char == None:
                    lexema = self.codigo[inicio_lexema:self.pos]
                else:
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    self.pos=self.pos-1;
                token = Token(self.count_line, 'caracter', lexema)
                self.estado = 0
                listTokens.append(token)

            elif self.estado == 555: ##ERRO DE CARACTER MAL FORMADO
                char = self.readNext()
                print("\nESTADO DE ERRO ", self.estado)
                print("lookhead: ", char)

                if(char == None):  # ERRO
                    lexema = self.codigo[inicio_lexema:self.pos]
                    token = Token(self.count_line, 'caracter_mal_formado', lexema)
                    listTokens.append(token)
                    break
                elif char == '\n' or char in delimitadores or char.isspace():
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'caracter_mal_formado', lexema)
                    self.estado = 0
                    listTokens.append(token)
                    self.pos=self.pos-1
                else:
                    self.estado = 555

            elif self.estado == 556: ##ERRO DE INDETIFICADOR MAL FORMADO
                char = self.readNext()
                print("\nESTADO DE ERRO ", self.estado)
                print("lookhead: ", char)

                if(char == None):  # ERRO
                    lexema = self.codigo[inicio_lexema:self.pos]
                    token = Token(self.count_line, 'identificador_mal_formado', lexema)
                    self.estado = 0
                    listTokens.append(token)
                    break
                elif ((char.isalpha() and self.semAcento(char)) or char.isnumeric() or char == "_"):
                    print("É UMA LETRA")
                    self.estado = 556
                elif char in ['+','-','/', '*','=', '<', '>','!','&','|','%',"\"","'",'\n'] or char in delimitadores or char.isspace():
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'identificador_mal_formado', lexema)
                    self.estado = 0
                    listTokens.append(token)
                    self.pos=self.pos-1
                else: 
                    self.estado = 556
            
            elif self.estado == 557: ##ERRO DE NÚMERO MAL FORMADO
                print("\nESTADO DE ERRO ", self.estado)
                print("lookhead: ", char)

                if char in ['+','-','/', '*','=', '<', '>','!','&','|','%',"\"","'",'\n'] or char in delimitadores or char.isspace():
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'numero_mal_formado', lexema)
                    self.estado = 0
                    listTokens.append(token)
                    self.pos=self.pos-1
                else:
                    self.estado = 557   
                if(char == None):
                    break
            
            elif self.estado == 558: ##COMENTÁRIO MAL FORMADO
                print("\nESTADO DE ERRO ", self.estado)
                print("lookhead: ", char)
                lexema = self.codigo[inicio_lexema:self.pos]
                token = Token(self.count_line, 'comentario_de_bloco_mal_formado', lexema)
                self.estado = 0
                listTokens.append(token)
                break
                
            elif self.estado == 559: ##ERRO SIMBOLO INVÁLIDO
                char = self.readNext()
                print("\nESTADO DE ERRO ", self.estado)
                print("lookhead: ", char)
                
                if(char == None):
                    lexema = self.codigo[inicio_lexema:self.pos]
                    token = Token(self.count_line, 'simbolo_invalido', lexema)
                    listTokens.append(token)
                    break
                if char == '\n' or char in delimitadores or char.isspace():
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'simbolo_invalido', lexema)
                    self.estado = 0
                    listTokens.append(token)
                    self.pos=self.pos-1
                else:
                    self.estado = 559

            elif self.estado == 560: ##ERRO DE PONTO FLUTUANTE MAL FORMADO
                char = self.readNext()
                print("\nESTADO DE ERRO ", self.estado)
                print("lookhead: ", char)
                if(char == None):
                    lexema = self.codigo[inicio_lexema:self.pos]
                    token = Token(self.count_line, 'ponto_flutuante_mal_formado', lexema)
                    listTokens.append(token)
                    break
                if char in ['+','-','/', '*','=', '<', '>','!','&','|','%',"\"","'",'\n'] or char in delimitadores or char.isspace():
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'ponto_flutuante_mal_formado', lexema)
                    self.estado = 0
                    listTokens.append(token)
                    self.pos=self.pos-1
                else:
                    self.estado = 560

            elif self.estado == 561: ##ERRO DE OPERADOR LÓGICO FLUTUANTE MAL FORMADO
                char = self.readNext()
                print("\nESTADO DE ERRO ", self.estado)
                print("lookhead: ", char)
                if(char == None):
                    lexema = self.codigo[inicio_lexema:self.pos]
                    token = Token(self.count_line, 'operador_logico_mal_formado', lexema)
                    listTokens.append(token)
                    break
                if char =='\n' or char in delimitadores or char.isspace():
                    lexema = self.codigo[inicio_lexema:self.pos-1]
                    token = Token(self.count_line, 'operador_logico_mal_formado', lexema)
                    listTokens.append(token)
                    self.estado = 0
                    self.pos=self.pos-1
                else:
                    self.estado = 561   

        return listTokens

    #ler o próximo caracter
    def readNext(self):
        if self.pos == len(self.codigo):
            return None
        char = self.codigo[self.pos]
        self.pos += 1
        return char

if __name__ == '__main__':
    analizador = analizador_lexico()
    analizador.readArchive("casos_de_erro/digito.txt")
    tokens = analizador.listToken()
    for token in tokens:
        print(token.get())


