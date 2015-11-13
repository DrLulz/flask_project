from flask import Flask
from hookserver import HookRoutes

app = Flask(__name__)
app.config.from_object('config')

#new
webhooks = HookRoutes()
app.register_blueprint(webhooks)
    
    
from app import views
