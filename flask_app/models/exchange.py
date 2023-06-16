from flask_app import app
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class Exchange: 

    def __init__(self, data):

        self.id = data['total_xp']
        self.total_xp = data['total_xp']
        self.total_xpcoin = data['total_xpcoin']
        self.total_lvlcoin = data['total_lvlcoin']
        self.total_dgcoin = data['total_dgcoin']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_info(data):
        query = 'SELECT * FROM exchange WHERE exchange.id = 1'

        results = connectToMySQL('test_schema').query_db(query)
        
        result = results[0]

        exchange_data = {
            'id': result['id'],
            'total_xp': result['total_xp'],
            'total_xpcoin': result['total_xpcoin'],
            'total_lvlcoin': result['total_lvlcoin'],
            'total_dgcoin': result['total_dgcoin'],
            'created_at': result['created_at'],
            'updated_at': result['updated_at']
        }

        exchange = Exchange(exchange_data)

        return exchange