# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError, AccessError
from .import git_first


class Process(models.Model):
    _name = 'mes.process'
    _description = "工段"
    _inherit = ['mail.thread']
    READONLY = {'draft': [('readonly', False)]}

    name = fields.Char(string=u'名称', required=True, index=True, copy=False, track_visibility='onchange', readonly=True, states=READONLY)
    code = fields.Char(string=u'编码', compute="get_code", store=True, readonly=True, states=READONLY, index=True)
    state = fields.Selection([('draft', '草稿'), ('approval', '待审核'), ('done', '完成')], string='状态', default='draft',
                             track_visibility='onchange', index=True)
    # first_letter = fields.Char(compute='_get_first_letter', store=True, string=u'名称首字母')
    #
    # @api.one
    # @api.depends('name')
    # def _get_first_letter(self):
    #     name = self.name
    #     if name:
    #         self.first_letter = git_first.get_first_letter(name)

    # 状态跳转方法
    @api.one
    def to_draft(self):
        """
        状态变成草稿
        :return:
        """
        self.state = 'draft'

    @api.one
    def to_approval(self):
        """
        状态变成one
        :return:
        """
        self.state = 'approval'

    @api.one
    def to_done(self):
        """
        状态变成完成
        :return:
        """
        self.state = 'done'


class ProductionSystem(models.Model):
    _name = 'partner.production_system'
    _description = "生产加工系统"
    READONLY = {'draft': [('readonly', False)]}

    name = fields.Char(string=u'名称', readonly=True, states=READONLY, index=True)
    state = fields.Selection([('draft', '草稿'), ('approval', '待审核'), ('done', '完成')], string='状态', default='draft',
                             track_visibility='onchange', index=True)

    @api.constrains('name')
    def _check_name(self):
        """限制生产加工系统不能重复出现"""
        names = self.search([('name', '=', self.name)])
        if len(names) > 1:
            raise ValidationError('该生产加工系统已经存在！')

    # 状态跳转方法
    @api.one
    def to_draft(self):
        """
        状态变成草稿
        :return:
        """
        self.state = 'draft'

    @api.one
    def to_approval(self):
        """
        状态变成one
        :return:
        """
        self.state = 'approval'

    @api.one
    def to_done(self):
        """
        状态变成完成
        :return:
        """
        self.state = 'done'


class Area(models.Model):
    """ 客户地区"""
    _name = 'partner.area'
    _description = "客户地区"
    READONLY = {'draft': [('readonly', False)]}

    name = fields.Char(string=u'名称', readonly=True, states=READONLY, index=True)
    archives_ids = fields.One2many('partner.archives', 'area_id', string=u'客户', index=True)
    state = fields.Selection([('draft', '草稿'), ('approval', '待审核'), ('done', '完成')], string='状态', default='draft',
                             track_visibility='onchange', index=True)

    @api.constrains('name')
    def _check_name(self):
        """限制客户地区不能重复出现"""
        names = self.search([('name', '=', self.name)])
        if len(names) > 1:
            raise ValidationError('该客户地区已经存在！')

    # 状态跳转方法
    @api.one
    def to_draft(self):
        """
        状态变成草稿
        :return:
        """
        self.state = 'draft'

    @api.one
    def to_approval(self):
        """
        状态变成one
        :return:
        """
        self.state = 'approval'

    @api.one
    def to_done(self):
        """
        状态变成完成
        :return:
        """
        self.state = 'done'

