from flask_app import app
from flask_app.controllers import users_controller, topics_controllers,posts_controllers

if __name__=="__main__":
    app.run(debug=True)