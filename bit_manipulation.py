import random
import struct


def float_to_bin(num):
    return format(struct.unpack("!I", struct.pack("!f", num))[0], "032b")


def bin_to_float(binary):
    return struct.unpack("!f", struct.pack("!I", int(binary, 2)))[0]


def extract_bit(a, start, end):
    x = 0
    for i in range(0, end - start):
        if a & 2 ** (start + i) > 0:
            x += 2 ** i

    return x


a = float_to_bin(random.random() * 10)
b = float_to_bin(random.random() * 10)
# a_gauche = a &
# b_gauche = b $
print(a)
print(b)

print(bin_to_float(a))
print(bin_to_float(b))

# print(bin(a_gauche | b_gauche))

# print(bin(extract_bit(a, 0, 9)))

gena = ""
genb = ""
for i in range(0, 3):
    gena += float_to_bin(random.random() * 10)
    genb += float_to_bin(random.random() * 10)
