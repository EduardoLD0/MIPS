from datos import functR, opI, opJ, registros

#string array
instrucciones = []
traduccion = []

#Manejo de direcciones de instrucciones
labelPending = {}
labelAdd = {} #diccionario de etiquetas con su direccion
instPoint = -1 #numero de la instruccion
baseAdd = "00400000" #direccion base instrucciones

#Contador de ciclos
numCiclos = []
instCiclos = []
retAdd = 0

#def getLabelAdd(label):
#    return add

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
            add = int(baseAdd, 16) + int(str(labelAdd[immediate]*4))  #Calcular direccion
            add = int(add)>>2 #con shift left
            ans = pBin(add, 26)
        else: #Si la etiqueta no se ha guardado todavia
            if immediate not in labelPending:
                labelPending[instPoint+1] = immediate
            ans = immediate
    return ans

def interpretar(ins):
    global instPoint, numCiclos, instrucciones
    try:
        ins = ins.replace("(", " ").replace(")", " ").replace(",", " ")
        ins = ins.lower().split() # ["add", "$s1", "$s2", "$s3"]
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
            instrucciones.append(ins)
            #Contar ciclos
            #if ins[0] == "lw": numCiclos += 5
            #else: numCiclos += 4

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
            instrucciones.append(ins)
            #Contar ciclos
            #if ins[0] == "beq" or ins[0] == "bne": numCiclos += 3
            #else: numCiclos += 4

            return op +" "+ rs +" "+ rt +" "+ immediate
        # Tipo J
        elif ins[0] in opJ:
            # Traduccion general tipo J
            op = opJ[ins[0]]
            address = getImm(ins[1],26)

            #Incrementar puntero de instrucciones
            instPoint+=1 
            instrucciones.append(ins)
            #Contar ciclos
            #numCiclos += 3

            return op +" "+ address

        elif ins[0][-1] == ":": #Si es un label
            label = ins[0].replace(":", "")
            labelAdd[label] = instPoint+1 #Agrega esta etiqueta con su direccion al arreglo
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
    instrucciones.clear()
    instPoint = -1

def traducir(inFile,outFile):
    reset() #Resetear variables globales

    # Abrir archivo con instrucciones
    with open(inFile, "r") as file: 
        for i in file:
            if i != '\n' and i != "":
                line = interpretar(i)
                if line != "":
                    traduccion.append(line)
                pass
    
    #Despuess de interpretar
    #revisar si queda algun label pendiente
    for l in range(len(instrucciones)):
        print(l,end=" ")
        print(instrucciones[l])
        if l in labelPending:
            add = labelAdd[labelPending[l]] #direccion guardada del label
            add = add - l - 1 #calcular direccion
            add = pBin(add, 16)
            traduccion[l] = traduccion[l].replace("exit",add)
            
    #Print in out file
    with open(outFile, 'w') as file:
        for l in traduccion:
            l += '\n'
            file.writelines(l)
"""
def contarCiclos():
    global numCiclos
    global instrucciones
    i = 0 #puntero
    while i in range(len(instrucciones)):
        numCiclos+=1
        jumps = {"beq", "bne", "j", "jal"}
        if instrucciones[i][0] in jumps:
            label = instrucciones[i][-1]
            if instrucciones[i][0] == "beq" or instrucciones[i][0] == "bne":
                o = i+1 #no toma el branch
            else:
                if label == "$ra":
                    lAdd = retAdd
                else:
                    lAdd = labelAdd[label]
            print(str(i)+" "+instrucciones[i][0]+" "+label+" "+str(lAdd))
            i = lAdd
        i+=1
    pass
"""

def getNumInst(inst):
    if inst == "beq" or inst == "bne" or inst == "j" or inst == "jal":
        return 3
    elif inst == "lw":
        return 5
    else:
        return 4

def bfs(grafo):
    pila = []
    pila.append(0)
    numNoCiclos = 0
    numCiclos = 0
    listaCiclos = []
    while len(pila) > 0:
        i = pila.pop()
        for j in grafo[i]:
            if j[1] == 0:
                pila.append(j[0])
                numNoCiclos += getNumInst(instrucciones[i][0])
            elif j[1] == 1:
                listaCiclos.append(i)
    for k in listaCiclos:
        pila.append(grafo[k][0][0])
        numCiclos += 3
        while pila[0] != k:
            i = pila.pop()
            for j in grafo[i]:
                if j[1] == 0:
                    pila.append(j[0])
                    numCiclos += getNumInst(instrucciones[i][0])
                elif j[1] == 1:
                    listaCiclos.append(j[1])
    return [numNoCiclos, numCiclos]


def contarCiclos():
    global numCiclos
    grafoInst = []
    for i in range(len(instrucciones)):
        inst = instrucciones[i][0]
        if inst == "j":
            grafoInst.append([[labelAdd[instrucciones[i][1]], 0]])
            pass
        elif inst == "beq":
            grafoInst.append([[i + 1, 1], [labelAdd[instrucciones[i][3]], 0]])
            pass
        else:
            grafoInst.append([[i + 1, 0]])
    grafoInst.append([[-1, -1]])
    numCiclos = bfs(grafoInst)
