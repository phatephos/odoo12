# -*- coding: utf-8 -*-


from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError, AccessError
import datetime


class Customer(models.Model):
    """客户档案"""
    _name='xr_base.customer'
    _description = u"客户"
    _inherit = ['mail.thread']

    name = fields.Char(string=u'客户', track_visibility='onchange', required=True)
    address = fields.Char(string=u'地址', track_visibility='onchange')
    area_id = fields.Many2one('xr_base.area', string=u'客户地区',
                              domain=[('state', '=', 'done')], track_visibility='onchange')
    business_licence = fields.Char(string=u'统一社会信用代码', track_visibility='onchange', required=True)
    mobile = fields.Char(string=u'手机', track_visibility='onchange')
    business_licence_image = fields.Binary(string=u'营业执照图片', track_visibility='onchange')
    main_business = fields.Text(string=u'主营业务', track_visibility='onchange')
    identity_no = fields.Char(string=u'法人身份证号', track_visibility='onchange')
    identity_no_image = fields.Binary(string=u'法人身份证图片', track_visibility='onchange')
    finance_phone = fields.Char(string=u'财务电话', track_visibility='onchange')
    inviting_id = fields.Many2one('xr_base.archives', domain=[('state', '=', 'done')],
                                  string=u'客户经理', track_visibility='onchange')
    account_ids = fields.One2many('xr_base.account', 'customer_name_id',
                                  string=u'银行账户', track_visibility='onchange')
    enclosure = fields.Binary(string=u'附件')
    enclosure_name = fields.Char(string=u'附件名称')
    note = fields.Text(string=u'备注', track_visibility='onchange')
    date = fields.Date(string=u'创建日期', default=fields.Date.context_today, track_visibility='onchange')
    state = fields.Selection([('draft', '草稿'),
                              ('approve', '待审核'),
                              ('done', '完成')
                              ], string='状态', default='draft',
                             track_visibility='onchange')

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
            return super(Customer, self).unlink()


class Account(models.Model):
    """银行档案"""
    _name = 'xr_base.account'
    _inherit = ['mail.thread']
    _description = u"银行账户"

    customer_name_id = fields.Many2one('xr_base.customer')
    account_opening = fields.Many2one('xr_base.customer',
                                      domain=[('state', '=', 'done')], string=u'开户公司')
    bank_name = fields.Char(string=u'账户名称', track_visibility='onchange',)
    number = fields.Char(string=u'银行账号', track_visibility='onchange', )
    note = fields.Text(string=u'备注')
    is_default = fields.Boolean(string=u'是否默认账户', default=False)
    state = fields.Selection([('draft', '草稿'),
                              ('approve', '待审核'),
                              ('done', '完成')
                              ], string='状态', default='draft',
                             track_visibility='onchange')

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
        if self.state == 'done' or self.state == 'approve':
            raise UserError(u'该状态下的单据不可删除！')
        else:
            return super(Account, self).unlink()


class Archives(models.Model):
    """客户经理档案"""
    _name = 'xr_base.archives'
    _inherit = ['mail.thread']
    _description = "客户联系人"

    name = fields.Char(string=u'名称', track_visibility='onchange', required=True)
    archives_id = fields.Many2one('xr_base.customer', string=u'客户',
                                  domain=[('state', '=', 'done')], track_visibility='onchange',  required=True)
    title = fields.Char(track_visibility='onchange', string=u'称谓')
    function = fields.Char(track_visibility='onchange', string=u'职位')
    email = fields.Char(track_visibility='onchange', string=u'邮箱',)
    phone = fields.Char(track_visibility='onchange', string=u'电话', )
    mobile = fields.Char(track_visibility='onchange', string=u'手机', )
    identity = fields.Char(track_visibility='onchange', string=u'身份证号',)
    stated_id = fields.Char(string=u'省/市', track_visibility='onchange')
    interest = fields.Text(track_visibility='onchange', string=u'爱好', )
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


class Area(models.Model):
    """客户地区档案"""
    _name = 'xr_base.area'
    _inherit = ['mail.thread']
    _description = "客户地区"

    name = fields.Char(string=u'地区名称', track_visibility='onchange', required=True)
    archives_ids = fields.One2many('xr_base.customer','area_id', string=u'客户',
                                   domain=[('state', '=', 'done')], track_visibility='onchange',  required=True)
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



