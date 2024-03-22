from core import give
import time, folderbase

def drop(wallet):
    if folderbase.ishere(wallet+"_faucet"):
        if float(folderbase.read(wallet+'_faucet')) < time.time():
            give(wallet, int((time.time() - (float(folderbase.read(wallet+"_faucet"))-3600))/3600))
            folderbase.write(wallet+"_faucet", time.time()+(60*60))
            return 'OK GOOD'
        else:
            return 'NO'
    else:
        give(wallet, 1)
        folderbase.write(wallet+"_faucet", time.time()+(60*60))
        return 'OK GOOD'