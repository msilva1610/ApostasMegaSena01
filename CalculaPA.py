def CalculaPA(dezenas):
    r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r12,r14,r15,r16,r17,r18,r19,r20 = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 
    dezenas.sort()
    ParDePAs = 0
    delta1 = dezenas[1] - dezenas[0]
    for index in range(len(dezenas) - 1):
        print(str(dezenas[index + 1]) + '-' + str(dezenas[index]) + '=' + str((dezenas[index + 1] - dezenas[index])))
        if (dezenas[index + 1] - dezenas[index]) == delta1:
            ParDePAs += 1
        elif delta1 == 3:
            r3 = ParDePAs
            delta1 = 0
        elif delta1 == 4:
            r4 = ParDePAs
            delta1 = 0
        elif delta1 == 5:
            r5 = ParDePAs
            delta1 = 0
        elif delta1 == 6:
            r6 = ParDePAs
            delta1 = 0                        
        elif delta1 == 7:
            r7 = ParDePAs
            delta1 = 0                        
        elif delta1 == 8:
            r8 = ParDePAs
            delta1 = 0
        elif delta1 == 9:
            r9 = ParDePAs
            delta1 = 0
        elif delta1 == 10:
            r10 = ParDePAs
            delta1 = 0
        elif delta1 == 11:
            r11 = ParDePAs
            delta1 = 0
        elif delta1 == 12:
            r12 = ParDePAs
            delta1 = 0
        elif delta1 == 13:
            r13 = ParDePAs
            delta1 = 0
        elif delta1 == 14:
            r14 = ParDePAs
            delta1 = 0
        elif delta1 == 15:
            r15 = ParDePAs
            delta1 = 0
        elif delta1 == 16:
            r16 = ParDePAs
            delta1 = 0
        elif delta1 == 17:
            r17 = ParDePAs
            delta1 = 0
        elif delta1 == 18:
            r18 = ParDePAs
            delta1 = 0
        elif delta1 == 19:
            r19 = ParDePAs
            delta1 = 0
        elif delta1 == 20:
            r20 = ParDePAs
            delta1 = 0            
    return r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r12,r14,r15,r16,r17,r18,r19,r20

# dezenas = [3, 7, 11, 15, 19, 23] # 5 Pares
# dezenas = [3, 7, 11, 15, 19, 24] # 4 Pares
# dezenas = [3, 7, 11, 17, 21, 24] # 3 Pares
dezenas = [5, 11, 17, 23, 24, 25] # 2 Pares
# dezenas = [3, 7, 12, 17, 20, 23] # 1 Pares

print(CalculaPA(dezenas))