"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """ User Table"""

    __tablename__='users'

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement= True)
    
    first_name = db.Column(db.String(25),
                           nullable = False
                           )
    
    last_name = db.Column(db.String(50),
                         nullable = False
                         )
    
    image_url = db.Column(db.String(),
                          default = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png'
                        )

    def __repr__(self):
        return f"<User {self.id} {self.first_name} {self.last_name} {self.image_url}>"

class Post(db.Model):
    """Post Table"""

    __tablename__='posts'

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement= True)
    
    title = db.Column(db.String(25),
                      nullable = False)
    
    content = db.Column(db.Text,
                        nullable = False)

    created_at = db.Column(db.DateTime,
                            nullable = False,
                            default= datetime.datetime.now)
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable = False)
    
    user = db.relationship('User', backref = 'posts')

    def __repr__(self):
        return f"<Post {self.id} {self.title} {self.content} {self.created_at}>" 