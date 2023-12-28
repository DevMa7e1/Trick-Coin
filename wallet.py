import colorama, requests, os
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
if(not os.path.exists("setup")):
    if(input("Do you already have a wallet? Y/n>").lower() == "n"):
        pasw = input("Password>")
        wallet = requests.post(ip+"/new", data={"user":input("Username>"), "password":pasw}).text
        print("This is your wallet:", wallet)
        print(f"{colorama.Fore.GREEN}You have been succesfully logged in!{colorama.Fore.RESET}")
        f = open("setup", 'w')
        f.write(f"{wallet},{pasw}")
        f.close()
    else:
        wlet = input("Wallet address>")
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
            #Start wallet code here!
            while(True):
                print(f"{colorama.Fore.BLUE}"+requests.post(ip+"/amount", data={"user": a[0]}).text, "TRICK", f"{colorama.Fore.RESET}")
                opt = input(f"{colorama.Fore.RED}1. Send{colorama.Fore.GREEN} \n2. Recive\n{colorama.Fore.CYAN}3. Hourly reward{colorama.Fore.RESET}\nOption number>")
                if(opt == "1"):
                    amount = input("Amount>")
                    to = input("Recipient wallet>")
                    if("OK GOOD" in requests.post(ip+"/transact", data={"from": a[0], "password":a[1], "to":to, "amount":amount}).text):
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
    else:
            print(f"{colorama.Fore.RED}You have not been succesfully logged in!{colorama.Fore.RESET}")
input()
