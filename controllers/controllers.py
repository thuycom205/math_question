# -*- coding: utf-8 -*-
# from odoo import http


# class AwsQuestion(http.Controller):
#     @http.route('/aws_question/aws_question/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/aws_question/aws_question/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('aws_question.listing', {
#             'root': '/aws_question/aws_question',
#             'objects': http.request.env['aws_question.aws_question'].search([]),
#         })

#     @http.route('/aws_question/aws_question/objects/<model("aws_question.aws_question"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('aws_question.object', {
#             'object': obj
#         })
