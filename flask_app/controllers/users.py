from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models.user import User
from flask_app.models.wallet import Wallet
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)



@app.route('/')
def home():

    return render_template('login/login.html')

@app.route('/existing/user')
def existing_user():

    return render_template('login/existing_user.html')

@app.route('/register/user', methods = ['POST'])
def register_user():

    if User.validate_user(request.form):
        data = {
            'user_name' : request.form['user_name'],
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email': request.form['email'],
            'password' : bcrypt.generate_password_hash(request.form['password'])
        }
        id = User.save(data)
        session['user_id'] = id
        return redirect('/user/home')
    else:
        return redirect('/')

@app.route('/user/home')
def user_home():
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'id' : session['user_id']
    }
    return render_template('user/user_home.html', user = User.get_by_id(data), wallet = User.get_wallet(data), score = User.get_total_xp(data))

@app.route('/portal')
def portal():
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'id' : session['user_id']
    }
    return render_template('user/portal.html', user = User.get_by_id(data), wallet = User.get_wallet(data))


@app.route('/edit/user/<int:id>')
def edit_user(id):
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'id' : id
    }
    user = {
        'id': session['user_id']
    }

    return render_template('user/edit_user.html', user = User.get_by_id(user), wallet = User.get_wallet(data) )

@app.route('/edit/user/email/<int:id>')
def edit_email(id):
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'id': id
    }

    return render_template('user/edit_email.html', user = User.get_by_id(data))

@app.route('/update/email/<int:id>', methods = ['POST'])
def update_email(id):
    if 'user_id' not in session:
        return redirect('/')
    if not User.validate_email(request.form):
        return redirect(f'/edit/user/email/{id}')
    data = {
        'id': id,
        'email' : request.form['email']
    }
    User.update_user_email(data)
    return redirect('/user/home')

@app.route('/update/user/info/<int:id>', methods=['POST'])
def update_user(id):
    if 'user_id' not in session:
        return redirect('/')
    if not User.validate_user_info(request.form):
        return redirect(f'/edit/user/{id}')
    data = {
        'id': id,
        'user_name' : request.form['user_name'],
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        }
    
    User.update_user_info(data)
    return redirect('/user/home')


@app.route('/user/info')
def show_user_info():
    if 'user_id' not in session:
        return redirect('/')
        
    data = {
        'id': session['user_id']
    }
    
    return render_template('/user/show_user.html', user = User.get_by_id(data), wallet = User.get_wallet(data))



@app.route('/login', methods = ['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash('invalid credentials', 'login')
        return redirect('/existing/user')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('invalid credentials', 'login')
        return redirect('/existing/user')
    session['user_id'] = user.id
    return redirect('/user/home')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    
