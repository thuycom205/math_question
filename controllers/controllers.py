# -*- coding: utf-8 -*-
from odoo import http
import logging
import json
from odoo.http import request

class AwsQuestion(http.Controller):
    @http.route('/aws_question/exam_header',type='json', auth='public')
    def index(self, **kw):
        ob = request.env.ref('aws_question.aws_question_abandoned_cart_onboarding_panel')
        html = ob.render({
            'company': 'company',
        })

        return {
            'html': html
        }

    @http.route('/aws_question/aws_question/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('aws_question.listing', {
            'root': '/aws_question/aws_question',
            'objects': http.request.env['aws_question.aws_question'].search([]),
        })

    @http.route('/aws_question/aws_question/objects/<model("aws_question.aws_question"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('aws_question.object', {
            'object': obj
        })
