from odoo import models, fields


class ItiTrack(models.Model):
    _name = 'iti.track.bns'
    # _rec_name = 'capacity'

    name = fields.Char()
    is_open = fields.Boolean()
    capacity = fields.Integer()
    student_ids = fields.One2many('iti.student.bns', 'track_id')
