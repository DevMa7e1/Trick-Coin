from core import give
import time, folderbase

def drop(wallet):
    if folderbase.ishere(wallet+"_faucet"):
        if int(folderbase.read(wallet+'')) < time.time():
            give(wallet, 1)
            folderbase.write(time.time()+(60*60))
            return 'OK GOOD'
        else:
            return 'NO'
    else:
        give(wallet, 1)
        folderbase.write(time.time()+(60*60))
        return 'OK GOOD'