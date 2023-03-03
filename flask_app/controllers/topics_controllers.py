from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.posts import Post
from flask_app.models.topics import Topic
from flask import flash

# =======================================topic render
@app.route('/topic/<int:id>')
def topic_page(id):
    if 'user_id' not in session:
        return redirect('/')
    return render_template('topic_page.html', topic = Topic.get_all_posts({'id' : id}))

@app.route('/post/delete/<int:topic_id>/<int:post_id>')
def delete_post(topic_id, post_id):

    Post.delete({'id' : post_id})
    return redirect(f'/topic/{topic_id}')