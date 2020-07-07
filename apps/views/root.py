# -*- coding: utf-8 -*-
import os

from flask import Blueprint, render_template, send_from_directory


bp = Blueprint('root', __name__, url_prefix='')

current_dir = os.path.abspath(os.path.dirname(__file__))
current_dir = current_dir.replace('views', '')


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(current_dir + '/static', 'favicon.ico')


@bp.route('/dffx')
def dffx():
    return send_from_directory(current_dir + '/static', 'file/RamPos+Bounce_66_[SIXVFX].ffx', as_attachment=True)
