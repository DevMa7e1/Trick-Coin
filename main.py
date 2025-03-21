from core import *
from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def home():
    return "OK GOOD"
@app.route("/new", methods = ['POST'])
def new():
    user = str(request.form['user'])
    pubkey = str(request.form['pubkey'])
    return str(assign_wallet(user, pubkey))
@app.route("/transact", methods = ['POST'])
def tr():
    data = str(request.form.get('data', False))
    data = data.split(',')
    _from = data[0]
    to = data[1]
    amoun = data[2]
    signed_message = data[3]
    if transact(_from, to, int(amoun), signed_message):
        return "OK GOOD"
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
    signed_message = request.form['signed']
    if ah != '':
        if auth(ah, signed_message):
            return "OK GOOD"
    return 'NO'
@app.route("/gettx", methods= ["POST"])
def amya():
    nr = request.form.get('nr')
    return get_tx(nr)
@app.route("/txs", methods= ["POST"])
def txs():
    wallet = request.form.get('wallet')
    if t_amount(wallet):
        return 'OK GOOD'
    return 'NO'
@app.route('/getunv', methods = ['POST'])
def getunv():
    return get_one_unvalidated_transaction(request.form.get('wallet'))
@app.route('/validate', methods=['POST'])
def validate():
    secret_id = (str(request.form.get('secret', False)))
    hash = (str(request.form.get('hash', False)))
    wallet = (str(request.form.get('wallet', False)))
    if validate_transaction_and_send_reward(wallet, hash, secret_id):
        return 'OK GOOD'
    return 'NO'
app.run("0.0.0.0", 9314, False)
