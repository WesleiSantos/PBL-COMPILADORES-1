class arquiv:
    def read_lines(name_arq):
        arquiv = open(name_arq, 'r', encoding="utf8")
        lines = arquiv.readline()
        arquiv.close()
        return lines
