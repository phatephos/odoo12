# -*- coding: utf-8 -*-
from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError, AccessError


class TransportMode(models.Model):
    """运输方式"""
    _name = 'crm_c.transport_mode'
    _description = u"运输方式"
    _inherit = ['mail.thread']

    name = fields.Char(string=u'运输方式名称', index=True)
    code = fields.Char(string=u'运输方式编码', index=True)

    _sql_constraints = [('check_name', 'unique(name)', u'需保证名称唯一性，请换一个名称输入')]