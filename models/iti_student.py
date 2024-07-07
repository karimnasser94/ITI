from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ItiStudent(models.Model):
    _name = 'iti.student.bns'

    name = fields.Char(required=True)
    email = fields.Char()
    birth_date = fields.Date()
    salary = fields.Float()
    tax = fields.Float(compute="calc_salary")
    net_salary = fields.Float(compute="calc_salary")
    address = fields.Text()
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female')]
    )
    accepted = fields.Boolean()
    level = fields.Integer()
    image = fields.Binary()
    cv = fields.Html()
    login_time = fields.Datetime()
    track_id = fields.Many2one('iti.track.bns')
    track_capacity = fields.Integer(related='track_id.capacity')
    skills_ids = fields.Many2many('iti.skills.bns')
    state = fields.Selection([
        ('applied', 'Applied'),
        ('first', 'First Interview'),
        ('second', 'Second Interview'),
        ('passed', 'Passed'),
        ('rejected', 'Rejected'),

    ], default='applied')

    @api.depends("salary")
    def calc_salary(self):
        for rec in self:
            rec.tax = rec.salary * 0.20
            rec.net_salary = rec.salary - rec.tax

    _sql_constraints = [
        ('unique_name', 'UNIQUE(email)', 'email Already Exist'),

    ]

    @api.constrains("salary")
    def change_salary(self):
        if self.salary > 10000:
            raise ValidationError('Salary Greater tha 10,000')

    @api.model
    def create(self, vals):
        name_split = vals['name'].split()
        vals['email'] = f"{name_split[0][0]}{name_split[1]}@gmail.com"
        search_students = self.search([('email', '=', vals['email'])])
        if search_students:
            raise ValidationError('Email already exist')
        track = self.env['iti.track.bns'].browse(vals['track_id'])
        if track.is_open is False:
            raise ValidationError('Selected Track is closed')
        return super().create(vals)

    def write(self, vals):
        if "name" in vals:
            name_split = vals['name'].split()
            vals['email'] = f"{name_split[0][0]}{name_split[1]}@gmail.com"
        return super().write(vals)

    def unlink(self):
        for rec in self:
            if rec.state in ['passed', 'rejected']:
                raise ValidationError("you can't delete this record")
            return super().unlink()

    def change_state(self):
        if self.state == 'applied':
            self.state = 'first'
        elif self.state == 'first':
            self.state = 'second'
        elif self.state in ['passed', 'rejected']:
            self.state = 'applied'

    def set_passed(self):
        if self.state == 'second':
            self.state = 'passed'

    def set_reject(self):
        if self.state == 'second':
            self.state = 'rejected'

    @api.onchange("gender")
    def _on_change_gender(self):
        if not self.gender:
            self.gender = "m"
            return {}
        if self.gender == 'm':
            self.salary = 1000
        else:
            self.salary = 5000
        return {
            'warning': {
                'title': 'Hello',
                'message': 'you changed the Gender'
            }
        }

