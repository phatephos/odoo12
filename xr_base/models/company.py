# -*- coding: utf-8 -*-


from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError, AccessError
import datetime


class Company(models.Model):
    """公司名称添加"""
    _name = 'xr_base.company'
    _description = u"公司档案"
    _inherit = ['mail.thread']

    name = fields.Char(string=u'公司全称', track_visibility='onchange', required=True)
    abbreviation = fields.Char(string=u'公司简称', track_visibility='onchange', required=True)
    business_licence = fields.Char(string=u'统一社会信用代码', track_visibility='onchange', required=True)
    address = fields.Char(string=u'地址', track_visibility='onchange')
    main_business = fields.Text(string=u'主营业务', track_visibility='onchange')
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

    @api.one
    def unlink(self):
        """在state字段不为草稿时不允许删除，"""
        if self.state != 'draft':
            raise UserError(u'完成状态下不允许删除。')
        else:
            return super(Company, self).unlink()




