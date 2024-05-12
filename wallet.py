import colorama, requests, os.path, rsa, hashlib, binascii
print(f"""{colorama.Fore.RED}
  OOOOO OOOO  O  OOOO  O O        O       O   OOO   O    O    OOOO OOOOO
    O   O  O  O  O     OO         O   O   O  O   O  O    O    OOO    O
    O   OOO   O  O     O O         O O O O   OOOOO  O    O    O      O
    O   O  O  O  OOOO  O  O         O   O    O   O  OOOO OOOO OOOO   O
{colorama.Fore.RESET}""")
wlet = ""
pasw = ""
ip = "https://e78a-2a02-2f0d-d806-9f00-d6b6-b593-8066-b51a.ngrok-free.app"
r = requests.get("https://devma7e1.pythonanywhere.com/ip")
if r.status_code == 200:
    print(f"{colorama.Fore.GREEN}Ip has been found!{colorama.Fore.RESET}")
    ip = r.text
publickey = rsa.PublicKey.load_pkcs1(requests.get(ip+'/getkey').text.encode())
def get_the_magic_string(god_awful_string):
    r = god_awful_string
    a  = ''
    dick = {}
    for i in range(len(r)):
        if r[i].isupper():
            dick.update({i : r[i]})
        else:
            a += r[i]
    b = bytes.fromhex(a.replace('\\x', '').replace("'", '').removeprefix('b'))
    c = b''
    i = -1
    while True:
        i += 1
        if i >= len(b)+len(dick)-1:
            break
        if i in dick:
            c += dick[i].encode()
            i -= 1
            c += str(chr(b[i])).encode('Latin-1')
            i += 1
        else:
            c += str(chr(b[i])).encode('Latin-1')
    return c
if(not os.path.exists("setup")):
    if(input("Do you already have a wallet? Y/n>").lower() == "n"):
        user = input("Username>")
        pasw = input("Password>")
        wallet = requests.post(ip+"/new", data={"user":user, "password":rsa.encrypt(pasw.encode(), publickey).decode('Latin-1')}).text
        print("This is your wallet:", wallet)
        print(f"{colorama.Fore.GREEN}You have been succesfully logged in!{colorama.Fore.RESET}")
        f = open("setup", 'w')
        f.write(f"{wallet},{pasw}")
        f.close()
    else:
        wlet = input("Username>")
        pasw = input("Password>")
        if("OK GOOD" in requests.post(ip+"/auth", data={"user": wlet, "password":rsa.encrypt(pasw.encode(), publickey).decode('Latin-1')}).text):
            print(f"{colorama.Fore.GREEN}You have been succesfully logged in!{colorama.Fore.RESET}")
            f = open("setup", 'w')
            f.write(f"{wlet},{pasw}")
            f.close()
        else:
            print(f"{colorama.Fore.RED}You have not been succesfully logged in!{colorama.Fore.RESET}")
else:
    f = open("setup")
    a = f.read().split(',')
    if("OK GOOD" in requests.post(ip+"/auth", data={"user": a[0], "password":rsa.encrypt(a[1].encode(), publickey).decode('Latin-1')}).text):
            print(f"{colorama.Fore.GREEN}You have been succesfully logged in!{colorama.Fore.RESET}")
            while(True):
                print(f"{colorama.Fore.BLUE}"+requests.post(ip+"/amount", data={"user": a[0]}).text, "TRICK", f"{colorama.Fore.RESET}")
                opt = input(f"{colorama.Fore.RED}1. Send{colorama.Fore.GREEN} \n2. Recive\n{colorama.Fore.CYAN}3. Hourly reward{colorama.Fore.RESET}\n{colorama.Fore.MAGENTA}4. Turn coins into file{colorama.Fore.YELLOW}\n5. Turn file into coins\n{colorama.Fore.RESET}Option number>")
                if(opt == "1"):
                    amount = input("Amount>")
                    to = input("Recipient user>")
                    if("OK GOOD" in requests.post(ip+"/transact", data={"data" : rsa.encrypt(f'{a[0]},{to},{amount},{a[1]}'.encode(), publickey).decode('Latin-1')}).text):
                        print(f"{colorama.Fore.GREEN}Transaction succsessful!{colorama.Fore.RESET}")
                    else:
                        print(f"{colorama.Fore.RED}Transaction unsuccsessful!{colorama.Fore.RESET}")
                elif(opt == "2"):
                    print(a[0])
                elif(opt == "3"):
                    if 'OK GOOD' in requests.post(ip+"/faucet", data={'wallet': a[0]}).text:
                        print(f"{colorama.Fore.GREEN}Hourly reward has been claimed.{colorama.Fore.RESET}")
                    else:
                        print(f'{colorama.Fore.RED}Hourly reward has not been claimed. Come an hour later!')
                elif(opt == "4"):
                    amount = input('Amount>')
                    req = requests.post(ip+"/mkcf", data={'data': rsa.encrypt(f'{a[0]},{amount},{a[1]}'.encode('Latin-1'), publickey).decode('Latin-1')})
                    if not ('NO' in req.text):
                        file = input('Path for file to create>')
                        if not file.endswith('.trick'):
                            file += '.trick'
                        try:
                            f = open(file, 'w')
                            f.write(req.text)
                            f.close()
                        except Exception as e:
                            print(e)
                            print('Try again.')
                        while not os.path.exists(file):
                            file = input('File did not create! Maybe the path is wrong.\nPath for file to create>')
                            if not file.endswith('.trick'):
                                file += '.trick'
                            try:
                                f = open(file, 'w')
                                f.write(req.text)
                                f.close()
                            except Exception as e:
                                print(e)
                                print('Try again.')
                elif(opt == "5"):
                    print('Tip: You can drag and drop files into the terminal to get their path.\n')
                    file = input('Path to file>')
                    while not os.path.exists(file):
                        file = input('File does not exist.\nPath to file>')
                    f = open(file, 'r')
                    read = f.read()
                    read = read.split(',', 1)
                    by = read[1]
                    print(f'You are reciving {read[0]} TRICK.')
                    try:
                        input("Are you sure that you want to recive those coins?\nPress enter to proceed or hit Ctrl+C to cancel.")
                        print(requests.post(ip+"/gcfc", data={'data': rsa.encrypt(f'{a[0]},{a[1]}'.encode('Latin-1'), publickey).decode('Latin-1'), 'fp': rsa.encrypt(by.encode(), publickey).decode('Latin-1')}).text)
                    except Exception as e:
                        print(f'{colorama.Fore.RED}Transaction stopped.{colorama.Fore.RESET}')
                        if input('Press enter to continue.') == 'error':
                            print(e)
                    except KeyboardInterrupt:
                        print(f'{colorama.Fore.RED}Transaction stopped.{colorama.Fore.RESET}')
    else:
            print(f"{colorama.Fore.RED}You have not been succesfully logged in!{colorama.Fore.RESET}")
input('Press enter to exit.')
