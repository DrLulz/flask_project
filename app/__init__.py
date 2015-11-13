from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

#new
app.config['KEY'] = b'dudicle'
webhooks = HookRoutes()
app.register_blueprint(webhooks)

@webhooks.hook('ping')
def ping(data, guid):
    return 'pong'
    
    
from app import views
