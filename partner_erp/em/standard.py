# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, QWebException, AccessError
from odoo.tools.translate import _
import datetime


class Standard(models.Model):
    """规范性文档，工单上引用的失效描述，失效原因，检测方法--黎洋"""
    _name = "em.standard"
    _description = "规范性文档"
    READONLY = {'draft': [('readonly', False)]}

    number = fields.Char(string=u'序号', readonly=True, states=READONLY, index=True)
    name = fields.Char(string=u'特征', readonly=True, states=READONLY, index=True)
    describe = fields.Text(string=u'描述', readonly=True, states=READONLY)
    standard_type = fields.Selection([
        ('describe', u'失效描述'),
        ('reason', u'失效原因'),
        ('method', u'检测方法')], string=u'规范类型', index=True, readonly=True, states=READONLY)
    state = fields.Selection([('draft', '草稿'),
                              ('confirm', '审批中'),
                              ('done', '完成')], string='状态', default='draft',
                             track_visibility='onchange', index=True)

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
            return super(Standard, self).unlink()