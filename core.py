import hashlib, folderbase, os, binascii, boss, html

# Trick Coin V2.1

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
        if len(a.split(',')) > 1 and not i.startswith('u.'):
            if a.split(',')[0] == user:
                all += int(a.split(",")[2])
            if a.split(',')[1] == user:
                all -= int(a.split(",")[2])
    return all
def t_amount(user : str):
    if folderbase.ishere(user+"_txs"):
        return True
    return False
def transact(_from : str, to : str, amoun : int, password : str = '', bypass = False):
    _from = html.escape(_from)
    to = html.escape(to)
    if not folderbase.ishere(_from+"_txs"):
        if (binascii.hexlify(hashlib.pbkdf2_hmac("sha256", password.encode(), b"salt", 1000000)).decode() == folderbase.read(_from).split(',')[1] or bypass) and amount(_from) >= amoun+1 and folderbase.ishere(to):
            z = hashlib.md5(f"{to},{_from},{str(amoun)}".encode()).hexdigest()
            folderbase.write('u.'+z, f"{to},{_from},{str(amoun)}")
            folderbase.write(_from+"_txs", '')
            return True
    return False
def give(to : str, amoun : int):
    transact('god', to, amoun, bypass=True)
def take(_from : str, amoun : int):
    return transact(_from, 'god', amoun, bypass=True)    
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
    txn = html.escape(txn)
    if folderbase.ishere(txn):
        a = folderbase.read(txn)
        return a
    return "NO"
requested_transactions = []
def get_one_unvalidated_transaction(wallet):
    data = ""
    wallet = html.escape(wallet)
    if folderbase.ishere(wallet):
        for key in os.listdir('folderbase'):
            if key.startswith('u.') and not key in requested_transactions:
                data = key.replace('u.', '')
                data += ','+hashlib.md5(f"{wallet},{folderbase.read(key).split(',')[1]},1".encode()).hexdigest()
                requested_transactions.append(key)
        if data != "":
            return data
    return 'NO'
def got_signature_from_miner(signature, public_key, hash, wallet, signature2, hash2):
    wallet = html.escape(wallet)
    if folderbase.ishere('u.'+hash) and folderbase.ishere(wallet):
        if boss.verify(signature, hash, public_key) and boss.verify(signature2, hash2, public_key) and hash2 == hashlib.md5(f"{wallet},{folderbase.read('u.'+hash).split(',')[1]},1".encode()).hexdigest():
            requested_transactions.remove('u.'+hash)
            folderbase.write(folderbase.read('n'), folderbase.read('u.'+hash)+f",{signature},{public_key}")
            folderbase.write('n', str(int(folderbase.read('n'))+1))
            folderbase.write(folderbase.read('n'), f"{wallet},{folderbase.read('u.'+hash).split(',')[1]},1,{signature2},{public_key}")
            folderbase.write('n', str(int(folderbase.read('n'))+1))
            folderbase.delete(folderbase.read('u.'+hash).split(',')[1]+"_txs")
            folderbase.delete('u.'+hash)
            return 'You recived 1 TRICK!'
    return 'NO'