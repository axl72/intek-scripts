def get_arguments(argumentos:list[str]):
    result = dict()
    for x in argumentos:
        if x[0] == '-':
            result[x[1:]]
        elif x[:2] == "--":
            result[]