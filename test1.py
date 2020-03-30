
aa = "%0*X".encode() % (16, ord('a'))
print(aa)
b = 'ABC'


aa = '%04X' %11
bb = '%04X' %12
print('aa:', aa)
print('bb:', bb)
cc = aa + bb
print('cc:', cc)

print('0x%04x 0x%04x' % (42, 44))
print('0x%0*X' % (6, 42))
print('0x%04X' % 42)


'''
def hexdump(src, length=16):
    result = []
    digits = 4

    s = src[:]
    print(s)
    hexa = " ".join(["%0*X" % (digits, ord(x)) for x in s.decode("ascii")])
    text = "".join([x if 0x20 <= ord(x) < 0x7F else "." for x in s.decode("ascii")])
    result.append("%04X   %-*s   %s" % (1, length * (digits + 1), hexa, text))

    print("\n".join(result))
'''