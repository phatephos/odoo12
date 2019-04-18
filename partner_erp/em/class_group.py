# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, QWebException, AccessError
from odoo.tools.translate import _


class ClassGroup(models.Model):
    """班组--杨丽宾"""
    _name = "em.class_group"
    _description = "班组"
    READONLY = {'draft': [('readonly', False)]}

    name = fields.Char(string=u'班组', readonly=True, states=READONLY, index=True)
    code = fields.Char(string=u'编号', readonly=True, states=READONLY, index=True)
    state = fields.Selection([('draft', '草稿'),
                              ('confirm', '审批中'),
                              ('done', '完成')], string='状态', default='draft',
                             track_visibility='onchange', index=True)
    group_users_ids = fields.Many2many('partner.archives', string=u'班组人员', domain="[('bill_type', '=', 'users')]", index=True)
    company_id = fields.Many2one('partner.archives', domain="[('is_company', '=', True)]", string='所属公司',
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
            return super(ClassGroup, self).unlink()