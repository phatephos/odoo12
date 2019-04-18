# -*- coding: utf-8 -*-
from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError, AccessError


class PaymentMethod(models.Model):
    """付款方式"""
    _name = 'crm_c.payment_method'
    _description = u"付款方式"
    _inherit = ['mail.thread']

    name = fields.Char(string=u'付款方式名称', index=True)
    code = fields.Char(string=u'付款方式编码', index=True)
    number= fields.Char(string=u'付款方式序号', index=True)
    _sql_constraints = [('check_name', 'unique(name)', u'需保证名称唯一性，请换一个名称输入')]