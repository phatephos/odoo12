# -*- coding: utf-8 -*-
from odoo import models, fields, api
import odoorpc
try:
    from xmlrpc import client as xmlrpclib
except ImportError:
    import xmlrpclib


class Post(models.Model):
    _name = "partner.post"
    _description = u'岗位信息'
    READONLY = {'draft': [('readonly', False)]}

    name = fields.Char(string=u'岗位名称', index=True, required=True, readonly=True, states=READONLY)
    department_id = fields.Many2one('human_resource.department', string='部门名称', index=True, ondelete='cascade', readonly=True, states=READONLY)
    company_id = fields.Many2one(string='公司', related='department_id.company_id', store=True, index=True, readonly=True, states=READONLY)

    hr_post_id = fields.Integer(string=u'人力系统上的岗位id', readonly=True, states=READONLY, index=True)
    state = fields.Selection([('draft', '草稿'), ('approval', '待审核'), ('done', '完成')], string='状态', default='draft',
                             track_visibility='onchange', index=True)

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


    def get_post(self):
        """岗位"""
        odoo = odoorpc.ODOO('hr.baoshunkeji.com', port=8069)
        odoo.login('hr_db', 'admin', 'OeN4Bj0^')
        if 'human_resource.post' in odoo.env:
            Order = odoo.env['human_resource.post']
            order_ids = Order.search([['is_erp', '=', False]], limit=10)
            for order in Order.browse(order_ids):
                if order.company_id.name == '宝舜科技股份有限公司':
                    company_id = self.env['partner.archives'].search([['name', '=', order.company_id.name]])[0].id
                    lineval = {}
                    lineval['hr_post_id'] = order.id
                    lineval['name'] = order.name
                    if order.department_id and order.department_id.name and self.env['human_resource.department'].search([['name', '=', order.department_id.name]]):
                        lineval['department_id'] = self.env['human_resource.department'].search([['name', '=', order.department_id.name]])[0].id
                    lineval['company_id'] = company_id
                    self.create(lineval)
                else:
                    lineval = {}
                    lineval['hr_department_id'] = order.id
                    lineval['name'] = order.name
                    if order.department_id and order.department_id.name and self.env['human_resource.department'].search([['name', '=', order.department_id.name]]):
                        lineval['department_id']  = self.env['human_resource.department'].search([['name', '=', order.department_id.name]])[0].id
                    lineval['hr_company_id'] = order.company_id.id
                    order[0].write(lineval)
                order.write({'is_erp': True})
        # server_conf = xmlrpclib.ServerProxy("http://hr.baoshunkeji.com/xmlrpc/common")
        # uid = server_conf.login('hr_db', 'admin', 'OeN4Bj0^')
        # server = xmlrpclib.ServerProxy("http://hr.baoshunkeji.com/xmlrpc/object")
        # ids = server.execute_kw('hr_db', uid, 'OeN4Bj0^',
        #                         'human_resource.post', 'search_read',
        #                         [[['is_erp', '=', False]
        #                           ]],
        #                         {'fields': ['id','name', 'department_id', 'company_id',
        #                                     ]})
        # for id in ids:
        #     post_id = self.env['partner.post'].search([['hr_post_id', '=', id['id']]])
        #     if id['company_id'][1] == '宝舜科技股份有限公司':
        #         company_id = self.env['partner.archives'].search([['name', '=', id['company_id'][1]]])[0].id
        #         if not post_id:
        #             lineval = {}
        #             lineval['hr_post_id'] = id['id']
        #             lineval['name'] = id['name']
        #             if id['department_id'] and id['department_id'][1] and self.env['human_resource.department'].search([['name', '=', id['department_id'][1]]]):
        #                 lineval['department_id']  = self.env['human_resource.department'].search([['name', '=', id['department_id'][1]]])[0].id
        #             lineval['company_id'] = company_id
        #             self.create(lineval)
        #         else:
        #             lineval = {}
        #             lineval['hr_post_id'] = id['id']
        #             lineval['name'] = id['name']
        #             if id['department_id'] and id['department_id'][1] and self.env['human_resource.department'].search([['name', '=', id['department_id'][1]]]):
        #                 lineval['department_id']  = self.env['human_resource.department'].search([['name', '=', id['department_id'][1]]])[0].id
        #             lineval['hr_company_id'] = id['company_id'][0]
        #             post_id[0].write(lineval)
        #
        #         i = id['id']
        #         server.execute_kw('hr_db', uid, 'OeN4Bj0^', 'human_resource.post', 'write', [[i], {'is_erp': True}])


