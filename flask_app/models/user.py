from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.wallet import Wallet
from flask import flash
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:

    def __init__(self, data):

        self.id = data['id']
        self.user_name = data['user_name']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.wallet = None


    @staticmethod
    def validate_user(user):
        is_valid = True
        query_email = 'SELECT * FROM users WHERE email = %(email)s;'
        query_username = 'SELECT * FROM users WHERE user_name = %(user_name)s'
        results_email = connectToMySQL('test_schema').query_db(query_email, user)
        results_user = connectToMySQL('test_schema').query_db(query_username, user)


        if len(results_email) >= 1:
            flash("email is already in use.", "register")
            is_valid = False
        if len(results_user) >= 1:
            flash("username is already taken.", "register")
            is_valid = False
        if len(user['user_name']) <= 5:
            flash("Username must be 6 characters long", "register")
            is_valid = False
        if len(user['first_name']) <= 2:
            flash("First Name must be 3 characters or more.", "register")
            is_valid = False
        if len(user['last_name']) <= 2:
            flash("Last Name must be 3 characters or more", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("invalid email", "register")
            is_valid = False
        if len(user['password']) <= 7:
            flash("Invalid password", "register")
            is_valid = False
        if user['password'] != user['confirm']:
            flash('passwords do not match', "register")
            is_valid = False
        return is_valid
        

    @staticmethod
    def validate_user_info(user):
        is_valid = True
        query_username = 'SELECT * FROM users WHERE user_name = %(user_name)s'
        results = connectToMySQL('test_schema').query_db(query_username, user)
    
        if len(results) >= 1:
            flash("Username is already taken or is current Username", "update")
            is_valid = False
        if len(user['user_name']) <= 5:
            flash("Username must be 6 characters long", "update")
            is_valid = False
        if len(user['first_name']) <= 3:
            flash("First Name must be 3 characters or more.", "update")
            is_valid = False
        if len(user['last_name']) <= 3:
            flash("Last Name must be 3 characters or more", "update")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_email(user):
        is_valid = True
        query_email = 'SELECT * FROM users WHERE email = %(email)s'
        results_email = connectToMySQL('test_schema').query_db(query_email, user)

        if len(results_email) >= 1:
            flash("email is already in use or is current email", "email")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("invalid email", "email")
            is_valid = False
        return is_valid
    
    @classmethod
    def get_by_email(cls, data):
            query = 'SELECT * FROM users WHERE email = %(email)s;'

            results = connectToMySQL('test_schema').query_db(query, data)

            if len(results) < 1:
                return False

            return cls(results[0])
    
    @classmethod
    def update_user_email(cls, data):
        if not cls.validate_email(data):
            return False
        
        query = 'UPDATE users SET email = %(email)s WHERE id = %(id)s;'

        return connectToMySQL('test_schema').query_db(query, data)
        
    @classmethod
    def get_by_id(cls, data):
            query = 'SELECT * FROM users WHERE id = %(id)s;'

            results = connectToMySQL('test_schema').query_db(query, data)

            return cls(results[0])
        
    @classmethod
    def get_all(cls):
            query = 'SELECT * FROM users;'

            users_from_db = connectToMySQL('test_schema').query_db(query)

            users = []

            for user in users_from_db:
                users.append( cls(user))

                return users



        
    @classmethod
    def save(cls, data):
            query = 'INSERT INTO users (user_name, first_name, last_name, email,password, created_at, updated_at) VALUES (%(user_name)s, %(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());'

            return connectToMySQL('test_schema').query_db(query, data)
    
    @classmethod
    def update_user_info(cls, data):
        if not cls.validate_user_info(data):
            return False
        
        query = 'UPDATE users SET user_name = %(user_name)s, first_name = %(first_name)s, last_name = %(last_name)s WHERE id = %(id)s;'

        return connectToMySQL('test_schema').query_db(query, data)
    
    @classmethod
    def get_wallet(cls, data):
        query = 'SELECT * FROM users LEFT JOIN wallets ON users.id = wallets.wallet_user_id WHERE users.id = %(id)s; '

        results = connectToMySQL('test_schema').query_db(query, data)

        result = results[0]
        this_user = cls(result)

        wallet_data = {
            'id' : result['wallets.id'],
            'total_xp_earned' : result['total_xp_earned'],
            'usd_balance' : result['usd_balance'],
            'xp_balance' : result['xp_balance'],
            'xpcoin_balance' : result['xpcoin_balance'],
            'lvlcoin_balance' : result['lvlcoin_balance'],
            'dgcoin_balance' : result['dgcoin_balance'],
            'user_id' : result['wallet_user_id'],
            'created_at' : result['wallets.created_at'],
            'updated_at' : result['wallets.updated_at']

        }
        this_user.wallet = Wallet(wallet_data)

        return this_user
    
    @classmethod
    def get_total_xp(cls, data):
        query = 'SELECT * FROM users LEFT JOIN wallets ON users.id = wallets.wallet_user_id where users.id = wallets.wallet_user_id ORDER BY total_xp_earned DESC LIMIT 10'

        results = connectToMySQL('test_schema').query_db(query, data)

        all_results = []

        for row in results:
            user_wallet = Wallet({
            'id' : row['wallets.id'],
            'total_xp_earned' : row['total_xp_earned'],
            'usd_balance' : row['usd_balance'],
            'xp_balance' : row['xp_balance'],
            'xpcoin_balance' : row['xpcoin_balance'],
            'lvlcoin_balance' : row['lvlcoin_balance'],
            'dgcoin_balance' : row['dgcoin_balance'],
            'user_id' : row['wallet_user_id'],
            'created_at' : row['wallets.created_at'],
            'updated_at' : row['wallets.updated_at']
            })
            user = cls(row)
            user.wallet = user_wallet
            
            all_results.append(user)

        return all_results
    
    