from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.posts import Post
from flask_app.models.topics import Topic
from flask import flash


# ===================================================Post render/action
@app.route('/post/<int:id>')
def post_template(id):
    if 'user_id' not in session:
        return redirect('/')
    return render_template('post.html', topic = Topic.one_topic({'id': id}))

@app.route('/create/post/<int:topic_id>', methods=['POST'])
def create_post(topic_id):


    data = {
        **request.form,
        "user_id": session['user_id'],
        "topic_id": topic_id,
    }
    Post.create_post(data)
    return redirect(f'/topic/{topic_id}')

# =====================================================Edit Render/Action

@app.route('/edit/<int:post_id>')
def render_edit(post_id):
    if 'user_id' not in session:
        return redirect('/')
    return render_template('edit.html', post = Post.show_one_post({'id' : post_id}))

@app.route('/edit/post/<int:topic_id>/<int:post_id>', methods=['POST'])
def edit_post(topic_id, post_id):

    Post.edit_post({**request.form, 'id':post_id})
    return redirect(f'/topic/{topic_id}')
