import rsa, os.path

if not os.path.exists('pub.rsa-key'):
    (publickey, privatekey) = rsa.newkeys(2048)
    f = open('pub.rsa-key', 'w')
    f.write(publickey.save_pkcs1().decode('Latin-1'))
    f.close()
    f = open('pri.rsa-key', 'w')
    f.write(privatekey.save_pkcs1().decode('Latin-1'))
    quit()

pub = open('pub.rsa-key')
public_plain_text = pub.read()
pub.close()
pub = open('pub.rsa-key')
pri = open('pri.rsa-key')
(publickey, privatekey) = (rsa.PublicKey.load_pkcs1(pub.read().encode('Latin-1')), rsa.PrivateKey.load_pkcs1(pri.read().encode('Latin-1')))
pri.close()
pub.close()

def get_password(got : str):
    return rsa.decrypt(got.encode('Latin-1'), privatekey).decode('Latin-1')
def get_public_key():
    return public_plain_text
def verify(signature : str, message : str, public_key : str):
    if len(public_key) == 775:
        try:
            rsa.verify(message.encode(), bytes.fromhex(signature), rsa.PublicKey.load_pkcs1(public_key.encode()))
            return True
        except:
            return False
    return False