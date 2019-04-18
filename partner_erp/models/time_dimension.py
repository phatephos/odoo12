# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, QWebException
import datetime


class TimeDimension(models.Model):
    _name = 'budget.time_dimension'
    _description = u"时间维度"
    _inherit = ['mail.thread']
    READONLY = {'draft': [('readonly', False)]}

    name = fields.Char(string=u'时间维度', track_visibility='onchange', readonly=True, states=READONLY)
    employee_id = fields.Many2one('partner.archives', '制单人', default=lambda self: self.env['partner.archives'].
                                  search([('user_id', '=', self.env.user.id)], limit=1).id,
                                  track_visibility='onchange', index=True, ondelete='restrict')
    bill_date = fields.Datetime(string=u'制单时间', default=datetime.datetime.now(), index=True)
    state = fields.Selection([('draft', '草稿'),
                              ('confirm', '审批中'),
                              ('done', '完成')], string='状态', default='draft', track_visibility='onchange', index=True)

    @api.constrains('name')
    def _check_name(self):
        """限制时间维度唯一"""
        names = self.search([('name', '=', self.name)])
        if len(names) > 1:
            raise ValidationError('时间维度已经存在！')

    @api.one
    def action_approval(self):
        """
        状态变成草稿
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
    def action_draft(self):
        """状态回退草稿"""
        self.state = 'draft'
        # self.reset_flow()

    @api.one
    def unlink(self):
        """在state字段不为草稿时不允许删除，"""
        if self.state == 'done' or self.state == 'confirm':
            raise UserError(u'该状态下的单据不可删除！')
        else:
            return super(TimeDimension, self).unlink()