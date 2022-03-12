from datos import functR, opI, opJ, registros
instAdd = {}

def traducir(ins):
    ins = ins.split() # ["add", "$s1", "$s2", "$s3"]
    reg = ins[1].split(",")
    # Traducir tipo R
    if ins[0] in functR:
        # Traduccion estandar tipo R
        op = 0b000000
        rd = registros[reg[0]]
        rs = registros[reg[1]]
        rt = registros[reg[2]]
        shamt = 0b000000
        funct = functR[ins[0]]
        # Caso sll y srl
        if ins[0] == "sll" or ins[0] == "srl":
            rs = 0b00000
            shamt = reg[3]
        # Caso jr
        elif ins[0] == "jr":
            rs = registros[reg[0]]
            rt = 0b00000
            rd = 0b00000
        # Caso mfc0
        elif ins[0] == "mfc0":
            op = 0b010000
            funct = 0b000000
            rd = bin(reg[0])
        # Caso mflo y mfhi
        elif ins[0] == "mflo" or ins[0] == "mfhi":
            rd = bin(reg[0])
        return op + rs + rt + rd + shamt + funct
    
    elif ins[0] in opI:
        # Traducción general tipo I
        op = opI[ins[0]]
        rt = registros[reg[0]]
        rs = registros[reg[1]]
        immediate = bin(reg[2])
        # Caso lui
        if ins[0] == "lui":
            rs = 0b00000
        # Caso lw, sw, lbu y sb
        elif ins[0] == "lw" or ins[0] == "sw" or ins[0] == "lbu" or ins[0] == "sb":
            immediate = bin(reg[1])
            rs = registros[reg[2]]
    
    elif ins[0] in opJ:
        # Traduccion general tipo J
        op = opJ[ins[0]]
        address = bin(ins[1])

    elif ins[0][-1] == ":": #Si es un label
        label = ins[0].replace(":", "")
        instAdd[label] = 
        
    else:
        print("Operacion inválida")

    


