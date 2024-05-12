from core import *
from faucet import drop
from flask import Flask, request
import hashlib, binascii, boss
app = Flask(__name__)

@app.route("/")
def home():
    return "OK GOOD"
@app.route("/new", methods = ['POST'])
def new():
    user = str(request.form['user'])
    password = str(request.form['password'])
    return str(assign_wallet(user, password))
@app.route("/transact", methods = ['POST'])
def tr():
    data = boss.get_password(str(request.form.get('data', False)))
    data = data.split(',')
    _from = data[0]
    to = data[1]
    amoun = data[2]
    password = data[3]
    transact(_from, to, int(amoun), password)
    return "OK GOOD"
@app.route("/amount", methods= ["POST"])
def am():
    user = request.form['user']
    return str(amount(user))
@app.route("/nr", methods= ["POST"])
def amy():
    return str(folderbase.read('n'))
@app.route('/auth', methods= ["POST"])
def au():
    ah = request.form['user']
    password = request.form['password']
    if ah != '':
        if auth(ah, password):
            return "OK GOOD"
    return 'NO'
@app.route("/gettx", methods= ["POST"])
def amya():
    nr = request.form.get('nr')
    return get_tx(nr)
@app.route("/wrgtx", methods= ["POST"])
def amyah():
    nr = request.form.get('nr')
    wallet = request.form.get('wallet')
    wrong_block(nr, wallet)
    return 'OK GOOD'
@app.route("/faucet", methods= ["POST"])
def faucet():
    wallet = request.form.get('wallet')
    return drop(wallet)
@app.route("/txs", methods= ["POST"])
def txs():
    wallet = request.form.get('wallet')
    return t_amount(wallet)
@app.route('/getkey')
def getkey():
    return boss.get_public_key()
@app.route('/mkcf', methods=['POST']) #make coin file
def mkcf():
    data = boss.get_password(str(request.form.get('data', False)))
    data = data.split(',')
    _from = data[0]
    amoun = data[1]
    password = data[2]
    return transfer_coins_to_file(amoun, _from, password)
@app.route('/gcfc', methods=['POST']) #get coin-file coins
def gcfc():
    data = boss.get_password(str(request.form.get('data', False)))
    file_password = boss.get_password(str(request.form.get('fp', False)))
    data = data.split(',')
    wallet = data[0]
    password = data[1]
    return convert_file_to_coins(wallet, password, file_password)
app.run("0.0.0.0", 9314, False)
