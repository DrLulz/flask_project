from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, DateField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    
class TaperForm(Form):
    start_date = DateField('Start Date', format='%m/%d/%Y')
    duration = IntegerField('Duration')
    pill_size = IntegerField('Pill Size')