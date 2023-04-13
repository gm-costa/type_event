import re

somente_numeros = "\d+"
letras_minusculas = "[a-z]+"
letras_maiusculas = "[A-Z]+"

def verificar_forca_senha(texto):
    def is_coincidente(texto, comparacao):
        padrao = re.compile(comparacao)
        retorno = re.fullmatch(padrao, texto)
        return True if retorno else False

    if (len(texto) < 8) or (is_coincidente(texto, somente_numeros)) or (is_coincidente(texto, letras_minusculas)) or (is_coincidente(texto, letras_maiusculas)):
        msg = 'senha fraca'
    elif (is_coincidente(texto, '[a-z0-9]{8,20}')) or (is_coincidente(texto, '[A-Z0-9]{8,20}')):
        msg = 'senha média'
    elif (is_coincidente(texto, '[a-zA-Z0-9]{8,20}')) or (is_coincidente(texto, '[a-z0-9\W]{8,20}')):
        msg = 'senha boa'
    elif (is_coincidente(texto, '[\w\W]{8,20}')):
        msg = 'senha forte'
    else:
        msg = f'senha deve ter no máximo 20 caracteres'

    # print(f'{msg}, foi passado {len(texto)} caracteres')
    return f'({msg})'

if __name__ == '__main__':

    # verificar_forca_senha("fulano")
    # verificar_forca_senha("f123455")
    # verificar_forca_senha("fula12no")
    # verificar_forca_senha("fula12nof34")
    # verificar_forca_senha("fula12nofHgfda12Yz")
    # verificar_forca_senha("fula12nof/Hgfda12")
    # verificar_forca_senha("fula12nof*gfda12&a45")
    # verificar_forca_senha("fula12nof*gf7da12&a45")
    # verificar_forca_senha("fula12nof*gfda12&a45")
    # verificar_forca_senha("fula12noH*gfda12&a45")

    print(verificar_forca_senha("fula12noH*gfda12&a45"))
