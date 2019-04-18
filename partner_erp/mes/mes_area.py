#  -*- coding:utf-8 -*-
from odoo import models, fields, api, _
import random
from datetime import *
from odoo.exceptions import AccessError, ValidationError


class Area(models.Model):
    """区域"""
    _name = 'mes.area'
    _description = "基地"
    _inherit = ['mail.thread']

    name = fields.Char(string=u'名称', required=True, track_visibility='onchange')
    code = fields.Char(string=u'编码', required=True, track_visibility='onchange')
    _sql_constraints = [('cons_tech_demo_name', 'UNIQUE(name)', u'名称已存在'),
                        ('cons_tech_demo_code', 'UNIQUE(code)', u'编号已存在')]