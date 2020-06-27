# -*- coding: utf-8 -*-

from odoo import models, fields, api,tools, _

class aws_axam_attemp(models.Model):
    _name = 'aws_question.aws_exam_attemp'
    _description = 'exam attemp'

    name = fields.Char()
    user_id = fields.Many2one('res.partner', string='User ID')
    exam_id = fields.Many2one('aws_question.aws_exam', string='Exam')

class aws_exam_attemp_question(models.Model):
    _name = 'aws_question.aws_exam_attemp_question'
    _description = 'exam attemp question'

    name = fields.Char()
    question_id = fields.Many2one('aws_question.aws_question', string='question')
    is_correct = fields.Boolean(string='Is correct')

    answer = fields.Text(string= 'Answer')
    comment = fields.Text(string = 'Comment')

class aws_exam(models.Model):
    _name = 'aws_question.aws_exam'
    _description = 'exam'

    name = fields.Char()

    is_topic = fields.Boolean(
        string='Topic',
        default=True)

    description = fields.Text()
    question_ids = fields.One2many('aws_question.aws_question' , 'exam_id', string='Question')


class aws_question(models.Model):
    _name = 'aws_question.aws_question'
    _description = 'question'

    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char(default='question')
    question = fields.Text(string="Question")
    answer = fields.Text(string="Answer")
    note = fields.Html(string = "Note")
    incorrect_count = fields.Integer(string="InCorrect count")
    description = fields.Text()

    exam_id = fields.Many2one('aws_question.aws_exam', string='Exam')
    priority_id = fields.Many2one('aws_question.aws_priority', string='Priority')
    tags_ids = fields.Many2many(string="Tags", comodel_name='aws_question.aws_tag',)




class aws_tag(models.Model):
    _name = 'aws_question.aws_tag'
    _description = 'aws_question.tag'

    name = fields.Char()
    question_ids = fields.Many2many(string="Question", comodel_name='aws_question.aws_question')

    description = fields.Text()

class aws_priority(models.Model):
    _name = 'aws_question.aws_priority'
    _description = 'aws_question.aws_priority'

    priority = fields.Integer(string="Priority")
    question_ids = fields.One2many('aws_question.aws_question' , 'priority_id', string='Question')

    def name_get(self):
        return [(seniority.id, str(seniority.priority)) for seniority in self]




