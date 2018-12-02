from app import db

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=False) 
    body = db.Column(db.Text(), unique=False)
    date = db.Column(db.DateTime, unique=False)
    owner = db.Column(db.Integer, unique=False)

    def __init__(self, title, body, owner_id):
        self.title = title
        self.body = body
        self.date = func.now()
        self.owner_id = owner_id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.email