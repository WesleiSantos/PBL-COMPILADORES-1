from analizador_lexico import Analizador_lexico
from analisador_sintatico import Analisador_sintatico

if __name__ == '__main__':
    symbol_table = ("program", "var", "const","register","function", "procedure","return", "main", "if", "else", "while","read","write", "integer", "real","boolean","char", "string", "true", "false")
    analizador = Analizador_lexico(symbol_table)
    lista_tokens = analizador.readTokensFiles()
    for token in lista_tokens:
        print("token: ",token.getLexema())
    analizador_sin = Analisador_sintatico(lista_tokens)
    analizador_sin.readTokens()