from flask import Flask, render_template, flash, redirect, request, abort
#from flask import render_template, flash, redirect
import io
import os
import re
import sys
import json
import subprocess
import requests
import ipaddress

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
                flash( 'Prescribe: {}mg x {}'.format( n[0], str(n[1]) ) )
                
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


@app.route("/pull", methods=['POST'])
def pull():
    # Store the IP address blocks that github uses for hook requests.
    hook_blocks = requests.get('https://api.github.com/meta').json()['hooks']

    # Check if the POST request if from github.com
    for block in hook_blocks:
        ip = ipaddress.ip_address(u'%s' % request.remote_addr)
        if ipaddress.ip_address(ip) in ipaddress.ip_network(block):
            break  # the remote_addr is within the network range of github
    else:
        abort(403)

    if request.headers.get('X-GitHub-Event') == "ping":
        return json.dumps({'msg': 'Hi!'})
    if request.headers.get('X-GitHub-Event') != "push":
        return json.dumps({'msg': "wrong event type"})

    repos = json.loads(io.open('repos.json', 'r').read())

    payload = json.loads(request.data)
    repo_meta = {
        'name': payload['repository']['name'],
        'owner': payload['repository']['owner']['name'],
    }
    match = re.match(r"refs/heads/(?P<branch>.*)", payload['ref'])
    repo = None
    if match:
        repo_meta['branch'] = match.groupdict()['branch']
        repo = repos.get('{owner}/{name}/branch:{branch}'.format(**repo_meta), None)
    if repo is None:
        repo = repos.get('{owner}/{name}'.format(**repo_meta), None)
    if repo and repo.get('path', None):
        if repo.get('action', None):
            for action in repo['action']:
                subprocess.Popen(action,
                                 cwd=repo['path'])
        else:
            subprocess.Popen(["git", "pull", "origin", "master"],
                             cwd=repo['path'])
    return 'OK'
