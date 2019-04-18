# -*- coding: utf-8 -*-
from odoo import models, fields, api
import odoorpc
from .import git_first


class QualityRequirement(models.Model):
    """ 产品质量要求"""
    _name = 'partner.quality_requirement'
    _inherit = ['mail.thread']
    _description = u'产品质量要求'
    READONLY = {'draft': [('readonly', False)]}

    @api.one
    @api.depends('standard_number')
    def _name_get(self):
        """拼名字"""
        self.name = self.standard_number
    name = fields.Char(compute='_name_get', store=True, index=True, readonly=True, states=READONLY)
    partner_id = fields.Many2one('partner.archives', domain="[('bill_type', '=', 'partner')]",track_visibility='onchange', ondelete='restrict', string=u'客户', required=True, index=True, readonly=True, states=READONLY)
    product_id = fields.Many2one('code.material_codes', string=u'产品', required=True, track_visibility='onchange',ondelete='restrict', index=True, readonly=True, states=READONLY)

    company_standard = fields.Text(track_visibility='onchange', string=u'我司标准', required=True, readonly=True, states=READONLY, index=True)
    partner_standard = fields.Text(track_visibility='onchange', string=u'客户标准', required=True, readonly=True, states=READONLY, index=True)
    standard_number = fields.Char(track_visibility='onchange', string=u'标准号', index=True, required=True, readonly=True, states=READONLY)

    state = fields.Selection([('draft', '草稿'), ('approval', '待审核'), ('done', '完成')], string='状态', default='draft',
                             track_visibility='onchange', index=True)
    # first_letter = fields.Char(compute='_get_first_letter', store=True, string=u'名称首字母')
    #
    # @api.one
    # @api.depends('name')
    # def _get_first_letter(self):
    #     name = self.name
    #     if name:
    #         self.first_letter = git_first.get_first_letter(name)

    # 状态跳转方法
    @api.one
    def to_draft(self):
        """
        状态变成草稿
        :return:
        """
        self.state = 'draft'

    @api.one
    def to_approval(self):
        """
        状态变成one
        :return:
        """
        self.state = 'approval'

    @api.one
    def to_done(self):
        """
        状态变成完成
        :return:
        """
        self.state = 'done'

    def get_quality_requirement(self):
        odoo = odoorpc.ODOO('baoshunkeji.com', port=8069)
        odoo.login('tender_db', 'admin', 'OeN4Bj0^')
        if 'crm_c.quality_requirement' in odoo.env:
            Order = odoo.env['crm_c.quality_requirement']
            order_ids = Order.search([['is_erp', '=', False]], limit=10)
            for order in Order.browse(order_ids):
                partner_id = self.env['partner.archives'].name_search(name=order.partner_id.name, limit=1)
                # material_id = self.env['code.material_codes'].name_search([product_name, '='], limit=1)
                material_id = self.env['code.material_codes'].name_search(name=order.product_id.name, limit=1)
                if partner_id and material_id:
                    lineval = {}
                    lineval['partner_id'] = partner_id[0][0]
                    lineval['product_id'] = material_id[0][0]
                    lineval['company_standard'] = order.company_standard
                    lineval['partner_standard'] = order.partner_standard
                    lineval['standard_number'] = order.standard_number if order.standard_number else '无'
                    self.create(lineval)
                order.write({'is_erp': True})

