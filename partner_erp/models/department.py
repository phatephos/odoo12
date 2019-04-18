# -*- coding: utf-8 -*-
from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError, AccessError
import datetime
import odoorpc
from .import git_first
try:
    from xmlrpc import client as xmlrpclib
except ImportError:
    import xmlrpclib


class Department(models.Model):
    _name = "human_resource.department"
    _description = "部门表"
    READONLY = {'draft': [('readonly', False)]}

    name = fields.Char(string=u"部门名称", readonly=True, states=READONLY, index=True)
    company_id = fields.Many2one('partner.archives', string='所属公司', index=True, ondelete='cascade', readonly=True, states=READONLY)
    parent_id = fields.Many2one('human_resource.department', string=u'上级部门', readonly=True, states=READONLY, index=True)
    dept_type = fields.Selection([('manage', '管理部门'),
                                  ('manufacture', '制造部门'),
                                  ('production', '生产部门')], default='manage', string=u'部门类型（科目用）', index=True, readonly=True, states=READONLY)
    hr_department_id = fields.Integer(string=u'人力系统上的部门id', readonly=True, states=READONLY)
    company_name = fields.Char(string=u"人力系统上的公司名称", readonly=True, states=READONLY, index=True)
    state = fields.Selection([('draft', '草稿'), ('approval', '待审核'), ('done', '完成')], string='状态', default='draft',
                             track_visibility='onchange', index=True)
    dept_category = fields.Selection([('administrative', '行政部门'),
                                      ('inspection', '检维修分厂'),
                                      ('tar', '焦油分厂'),
                                      ('quality','质检'),
                                      ('hydrogenation','蒽加氢分厂'),
                                      ('microspheres','炭微球')], string=u'部门类别（审批流用）', index=True, readonly=True,
                                 states=READONLY)
    department_category_id = fields.Many2one('human_resource.department_category', string=u'部门类别(新)', index=True)
    note = fields.Text(string=u'备注')
    management_caliber_id = fields.Many2one('partner.management_caliber', string=u'管理口径')
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

    def _get_company_id(self, company_name):
        company = self.env['partner.archives']
        company_ids = company.search([['name', '=', company_name]])
        company_id = company_ids[0].id
        return company_id


    def unlink_dept(self):
        self.unlink()

    @api.constrains('name')
    def _check_name(self):
        """限制部门名字不能重复出现"""
        names = self.search([('name', '=', self.name), ('company_id','=',self.company_id.id)])
        if len(names) > 1:
            raise ValidationError('该部门名字已经存在！')

    def get_department(self):
        """部门"""
        odoo = odoorpc.ODOO('hr.baoshunkeji.com', port=8069)
        odoo.login('hr_db', 'admin', 'OeN4Bj0^')
        if 'human_resource.department' in odoo.env:
            Order = odoo.env['human_resource.department']
            order_ids = Order.search([['is_erp', '=', False]], limit=10)
            for order in Order.browse(order_ids):
                if order.company_id.name == '宝舜科技股份有限公司':
                    company_id = self._get_company_id(order.company_id.name)
                    lineval = {}
                    lineval['hr_department_id'] = order.id
                    lineval['name'] = order.name
                    lineval['company_name'] = order.company_id.name
                    lineval['company_id'] = company_id
                    self.create(lineval)
                else:
                    lineval = {}
                    lineval['hr_department_id'] = order.id
                    lineval['name'] = order.name
                    lineval['company_name'] = order.company_id.name
                    lineval['company_id'] = company_id
                    order[0].write(lineval)
                order.write({'is_erp': True})
        # server_conf = xmlrpclib.ServerProxy("http://hr.baoshunkeji.com/xmlrpc/common")
        # uid = server_conf.login('hr_db', 'admin', 'OeN4Bj0^')
        # server = xmlrpclib.ServerProxy("http://hr.baoshunkeji.com/xmlrpc/object")
        # ids = server.execute_kw('hr_db', uid, 'OeN4Bj0^',
        #                         'human_resource.department', 'search_read',
        #                         [[['is_erp', '=', False]
        #                           ]],
        #                         {'fields': ['id', 'name', 'company_id',
        #                                     ]})
        # for id in ids:
        #     department_id = self.env['human_resource.department'].search([['hr_department_id', '=', id['id']]])
        #     if id['company_id'][1] == '宝舜科技股份有限公司':
        #         company_id = self._get_company_id(id['company_id'][1])
        #         if not department_id :
        #             lineval = {}
        #             lineval['hr_department_id'] = id['id']
        #             lineval['name'] = id['name']
        #             lineval['company_name'] = id['company_id'][1]
        #             lineval['company_id'] = company_id
        #             self.create(lineval)
        #         else:
        #             lineval = {}
        #             lineval['hr_department_id'] = id['id']
        #             lineval['name'] = id['name']
        #             lineval['company_name'] = id['company_id'][1]
        #             lineval['company_id'] = company_id
        #             department_id[0].write(lineval)
        #         i = id['id']
        #         server.execute_kw('hr_db', uid, 'OeN4Bj0^', 'human_resource.department', 'write', [[i], {'is_erp': True}])


class DepartmentCategory(models.Model):
    _name = "human_resource.department_category"
    _description = "部门类别"
    READONLY = {'draft': [('readonly', False)]}

    department_ids = fields.One2many('human_resource.department', 'department_category_id', string=u'部门类别', index=True)
    name = fields.Char(string=u'部门类别名称', readonly=True, states=READONLY, index=True)
    company_id = fields.Many2one('partner.archives', string=u'所属公司', domain="[('is_company', '=', True)]",
                                 readonly=True, states=READONLY, index=True)
    state = fields.Selection([('draft', '草稿'), ('approval', '待审核'), ('done', '完成')], string='状态', default='draft',
                             track_visibility='onchange', index=True)
    first_letter = fields.Char(compute='_get_first_letter', store=True, string=u'名称首字母')

    @api.one
    @api.depends('name')
    def _get_first_letter(self):
        name = self.name
        if name:
            self.first_letter = git_first.get_first_letter(name)

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