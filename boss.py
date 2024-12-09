import rsa, os

if not os.path.exists('pub.rsa-key'):
    os.mkdir("folderbase")
    f = open('./folderbase/n', 'w')
    f.write("1")
    f.close()
    f = open('./folderbase/0', 'w')
    f.write('')
    quit()

def verify(signature : str, message : str, public_key : str):
    if len(public_key) == 775:
        try:
            rsa.verify(message.encode(), bytes.fromhex(signature), rsa.PublicKey.load_pkcs1(public_key.encode()))
            return True
        except:
            return False
    return False