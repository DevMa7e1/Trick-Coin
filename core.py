import hashlib, folderbase, os, binascii, boss, html, time, random, string

# Trick Coin V2.2

def assign_wallet(user,password:str):
    a = html.escape(user)
    if folderbase.ishere(user):
        return 'User already exists.'
    folderbase.write(a, f" ,{binascii.hexlify(hashlib.pbkdf2_hmac('sha256', (password.encode())).encode(), b'salt', 1000000).decode()}")
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
def transact(_from : str, to : str, amoun : int, password : str = '', bypass = False, nonexistent = False):
    _from = html.escape(_from)
    to = html.escape(to)
    if not folderbase.ishere(_from+"_txs"):
        if (binascii.hexlify(hashlib.pbkdf2_hmac("sha256", password.encode(), b"salt", 1000000)).decode() == folderbase.read(_from).split(',')[1] or bypass) and amount(_from) >= amoun+1 > 0 and (folderbase.ishere(to) or nonexistent):
            z = hashlib.md5(f"{to},{_from},{str(amoun)}".encode()).hexdigest()
            folderbase.write('u.'+z, f"{to},{_from},{str(amoun)}")
            folderbase.write(_from+"_txs", '')
            return True
    return False
def give(to : str, amoun : int, nonexistent = False):
    transact('god', to, amoun, bypass=True, nonexistent=nonexistent)
def take(_from : str, amoun : int):
    return transact(_from, 'god', amoun, bypass=True)    
def auth(wallet, password : str, decrypt = True):
    wallet = html.escape(wallet)
    if folderbase.ishere(wallet):
        a = folderbase.read(wallet)
        if decrypt:
            if a.split(',')[1] == binascii.hexlify(hashlib.pbkdf2_hmac("sha256", password.encode(), b"salt", 1000000)).decode():
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
            if key.startswith('u.') and not key in requested_transactions and folderbase.read(key).split(',')[2] != "0":
                data = key.replace('u.', '')
                data += ','+hashlib.md5(f"{wallet},{folderbase.read(key).split(',')[1]},1".encode()).hexdigest()
                requested_transactions.append(key)
                break
        if data != "":
            return data
        else:
            for key in os.listdir('folderbase'):
                if key.startswith('u.') and not key in requested_transactions:
                    data = key.replace('u.', '')
                    data += ','+hashlib.md5(f"{wallet},{folderbase.read(key).split(',')[1]},1".encode()).hexdigest()
                    requested_transactions.append(key)
                    break
        if data != "":
            return data
    return 'NO'
def got_signature_from_miner(signature, public_key, hash, wallet, signature2, hash2):
    wallet = html.escape(wallet)
    if folderbase.ishere('u.'+hash) and folderbase.ishere(wallet):
        if boss.verify(signature, hash, public_key) and boss.verify(signature2, hash2, public_key) and hash2 == hashlib.md5(f"{wallet},{folderbase.read('u.'+hash).split(',')[1]},1".encode()).hexdigest():
            isGoodToGo = True
            for key in os.listdir('folderbase'):
                try:
                    if folderbase.read(key).split(',')[4] == public_key:
                        isGoodToGo = False
                        break
                except:
                    ()
            if isGoodToGo:
                requested_transactions.remove('u.'+hash)
                folderbase.write(folderbase.read('n'), folderbase.read('u.'+hash)+f",{signature},{public_key}")
                if folderbase.read("u."+hash).split(',')[2] == "0":
                    folderbase.delete(folderbase.read("n"))
                else:
                    folderbase.write('n', str(int(folderbase.read('n'))+1))
                folderbase.write(folderbase.read('n'), f"{wallet},{folderbase.read('u.'+hash).split(',')[1]},1,{signature2},{public_key}")
                folderbase.write('n', str(int(folderbase.read('n'))+1))
                folderbase.delete(folderbase.read('u.'+hash).split(',')[1]+"_txs")
                folderbase.delete('u.'+hash)
                if time.time() % 1000 == 0:
                    give(wallet, 1)
                    return 'You recived 2 TRICK!'
                randomStringOfTenLetters = random.choice(string.ascii_letters)+random.choice(string.ascii_letters)+random.choice(string.ascii_letters)+random.choice(string.ascii_letters)+random.choice(string.ascii_letters)+random.choice(string.ascii_letters)+random.choice(string.ascii_letters)+random.choice(string.ascii_letters)+random.choice(string.ascii_letters)+random.choice(string.ascii_letters)
                give(randomStringOfTenLetters, 0, True)
                return 'You recived 1 TRICK!'
    return 'NO'