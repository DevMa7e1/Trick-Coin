from core import *
from flask import Flask, request
import hashlib, binascii
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
    _from = str(request.form['from'])
    to = str(request.form.get('to', False))
    amoun = str(request.form.get('amount', False))
    password = str(request.form.get('password', False))
    if int(amount(_from)) >= int(amoun) and binascii.hexlify(hashlib.pbkdf2_hmac("sha256", password.encode(), b"salt", 1000000)) == folderbase.read(_from).split(',')[1]:
        transact(_from, to, int(amoun), password, bypass=False)
        return "OK GOOD"
    else:
        return 'NO'
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
    return 'OK'

app.run("0.0.0.0", 9314, False)
