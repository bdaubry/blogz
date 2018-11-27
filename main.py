from flask import request, redirect, render_template, session, flash
#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import cgi
from app import app, db  
from models import User, Blog

@app.route('/')
def reroute():
    return redirect('/blog')

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


if __name__ == "__main__":
    app.run()