import os
from flask import Flask, Blueprint, jsonify, request, render_template, redirect, url_for
from .settings import *
from .battle import run_battle
from flask_uploads import UploadSet

main = Blueprint('main', __name__, url_prefix=SITE_ROOT)
players = UploadSet('players', "py")

@main.route('/')
def index():
    players = [ (k,v) for k, v in run_battle().items() ]
    players = sorted(players, key=lambda p: p[1]["wins"] - p[1]["losses"],
            reverse=True)
    
    return render_template('index.html', players=players)



@main.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'player' in request.files:
        f = request.files['player'].filename
        dest = "/var/www/allumette/app/players/"+f
        if os.path.exists(dest):
            os.remove(dest)
        players.save(request.files['player'])
        return redirect(url_for("main.index"))
    return render_template('upload.html')
