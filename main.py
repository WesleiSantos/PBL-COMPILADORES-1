from analizador_lexico import Analizador_lexico

if __name__ == '__main__':
    symbol_table = ("program", "var", "const","register","function", "procedure","return", "main", "if", "else", "while","read","write", "integer", "real","boolean","char", "string", "true", "false","for")
    analizador = Analizador_lexico(symbol_table)
    analizador.readTokensFiles()