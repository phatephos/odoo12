# -*- coding: utf-8 -*-
from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError, AccessError
from .import git_first
import datetime
import odoorpc


class ChangeArchives(models.Model):
    """客户档案变更"""
    _name = 'partner.change_archives'
    _inherit = ['mail.thread']
    _description = "客户信息变更"
    READONLY = {'draft': [('readonly', False)]}

    name = fields.Char('变更名称', index=True, track_visibility='onchange', readonly=True, states=READONLY, required=True)
    archives_id = fields.Many2one('partner.archives', string=u'客户', required=True)
    flow_company_id = fields.Many2one('partner.archives', string=u'客户公司', related='archives_id.flow_company_id', store=True)
    is_sale = fields.Boolean('是否是销售客户', track_visibility='onchange', related='archives_id.is_sale', store=True,
                             readonly=True, states=READONLY, index=True)
    is_purchase = fields.Boolean('是否是采购客户', track_visibility='onchange', related='archives_id.is_purchase', store=True,
                                 readonly=True, states=READONLY, index=True)
    is_middle = fields.Boolean('是否是中间客户', track_visibility='onchange', related='archives_id.is_middle', store=True,
                               readonly=True, states=READONLY, index=True)
    is_material = fields.Boolean('是否是物资客户', track_visibility='onchange', related='archives_id.is_material',
                                 store=True, readonly=True, states=READONLY, index=True)
    state = fields.Selection([('draft', '草稿'),
                              ('confirm', '审批中'),
                              ('done', '完成')], string='状态', default='draft',
                             track_visibility='onchange', copy=False, index=True)

    @api.one
    def action_approval(self):
        """审批"""
        if self.state == 'draft':
            self.state = 'confirm'

    @api.one
    def action_approved(self):
        """完成并创建订单"""
        self.state = 'done'
        partner_id = self.env['partner.archives'].search([['id', '=', self.archives_id.id]])
        if partner_id:
            partner_id.write({'name': self.name})

    @api.one
    def action_draft(self):
        """状态变成草稿"""
        self.state = 'draft'
        # self.reset_flow()

    @api.one
    def unlink(self):
        """在state字段不为草稿时不允许删除，"""
        if self.state == 'done' or self.state == 'confirm':
            raise UserError(u'该状态下的单据不可删除！')
        else:
            return super(ChangeArchives, self).unlink()