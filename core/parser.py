import glob
import re
def main():
    pass
def syscall_parser(ruta):
    full_syscalls = []
    rutas=glob.glob(ruta+"/*")
    for file in rutas:
        with open(file,"r") as f:
            full_syscalls.append(single_syscall_parser(f.readlines()))
    return full_syscalls


# Parsea una entrada unica de syscall
def single_syscall_parser(lines):
    lines = list(map(lambda x: re.sub("\s+", "", x), lines))  # retiramos caracteres especiales y espacios [ \t\n\r\f\v]
    syscalls = list(map(lambda x: x.split("(")[0], lines)) # Almacenamos las syscalls en una lista
    res = list(map(lambda x: x.split("=")[-1] if len(x.split("=")) > 1 else "", lines)) # Almacenamos los resultados asociados a esas sycalls
    params = list(map(lambda x, y, z: x[len(y) + 1:-(len(z) + 2)], lines, syscalls, res)) # Obtenemos los parámetros en bruto (sin splitear)
    refinedparams = list(map(lambda x: re.split(",(?=(?:[^\[\]]|\[[^\[\]]*\])*$)(?=(?:[^\{\}]|\{[^\{\}]*\})*$)(?=(?:[^\"]|\"[^\"]*\")*$)(?=(?:[^']|'[^']*')*$)|(?<=[\'\"\]\}]),(?=[\{\[\'\!])",x), params))
    # obtenemos los parámetros refinados, la expresión regular obtiene todas las comas que no estén dentro de un parámetro válido.
    # Por ejemplo  en la cadena:("a","v","s",["a","v"],"a,s,f") solo nos interesan las comas 1,2,3 y 5, las otras forman parte de un parámetro anidado

    finallist = list(map(lambda x, y, z: {"syscall": x, "params": y, "res": z}, syscalls, refinedparams, res)) # obtenemos una lista de diccionarios con cada syscall

    return finallist




if __name__ == '__main__':
    main()