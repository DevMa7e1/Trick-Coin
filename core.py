import hashlib, folderbase, string, random, os
key = "jxpblhIqvsoPKC"
def assign_wallet(user,password):
    global key
    a = ""
    for i in range(1, 15):
        a += random.choice(string.ascii_letters)
    b = str(user+hashlib.sha256(password.encode()).hexdigest()+key).encode()
    c = hashlib.sha256(b).hexdigest()
    folderbase.write(a, f"{user},{hashlib.sha256(password.encode()).hexdigest()},{c}")
    return a
def amount(user):
    all = 0
    for i in os.listdir(os.getcwd()+"/folderbase"):
        f = open('folderbase/'+i)
        a = f.read()
        if len(a.split(',')) > 1:
            if a.split(',')[0] == user:
                all += int(a.split(",")[2])
            if a.split(',')[1] == user:
                all -= int(a.split(",")[2])
    return all
def transact(_from : str, to : str, amoun : int, password : str, bypass : False):
    if amount(_from) >= amoun and (bypass or folderbase.read(_from).split(',')[1] == hashlib.sha256(password.encode()).hexdigest()):
        y = str(int(folderbase.read('n'))-1)
        x = folderbase.read(y).encode()
        z = hashlib.sha256(x).hexdigest()
        folderbase.write(folderbase.read("n"), f"{to},{_from},{str(amoun)},{z}")
        folderbase.write("n", int(folderbase.read("n"))+1)
def give(to : str, amoun : int):
    y = str(int(folderbase.read('n'))-1)
    x = folderbase.read(y).encode()
    z = hashlib.sha256(x).hexdigest()
    folderbase.write(folderbase.read("n"), f"{to},god,{str(amoun)},{z}")
    folderbase.write("n", int(folderbase.read("n"))+1)
def auth(wallet, password : str):
    global key
    if folderbase.ishere(wallet):
        a = folderbase.read(wallet)
        if a.split(',')[1] == hashlib.sha256(password.encode()).hexdigest() and hashlib.sha256((a.split(',')[0]+a.split(',')[1]).encode()).hexdigest() == a.split(',')[2]:
            return True
        else:
            return False
    else:
        return False
def verify(tx : int, user : str):
    #OBSOLETE!!! DO NOT USE!!!
    for i in range(tx, int(folderbase.read('n'))):
        if not folderbase.read(str(i)).split(',')[2] == hashlib.sha256(folderbase.read(str(i-1)).encode()).hexdigest():
            print(f"Wrong block detected! {i - 1}")
            a = folderbase.read(str(i - 1)).split(',')
            if a[2] < 1:
                transact(a[0], user, int(a[2]), "", True)
            elif a[2] > 10 and a[2] < 100:
                transact(a[0], user, int(a[2]) / 2, True)
            elif a[2] > 100:
                transact(a[0], user, 100, "", True)
            folderbase.delete(str(i - 1))
        else:
            z = int(folderbase.read('n'))
            give(user, z-(z - tx))
    folderbase.write('v', folderbase.read('n'))
def get_tx(txn):
    if folderbase.ishere(txn):
        a = folderbase.read(txn)
        return a
    return "NO"
def wrong_block(txn, wallet):
    a = folderbase.read(str(int(txn)+1))
    b = folderbase.read(txn)
    if(a.split(',')[2] == hashlib.sha256(b).hexdigest()):
        give(wallet, 1)