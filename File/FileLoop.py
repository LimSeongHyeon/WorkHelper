


with open("test.txt", "rb") as f:
    while (byte := f.read(117)):
        print(byte.decode())