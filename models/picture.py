# -*- coding: utf-8 -*-

from odoo import models, fields, api,tools, _

class aws_axam_attemp(models.Model):
    _name = 'picture_question.aws_exam_attemp'
    _description = 'exam attemp'
    user_id = fields.Many2one('res.partner', string='User ID')
    exam_id = fields.Many2one('picture_question.aws_exam', string = 'Exam ID')
    finished_in_x_minutue = fields.Integer(string='finish in x minute')
    question_ids = fields.One2many('picture_question.aws_exam_attemp_question' ,'exam_id', string='Questions')

class aws_exam_attemp_question(models.Model):
    _name = 'picture_question.aws_exam_attemp_question'
    _description = 'exam attemp question'
    myquestion_id = fields.Many2one('picture_question.aws_exam_question', string='Question ID')
    is_correct = fields.Boolean(string="Is correct")
    answer = fields.Text(string="Answer")
    exam_id = fields.Many2one('picture_question.aws_exam_attemp' , string='Exam')



class aws_exam_question(models.Model):
    _name = 'picture_question.aws_exam_question'
    name = fields.Char()
    picture = fields.Html(string='Picture' )
    answer = fields.Text(string='Answer')
    score = fields.Integer(string='Score')
    is_correct = fields.Boolean(string='Is correct')
    exam_id = fields.Many2one('picture_question.aws_exam', string='Exam ID')
    question_id = fields.Many2one('picture_question.picture_question', string='Question ID')

    attemp_ids = fields.One2many('picture_question.aws_exam_attemp_question','myquestion_id' , string= 'Attemp IDS')


    def _compute_worked_hours(self):
        for question in self:
            if question.question_id:
                picture = question.question_id.picture_id.picture
                question.picture = picture
            else:
                question.picture = False
    def next_question(self):
        answer = self.answer

        questionidarr = self.env.context['qid']
        attemp_id = self.env.context['exam_attemp']
        myid = self.id

        question_attemp = self.env['picture_question.aws_exam_attemp_question'].search([('exam_id', '=', attemp_id),('myquestion_id', '=', myid)])

        if question_attemp:
            for qattem in question_attemp:
                qattem.write({'answer' : answer})


        x = myid + 1
        action = {
            'name': _('Question'),
            'type': 'ir.actions.act_window',
            'res_model': 'picture_question.aws_exam_question',
        }

        action['context'] = {'form_view_initial_mode': 'edit','qid' : questionidarr, 'exam_attemp' : attemp_id}

        action.update({
            'view_mode': 'form',
            'res_id': x,
        })

        return action


class aws_exam(models.Model):
    _name = 'picture_question.aws_exam'
    _description = 'exam'

    name = fields.Char()
    user_attemp_id = fields.One2many('picture_question.aws_exam_attemp' , 'exam_id', string='Picture')

    is_topic = fields.Boolean(
        string='Topic',
        default=True)

    description = fields.Text()
    active_domain = fields.Text('Active domain', readonly=True)
    question_ids = fields.Many2many('picture_question.picture_question' , string='Question')
    picture_ids = fields.One2many('picture_question.picture_illu' , 'exam_id', string='Picture')
    score = fields.Integer(string='Total Score')

    my_question_ids = fields.One2many('picture_question.aws_exam_question' , 'exam_id', string='Question')


    def take_exam(self):
        active_id = self.env.context.get('active_id')
        amyid = self.env.context.get('id')
        self.ensure_one()
        myids = self.ids
        myid = self.id
        x = 1

        #create exam attemp for user
        user_exam_vals = {}
        user_exam_vals['user_id'] = self.env.uid
        user_exam_vals['exam_id'] = myid

        exam_attempt = self.env['picture_question.aws_exam_attemp'].create(user_exam_vals)

        # End of create attemp

        #Create questions for attemp exam

        for exam in self:
            myquestion_ids = exam['my_question_ids']
            array_question = []
            array_question_attempt = []

            for questionId in myquestion_ids:
                x = questionId['id']
                array_question.append(x)

                question_attempt_val  = {}
                question_attempt_val['exam_id'] = exam_attempt.id
                question_attempt_val['myquestion_id'] = x
                array_question_attempt.append(question_attempt_val)

            exam_attempt_question = self.env['picture_question.aws_exam_attemp_question'].create(array_question_attempt)

        action = {
            'name': _('Debit Notes'),
            'type': 'ir.actions.act_window',
            'res_model': 'picture_question.aws_exam_question',
            }
        action['context'] = {'form_view_initial_mode': 'edit' , 'qid' : array_question, 'exam_attemp' : exam_attempt.id}

        action.update({
            'view_mode': 'form',
            'res_id': array_question[0],
        })

        return action



    @api.model
    def create(self, vals):
        if vals['picture_ids']:
            question_id_arr = []
            for pic_id in vals['picture_ids']:
                picObj = self.env['picture_question.picture_illu'].browse(pic_id[1])
                question_ids = picObj['question_ids']
                # question_id_int = []
                for questionId in question_ids:
                    question_id_arr.append(questionId['id'])




                # question_id_arr.append(question_ids)
            q_f= [6,False, question_id_arr]
            q_s = []
            q_s.append(q_f)
            vals['question_ids'] = q_s
            result = super(aws_exam, self).create(vals)

            for qu_id in question_id_arr:
                # create question object
                question_vals = {}
                resultId = result['id']
                question_vals['exam_id'] =result['id']
                question_vals['question_id'] =qu_id
                picIllus = self.env['picture_question.picture_question'].browse(qu_id).picture_id
                html = picIllus['picture']
                question_vals['picture'] = html
                self.env['picture_question.aws_exam_question'].create(question_vals)
            return  result;


        else:
            x = 1
            return super(aws_exam, self).create(vals)
        return super(aws_exam, self).create(vals)


    def write(self, vals):
        if vals['picture_ids']:
            question_id_arr = []
            for pic_id in vals['picture_ids']:
                picObj = self.env['picture_question.picture_illu'].browse(pic_id)
                question_ids = picObj['question_ids']
                question_id_arr.append(question_ids)
            vals['question_ids'] = question_id_arr
            return super(aws_exam, self).write(vals)
        else:
            x = 1
            return super(aws_exam, self).write(vals)



class picture_illustration(models.Model):
    _name = 'picture_question.picture_illu'
    _description = 'picture question'
    name = fields.Char()
    picture = fields.Html(string = "picture")
    question_ids = fields.One2many('picture_question.picture_question' , 'picture_id', string='Picture')
    exam_id = fields.Many2one('picture_question.aws_exam', string='Exam')


    def action_create_picture_exam(self):
        x =1
        # for order in self:
        composer_form_view_id = self.env.ref('aws_question.aws_question_picture_exam_form').id


        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'picture_question.aws_exam',
            'view_id': composer_form_view_id,
            'target': 'new',
            'context': {
                'default_picture_ids': self.ids,
            },
        }

class picture_question(models.Model):
    _name = 'picture_question.picture_question'
    _description = 'question'

    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char(default='question')
    question = fields.Text(string="Question")
    answer = fields.Text(string="Answer")
    note = fields.Html(string = "Note")
    incorrect_count = fields.Integer(string="InCorrect count")
    description = fields.Text()

    exam_id = fields.Many2one('picture_question.aws_exam', string='Exam')
    picture_id = fields.Many2one('picture_question.picture_illu', string='Picture')
    priority_id = fields.Many2one('picture_question.aws_priority', string='Priority')
    tags_ids = fields.Many2many(string="Tags", comodel_name='picture_question.aws_tag',)

    my_question_ids = fields.One2many('picture_question.aws_exam_question' , 'question_id', string='Question In Exam')


class aws_question_compose_exam(models.TransientModel):
    _name = 'aws_question.compose.exam'
    use_active_domain = fields.Boolean('Use active domain')
    active_domain = fields.Text('Active domain', readonly=True)

class aws_tag(models.Model):
    _name = 'picture_question.aws_tag'
    _description = 'picture_question.tag'

    name = fields.Char()
    question_ids = fields.Many2many(string="Question", comodel_name='picture_question.picture_question')

    description = fields.Text()

class aws_priority(models.Model):
    _name = 'picture_question.aws_priority'
    _description = 'picture_question.aws_priority'

    priority = fields.Integer(string="Priority")
    question_ids = fields.One2many('picture_question.picture_question' , 'priority_id', string='Question')

    def name_get(self):
        return [(seniority.id, str(seniority.priority)) for seniority in self]




