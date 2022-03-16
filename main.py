# Programa para traducir instrucciones de MIPS y calcular el tiempo de ejecución
# Profe ponganos 5 por fa
import traductor
from traductor import traducir, contarCiclos

def main():
    traducir("mips.txt","out.txt")
    contarCiclos()
    f = int(input("Ingrese la frecuencia en Ghz: "))
    print("Numero de ciclos: " + str(traductor.numCiclos[0]) + " + " + str(traductor.numCiclos[1]) + "X")
    print("Tiempo: " + str(traductor.numCiclos[0] / f) + " + " + str(traductor.numCiclos[1] / f) + "X" + " ns")

main()