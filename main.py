from flask import request, redirect, render_template, session, flash
#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import cgi
from app import app, db  
from models import User, Blog


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = User.query.filter_by(username=username)
        if users.count() == 1:
            user = users.first()
            if password == user.password:
                session['user'] = user.username
                flash('welcome back, '+user.username)
                return redirect("/newpost")
            else:
                flash('bad password')
        else:
            flash('bad username')
        return redirect("/login")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        if username == '' or password == '' or verify == '':
            flash('no field on this page can be blank')
            return redirect('/signup')
        user_db_count = User.query.filter_by(username=username).count()
        if user_db_count > 0:
            flash(username + ' is already a registered user')
            return redirect('/signup')
        if password != verify:
            flash('passwords did not match')
            return redirect('/signup')
        if len(password) < 4:
            flash('password is too short')
            return redirect('/signup')
        if len(username) < 4:
            flash('username is too short')
            return redirect('/signup')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        session['user'] = user.username
        return redirect("/")
    else:
        return render_template('signup.html')

@app.route("/logout", methods=['POST'])
def logout():
    del session['user']
    return redirect("/blog")


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    posts = Blog.query.order_by('id DESC').all()
    blogid = request.args.get('id')
    userid = request.args.get('userid')

    if blogid: #!= None:
        blogpost = Blog.query.filter_by(id=blogid).first()
        #if request.method == 'POST':
        #    blogpost.title == new_title
        #    blogpost.body == new_body

        print(blogpost.title)
        print(blogpost.body)
        return render_template('blog.html',blogid=blogpost.id, title=blogpost.title, body=blogpost.body, date=blogpost.date, owner=blogpost.owner.username)

    if userid: #!= None:
        blogs = Blog.query.filter_by(owner_id=userid).all()
        user = User.query.filter_by(id=userid).first()
        return render_template('singleUser.html', posts=blogs, username=user.username, pagetitle=user.username+"'s Posts")
        #return render_template('blog.html', blogid=blogs.id, title=blogs.title, body=blogs.body, date=blogs.date, owner=blogs.owner.username)

    return render_template('blog.html', posts=posts, pagetitle="Build-A-Blog")

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if request.method == 'POST':
        #pull blog information from form, save in variables
        title = request.form['title']
        body = request.form['body']
        if title == "" and body == "":
            return render_template('newpost.html', pagetitle="New Post")
        if title == "":
            error = "Title can't be blank"
            return render_template('newpost.html', body=body, error_msg=error)
        if body == "":
            error = "Body can't be blank"
            return render_template('newpost.html', title=title, error_msg=error)
        #create a new post using the Blog class
        newpost = Blog(title, body, logged_in_user())
        #add the blog post to the database, which needs title and body
        db.session.add(newpost)
        db.session.commit()
        lastid = Blog.query.order_by('id DESC').first()
        return redirect('/blog?id='+str(lastid.id))
    
    return render_template('newpost.html', pagetitle="New Post")


@app.route('/')
def index():
    users = User.query.order_by('username ASC').all()
    return render_template('index.html', users=users)

# def reroute():
#     return redirect('/blog')

def logged_in_user():
    owner = User.query.filter_by(username=session['user']).first()
    return owner

endpoints_without_login = ['index', 'login', 'signup', 'reroute', 'blog', 'static']

@app.before_request
def require_login():
    if not ('user' in session or request.endpoint in endpoints_without_login):
        flash('you must be logged in to complete that action')
        return redirect('/login')

app.secret_key = 'WOWweEEILoFELauncerCODERItsMYfavorIETCLase'

if __name__ == "__main__":
    app.run()