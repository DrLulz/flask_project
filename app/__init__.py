from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

#new
app.config['KEY'] = b'dudicle'

from app import views
