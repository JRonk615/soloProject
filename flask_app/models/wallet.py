from flask_app import app
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL



class Wallet:
    

    def __init__(self, data):

        self.id = data['id']
        self.total_xp_earned = data['total_xp_earned']
        self.usd_balance = data['usd_balance']
        self.xp_balance = data['xp_balance']
        self.xpcoin_balance = data['xpcoin_balance']
        self.lvlcoin_balance = data['lvlcoin_balance']
        self.dgcoin_balance = data['dgcoin_balance']
        self.wallet_user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.earn_rate = 1000

    @classmethod
    def save(cls, data):

        query = 'INSERT INTO wallets (total_xp_earned,usd_balance, xp_balance, xpcoin_balance, lvlcoin_balance, dgcoin_balance, wallet_user_id, created_at, updated_at) VALUES (%(total_xp_earned)s,%(usd_balance)s, %(xp_balance)s, %(xpcoin_balance)s, %(lvlcoin_balance)s, %(dgcoin_balance)s, %(wallet_user_id)s, NOW(), NOW())'

        results = connectToMySQL('test_schema').query_db(query, data)

        return results
    
    @classmethod
    def get_wallet_by_id(cls, data):
        query = 'SELECT * FROM wallets WHERE wallets.id = %(id)s'

        results = connectToMySQL('test_schema').query_db(query, data)

        result = results[0]

        wallet_data = {
            'id' : result['id'],
            'total_xp_earned' : result['total_xp_earned'],
            'usd_balance' : result['usd_balance'] ,
            'xp_balance' : result['xp_balance'],
            'xpcoin_balance' : result['xpcoin_balance'],
            'lvlcoin_balance' : result['lvlcoin_balance'],
            'dgcoin_balance' : result['dgcoin_balance'],
            'user_id' : result['wallet_user_id'],
            'created_at' : result['created_at'],
            'updated_at' : result['updated_at']

        }
        this_wallet = Wallet(wallet_data)

        return this_wallet
    
    @classmethod
    def earn_xp(cls, data):
        query = 'UPDATE wallets SET xp_balance = (xp_balance + %(xp_balance)s), total_xp_earned = (total_xp_earned + %(total_xp_earned)s) WHERE wallets.id = %(id)s'
        exchange_query = 'UPDATE exchange SET total_xp = (total_xp + %(xp_balance)s) WHERE exchange.id = 1;'

        

        return connectToMySQL('test_schema').query_db(query, data), connectToMySQL('test_schema').query_db(exchange_query, data)
    
    @classmethod
    def earn_xpcoin(cls, data):
        is_valid = True

        query = 'SELECT * FROM wallets WHERE wallets.id = %(id)s'

        results = connectToMySQL('test_schema').query_db(query, data)

        result = results[0]

        wallet_data = {
            'id' : result['id'],
            'total_xp_earned' : result['total_xp_earned'],
            'usd_balance' : result['usd_balance'] ,
            'xp_balance' : result['xp_balance'],
            'xpcoin_balance' : result['xpcoin_balance'],
            'lvlcoin_balance' : result['lvlcoin_balance'],
            'dgcoin_balance' : result['dgcoin_balance'],
            'user_id' : result['wallet_user_id'],
            'created_at' : result['created_at'],
            'updated_at' : result['updated_at']

        }
        this_wallet = Wallet(wallet_data)

        if this_wallet.xp_balance < 10000:
            flash('10000 XP is required to swap for XPCoin', 'xpcoin')
            is_valid = False
            return is_valid
        else:
            query = 'UPDATE wallets SET xp_balance = (xp_balance - %(xp_balance)s), xpcoin_balance = (xpcoin_balance + 1000) WHERE wallets.id = %(id)s'
            exchange_query = 'UPDATE exchange SET total_xp = (total_xp - %(xp_balance)s), total_xpcoin = (total_xpcoin + 1000) WHERE exchange.id = 1'
            return connectToMySQL('test_schema').query_db(query, data),connectToMySQL('test_schema').query_db(exchange_query, data)
        
    @classmethod
    def earn_lvlcoin(cls, data):
        is_valid = True

        query = 'SELECT * FROM wallets WHERE wallets.id = %(id)s'

        results = connectToMySQL('test_schema').query_db(query, data)

        result = results[0]

        wallet_data = {
            'id' : result['id'],
            'total_xp_earned' : result['total_xp_earned'],
            'usd_balance' : result['usd_balance'] ,
            'xp_balance' : result['xp_balance'],
            'xpcoin_balance' : result['xpcoin_balance'],
            'lvlcoin_balance' : result['lvlcoin_balance'],
            'dgcoin_balance' : result['dgcoin_balance'],
            'user_id' : result['wallet_user_id'],
            'created_at' : result['created_at'],
            'updated_at' : result['updated_at']

        }
        this_wallet = Wallet(wallet_data)

        if this_wallet.xpcoin_balance < 1000:
            flash('1000 XPCoin is required to swap for LVLCoin', 'LVLCoin')
            is_valid = False
            return is_valid
        else:
            query = 'UPDATE wallets SET xpcoin_balance = (xpcoin_balance - %(xpcoin_balance)s), lvlcoin_balance = (lvlcoin_balance + 100) WHERE wallets.id = %(id)s'
            exchange_query = 'UPDATE exchange SET total_xpcoin = (total_xpcoin - %(xpcoin_balance)s), total_lvlcoin = (total_lvlcoin + 100) WHERE exchange.id = 1'
            return connectToMySQL('test_schema').query_db(query, data),connectToMySQL('test_schema').query_db(exchange_query, data)
        
    @classmethod
    def earn_dgccoin(cls, data):
        is_valid = True

        query = 'SELECT * FROM wallets WHERE wallets.id = %(id)s'

        results = connectToMySQL('test_schema').query_db(query, data)

        result = results[0]

        wallet_data = {
            'id' : result['id'],
            'total_xp_earned' : result['total_xp_earned'],
            'usd_balance' : result['usd_balance'] ,
            'xp_balance' : result['xp_balance'],
            'xpcoin_balance' : result['xpcoin_balance'],
            'lvlcoin_balance' : result['lvlcoin_balance'],
            'dgcoin_balance' : result['dgcoin_balance'],
            'user_id' : result['wallet_user_id'],
            'created_at' : result['created_at'],
            'updated_at' : result['updated_at']

        }
        this_wallet = Wallet(wallet_data)

        if this_wallet.lvlcoin_balance < 100:
            flash('100 LVLCoin is required to swap for DGCoin', 'DGCoin')
            is_valid = False
            return is_valid
        else:
            query = 'UPDATE wallets SET lvlcoin_balance = (lvlcoin_balance - %(lvlcoin_balance)s), dgcoin_balance = (dgcoin_balance + 1) WHERE wallets.id = %(id)s'
            exchange_query = 'UPDATE exchange SET total_lvlcoin = (total_lvlcoin - %(lvlcoin_balance)s), total_dgcoin = (total_dgcoin + 1) WHERE exchange.id = 1'
            
            return connectToMySQL('test_schema').query_db(query, data), connectToMySQL('test_schema').query_db(exchange_query, data)