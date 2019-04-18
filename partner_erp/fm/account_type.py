# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, QWebException
from odoo.tools.translate import _
from datetime import *
import time
import json
import logging
_logger = logging.getLogger(__name__)


class FmAccountType(models.Model):
    _name = 'fm.account.type'
    _description = u"科目类型"
    _inherit = ['mail.thread']

    name = fields.Char(string=u'科目类型', index=True, required=True,)
    account_type = fields.Selection([('asset', u'资产类'),
                                     ('liabilities', u'负债类'),
                                     ('common', u'共同类'),
                                     ('ownership', u'所有者权益类'),
                                     ('cost', u'成本类'),
                                     ('profit_loss', u'损益类'),
                              ], string=u'类型', required=True, copy=False, index=True)
    active = fields.Boolean(string=u'有效', default=True)
