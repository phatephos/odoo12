# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, QWebException, AccessError
from odoo.tools.translate import _
import datetime


class InventoryOrganization(models.Model):
    """库存组织"""
    _name = 'em.inventory_organization'
    _description = u"库存组织"
    _inherit = ['mail.thread']
    READONLY = {'draft': [('readonly', False)]}

    name = fields.Char(string=u'名称', compute='get_name', index=True, store=True)
    inventory_organization_name = fields.Char(string=u'名称', required=True, index=True, copy=False, track_visibility='onchange', readonly=True,
                       states=READONLY)
    code = fields.Char(string=u'编码', readonly=True, states=READONLY, index=True)
    company_id = fields.Many2one('partner.archives', string=u'公司', domain="[('is_company', '=', True)]", index=True)
    state = fields.Selection([('draft', '草稿'),
                              ('confirm', '审批中'),
                              ('notifying', '知会中'),
                              ('done', '完成')], string='状态', default='draft', track_visibility='onchange', index=True)

    @api.one
    @api.depends('inventory_organization_name', 'code')
    def get_name(self):
        """拼名字"""
        self.name = self.code + self.inventory_organization_name

    @api.one
    def action_approval(self):
        """
        状态变成草稿
        :return:
        """
        if self.state == 'draft':
            self.state = 'confirm'

    @api.one
    def action_notifying(self):
        """
        状态变成审批
        :return:
        """
        self.state = 'notifying'

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
            return super(InventoryOrganization, self).unlink()
