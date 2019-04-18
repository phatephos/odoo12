# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, QWebException, AccessError
from odoo.tools.translate import _
import datetime
from .import git_first


class Document(models.Model):
    """现金流量"""
    _name = 'partner.document'
    _description = u"操作文档"
    _inherit = ['mail.thread']

    name = fields.Char(string=u'点击查看：', index=True)