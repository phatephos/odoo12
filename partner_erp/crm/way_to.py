# -*- coding: utf-8 -*-
from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError, AccessError


class WayTo(models.Model):
    """到厂方式"""
    _name = 'crm_c.way_to'
    _description = u"到厂方式"
    _inherit = ['mail.thread']

    name = fields.Char(string=u'到厂方式', index=True)
    code = fields.Char(string=u'到厂方式编码', index=True)

    _sql_constraints = [('way_to', 'unique(name)', u'已经存在改到厂方式')]