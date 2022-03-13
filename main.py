# Programa para traducir instrucciones de MIPS y calcular el tiempo de ejecución
import traductor
from traductor import traducir

def main():
    traducir("mips.txt","out.txt")

###FALTA
###Contar ciclos (stack pointer)
###Calculos de direccion de etiqueta segun funcion

main()