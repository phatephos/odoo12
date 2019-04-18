# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, QWebException
from odoo.tools.translate import _
import datetime
import time
import logging
_logger = logging.getLogger(__name__)


class FmAccountDepreciationMethod(models.Model):
    _name = 'fm.account.depreciation.method'
    _description = u"折旧方式"
    _inherit = ['mail.thread']

    name = fields.Char(string=u'折旧方法名称', index=True, required=True,)
    # month_amount = fields.Float(string=u'使用月限')
    # depreciation_amount = fields.Float(string=u'折旧数量')
    depreciation_formula = fields.Text(string=u'月折旧额公式')
    depreciation_describe = fields.Text(string=u'月折旧率公式')
