import sys
import socket
import threading


def hexdump(src, length=10):
    result = []
#    digits = 4 if isinstance(src, unicode) else 2
    digits = 4
    for i in range(0, len(src), length):
        s = src[i:i + length]
        print('[*] s:', s)

        hexa = ' '.join(["%0*X" % (digits, ord(x)) for x in s])
        print('hexa:', hexa)

        text = ''.join([x if 0x20 <= ord(x) < 0x7F else '.' for x in s])
        print('text:', text)

        result.append("%04X   %-*s   %s" % (i, length * (digits + 1), hexa, text))

    print('\n'.join(result))

'''
def hexdump(src, length=16):
    result = []
    digits = 4

    s = src[:]
    print(s)
    hexa = " ".join(["%0*X" % (digits, ord(x)) for x in s.decode("utf-8")])
    text = "".join([x if 0x20 <= ord(x) < 0x7F else "." for x in s.decode("utf-8")])
    result.append("%04X   %-*s   %s" % (1, length * (digits + 1), hexa, text))

    print("\n".join(result))
'''
'''
        for x in s:
            if 0x20 <= ord(x) < 0x7F:
                print('true:', x, ord(x), hex(ord(x)), '0x20, 0x7F')
            else:
                print('else:', x, ord(x), hex(ord(x)), '0x20, 0x7F')

                print('.')
'''

test_data = 'abcdefghijklmnopqrstuvwxyz0123456789사랑하는 사람abcdefghijklmnopqrstuvwxyz0123456789'
remote_buffer = test_data
print(remote_buffer)
hexdump(remote_buffer)