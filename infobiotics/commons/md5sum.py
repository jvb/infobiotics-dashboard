import hashlib

def md5sum(fileName, blockSize=2**20):
    file = open(fileName, 'r')
    md5 = hashlib.md5()
    while True:
        data = file.read(blockSize)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()


if __name__ == '__main__':
    import sys
    for file_name in sys.arv[1:]:
        print file_name, md5sum(file_name)
    