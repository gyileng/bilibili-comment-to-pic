# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request, session

from apps import result
from apps.spiders.bilibili_comment import Bilibili

bp = Blueprint('bilibili', __name__, url_prefix='/api/bilibili')


@bp.route('/comments', methods=['POST'])
def comments():
    status = session.get('gt_server_status', None)
    if not status:
        return result.from_data(status)

    content = request.json or {}
    bv = content.get('bv', '')
    if not bv:
        return jsonify('error')
    bi = Bilibili(bv)
    comments, bv_title = bi.start_task()
    return result.from_data({'comments': comments, 'bv_title': bv_title})
