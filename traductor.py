from datos import functR, opI, opJ, registros
#Manejo de direcciones de instrucciones
instAdd = {} #diccionario de etiquetas con su direccion
instPoint = 0 #numero de la instruccion
baseAdd = 0
#Contador de ciclos
numCiclos = 0

# Imprimir binario
def pBin(n,p):
    if int(n) < 0:
        binary = str("{}".format(bin(int((1<<int(p)) - abs(int(n)))).replace("0b", "")))
    else:
        binary = str("{}".format(bin(int(n)).replace("0b", "").zfill(p)))
    return binary

def traducir(ins):
    global instPoint, numCiclos
    ins = ins.replace("(", " ").replace(")", " ")
    ins = ins.replace(",", " ").split() # ["add", "$s1", "$s2", "$s3"]
    print(ins)
    # Traducir tipo R
    if ins[0] in functR:
        op = "000000"
        funct = functR[ins[0]]
        # Caso sll y srl
        if ins[0] == "sll" or ins[0] == "srl":
            rs = "00000"
            rt = registros[ins[2]]
            rd = registros[ins[1]]
            shamt = ins[4]
        # Caso jr
        elif ins[0] == "jr":
            rs = registros[ins[1]]
            rt = rd = shamt = "00000"
        # Caso mfc0
        elif ins[0] == "mfc0":
            op = "010000"
            funct = "000000"
            rd = pBin(ins[1],5)
            rs = rt = "00000"
        # Caso mflo y mfhi
        elif ins[0] == "mflo" or ins[0] == "mfhi":
            rd = pBin(ins[1],5)
            rs = rt = "00000"
        else:
        # Traduccion estandar tipo R
            rd = registros[ins[1]]
            rs = registros[ins[2]]
            rt = registros[ins[3]]
            shamt = "00000"

        #Incrementar puntero de instrucciones
        instPoint+=4 
        #Contar ciclos
        if ins[0] == "lw": numCiclos += 5
        else: numCiclos += 4

        return op + " "+ rs +" "+ rt +" "+ rd +" "+ shamt +" "+ funct
    
    elif ins[0] in opI:
        # Traducción general tipo I
        op = opI[ins[0]]
        rt = registros[ins[1]]
        rs = registros[ins[3]]
        immediate = pBin(ins[2],16)
        # Caso lui
        if ins[0] == "lui":
            rs ="00000"
        # Caso lw, sw, lbu y sb
        elif ins[0] == "lw" or ins[0] == "sw" or ins[0] == "lbu" or ins[0] == "sb":
            immediate = pBin(ins[2],16)
            rs = registros[ins[3]]

        #Incrementar puntero de instrucciones
        instPoint+=4 
        #Contar ciclos
        if ins[0] == "beq" or ins[0] == "bne": numCiclos += 3
        else: numCiclos += 4

        return op +" "+ rs +" "+ rt +" "+ immediate
    
    elif ins[0] in opJ:
        # Traduccion general tipo J
        op = opJ[ins[0]]
        address = pBin(ins[1],26)

        #Incrementar puntero de instrucciones
        instPoint+=4 
        #Contar ciclos
        numCiclos += 3

        return op +" "+ address

    elif ins[0][-1] == ":": #Si es un label
        label = ins[0].replace(":", "")
        instAdd[label] = instPoint #Agrega esta etiqueta con su direccion al arreglo
        print(instAdd)
        return None
    else: #Si es comentario, linea en blanco, o instruccion no valida
        return None



print(traducir("lw $s1, 5($s2)"))
print(traducir("Main:"))

