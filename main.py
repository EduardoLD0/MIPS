# Programa para traducir instrucciones de MIPS y calcular el tiempo de ejecución
# Profe ponganos 5 por fa
import traductor
from traductor import traducir, contarCiclos

def main():
    traducir("mips.txt","out.txt")
    contarCiclos()
    print(traductor.numCiclos)
###FALTA
###Contar ciclos (stack pointer)
###Calculos de direccion de etiqueta segun funcion
###Agregar ra a etiquetas

main()