class arquiv:
    def read_lines(name_arq):
        arquiv = open(name_arq, 'r', encoding="utf8")
        lines = arquiv.readlines()
        arquiv.close()
        return lines
