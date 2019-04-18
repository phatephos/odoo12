# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, QWebException, AccessError
from odoo.tools.translate import _
import datetime


class CurrencyType(models.Model):
    """继承币种"""
    _inherit = 'res.currency'
    _description = u"币种"

    # currency_type_id = fields.Many2one('partner.currency_type', string=u'币种类别', index=True)