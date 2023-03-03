from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import posts, user
from flask import flash

class Topic:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posts = []

    @classmethod
    def all_topics(cls):
        query = """
        SELECT * FROM topics;
        """
        all_topics = []
        result = connectToMySQL('personal_project_schema').query_db(query)
        for row in result:
            all_topics.append(cls(row))
        return all_topics
    
    @classmethod
    def one_topic(cls,data):
        query = """
        SELECT * FROM topics
        WHERE topics.id = %(id)s;
        """
        result =  connectToMySQL('personal_project_schema').query_db(query, data)
        if result:
            return cls(result[0])
        return False
    
    @classmethod
    def get_all_posts(cls, data):
        query = """
        SELECT * FROM topics
        LEFT JOIN posts
        ON topics.id = posts.topic_id
        LEFT JOIN users
        ON users.id = posts.user_id
        WHERE topics.id = %(id)s;
        """

        results = connectToMySQL('personal_project_schema').query_db(query,data)
        if results:
            this_topic = cls(results[0])
            for row in results:
                # this_topic = cls(results[0])
                users_data = {
                    **row,
                    'id' : row['users.id'],
                    'created_at' : row['users.created_at'],
                    'updated_at' : row['users.updated_at']
                }
                posts_data = {
                    **row,
                    'id' : row['posts.id'],
                    'description' : row['posts.description'],
                    'created_at' : row['posts.created_at'],
                    'updated_at' : row['posts.updated_at']
                }
                this_post = posts.Post(posts_data)
                this_post.user = user.User(users_data)
                this_topic.posts.append(this_post)
            return this_topic
        return False
