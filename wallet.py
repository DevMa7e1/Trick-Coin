import colorama, requests, os.path, time, rsa, multiprocessing

if __name__ == '__main__':
    print(f"""{colorama.Fore.RED}
  OOOOO OOOO  O  OOOO  O O        O       O   OOO   O    O    OOOO OOOOO
    O   O  O  O  O     OO         O   O   O  O   O  O    O    OOO    O
    O   OOO   O  O     O O         O O O O   OOOOO  O    O    O      O
    O   O  O  O  OOOO  O  O         O   O    O   O  OOOO OOOO OOOO   O
{colorama.Fore.RESET}""")
def create(certs):
    print("Thread started!")
    starttime = time.time()
    pub, pri = rsa.newkeys(4096)
    stoptime = time.time()
    print('Mining rate:', (1/((stoptime-starttime)/60)), 'cert/min')
    certs.append((pub, pri))

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
            pasw = input("Password>")
            wallet = requests.post(ip+"/new", data={"user":user, "password":pasw}).text
            print("This is your wallet:", wallet)
            print(f"{colorama.Fore.GREEN}You have been succesfully logged in!{colorama.Fore.RESET}")
            f = open("setup", 'w')
            f.write(f"{wallet},{pasw}")
            f.close()
        else:
            wlet = input("Username>")
            pasw = input("Password>")
            if("OK GOOD" in requests.post(ip+"/auth", data={"user": wlet, "password":pasw}).text):
                print(f"{colorama.Fore.GREEN}You have been succesfully logged in!{colorama.Fore.RESET}")
                f = open("setup", 'w')
                f.write(f"{wlet},{pasw}")
                f.close()
            else:
                print(f"{colorama.Fore.RED}You have not been succesfully logged in!{colorama.Fore.RESET}")
    else:
        f = open("setup")
        a = f.read().split(',')
        if("OK GOOD" in requests.post(ip+"/auth", data={"user": a[0], "password":a[1]}).text):
                print(f"{colorama.Fore.GREEN}You have been succesfully logged in!{colorama.Fore.RESET}")
                while(True):
                    print(f"{colorama.Fore.BLUE}"+requests.post(ip+"/amount", data={"user": a[0]}).text, "TRICK", f"{colorama.Fore.RESET}")
                    opt = input(f"{colorama.Fore.RED}1. Send{colorama.Fore.GREEN} \n2. Recive\n{colorama.Fore.CYAN}3. Start mining\n{colorama.Fore.RESET}Option number>")
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
                            if("OK GOOD" in requests.post(ip+"/transact", data={"data" : f'{a[0]},{to},{amount},{a[1]}'}).text):
                                print(f"{colorama.Fore.GREEN}Transaction sent to validation!{colorama.Fore.RESET}")
                            else:
                                print(f"{colorama.Fore.RED}Transaction was unsuccsessful!{colorama.Fore.RESET}")
                        else:
                            print(f'{colorama.Fore.YELLOW}Transaction aborted{colorama.Fore.RESET}')
                    elif(opt == "2"):
                        print(a[0])
                    elif(opt == "3"):
                        certs = []
                        threads = int(input("Number of threads>"))
                        while True:
                            manager = multiprocessing.Manager()
                            certs = manager.list()
                            with multiprocessing.Pool(processes=threads) as pool:
                                pool.map(create, [certs] * threads)
                            print(f'Generated {threads} new certificates!')
                            while(len(certs) > 0):
                                print('Waiting for task.')
                                tx = requests.post(ip+"/getunv", data={'wallet' : a[0]})
                                if tx.text != 'NO' and tx.status_code == 200:
                                    print('Recived new task:',tx.text)
                                    signature = rsa.sign(tx.text.split(',')[0].encode(), certs[0][1], 'SHA-256')
                                    hash = tx.text.split(',')[0].encode()
                                    signature2 = rsa.sign(tx.text.split(',')[1].encode(), certs[0][1], 'SHA-256').hex()
                                    print(requests.post(ip+"/validate", data= {'wallet' : f'{a[0]}', "sig" : signature.hex(), "pub": certs[0][0].save_pkcs1().decode(), 'hash' : hash, 'sig2' : signature2, 'hash2' : tx.text.split(',')[1]}).text)
                                    certs.pop()
                                time.sleep(1)
        else:
                print(f"{colorama.Fore.RED}You have not been succesfully logged in!{colorama.Fore.RESET}")
    input('Press enter to exit.')
