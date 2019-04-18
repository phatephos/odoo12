# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, QWebException, AccessError
from odoo.tools.translate import _
import datetime
from .import git_first
try:
    from xmlrpc import client as xmlrpclib
except ImportError:
    import xmlrpclib
import odoorpc
import socket


class Project(models.Model):
    """项目"""
    _name = 'em.project'
    _description = u"项目"
    _inherit = ['mail.thread']
    READONLY = {'draft': [('readonly', False)]}

    project_name = fields.Char(string=u'名称', required=True, track_visibility='onchange',
                               readonly=True, states=READONLY, store=True, index=True)
    code = fields.Char(string=u'项目编码', readonly=True, states=READONLY, index=True)
    state = fields.Selection([('draft', '草稿'),
                              ('confirm', '审批中'),
                              ('done', '完成')], string='状态', default='draft',track_visibility='onchange', index=True)
    name = fields.Char(string=u'项目名称', compute='get_name', store=True, index=True, readonly=True, states=READONLY)
    start_date = fields.Date(string=u'项目开始时间', readonly=True, states=READONLY, index=True)
    end_date = fields.Date(string=u'项目结束时间', readonly=True, states=READONLY, index=True)
    company_id = fields.Many2one('partner.archives',string=u'项目所属公司', domain="[('is_company', '=', True)]", index=True)
    # first_letter = fields.Char(compute='_get_first_letter', store=True, string=u'名称首字母')
    #
    # @api.one
    # @api.depends('name')
    # def _get_first_letter(self):
    #     name = self.name
    #     if name:
    #         self.first_letter = git_first.get_first_letter(name)

    @api.one
    @api.depends('project_name', 'code')
    def get_name(self):
        """拼名字"""
        self.name = self.code + self.project_name

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
        self.create_tender_project()

    def create_tender_project(self):
        """项目创建审批完成后自动创建到招投标项目中"""
        hostname = socket.gethostname()
        if socket.gethostbyname(hostname) == '39.106.203.73':
            odoo = odoorpc.ODOO('baoshunkeji.com', port=8069)
            odoo.login('tender_db', 'admin', 'OeN4Bj0^')
            print("连接成功！")
            tender_project_id = odoo.env['tender.project'].search([['code', '=', self.code]], limit=1)
            if not tender_project_id:
                res_company_id = odoo.env['res.company'].search([['name', '=', self.company_id.name]], limit=1)
                lineva2 = {}
                lineva2['name'] = self.project_name
                lineva2['code'] = self.code
                lineva2['company_id'] = res_company_id[0] if res_company_id else False
                odoo.env['tender.project'].create(lineva2)

    @api.one
    def unlink(self):
        """在state字段不为草稿时不允许删除，"""
        if self.state == 'done' or self.state == 'confirm':
            raise UserError(u'该状态下的单据不可删除！')
        else:
            return super(Project, self).unlink()