# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, QWebException
from odoo.tools.translate import _
from datetime import *
import time
import json
import logging
_logger = logging.getLogger(__name__)


class FmAccountJournal(models.Model):
    _name = 'fm.account.journal'
    _description = u"账簿"
    _inherit = ['mail.thread']

    name = fields.Char(string=u'名称', index=True, required=True,)
    company_id = fields.Many2one('partner.archives', string=u'公司', ondelete='restrict', track_visibility='onchange',
                                 index=True, required=True, domain=[('is_company','=',True)])
    # journal_type = fields.Selection([('sale', u'销售'),
    #                              ('purchase', u'采购'),
    #                              ('bank', u'银行'),
    #                              ('cash', u'现金'),
    #                              ('other', u'杂项'),
    #                           ], string=u'类型', required=True, cope=False, index=True)
    # debit_account_id = fields.Many2one('fm.account', index=True,  string=u'默认借方科目', ondelete='restrict')
    # credit_account_id = fields.Many2one('fm.account', index=True, string=u'默认贷方科目', ondelete='restrict')
    active = fields.Boolean(string=u'有效', default=True)
