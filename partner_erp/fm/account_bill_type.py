# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, QWebException
from odoo.tools.translate import _
import datetime, time, pytz
from dateutil.relativedelta import relativedelta


import logging
_logger = logging.getLogger(__name__)


class FmAccountBillType(models.Model):
    """票据类型"""
    _name = 'fm.account_bill_type'
    _description = u"票据类型"
    _inherit = ['mail.thread']

    name = fields.Char(string=u'名称', index=True, required=True )
    bill_type = fields.Char(string=u'票据大类', index=True, required=True)
    bill_attribute = fields.Char(string=u'票据属性', index=True, required=True)

    _sql_constraints = [('name_UNIQUE', 'unique (name)', "名称已存在!")]