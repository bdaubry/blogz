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
        email = request.form['email']
        password = request.form['password']
        users = User.query.filter_by(email=email)
        if users.count() == 1:
            user = users.first()
            if password == user.password:
                session['user'] = user.email
                flash('welcome back, '+user.email)
                return redirect("/")
        flash('bad username or password')
        return redirect("/login")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        if not is_email(email):
            flash('zoiks! "' + email + '" does not seem like an email address')
            return redirect('/register')
        email_db_count = User.query.filter_by(email=email).count()
        if email_db_count > 0:
            flash('yikes! "' + email + '" is already taken and password reminders are not implemented')
            return redirect('/register')
        if password != verify:
            flash('passwords did not match')
            return redirect('/register')
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        session['user'] = user.email
        return redirect("/")
    else:
        return render_template('register.html')

def is_email(string):
    # for our purposes, an email string has an '@' followed by a '.'
    # there is an embedded language called 'regular expression' that would crunch this implementation down
    # to a one-liner, but we'll keep it simple:
    atsign_index = string.find('@')
    atsign_present = atsign_index >= 0
    if not atsign_present:
        return False
    else:
        domain_dot_index = string.find('.', atsign_index)
        domain_dot_present = domain_dot_index >= 0
        return domain_dot_present

@app.route("/logout", methods=['POST'])
def logout():
    del session['user']
    return redirect("/")


@app.route('/blog', methods=['GET', 'POST'])
def index():
    posts = Blog.query.order_by('id DESC').all()
    blogid = request.args.get('id')

    if blogid != None:
        blogpost = Blog.query.filter_by(id=blogid).first()
        #if request.method == 'POST':
        #    blogpost.title == new_title
        #    blogpost.body == new_body

        print(blogpost.title)
        print(blogpost.body)
        return render_template('blog.html',blogid=blogpost.id, title=blogpost.title, body=blogpost.body, date=blogpost.date)

        


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
        newpost = Blog(title, body)
        #add the blog post to the database, which needs title and body
        db.session.add(newpost)
        db.session.commit()
        lastid = Blog.query.order_by('id DESC').first()
        return redirect('/blog?id='+str(lastid.id))
    
    return render_template('newpost.html', pagetitle="New Post")

@app.route('/')
def reroute():
    return redirect('/blog')

def logged_in_user():
    owner = User.query.filter_by(email=session['user']).first()
    return owner.id

endpoints_without_login = ['login', 'register']

@app.before_request
def require_login():
    if not ('user' in session or request.endpoint in endpoints_without_login):
        return redirect("/login")

app.secret_key = 'WOWweEEILoFELauncerCODERItsMYfavorIETCLase'

if __name__ == "__main__":
    app.run()