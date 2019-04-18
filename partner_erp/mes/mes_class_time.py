#  -*- coding:utf-8 -*-
from odoo import models, fields, api, _
import random
from datetime import *
from odoo.exceptions import AccessError, ValidationError


class ClassTime(models.Model):
    """班次"""
    _name = 'mes.class_time'
    _description = "班次"
    _inherit = ['mail.thread']

    code = fields.Char(string=u'编码', required=True, track_visibility='onchange')
    name = fields.Char( string=u"名称", required=True, track_visibility='onchange')
    kind = fields.Selection([('two', '两班倒'),
                              ('three', '三班倒'),
                              ], default='three', string=u"类型", required=True)
    _sql_constraints = [('cons_tech_demo_name', 'UNIQUE(name, kind)', u'该班次已存在'),
                        ('cons_tech_demo_code', 'UNIQUE(code)', u'编号已存在')]