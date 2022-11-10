import hashlib
import datetime

def md5():
    h5 = hashlib.md5()
    file = input("Percorso: ")
    #test
    #file = (r'C:/Users/TARLUC/PycharmProjects/box/venv/CallFunction')
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h5.update(chunk)
    print(h5.hexdigest()+"\n")
    with open("log.txt", "a") as log:
        log.write(str(datetime.datetime.now())+" "+file+" "+h5.hexdigest()+"\n")
    return h5.hexdigest()
