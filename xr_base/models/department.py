# -*- coding: utf-8 -*-


from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError, AccessError


class Department(models.Model):
    """部门档案"""
    _name = 'xr_base.department'
    _description = u"部门"
    _inherit = ['mail.thread']

    name = fields.Char(string=u'部门名称', track_visibility='onchange', required=True)
    state = fields.Selection([('draft', '草稿'),
                              ('approve', '待审核'),
                              ('done', '完成')
                              ], string='状态', default='draft', track_visibility='onchange')

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


