# Programa para traducir instrucciones de MIPS y calcular el tiempo de ejecución
# Profe ponganos 5 por fa
import traductor
from traductor import traducir, contarCiclos

def main():
    traducir("mips.txt","out.txt")
    contarCiclos()
    print(str(traductor.numCiclos[0]) + " + " + str(traductor.numCiclos[1]) + "X")
###FALTA
###Contar ciclos (stack pointer)
###Calculos de direccion de etiqueta segun funcion
###Agregar ra a etiquetas

main()