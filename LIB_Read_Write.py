def readfile():
    f = open('Price.txt', 'r')
    if f.mode=='r':
        content=f.read()
    f.close()
    return content

def writefile(number):
    f =open('Price.txt', 'w')
    if f.mode== "w":
        f.write(number)
    f.close()