# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, SUPERUSER_ID


class NewMaterial(models.Model):
    _name='xr_base.new_material'
    _description = u"新材料"
    _inherit = ['mail.thread']

    name = fields.Char(string=u'新材料', track_visibility='onchange')
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


class NewTechnology(models.Model):
    _name='xr_base.new_technology'
    _description = u"新工艺"
    _inherit = ['mail.thread']

    name = fields.Char(string=u'新工艺', track_visibility='onchange')
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

