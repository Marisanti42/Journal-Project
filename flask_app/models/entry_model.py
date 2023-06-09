from flask_app.config.mysqlconnnection import connectToMySQL
from flask_app.models import user_model
from flask import flash

class Entry:
    db = "notebook_schema"

    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.content = data['content']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner = None

#CREATE
    @classmethod
    def new_entry(cls,data):
        query="""INSERT INTO entries(title, content, user_id)
        VALUES (%(title)s, %(content)s, %(user_id)s);"""
        results = connectToMySQL(cls.db).query_db(query,data)
        return results

#READ
    @classmethod
    def get_all_entries(cls):
        query="SELECT * FROM entries LEFT JOIN users ON entries.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        if not results:
            return []
        print("**********************")
        print(results)
        entry = []
        this_entry = None
        for row in results:
            if this_entry == None or this_entry.id != row['id']:
                this_entry = cls(row)
                data = {
                    'id':row["users.id"],
                    'first_name':row["first_name"],
                    'last_name':row["last_name"],
                    'email':row["email"],
                    'password':row["password"],
                    'created_at':row["users.created_at"],
                    'updated_at':row["users.updated_at"]
                }
                this_entry.owner = user_model.User(data)
                entry.append(this_entry)
        return entry

    @classmethod
    def view_entry(cls,id):
        data = {"id":id}
        query = """SELECT * FROM entries
        LEFT JOIN users ON entries.user_id = users.id
        WHERE entries.id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        this_entry = cls(results[0])
        data = {
            'id':results[0]["users.id"],
            'first_name':results[0]["first_name"],
            'last_name':results[0]["last_name"],
            'email':results[0]["email"],
            'password':results[0]["password"],
            'created_at':results[0]["users.created_at"],
            'updated_at':results[0]["users.updated_at"]
        }
        this_owner = user_model.User(data)
        this_entry.owner = this_owner
        print(this_entry)
        return this_entry
    
#validiate entry
    @staticmethod
    def validate_entry(entry):
        print(entry)
        is_valid=True
        if len(entry['title']) < 2:
            flash("Title must contain at least 2 characters.")
            is_valid = False
        if len(entry['content']) < 2:
            flash("Entry must contain at least 2 characters.")
            is_valid = False
        return is_valid
    
#UPDATE
    @classmethod
    def update_entry(cls,data):
        query = """UPDATE entries SET
        title = %(title)s,
        content = %(content)s,
        updated_at = %(updated_at)s
        WHERE id = %(id)s
        AND entry.user_id = %(user_id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
    
#DELETE
    @classmethod
    def delete_entry(cls,id):
        data = {'id':id}
        query = "DELETE FROM  entries WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
    