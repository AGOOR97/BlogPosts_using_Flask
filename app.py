## Improt the Libraries
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


## Create an app and confiuration for database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

## Create the class (taking object for each class)
class BlogPost(db.Model):
    ## Create the structure of Database
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__ (self):   ## for what will be returned at terminal
        return f'Blog Post {self.id}'



## Route for Home page
@app.route('/')
def home():
    return render_template('index.html')

## Route for Posts page
@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_author = request.form['author']
        post_content = request.form['content']
        ## create object from the class
        new_post = BlogPost(title=post_title, author=post_author, content=post_content)
        db.session.add(new_post)  ## add to database
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.all()
        return render_template('posts.html', posts=all_posts)


## Route for delete posts
@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)  ## get the post acc. to id
    db.session.delete(post)  
    db.session.commit()
    return redirect('/posts')


## Route for editing posts
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)  # get the desired post
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()  ## commit to db
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)

## Route for creating new posts
@app.route('/posts/new', methods=['GET', 'POST'])
def new_posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_author = request.form['author']
        post_content = request.form['content']
        ## create object from the class
        new_post = BlogPost(title=post_title, author=post_author, content=post_content)
        db.session.add(new_post)  ## add to database
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_posts.html')

## Run the app
if __name__ == '__main__':
    app.run(debug=True)