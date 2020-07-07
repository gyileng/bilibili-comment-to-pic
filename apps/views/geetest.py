# -*- coding: utf-8 -*-
from flask import Blueprint, request, session

from apps import result
from apps.common.geetest import GeetestLib

bp = Blueprint('geetest', __name__, url_prefix='/api/geetest')


@bp.route('/captcha', methods=["GET"])
def captcha():
    gt = GeetestLib()
    status = gt.pre_process()
    session[gt.GT_STATUS_SESSION_KEY] = status
    response_str = gt.get_response_str()
    return result.from_data(response_str)


@bp.route('/validate', methods=["POST"])
def geetest_validate():
    content = request.json or {}
    gt = GeetestLib()
    challenge = content.get(gt.FN_CHALLENGE, None)
    validate = content.get(gt.FN_VALIDATE, None)
    seccode = content.get(gt.FN_SECCODE, None)
    ret = gt.failback_validate(challenge, validate, seccode)
    ret = {"status": "success"} if ret else {"status": "fail"}
    return result.from_data(ret)
