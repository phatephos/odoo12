# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, QWebException
from odoo.tools.translate import _
import datetime
import time
import logging
_logger = logging.getLogger(__name__)


class CashFlowItems(models.Model):
    """现金流量表项目"""
    _name = 'fm.cash_flow_items'
    _description = u"现金流量表项目"
    _inherit = ['mail.thread']

    name = fields.Char(string=u'项目名称', index=True, required=True, track_visibility='onchange')
    code = fields.Char(string=u'项目代码', index=True, required=True, track_visibility='onchange')
    active = fields.Boolean(string=u'有效', default=True)
    note = fields.Text(string=u'备注')

    _sql_constraints = [('name_UNIQUE', 'unique (name)', "项目名称已存在!"), ('code_UNIQUE', 'unique (code)', "项目代码已存在!")]