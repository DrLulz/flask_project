from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, DateField, IntegerField
from wtforms.validators import DataRequired
from datetime import date

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    
class TaperForm(Form):
    date_1 = DateField('Start Date', format='%m/%d/%Y', default=date.today, validators=[DataRequired()])
    time_1 = IntegerField('Duration', validators=[DataRequired()])
    dose_1 = IntegerField('Dose', validators=[DataRequired()])
    date_2 = DateField('Start Date', format='%m/%d/%Y', default=date.today, validators=[DataRequired()])
    time_2 = IntegerField('Duration', validators=[DataRequired()])
    dose_2 = IntegerField('Dose', validators=[DataRequired()])