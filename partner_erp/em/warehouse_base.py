# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, QWebException, AccessError
from odoo.tools.translate import _
import datetime


class WarehouseBase(models.Model):
    """仓库"""
    _name = 'em.warehouse_base'
    _description = u"仓库"
    _inherit = ['mail.thread']
    READONLY = {'draft': [('readonly', False)]}

    warehouse_name = fields.Char(string=u'名称', required=True, track_visibility='onchange', readonly=True,
                                 states=READONLY, store=True, index=True)
    code = fields.Char(string=u'编码', readonly=True, states=READONLY, index=True)
    inventory_organization_id = fields.Many2one('em.inventory_organization',string=u'存货组织名称', index=True)
    company_id = fields.Many2one('partner.archives', string=u'公司', domain="[('is_company', '=', True)]", index=True)
    inventory_organization_code = fields.Char(string=u'存货组织编码',related='inventory_organization_id.code', store=True, index=True)
    state = fields.Selection([('draft', '草稿'),
                              ('confirm', '审批中'),
                              ('done', '完成')], string='状态', default='draft',
                             track_visibility='onchange', index=True)
    name = fields.Char(string=u'名称', compute='get_name', index=True, store=True)

    @api.one
    @api.depends('warehouse_name', 'code')
    def get_name(self):
        """拼名字"""
        self.name = self.code + self.warehouse_name

    @api.one
    def action_draft(self):
        """
        状态变成草稿
        :return:
        """
        self.state = 'draft'

    @api.one
    def action_approval(self):
        """
        状态变成审批
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
    def unlink(self):
        """在state字段不为草稿时不允许删除，"""
        if self.state == 'done' or self.state == 'confirm':
            raise UserError(u'该状态下的单据不可删除！')
        else:
            return super(WarehouseBase, self).unlink()
