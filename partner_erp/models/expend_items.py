# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, QWebException, AccessError
from odoo.tools.translate import _
import datetime
from .import git_first


class ExpendItems(models.Model):
    """预算装置"""
    _name = 'partner.expend_items'
    _description = u"支出项目"
    _inherit = ['mail.thread']
    READONLY = {'draft': [('readonly', False)]}

    name = fields.Char(string=u'支出项目名称', index=True, readonly=True, states=READONLY)
    expenditure_business_id = fields.Many2one('partner.expenditure_business', string=u'支出业务', readonly=True, states=READONLY)
    company_id = fields.Many2one('partner.archives', domain="[('is_company', '=', True)]", string=u'公司', readonly=True, states=READONLY)
    state = fields.Selection([('draft', '草稿'),
                              ('confirm', '审批中'),
                              ('done', '完成')], string='状态', default='draft', track_visibility='onchange', index=True)
    expend_type = fields.Selection([('in', '收入项目'),
                                    ('out', '支出项目')], track_visibility='onchange', index=True)
    first_letter = fields.Char(compute='_get_first_letter', store=True, string=u'名称首字母')

    @api.one
    @api.depends('name')
    def _get_first_letter(self):
        name = self.name
        if name:
            self.first_letter = git_first.get_first_letter(name)

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
            return super(ExpendItems, self).unlink()
