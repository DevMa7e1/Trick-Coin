import hashlib, folderbase, os, binascii, boss, html, random, string

# Trick Coin V2

def assign_wallet(user,password):
    a = html.escape(user)
    if folderbase.ishere(user):
        return 'User already exists.'
    folderbase.write(a, f" ,{binascii.hexlify(hashlib.pbkdf2_hmac('sha256', (boss.get_password(password)).encode(), b'salt', 1000000)).decode()}")
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
def t_amount(user : str):
    return folderbase.read(user+"_txs")
def transact(_from : str, to : str, amoun : int, password : str, bypass = False):
    _from = html.escape(_from)
    to = html.escape(to)
    if binascii.hexlify(hashlib.pbkdf2_hmac("sha256", password.encode(), b"salt", 1000000)) == folderbase.read(_from).split(',')[1]:
        ()
    elif not amount(_from) >= amoun:
        ()
    elif not folderbase.ishere(to):
        ()
    else:
        y = str(int(folderbase.read('n'))-1)
        x = folderbase.read(y).encode()
        z = hashlib.sha256(x).hexdigest()
        folderbase.write(folderbase.read("n"), f"{to},{_from},{str(amoun)},{z}")
        if folderbase.ishere(to+"_txs"):
            folderbase.write(to+"_txs", str(int(folderbase.read(to+"_txs"))+1))
        else:
            folderbase.write(to+"_txs", '1')
        folderbase.write("n", int(folderbase.read("n"))+1)
def give(to : str, amoun : int):
    y = str(int(folderbase.read('n'))-1)
    x = folderbase.read(y).encode()
    z = hashlib.sha256(x).hexdigest()
    folderbase.write(folderbase.read("n"), f"{to},god,{str(amoun)},{z}")
    folderbase.write("n", int(folderbase.read("n"))+1)
    if folderbase.ishere(to+"_txs"):
        folderbase.write(to+"_txs", str(int(folderbase.read(to+"_txs"))+1))
    else:
        folderbase.write(to+"_txs", '1')
def take(_from : str, amoun : int):
    if amount(_from) >= amoun:
        y = str(int(folderbase.read('n'))-1)
        x = folderbase.read(y).encode()
        z = hashlib.sha256(x).hexdigest()
        folderbase.write(folderbase.read("n"), f"god,{_from},{str(amoun)},{z}")
        folderbase.write("n", int(folderbase.read("n"))+1)
        return True
    else:
        return False
def auth(wallet, password : str, decrypt = True):
    wallet = html.escape(wallet)
    if folderbase.ishere(wallet):
        a = folderbase.read(wallet)
        if decrypt:
            if a.split(',')[1] == binascii.hexlify(hashlib.pbkdf2_hmac("sha256", boss.get_password(password).encode(), b"salt", 1000000)).decode():
                return True
            else:
                return False
        else:
            if a.split(',')[1] == binascii.hexlify(hashlib.pbkdf2_hmac("sha256", password.encode(), b"salt", 1000000)).decode():
                return True
            else:
                return False
    else:
        return False
def get_tx(txn):
    if folderbase.ishere(txn):
        a = folderbase.read(txn)
        return a
    return "NO"
def wrong_block(txn, wallet):
    a = folderbase.read(str(int(txn)+1))
    b = folderbase.read(txn)
    if(a.split(',')[3] != hashlib.sha256(b.encode()).hexdigest()):
        folderbase.write(txn, "")
        for i in range(int(txn)+1, int(folderbase.read('n'))):
            z = folderbase.read(str(i)).split(',')
            folderbase.write(str(i), f"{z[0]},{z[1]},{z[2]},{hashlib.sha256(folderbase.read(str(i-1)).encode()).hexdigest()}")
        give(wallet, 1)
def transfer_coins_to_file(amoun, wallet, passwd):
    if binascii.hexlify(hashlib.pbkdf2_hmac("sha256", passwd.encode(), b"salt", 1000000)).decode() == folderbase.read(wallet).split(',')[1]:
        password = ''
        for i in range(20):
            password += random.choice(string.ascii_letters)
        if take(wallet, int(amoun)):
            folderbase.write(binascii.hexlify(hashlib.pbkdf2_hmac("sha256", password.encode(), b"salt", 1000000)).decode(), amoun)
        return f'{amoun},{password}'
    else:
        return 'NO'
def convert_file_to_coins(wallet, password, file_password : str):
    if folderbase.ishere(binascii.hexlify(hashlib.pbkdf2_hmac("sha256", file_password.encode(), b"salt", 1000000)).decode()):
        if auth(wallet, password, False):
            give(wallet, folderbase.read(binascii.hexlify(hashlib.pbkdf2_hmac("sha256", file_password.encode(), b"salt", 1000000)).decode()))
            folderbase.delete(binascii.hexlify(hashlib.pbkdf2_hmac("sha256", file_password.encode(), b"salt", 1000000)).decode())
            return 'Coins recovered succesfully!'
        else:
            return 'Wrong password!'
    else:
        return 'Coin file is invalid!'