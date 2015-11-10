from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm, TaperForm
from taper import Taper

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'user'}  # fake user
    posts = [  # fake array of posts
        { 
            'author': {'nickname': 'Faulkner'}, 
            'body': 'To say that Mr. Hollis is noncompliant is similar to saying that the surface of the sun is warm.' 
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)


@app.route('/taper', methods=['GET', 'POST'])
def taper():
    form = TaperForm()
    t = Taper()
    if form.validate_on_submit():
            args = {'1': {'dose': form.dose_1.data, 'time': form.time_1.data},
                    '2': {'dose': form.dose_2.data, 'time': form.time_2.data}
                    }
            
            # Display Input
            flash('Phase 1: Start Date={}, Days={}, Dose/Day={}'.format(form.date_1.data, form.time_1.data, form.dose_1.data))
            flash('Phase 2: Start Date={}, Days={}, Dose/Day={}'.format(form.date_2.data, form.time_2.data, form.dose_2.data))
            
            for n in t.calc(args):
                flash('Prescribe: Quantity-{} Dose-{}mg'.format(str(n[1]), n[0]))
                
            return redirect('/taper')
    return render_template('taper.html',
                            title='Drug Taper',
                            form=form,
                            sizes=app.config['PILL_SIZES'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html', 
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])