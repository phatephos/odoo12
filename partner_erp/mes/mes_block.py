#  -*- coding:utf-8 -*-
from odoo import models, fields, api, _
import random
from datetime import *
from odoo.exceptions import AccessError, ValidationError


class Block(models.Model):
    """生产装置"""
    _name = 'mes.block'
    _description = "生产装置"
    _inherit = ['mail.thread']

    area_id = fields.Many2one('mes.area', string="基地", track_visibility='onchange')
    name = fields.Char(string=u'名称', required=True, track_visibility='onchange')
    code = fields.Char(string=u'编码', required=True, track_visibility='onchange')
    _sql_constraints = [('cons_tech_demo_name', 'UNIQUE(name)', u'名称已存在'),
                        ('cons_tech_demo_code', 'UNIQUE(code)', u'编号已存在')]
    company_id = fields.Many2one('partner.archives', domain="[('is_company', '=', True)]", string=u'公司')
    production_system_id = fields.Many2one('partner.production_system', string=u'生产加工系统')
    active = fields.Boolean(default=True, index=True)