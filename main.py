from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:jamal@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    body = db.Column(db.String(800))


    def __init__(self, title, body):
        self.title = title 
        self.body = body


@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog')
def blog():
    single = request.args.get('id')
    if not single:
        blog = Blog.query.all()
        return render_template('blogs.html',title="Building a Blog", posts=blog)
    else:
        single = int(single)
        blog = Blog.query.filter_by(id=single).all()
        print(blog)
        return render_template('blog_one.html',title="Building a Blog", heading_top=blog, posts=blog)



@app.route('/newpost', methods=['POST','GET'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if not title or not body:
            flash('Please make sure you\'ve entered data in both fields.')
            return render_template('newpost.html', heading_top="Add a Blog Entry")
        blogpost = Blog(title, body)
        db.session.add(blogpost)
        db.session.commit()
        print(blogpost.id)
        return redirect('/blog?id={0}'.format(blogpost.id))

    return render_template('newpost.html', heading_top="Add a Blog Entry")
    
@app.route('/blog_one')
def single_blog():
    return render_template('blog_one.html')

if __name__ == '__main__':
    app.run()