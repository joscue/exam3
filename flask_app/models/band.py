from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Mag:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM magazines
                JOIN users on magazines.user_id = users.id;
                """
        results = connectToMySQL('exam_magazines').query_db(query)
        magazines = []
        for row in results:
            this_magazine = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            this_magazine.creator = user.User(user_data)
            magazines.append(this_magazine)
        return magazines
    @classmethod
    def save(cls, data):
        query = "INSERT INTO magazines ( name, description, user_id, created_at, updated_at ) VALUES ( %(name)s , %(description)s , %(user_id)s , NOW() , NOW() );"
        return connectToMySQL('exam_magazines').query_db( query, data )
    
    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM magazines
                JOIN users on magazines.user_id = users.id
                WHERE magazines.id = %(id)s;
                """
        result = connectToMySQL('exam_magazines').query_db(query,data)
        if not result:
            return False
        result = result[0]
        this_magazine = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        this_magazine.creator = user.User(user_data)
        return this_magazine
    
    @classmethod 
    def get_by_user(cls,data):
        query = "SELECT * FROM magazines WHERE user_id  = %(id)s;"
        result = connectToMySQL('exam_magazines').query_db(query,data)
        mags = []
        for row in result:
            mags.append( cls(row) )
        return mags
    
    @classmethod
    def  delete(cls,data):
        query = "DELETE FROM magazines WHERE id = %(id)s"
        return connectToMySQL('exam_magazines').query_db(query,data)
    
    @staticmethod
    def validate_mag(mag):
        is_valid = True
        if len(mag['name']) < 2:
            flash("Title must be at least 2 characters","retry")
            is_valid = False
        if len(mag['description'])  < 10:
            flash("Description must be at least 10 characters")
            is_valid = False
        return is_valid