from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models.user import User
from flask_app.models.wallet import Wallet
from flask_app.models.exchange import Exchange

@app.route('/create/wallet')
def create_wallet():
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'id': session['user_id']
    }

    return render_template('wallet/create_wallet.html', user = User.get_by_id(data))

@app.route('/connect/created/wallet', methods = ['POST'])
def connect_wallet():
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'total_xp_earned' : request.form['total_xp_earned'],
        'usd_balance' : request.form['usd_balance'],
        'xp_balance' : request.form['xp_balance'],
        'xpcoin_balance' : request.form['xpcoin_balance'],
        'lvlcoin_balance' : request.form['lvlcoin_balance'],
        'dgcoin_balance' : request.form['dgcoin_balance'],
        'wallet_user_id' : request.form['wallet_user_id']
    }

    Wallet.save(data)

    return redirect('/user/home')

@app.route('/view/wallet/<int:id>')
def view_wallet(id):

    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'id' : id
    }

    user = {
        'id' : session['user_id']
    }

    chart_data = [
        ("Total XP", 100000),
        ("Total LVLCOin", 11),
        ("Total DGCoin", 1)
    ]
    labels = [row[0] for row in chart_data]
    values = [row[1] for row in chart_data]
    return render_template('wallet/view_wallet.html', wallet = Wallet.get_wallet_by_id(data), user = User.get_by_id(user), labels = labels, values = values)

@app.route('/exchange/<int:id>')
def exchange(id):
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'id' : id
    }

    user = {
            'id':session['user_id']
    }
    return render_template('exchange/exchange.html',wallet = Wallet.get_wallet_by_id(data), user = User.get_by_id(user), wallet_info = User.get_wallet(user), exchange = Exchange.get_info())

@app.route('/earn/xp/<int:id>')
def earn_xp(id):

    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'id' : id
    }

    user = {
        'id' : session['user_id']
    }

    return render_template('wallet/earn_xp.html', wallet = Wallet.get_wallet_by_id(data), user = User.get_by_id(user), wallet_info = User.get_wallet(user), exchange = Exchange.get_info())

@app.route('/earned/xp/<int:id>', methods = ['POST'])
def earned_xp(id):

    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'id' : id,
        'total_xp_earned' : request.form['total_xp_earned'],
        'xp_balance' : request.form['xp_balance']
    }
    Wallet.earn_xp(data)
    return redirect(f'/exchange/{id}')

@app.route('/earned/xpcoin/<int:id>', methods = ['POST'])
def earned_xpcoin(id):

    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'id' : id,
        'xp_balance' : request.form['xp_balance']
    }
    Wallet.earn_xpcoin(data)
    return redirect(f'/earn/xp/{id}')

@app.route('/earned/lvlcoin/<int:id>', methods = ['POST'])
def earned_lvlcoin(id):

    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'id' : id,
        'xpcoin_balance' : request.form['xpcoin_balance']
    }
    Wallet.earn_lvlcoin(data)
    return redirect(f'/earn/xp/{id}')

@app.route('/earned/dgcoin/<int:id>', methods = ['POST'])
def earned_dgcoin(id):
        if 'user_id' not in session:
            return redirect('/')
        
        data = {
            'id': id,
            'lvlcoin_balance': request.form['lvlcoin_balance']

        }
        Wallet.earn_dgccoin(data)
        return redirect(f'/earn/xp/{id}')
    
