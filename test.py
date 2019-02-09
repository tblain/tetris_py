a = int('010010101011010101011', 2)
b = int('010100101010110111010', 2)
a_gauche = a & int('11111111110000000000', 2)
b_gauche = b & int('00000000001111111111', 2)
#print(bin(a_gauche | b_gauche))

def extract_bit(a, start, end):
    x = 0
    for i in range(0, end - start):
        if a & 2 ** (start + i) > 0:
           x += 2 ** i

    return x

print(bin(extract_bit(a, 0, 9)))
