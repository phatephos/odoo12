# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, QWebException
from odoo.tools.translate import _
import datetime
import time
import logging
_logger = logging.getLogger(__name__)


class FmAccountAssetType(models.Model):
    _name = 'fm.account.asset.type'
    _description = u"资产类别"
    _inherit = ['mail.thread']

    name = fields.Char(string=u'类别名称', index=True, required=True,)
    code = fields.Char(string=u'类别编码')
    use_year = fields.Integer(string=u'使用年限')
    use_month = fields.Integer(string=u'使用月限')
    # net_salvage = fields.Float(string=u'净残值率', default=0.05)
    depreciation_method_id = fields.Many2one('fm.account.depreciation.method', string=u'折旧方式', ondelete='restrict')
    account_id = fields.Many2one('fm.account', index=True, string=u'资产科目', ondelete='restrict')
    journal_id = fields.Many2one('fm.account.journal', index=True, string=u'账簿', ondelete='restrict')
    depreciation_account_id = fields.Many2one('fm.account', index=True, string=u'折旧资产科目', ondelete='restrict')
    cost_account_id = fields.Many2one('fm.account', index=True, string=u'费用科目', ondelete='restrict')

