# -*- coding: utf-8 -*-
from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError, AccessError


class FmAccountTax(models.Model):
    _name = 'fm.account.tax'
    _description = u"税率"
    _inherit = ['mail.thread']

    name = fields.Char(string=u'名称', index=True, required=True,)
    tax_type = fields.Selection([('sale', u'销售'),
                                 ('purchase', u'采购'),
                                 ('transport', u'运输'),
                                 ('other', u'其他'),
                              ], string=u'类型', required=True, cope=False, index=True)
    # account_id = fields.Many2one('fm.account', index=True, required=True, string=u'科目')
    amount = fields.Float(string=u'税')
    active = fields.Boolean(string=u'有效', default=True)