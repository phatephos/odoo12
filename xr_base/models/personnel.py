# -*- coding: utf-8 -*-


from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError, AccessError
import datetime


class Personnel(models.Model):
    """人员档案"""
    _name = 'xr_base.personnel'
    _description = u"人员"
    _inherit = ['mail.thread']

    name = fields.Char(string=u'名称', track_visibility='onchange', required=True)
    ID_number = fields.Char(string=u'身份证号码', track_visibility='onchange')
    customer_id = fields.Many2one('xr_base.customer', string=u'公司',
                                  domain=[('state', '=', 'done')], track_visibility='onchange')
    department_id = fields.Many2one('xr_base.department', string=u'部门',
                                    domain=[('state', '=', 'done')], track_visibility='onchange')
    telephone = fields.Char(string=u'电话', track_visibility='onchange')
    state = fields.Selection([('draft', u'草稿'),
                              ('approve', u'待审批'),
                              ('done', u'已审批'),
                              ], string=u'状态', default='draft', track_visibility='onchange')
    user_id = fields.Many2one('res.users', string='用户', track_visibility='onchange', required=True)

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
            return super(Personnel, self).unlink()
        else:
            raise UserError(_("状态不是草稿，不能删除！"))

