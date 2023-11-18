import re

NUM_OR_DOT_REGEX = re.compile(r'^[0-9.]$')

#verifca se é intervalo de 0 a 9 ou .
def isNumOrDot(string: str):
    return bool(NUM_OR_DOT_REGEX.search(string))

# verifica se está vazio
def isEmpty(string: str):
    return len(string) == 0

# verifica se o número é válido
def isValidNumber(string: str):
    valid = False
    try:
        float(string)
        valid = True
    except ValueError:
        valid = False
    return valid