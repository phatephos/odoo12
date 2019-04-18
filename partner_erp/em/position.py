# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, QWebException, AccessError
from odoo.tools.translate import _


class Position(models.Model):
    """设备位置--黎洋"""
    _name = "em.position"
    _description = "位置"
    READONLY = {'draft': [('readonly', False)]}

    name = fields.Char(string=u'位置名称', index=True)
    position_code = fields.Char(string=u'位置编码', index=True)
    # name = fields.Char(compute='_get_name', store=True, string=u'位置名称')
    # # code = fields.Char(string=u'位置编码')
    # # equipment_card_id = fields.Many2one('em.equipment_card', string='设备')
    # store_name = fields.Char(required=True, string=u'名称', readonly=True, states=READONLY)
    # long_name = fields.Char(compute='_get_name', string=u'分类名称', readonly=True, states=READONLY)
    position_id = fields.Many2one('em.position', domain="[('is_material', '=', False)]", string=u'父级位置名称',
                                  readonly=True, states=READONLY, ondelete='restrict', index=True)
    is_material = fields.Boolean(default=False, string=u'是否最后一级', readonly=True, states=READONLY, index=True)
    state = fields.Selection([('draft', '草稿'),
                              ('confirm', '审批中'),
                              ('done', '完成')], string='状态', default='draft', track_visibility='onchange', index=True)
    company_id = fields.Many2one('partner.archives', string='所属公司', domain="[('bill_type', '=', 'partner')]",
                                 index=True, ondelete='cascade', readonly=True, states=READONLY)

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
            return super(Position, self).unlink()

    # @api.one
    # @api.depends('position_id')
    # def _get_name(self):
    #     """拼名字（父级/第二父级）--黎洋"""
    #     if self.store_name:
    #         names = self.store_name
    #         parent_name = self.position_id
    #         while parent_name:
    #             names = parent_name.store_name + '/' + names
    #             parent_name = parent_name.position_id
    #         self.long_name = names
    #         self.name = names