from flask import Flask, request, redirect, render_template, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()
    posts = Post.query.all()
    print(posts)

@app.route('/')
def root():
    return redirect("/users")

@app.route('/users')
def users_index():
    users = User.query.all()
    print(users)
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=["GET"])
def users_new_form():
    return render_template('users/new.html')

@app.route("/users/new", methods=["POST"])
def users_new():
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>')
def users_show(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)

@app.route('/users/<int:user_id>/edit', methods = ["GET"])
def users_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

### post routes

@app.route('/users/<int:user_id>/posts/new', methods=["GET"])
def new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('posts/newpost.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_post(user_id):
    new_post = Post(
        title=request.form['title'],
        content=request.form['content'],
        user_id=user_id)
    
    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('users_show', user_id=user_id))

@app.route('/posts')
def posts_index():
    posts = Post.query.all()
    return render_template('posts/index.html', posts=posts)

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/showpost.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["GET"])
def posts_edit_form(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/editpost.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_edit(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    print(f"Edited Post ID: {post.id}, Title: {post.title}, Content: {post.content}")

    return redirect(url_for('show_post', post_id=post.id))

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    print(f"Deleted Post ID: {post.id}")

    return redirect(url_for('users_show', user_id=post.user_id))

if __name__ == '__main__':
    app.run(debug=True)
