from datos import functR, opI, opJ, registros

#string array
traduccion = []

#Manejo de direcciones de instrucciones
labelPending = []
labelAdd = {} #diccionario de etiquetas con su direccion
instPoint = 0 #numero de la instruccion
baseAdd = "00400000" #direccion base instrucciones

#Contador de ciclos
numCiclos = 0

# Imprimir binario
def pBin(n,p):
    if int(n) < 0:
        binary = str("{}".format(bin(int((1<<int(p)) - abs(int(n)))).replace("0b", "")))
    else:
        binary = str("{}".format(bin(int(n)).replace("0b", "").zfill(p)))
    return binary

# Determina si el immediate de una tipo I es label, direccion hex o numero en binario
def getImm(immediate, p):
    if immediate.isdecimal():
        #print("decimal")
        ans = pBin(immediate,p)
    elif immediate[:2] == "0x":
        #print("hex") 
        ans = bin(int(immediate, 16))[2:].zfill(p)
    else:
        #Manejo de etiquetas
        if immediate in labelAdd: #Si ya se guardo la direccion de la etiqueta
            print("label "+str(labelAdd[immediate]*4))
            add = int(baseAdd, 16) + int(str(labelAdd[immediate]*4))  #Calcular direccion
            add = int(add)>>2 #con shift left
            ans = pBin(add, 26)
        else: #Si la etiqueta esta debajo de donde se llama
            if immediate not in labelPending:
                labelPending.append(immediate)
            print("Pending")
            ans = "pending"
    return ans

def interpretar(ins):
    global instPoint, numCiclos
    try:
        ins = ins.replace("(", " ").replace(")", " ").replace(",", " ")
        ins = ins.lower().split() # ["add", "$s1", "$s2", "$s3"]
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
                shamt = getImm(ins[3], 5)
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

            #Incrementar puntero de instrucciones y ciclos de relog
            instPoint+=1 
            #Contar ciclos
            if ins[0] == "lw": numCiclos += 5
            else: numCiclos += 4

            return op + " "+ rs +" "+ rt +" "+ rd +" "+ shamt +" "+ funct
        #Tipo I
        elif ins[0] in opI:
            op = opI[ins[0]]
            rt = registros[ins[1]]
            # Caso lui
            if ins[0] == "lui":
                rs ="00000"
                immediate = getImm(ins[2],16)
            # Caso lw, sw, lbu y sb
            elif ins[0] == "lw" or ins[0] == "sw" or ins[0] == "lbu" or ins[0] == "sb":
                immediate = getImm(ins[2],16)
                rs = registros[ins[3]]
            else:
                # Traducción general tipo I
                rs = registros[ins[2]]
                immediate = getImm(ins[3],16)
                
            #Incrementar puntero de instrucciones
            instPoint+=1 
            #Contar ciclos
            if ins[0] == "beq" or ins[0] == "bne": numCiclos += 3
            else: numCiclos += 4

            return op +" "+ rs +" "+ rt +" "+ immediate
        # Tipo J
        elif ins[0] in opJ:
            # Traduccion general tipo J
            op = opJ[ins[0]]
            address = getImm(ins[1],26)

            #Incrementar puntero de instrucciones
            instPoint+=1 
            #Contar ciclos
            numCiclos += 3

            return op +" "+ address

        elif ins[0][-1] == ":": #Si es un label
            label = ins[0].replace(":", "")
            labelAdd[label] = instPoint #Agrega esta etiqueta con su direccion al arreglo
            return ""
        else: #Si es comentario, linea en blanco, o instruccion no valida
            return ""
    except KeyError:
        return "Registros invalidos"
    except IndexError:
        return "Sintaxis invalida"

def reset():
    labelPending.clear()
    labelAdd.clear()
    traduccion.clear()

def traducir(inFile,outFile):
    reset()

    with open(inFile, "r") as file: # Abrir archivo con instrucciones
        for i in file:
            if i != '\n' and i != "":
                traduccion.append(interpretar(i))
                #print(traduccion)
                pass
    
    #desps de interpretar
    print()
    for l in labelPending:
        print(l)

    with open(outFile, 'w') as file:
        for l in traduccion:
            l += '\n'
            file.writelines(l)