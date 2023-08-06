from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from env import SECRET_KEY,DB_NAME

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_NAME
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
db = SQLAlchemy(app)
app.secret_key = SECRET_KEY

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    body = db.Column(db.String())

admin = Admin(app, name='ПАНЕЛЬ ПОСТОВ', template_mode='bootstrap3')
admin.add_view(ModelView(Post, db.session))

app.run()
