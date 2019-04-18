# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, QWebException
from odoo.tools.translate import _
from datetime import *
import time
import json
import logging

_logger = logging.getLogger(__name__)


class FmAccount(models.Model):
    _name = 'fm.account'
    _description = u"科目表"
    _inherit = ['mail.thread']
    _order = 'code asc'

    name = fields.Char(string=u'科目显示名称', index=True, compute='update_parent_name', store=True)
    name_dir = fields.Char(string=u'科目名称', index=True, required=True)
    code = fields.Char(string=u'科目编码', index=True, required=True)
    orientation = fields.Selection([('1', u'借'),
                                    ('2', u'贷')], index=True, string=u'方向', default='1', track_visibility='onchange')
    gradation = fields.Integer(string='级次', compute="get_gradation", store=True)
    newly_added = fields.Boolean( string=u'新增', index=True)
    delete_bool = fields.Boolean(string=u'删除', index=True)
    retain_bool = fields.Boolean(string=u'保留', index=True)
    sealed_bool = fields.Boolean(string=u'是否封存', index=True)
    enable_date = fields.Date(string='启用日期')
    end_date = fields.Date(string='终止日期')
    accounting_interval_id = fields.Many2one('fm.accounting_interval', string=u'源头起始期间', index=True)
    account_type_id = fields.Many2one('fm.account.type', index=True, string=u'科目类型', ondelete='restrict')
    parent_id = fields.Many2one('fm.account', index=True, string=u'上级科目', ondelete='restrict')
    tag_ids = fields.Many2many('fm.account.tag', 'fm_account_account_tag_ref', 'account_id', 'tag_id', string=u'标签', index=True, ondelete='restrict')
    active = fields.Boolean(string=u'有效', default=True, index=True)
    type = fields.Selection([('others', '其他类'), ('cash', '现金类'), ('bank', '银行类'), ('equivalents', '现金等价物')], string='科目类型', index=True)
    amount_boolean = fields.Boolean(string='是否数量金额')
    is_quote = fields.Boolean(string=u'是否能被引用', default=True)

    def change_is_quote(self):
        if self.is_quote is True:
            self.is_quote = False
        elif self.is_quote is False:
            self.is_quote = True

    @api.one
    @api.depends('code')
    def get_gradation(self):
        if self.code:
            self.gradation = (len(self.code) - 2) / 2

    def update_parent(self):
        """批量初始化"""
        for i in self.env['fm.account'].search([]):
            i.update_name_asc()

    def update_gradation(self):
        """批量初始化"""
        for i in self.env['fm.account'].search([]):
            i.get_gradation()

    @api.one
    @api.depends('gradation', 'name_dir')
    def update_parent_name(self):
        """更新上级科目"""
        if self.name_dir:
            if self.gradation == 1:
                self.name = self.name_dir
            elif self.gradation == 2:
                parent_account = self.env['fm.account'].search([['code', '=', self.code[0: 4]]])
                if parent_account:
                    self.parent_id = parent_account.id
                    self.name = self.name_dir + '\\' + parent_account.name_dir
            elif self.gradation == 3:
                parent_account2 = self.env['fm.account'].search([['code', '=', self.code[0: 6]]])
                parent_account1 = self.env['fm.account'].search([['code', '=', self.code[0: 4]]])
                if parent_account2 and parent_account1:
                    self.parent_id = parent_account2.id
                    self.name = self.name_dir + '\\' + parent_account2.name_dir + '\\' + parent_account1.name_dir
            elif self.gradation == 4:
                parent_account3 = self.env['fm.account'].search([['code', '=', self.code[0: 8]]])
                parent_account2 = self.env['fm.account'].search([['code', '=', self.code[0: 6]]])
                parent_account1 = self.env['fm.account'].search([['code', '=', self.code[0: 4]]])
                if parent_account2 and parent_account1:
                    self.parent_id = parent_account2.id
                    self.name = self.name_dir + '\\' + parent_account3.name_dir +  '\\' + parent_account2.name_dir + '\\' + parent_account1.name_dir
            elif self.gradation == 5:
                parent_account4 = self.env['fm.account'].search([['code', '=', self.code[0: 10]]])
                parent_account3 = self.env['fm.account'].search([['code', '=', self.code[0: 8]]])
                parent_account2 = self.env['fm.account'].search([['code', '=', self.code[0: 6]]])
                parent_account1 = self.env['fm.account'].search([['code', '=', self.code[0: 4]]])
                if parent_account2 and parent_account1:
                    self.parent_id = parent_account2.id
                    self.name = self.name_dir + '\\' + parent_account4.name_dir +  '\\' + parent_account3.name_dir + \
                                '\\' + parent_account2.name_dir + '\\' + parent_account1.name_dir

    @api.one
    @api.depends('gradation', 'name_dir')
    def update_name_asc(self):
        """更新上级科目"""
        if self.name_dir:
            if self.gradation == 1:
                self.name = self.name_dir
            elif self.gradation == 2:
                parent_account = self.env['fm.account'].search([['code', '=', self.code[0: 4]]])
                if parent_account:
                    self.name = parent_account.name_dir + '\\' + self.name_dir
            elif self.gradation == 3:
                parent_account2 = self.env['fm.account'].search([['code', '=', self.code[0: 6]]])
                parent_account1 = self.env['fm.account'].search([['code', '=', self.code[0: 4]]])
                if parent_account2 and parent_account1:
                    self.name = parent_account1.name_dir + '\\' + parent_account2.name_dir + '\\' + self.name_dir
            elif self.gradation == 4:
                parent_account3 = self.env['fm.account'].search([['code', '=', self.code[0: 8]]])
                parent_account2 = self.env['fm.account'].search([['code', '=', self.code[0: 6]]])
                parent_account1 = self.env['fm.account'].search([['code', '=', self.code[0: 4]]])
                if parent_account2 and parent_account1:
                    self.name = parent_account1.name_dir + '\\' + parent_account2.name_dir + '\\' + parent_account3.name_dir + '\\' + self.name_dir
            elif self.gradation == 5:
                parent_account4 = self.env['fm.account'].search([['code', '=', self.code[0: 10]]])
                parent_account3 = self.env['fm.account'].search([['code', '=', self.code[0: 8]]])
                parent_account2 = self.env['fm.account'].search([['code', '=', self.code[0: 6]]])
                parent_account1 = self.env['fm.account'].search([['code', '=', self.code[0: 4]]])
                if parent_account2 and parent_account1:
                    self.name = parent_account1.name_dir + '\\' + parent_account2.name_dir + \
                                '\\' + parent_account3.name_dir + '\\' + parent_account4.name_dir + '\\' + self.name_dir