from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, DateField, IntegerField
from wtforms.validators import DataRequired
from datetime import date

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    
class TaperForm(Form):
    start_date = DateField('Start Date', format='%m/%d/%Y', default=date.today, validators=[DataRequired()])
    duration = IntegerField('Duration', validators=[DataRequired()])
    pill_size = IntegerField('Dose', validators=[DataRequired()])