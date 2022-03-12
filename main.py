# Programa para traducir instrucciones de MIPS y calcular el tiempo de ejecución
import traductor
from traductor import traducir

def main():
    file = open("mips.txt", "r") # Abrir archivo con instrucciones
    for i in file:
        traducir(i) 
        pass

    

    #print("{}".format(bin(4).replace("0b", "").zfill(5)))

main()