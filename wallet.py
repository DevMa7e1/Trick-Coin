import colorama, requests, os, time, rsa, binascii, time

if __name__ == '__main__':
    print(f"""{colorama.Fore.RED}
  OOOOO OOOO  O  OOOO  O O        O       O   OOO   O    O    OOOO OOOOO
    O   O  O  O  O     OO         O   O   O  O   O  O    O    OOO    O
    O   OOO   O  O     O O         O O O O   OOOOO  O    O    O      O
    O   O  O  O  OOOO  O  O         O   O    O   O  OOOO OOOO OOOO   O
{colorama.Fore.RESET}""")
if __name__ == '__main__':
    wlet = ""
    pasw = ""
    ip = "https://e78a-2a02-2f0d-d806-9f00-d6b6-b593-8066-b51a.ngrok-free.app"
    r = requests.get("https://devma7e1.pythonanywhere.com/ip")
    if r.status_code == 200:
        print(f"{colorama.Fore.GREEN}Ip has been found!{colorama.Fore.RESET}")
        ip = r.text
    if os.path.exists('DevMode.activate'):
        print("Developer mode active!")
        ip = 'http://localhost:9314'
    if(not os.path.exists("setup")):
        if(input("Do you already have a wallet? Y/n>").lower() == "n"):
            user = input("Username>")
            print("Generating your RSA certificate pair.")
            (pub, priv) = rsa.newkeys(4096)
            wallet = requests.post(ip+"/new", data={"user":user,"pubkey":pub.save_pkcs1().decode()}).text
            print("This is your wallet:", wallet)
            print(f"{colorama.Fore.GREEN}You have been succesfully logged in!{colorama.Fore.RESET}")
            f = open("setup", 'w')
            f.write(f"{wallet},{priv.save_pkcs1().decode()}")
            f.close()
        else:
            wlet = input("Username>")
            privkey = input("Path to private key>")
            f = open(privkey)
            privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())
            f.close()
            if("OK GOOD" in requests.post(ip+"/auth", data={"user": wlet, "signed":binascii.hexlify(rsa.sign(wlet.encode(), privkey, 'SHA-256')).decode()}).text):
                print(f"{colorama.Fore.GREEN}You have been succesfully logged in!{colorama.Fore.RESET}")
                f = open("setup", 'w')
                f.write(f"{wlet},{privkey.save_pkcs1().decode()}")
                f.close()
            else:
                print(f"{colorama.Fore.RED}You have not been succesfully logged in!{colorama.Fore.RESET}")
    else:
        f = open("setup")
        a = f.read().split(',')
        privkey = rsa.PrivateKey.load_pkcs1(a[1].encode())
        if("OK GOOD" in requests.post(ip+"/auth", data={"user": a[0], "signed":binascii.hexlify(rsa.sign(a[0].encode(), privkey, 'SHA-256')).decode()}).text):
                print(f"{colorama.Fore.GREEN}You have been succesfully logged in!{colorama.Fore.RESET}")
                while(True):
                    print(f"{colorama.Fore.BLUE}"+requests.post(ip+"/amount", data={"user": a[0]}).text, "TRICK", f"{colorama.Fore.RESET}")
                    opt = input(f"{colorama.Fore.RED}1. Send{colorama.Fore.GREEN} \n2. Recive\n{colorama.Fore.CYAN}3. Start mining\n{colorama.Fore.RESET}{colorama.Fore.MAGENTA}4. Export private key{colorama.Fore.RESET}\nOption number>")
                    if(opt == "1"):
                        if 'OK GOOD' in requests.post(ip+"/txs", data={'wallet' : a[0]}).text:
                            print(f'{colorama.Fore.RED}You still have unverified transactions! Hang on tight while somebody validates your transactions.{colorama.Fore.RESET}')
                            break
                        print(f"{colorama.Fore.YELLOW}A tax of 1 TRICK is applied to every transaction.\nIf the transaction looks like it didn't go through, wait 24h before reporting the problem.{colorama.Fore.RESET}")
                        amount = input("Amount>")
                        while int(amount)+1 > int(requests.post(ip+"/amount", data={"user": a[0]}).text):
                            print(f"{colorama.Fore.RED}You do not have enough coins for this transaction.{colorama.Fore.YELLOW}\nRemember, the 1 TRICK tax is taken into account.{colorama.Fore.RESET}")
                            amount = input("Amount>")
                        to = input("Recipient user>")
                        sure = input(f"Total: {str(int(amount)+1)}. Are you sure you want to continue? Y/n>").upper()
                        if sure == 'Y':
                            random = str(int.from_bytes(os.urandom(1))+int.from_bytes(os.urandom(1))+int.from_bytes(os.urandom(1))+int.from_bytes(os.urandom(1))+int.from_bytes(os.urandom(1))+int.from_bytes(os.urandom(1)))
                            if("OK GOOD" in requests.post(ip+"/transact", data={"data" : f'{a[0]},{to},{amount},{binascii.hexlify(rsa.sign(random.encode(), privkey, 'SHA-256')).decode()}'}).text):
                                print(f"{colorama.Fore.GREEN}Transaction sent to validation!{colorama.Fore.RESET}")
                            else:
                                print(f"{colorama.Fore.RED}Transaction was unsuccsessful!{colorama.Fore.RESET}")
                        else:
                            print(f'{colorama.Fore.YELLOW}Transaction aborted{colorama.Fore.RESET}')
                    elif(opt == "2"):
                        print(a[0])
                    elif(opt == "3"):
                        while(True):
                            trx = requests.post(ip+"/getunv", data={"wallet":a[0]}).text
                            if trx == "NO":
                                print("No transactions to validate.")
                                time.sleep(10)
                            else:
                                data = trx.split(',')
                                pubkey = rsa.PublicKey.load_pkcs1(data[2].encode())
                                secret = 0
                                for i in range(1536):
                                    print(i, 'out of', 1536, end='\r')
                                    try:
                                        rsa.verify(str(i).encode(), bytes.fromhex(data[1]), pubkey)
                                        secret = i
                                        break
                                    except:
                                        pass
                                print()
                            if requests.post(ip+"/validate", data={'wallet' : a[0], 'secret': str(secret), 'hash': data[0]}).text == 'OK GOOD':
                                print(f"{colorama.Fore.GREEN}Transaction validated!{colorama.Fore.RESET}")
                    elif(opt == "4"):
                        print(f"{colorama.Fore.CYAN}Private key:{colorama.Fore.GREEN}\n{a[1]}{colorama.Fore.RESET}")
        else:
                print(f"{colorama.Fore.RED}You have not been succesfully logged in!{colorama.Fore.RESET}")
    input('Press enter to exit.')
