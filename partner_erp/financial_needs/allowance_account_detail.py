# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, QWebException, AccessError
from odoo.tools.translate import _
import datetime


class AllowanceAccountDetail(models.Model):
    """备抵账户"""
    _name = 'partner.allowance_account_detail'
    _description = u"备抵账户明细"
    _inherit = ['mail.thread']
    READONLY = {'draft': [('readonly', False)]}

    name = fields.Char(string=u'名称', index=True, readonly=True, states=READONLY)
    allowance_account_id = fields.Many2one('partner.allowance_account', string=u'备抵账户')
    state = fields.Selection([('draft', '草稿'),
                              ('confirm', '审批中'),
                              ('done', '完成')], string='状态', default='draft', track_visibility='onchange', index=True)

    @api.one
    def action_approval(self):
        """
        状态变成草稿
        :return:
        """
        if self.state == 'draft':
            self.state = 'confirm'

    @api.one
    def action_approved(self):
        """
        状态变成完成
        :return:
        """
        self.state = 'done'

    @api.one
    def action_draft(self):
        """状态回退草稿"""
        self.state = 'draft'
        # self.reset_flow()

    @api.one
    def unlink(self):
        """在state字段不为草稿时不允许删除，"""
        if self.state == 'done' or self.state == 'confirm':
            raise UserError(u'该状态下的单据不可删除！')
        else:
            return super(AllowanceAccount, self).unlink()