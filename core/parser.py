import glob
import re
import os

def syscall_parser(sample_name):
    full_syscalls = {}

    strace_outputs = glob.glob(sample_name + "/*")

    for file in strace_outputs:
        if re.search('\.[0-9]+', file) is not None:
            with open(file, "r") as f:
                filename = os.path.basename(file)
                pid = filename.split(".")[1]
                full_syscalls[pid] = {}

                syscalls, params, results = single_syscall_parser(f.readlines())
                full_syscalls[pid]['syscalls'] = syscalls
                full_syscalls[pid]['params'] = params
                full_syscalls[pid]['results'] = results

    return full_syscalls


# Parsea una entrada unica de syscall
def single_syscall_parser(lines):
    lines = list(map(lambda x: re.sub("\s+", "", x), lines))  # retiramos caracteres especiales y espacios [ \t\n\r\f\v]

    syscalls = list(map(lambda x: x.split("(")[0], lines))  # Almacenamos las syscalls en una lista

    res = list(map(lambda x: x.split("=")[-1] if len(x.split("=")) > 1 else "",
                   lines))  # Almacenamos los resultados asociados a esas sycalls

    params = list(map(lambda x, y, z: x[len(y) + 1:-(len(z) + 2)], lines, syscalls,
                      res))  # Obtenemos los parámetros en bruto (sin splitear)

    refinedparams = list(map(lambda x: re.split(
        ",(?=(?:[^\[\]]|\[[^\[\]]*\])*$)(?=(?:[^\{\}]|\{[^\{\}]*\})*$)(?=(?:[^\"]|\"[^\"]*\")*$)(?=(?:[^']|'[^']*')*$)|(?<=[\'\"\]\}]),(?=[\{\[\'\!])",
        x), params))

    # obtenemos los parámetros refinados, la expresión regular obtiene todas las comas que no estén dentro de un parámetro válido.
    # Por ejemplo  en la cadena:("a","v","s",["a","v"],"a,s,f") solo nos interesan las comas 1,2,3 y 5, las otras forman parte de un parámetro anidado

    #finallist = list(map(lambda x, y, z: {"syscall": x, "params": y, "res": z}, syscalls, refinedparams,
    #                     res))  # obtenemos una lista de diccionarios con cada syscall

    return syscalls, params, res
