import re
from random import randint, choice


def gera_senha():
    string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/*-+.!@#$'
    tamanho = randint(2, 12)
    senha = ''
    for i in range(tamanho):
        senha += choice(string)
    return senha

def verificar_forca_senha(senha):
    t_senha = len(senha)

    tem_numero = True if re.search(re.compile('\d'), senha) else False 
    tem_minuscula = True if re.search(re.compile('[a-z]'), senha) else False
    tem_maiuscula = True if re.search(re.compile('[A-Z]'), senha) else False
    tem_char_especial = True if re.search(re.compile('\W'), senha) else False

    so_numeros = re.fullmatch(re.compile('\d+'), senha)
    so_minusculas = True if re.fullmatch(re.compile('[a-z]+'), senha) else False
    so_maiusculas = True if re.fullmatch(re.compile('[A-Z]+'), senha) else False

    letras_numeros = (tem_minuscula and tem_numero) or (tem_maiuscula and tem_numero)
    min_mai_numeros = tem_minuscula and tem_maiuscula and tem_numero
    min_num_especial = tem_minuscula and tem_numero and tem_char_especial
    mai_num_especial = tem_maiuscula and tem_numero and tem_char_especial
    complexa = tem_minuscula and tem_maiuscula and tem_numero and tem_char_especial

    s_fraca = (t_senha < 8) or (so_minusculas or so_maiusculas or so_numeros)
    s_media = (t_senha >= 8) and letras_numeros
    s_boa = (t_senha >= 8) and (min_mai_numeros or min_num_especial or mai_num_especial)
    s_forte = (t_senha >= 8) and complexa

    if s_forte:
        msg = 'forte'
    elif s_boa:
        msg = 'boa'
    elif s_media:
        msg = 'média'
    elif s_fraca:
        msg = 'fraca'

    return f"'{senha}' é {msg}  ==> tamanho: {t_senha}"

if __name__ == '__main__':

    for i in range(5):
        print(verificar_forca_senha(gera_senha()))
