from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import topics
from flask import flash

class Post:
    def __init__(self, data):
        self.id = data['id']
        self.description = data['description']
        self.number = data['number']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.topic_id = data['topic_id']
        self.user = None

    @classmethod
    def create_post(cls, data):
        query = "INSERT INTO posts (description, number, date, user_id, topic_id) VALUES (%(description)s, %(number)s, %(date)s, %(user_id)s, %(topic_id)s)"
        return connectToMySQL('personal_project_schema').query_db( query, data)
    
    @classmethod
    def edit_post(cls, data):
        query= "UPDATE posts SET description=%(description)s,number=%(number)s,date=%(date)s WHERE id = %(id)s;"
        return connectToMySQL('personal_project_schema').query_db(query,data)
    
    @classmethod
    def show_one_post(cls, data):
        query = """
        SELECT * FROM posts
        LEFT JOIN topics
        ON topics.id = posts.topic_id
        WHERE posts.id = %(id)s;
        """
        results = connectToMySQL('personal_project_schema').query_db(query,data)
        if results:
            this_post = cls(results[0])
            topic_data = {
                **results[0],
                'id' : results[0]['topics.id'],
                'created_at' : results[0]['topics.created_at'],
                'updated_at' : results[0]['topics.updated_at']
            }
            this_topic = topics.Topic(topic_data)
            this_post.topic = this_topic
            return this_post
        return False
    

    @classmethod
    def delete(cls, data):
        query = """
            DELETE FROM posts WHERE id = %(id)s;
            """
        
        return connectToMySQL('personal_project_schema').query_db(query, data)

