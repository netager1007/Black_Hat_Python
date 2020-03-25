import sys

file_path = sys.argv[1]
print('[*]', sys.argv[0], sys.argv[1])

if len(sys.argv) != 2:
    print('insufficient arguments')
    sys.exit(0)
print("File Paht:", file_path)