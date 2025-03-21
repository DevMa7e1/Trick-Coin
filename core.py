import hashlib, folderbase, os, binascii, boss, html, time, random, string

# Trick Coin V3.0

def assign_wallet(user,public_key:str):
    a = html.escape(user)
    if folderbase.ishere(user):
        return 'User already exists.'
    folderbase.write(a, public_key)
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
def transact(_from : str, to : str, amoun : int, signed_message : str = ''):
    _from = html.escape(_from)
    to = html.escape(to)
    if not folderbase.ishere(_from+"_txs") and amount(_from) >= amoun+1 and folderbase.ishere(_from) and folderbase.ishere(to):
        z = hashlib.md5(f"{to},{_from},{str(amoun)},{signed_message}".encode()).hexdigest()
        folderbase.write('u.'+z, f"{to},{_from},{str(amoun)},{signed_message}")
        folderbase.write(_from+"_txs", '')
        return True
    return False
def auth(wallet : str, signed_message):
    wallet = html.escape(wallet)
    if folderbase.ishere(wallet):
        a = folderbase.read(wallet)
        if boss.verify(signed_message, wallet, a):
            return True
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
                data = key
                data += ','+folderbase.read(key).split(',')[3]+','+folderbase.read(folderbase.read(key).split(',')[1]) # signed message and public key of sender
                requested_transactions.append(key)
                break
        if data != "":
            return data
    return 'NO'
#Unvalidated transaction format: to,from,amount,signed_message
def validate_transaction_and_send_reward(wallet : str, unverified_tx, secret_id : str):
    ok = False
    if unverified_tx in requested_transactions and folderbase.ishere(unverified_tx):
        a = folderbase.read(unverified_tx).split(',')
        if boss.verify(a[3], secret_id, folderbase.read(a[1])):
            if amount(a[1]) >= int(a[2])+1:
                folderbase.write(folderbase.read('n'), f'{a[0]},{a[1]},{a[2]},{a[3]},{secret_id}') # for later validation purposes
                folderbase.write('n', str(int(folderbase.read('n'))+1))
                folderbase.write(folderbase.read('n'), f'{wallet},{a[1]},{1},{a[3]},{secret_id}') # reward
                folderbase.write('n', str(int(folderbase.read('n'))+1))
                ok = True
    if ok:
        folderbase.delete(unverified_tx)
        requested_transactions.remove(unverified_tx)
        folderbase.delete(a[1]+"_txs")
    if ok:
        return True
    return False
#Validated transaction format: to,from,amount,signed_message,secret_id