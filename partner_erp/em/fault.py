# -*- coding: utf-8 -*-
from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError, AccessError
import datetime


class Phenomenon(models.Model):
    _name = "em.phenomenon"
    _description = "故障现象"
    READONLY = {'draft': [('readonly', False)]}

    name = fields.Char(string=u'故障现象名称', compute='get_name', required=True, index=True)
    phenomenon_name = fields.Char(string=u'故障现象', required=True, index=True, copy=False,
                                              track_visibility='onchange', readonly=True,
                                              states=READONLY)
    code = fields.Char(string=u'编码', readonly=True, states=READONLY, index=True)
    note = fields.Text(string=u'备注')
    state = fields.Selection([('draft', '草稿'),
                              ('confirm', '审批中'),
                              ('notifying', '知会中'),
                              ('done', '完成')], string='状态', default='draft', track_visibility='onchange', index=True)

    @api.one
    @api.depends('phenomenon_name', 'code')
    def get_name(self):
        """拼名字"""
        self.name = self.code + self.phenomenon_name

    @api.one
    def action_approval(self):
        """
        状态变成草稿
        :return:
        """
        if self.state == 'draft':
            self.state = 'confirm'

    @api.one
    def action_notifying(self):
        """
        状态变成审批
        :return:
        """
        self.state = 'notifying'

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
            return super(Phenomenon, self).unlink()


class Reason(models.Model):
    _name = "em.reason"
    _description = "故障原因"
    READONLY = {'draft': [('readonly', False)]}

    name = fields.Char(string=u'故障原因名称', compute='get_name', required=True, index=True)
    reason_name = fields.Char(string=u'故障原因', required=True, index=True, copy=False,
                                              track_visibility='onchange', readonly=True,
                                              states=READONLY)
    code = fields.Char(string=u'编码', readonly=True, states=READONLY, index=True)
    note = fields.Text(string=u'备注')
    state = fields.Selection([('draft', '草稿'),
                              ('confirm', '审批中'),
                              ('notifying', '知会中'),
                              ('done', '完成')], string='状态', default='draft', track_visibility='onchange', index=True)

    @api.one
    @api.depends('reason_name', 'code')
    def get_name(self):
        """拼名字"""
        self.name = self.code + self.reason_name

    @api.one
    def action_approval(self):
        """
        状态变成草稿
        :return:
        """
        if self.state == 'draft':
            self.state = 'confirm'

    @api.one
    def action_notifying(self):
        """
        状态变成审批
        :return:
        """
        self.state = 'notifying'

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
            return super(Reason, self).unlink()


class Measures(models.Model):
    _name = "em.measures"
    _description = "维修措施"
    READONLY = {'draft': [('readonly', False)]}

    name = fields.Char(string=u'维修措施名称', compute='get_name', required=True, index=True)
    measures_name = fields.Char(string=u'维修措施', required=True, index=True, copy=False,
                                              track_visibility='onchange', readonly=True,
                                              states=READONLY)
    code = fields.Char(string=u'编码', readonly=True, states=READONLY, index=True)
    note = fields.Text(string=u'备注')
    state = fields.Selection([('draft', '草稿'),
                              ('confirm', '审批中'),
                              ('notifying', '知会中'),
                              ('done', '完成')], string='状态', default='draft', track_visibility='onchange', index=True)

    @api.one
    @api.depends('measures_name', 'code')
    def get_name(self):
        """拼名字"""
        self.name = self.code + self.measures_name

    @api.one
    def action_approval(self):
        """
        状态变成草稿
        :return:
        """
        if self.state == 'draft':
            self.state = 'confirm'

    @api.one
    def action_notifying(self):
        """
        状态变成审批
        :return:
        """
        self.state = 'notifying'

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
            return super(Measures, self).unlink()
