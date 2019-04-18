# -*- coding: utf-8 -*-


from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError, AccessError
import datetime


class Product(models.Model):
    """产品模块"""
    _name = 'xr_base.product'
    _description = u"新产品"
    _inherit = ['mail.thread']

    name = fields.Char(string=u'产品名称', track_visibility='onchange',required=True)
    weight = fields.Float(string=u'单重(kg)', track_visibility='onchange')
    describe = fields.Text(string=u'产品描述', track_visibility='onchange')
    state = fields.Selection([('draft', u'草稿'),
                              ('approve', u'待审批'),
                              ('done', u'已审批'),
                              ], string=u'状态', default='draft', track_visibility='onchange')

    @api.one
    def to_draft(self):
        """
        状态变成草稿
        :return:
        """
        self.state = 'draft'

    @api.one
    def to_approve(self):
        """
        状态变成one
        :return:
        """
        self.state = 'approve'

    @api.one
    def to_done(self):
        """
        状态变成完成
        :return:
        """
        self.state = 'done'

    @api.one
    def unlink(self):
        if self.state == 'draft':
            return super(Product, self).unlink()
        else:
            raise UserError(_("状态不是草稿，不能删除！"))
