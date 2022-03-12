# Programa para traducir instrucciones de MIPS y calcular el tiempo de ejecución
import traductor
from traductor import traducir

def main():
    file = open("mips.txt", "r") # Abrir archivo con instrucciones
    for i in file:
        print(traducir(i)) 
        pass

###FALTA
###Contar ciclos (stack pointer)
###Interpretar si el immediate es decimal, hex o etiqueta
###Manejo de excepciones

main()