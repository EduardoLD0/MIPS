# Programa para traducir instrucciones de MIPS y calcular el tiempo de ejecución
#from traductor import traducir as tr
baseAdd = 0

def main():
    file = open("mips.txt", "r") # Abrir archivo con instrucciones
    for i in file:
        tr(i)
        instPoint+=4 #Incrementar puntero de instrucciones
        pass

    

    print("{}".format(bin(4).replace("0b", "").zfill(5)))

main()