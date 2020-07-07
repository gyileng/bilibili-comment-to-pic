# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify

bp = Blueprint('login', __name__, url_prefix='/login')


@bp.route('', methods=['POST'])
def login():
    return jsonify('hello')
