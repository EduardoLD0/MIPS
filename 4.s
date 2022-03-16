main:
    lui $s0, 0x1000
    ori $s0, $s0, 0x00000
    lw $s1, 8($s0) #a
    lw $s2, 12($s0) #c
    lw $s3, 16($s0) #d
    addi $t0, $0, 1 #i = 1
    addi $t1, $0, 100 #size
    addi $t2, $0, 0 #offset
for:
    beq $t0, $t1, exit
    sll $t5, $t2, 2  
    add $s4, $s0, $t5   #$s4 0x10000004
    lw $s5, 20($s4) #b(1) b(2)
    sub $t3, $s1, $s2 #(a-c) = $t3
    sll $t4, $t0, 3 # (i*8) = $t4
    mult $t3, $t4
    mflo $s5   #b(i)
    addi $t0, $t0, 1
    addi $t2, $t2, 1
    sw $s5, 20($s4) #b(1) = 5 -> 0x10000014 b(2) = 10 -> 0x10000018
    j for
    addi $sp, $sp, -4
    sw $ra, 0($sp)
    jal menor
    sw $s3, 16($s0)
    lw $ra, 0($sp)
    addi $sp, $sp, 4
    jr $ra
menor:
    lw $s6, 20($s0) #b(1)
    addi $t6, $s6, 0 # t6 = b(1) -> temp = b(1)
    addi $t1, $t1, -1 #size - 1 (99)
    addi $t0, $0, 1 #i = 1
for2:
    beq $t1, $t0, exit
    addi $t2, $0, 1 #nuevo offset
    sll $t5, $t1, 2 
    add $s4, $s0, $t5 #0x100000004
    lw $s7, 20($s4) # S = b(i+1) i = 1
    slt $t7, $s7, $t6 #tem > s ? 1 | 0
    beq $t7, $0, continue
    addi $t6, $s7, 0
continue:
    j for2
exit:
    jr $ra



