# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, QWebException
import datetime,time


class AccountingInterval(models.Model):
    """会计期间"""
    _name = 'fm.accounting_interval'
    _description = u"会计期间"
    _inherit = ['mail.thread']

    name = fields.Char(string=u"会计区间", compute='get_accounting_interval', store=True, index=True)
    accounting_start = fields.Date(string=u'会计开始日期', default=fields.Date.context_today,
                                   index=True, track_visibility='onchange')
    accounting_end = fields.Date(string=u'会计结束日期', default=fields.Date.context_today,
                                 index=True, track_visibility='onchange')
    accounting_year = fields.Char(string=u"会计年度", compute='get_accounting_interval', store=True, index=True)
    accounting_month = fields.Char(string=u"会计月", compute='get_accounting_interval', store=True, index=True)
    input_person = fields.Many2one('partner.archives', '录入人', default=lambda self: self.env['partner.archives'].
                                   search([('user_id', '=', self.env.user.id)], limit=1).id,
                                   track_visibility='onchange', index=True, ondelete='restrict')
    order_date = fields.Date(string=u'创建日期', default=time.strftime('%Y-%m-%d'), index=True, track_visibility='onchange')

    @api.one
    @api.depends('accounting_end')
    def get_accounting_interval(self):
        # start_year = str(self.accounting_start)[:4]
        # end_year = str(self.accounting_end)[:4]
        # start_month = str(self.accounting_start)[5:7]
        # end_month = str(self.accounting_end)[5:7]
        if self.accounting_end:
            self.name = str(self.accounting_end)[:4] + '年' + str(self.accounting_end)[5:7] + '月'
            self.accounting_year = str(self.accounting_end)[:4]
            self.accounting_month = str(self.accounting_end)[5:7]

    @api.constrains('name')
    def _check_name(self):
        """限制会计区间不能重复出现"""
        names = self.search([('name', '=', self.name)])
        if len(names) > 1:
            raise ValidationError('会计区间已经存在！')

    @api.constrains('accounting_start', 'accounting_end')
    def constrains_accounting_interval(self):
        """约束快开始日期结束日期"""
        if self.accounting_start and self.accounting_end:
            d1 = datetime.datetime.strptime(self.accounting_start, '%Y-%m-%d')
            d2 = datetime.datetime.strptime(self.accounting_end, '%Y-%m-%d')
            if (d2 - d1).days < 27 or (d2 - d1).days > 31:
                raise UserError(u'请确认会计开始日期、结束日期是否正确')