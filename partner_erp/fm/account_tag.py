# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, QWebException
from odoo.tools.translate import _
from datetime import *
import time
import json
import logging
_logger = logging.getLogger(__name__)


class FmAccountTag(models.Model):
    _name = 'fm.account.tag'
    _description = u"科目标签"
    _inherit = ['mail.thread']

    name = fields.Char(string=u'名称', index=True, required=True,)
    active = fields.Boolean(string=u'有效', default=True)
    model_ids = fields.Many2many('ir.model', string=u"辅助明细")
