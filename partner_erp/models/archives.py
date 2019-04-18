# -*- coding: utf-8 -*-
from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError, AccessError
from .import git_first
import datetime
import odoorpc
try:
    from xmlrpc import client as xmlrpclib
except ImportError:
    import xmlrpclib


class Archives(models.Model):
    """客户档案"""
    _name = 'partner.archives'
    _inherit = ['mail.thread']
    _description = "客户档案"
    READONLY = {'draft': [('readonly', False)]}

    name = fields.Char('名称', index=True, track_visibility='onchange')
    hr_company_id = fields.Integer(string=u'人力系统上的公司id', track_visibility='onchange', readonly=True, states=READONLY)
    post_id = fields.Many2one('partner.post', string=u'岗位', track_visibility='onchange', ondelete='restrict', states=READONLY, index=True)
    short_name = fields.Char(string=u'简称', track_visibility='onchange', states=READONLY, index=True)
    code = fields.Char('编码', index=True, track_visibility='onchange', states=READONLY)
    website = fields.Char('网站', track_visibility='onchange', states=READONLY, index=True)
    phone = fields.Char('电话', track_visibility='onchange', states=READONLY, index=True)
    address = fields.Char('地址', track_visibility='onchange', states=READONLY, index=True)
    zone_code = fields.Char('区号', track_visibility='onchange', states=READONLY, index=True)
    fax = fields.Char('传真', track_visibility='onchange', states=READONLY, index=True)
    mobile = fields.Char('手机', track_visibility='onchange', states=READONLY, index=True)
    bank_of_deposit = fields.Char('开户行', track_visibility='onchange', states=READONLY, index=True)
    bank_account = fields.Char('银行账户', track_visibility='onchange', states=READONLY, index=True)
    dollar_account = fields.Char('美元账户', track_visibility='onchange', states=READONLY, index=True)
    finance_phone = fields.Char('财务电话', track_visibility='onchange', states=READONLY, index=True)
    business_licence = fields.Char('统一社会信用代码', track_visibility='onchange', index=True)
    business_licence_image = fields.Binary('营业执照图片', track_visibility='onchange', states=READONLY)
    main_business = fields.Text('主营业务', track_visibility='onchange', states=READONLY)
    logo = fields.Binary('公司logo', track_visibility='onchange', states=READONLY)
    email = fields.Char('邮箱', track_visibility='onchange', states=READONLY, index=True)
    note = fields.Text('备注', track_visibility='onchange', states=READONLY)
    legal_person = fields.Char(track_visibility='onchange', string=u'法人', index=True)
    identity_no = fields.Char('法人身份证号', track_visibility='onchange', states=READONLY, index=True)
    identity_no_image = fields.Binary('法人身份证图片', track_visibility='onchange', states=READONLY)
    datas = fields.Binary('附件', compute='_compute_datas', inverse='_inverse_datas', states=READONLY, store=True)
    datas_fname = fields.Char('附件名称', states=READONLY, index=True)
    inviting_id = fields.Many2one('partner.archives', '客户经理', domain="[('bill_type', '=', 'users')]",
                                  ondelete='restrict', track_visibility='onchange', states=READONLY, index=True)
    # create_id = fields.Many2one('res.users', '创建人', default=lambda self: self._uid, readonly=True, states=READONLY)
    partner_type = fields.Selection([('1', '销售客户'), ('2', '采购客户'), ('3', '中间商'), ('4', '物资采购客户')], '客户类型',
                                    track_visibility='onchange', states=READONLY, index=True)

    is_sale = fields.Boolean('是否是销售客户', track_visibility='onchange', default=False, states=READONLY, index=True)
    is_purchase = fields.Boolean('是否是采购客户', track_visibility='onchange', default=False, states=READONLY, index=True)
    is_middle = fields.Boolean('是否是中间客户', track_visibility='onchange', default=False, states=READONLY, index=True)
    is_material = fields.Boolean('是否是物资客户', track_visibility='onchange', default=False, states=READONLY, index=True)
    is_equipment = fields.Boolean('是否是设备客户', track_visibility='onchange', default=False, states=READONLY, index=True)
    is_company = fields.Boolean('是否公司', track_visibility='onchange', default=False, states=READONLY, index=True)

    date = fields.Date('创建日期', track_visibility='onchange', default=fields.Date.context_today, states=READONLY)
    active = fields.Boolean(default=True, track_visibility='onchange', states=READONLY, index=True)

    account_ids = fields.One2many('partner.account', 'archives_id', '银行账户', track_visibility='onchange', ondelete='restrict', states=READONLY, index=True)
    area_id = fields.Many2one('partner.area', '客户地区', track_visibility='onchange', ondelete='restrict', states=READONLY, index=True)

    bill_type = fields.Selection([('partner', '客户档案'),
                                  ('users', '人员信息'),
                                  ('company', '公司档案'),],string=u'类型',
                                    track_visibility='onchange', readonly=True, states=READONLY, index=True)
    company_id = fields.Many2one('partner.archives', track_visibility='onchange', domain="[('bill_type', '=', 'company')]", string='公司',
                                 ondelete='restrict', readonly=True, states=READONLY, index=True)
    department_id = fields.Many2one('human_resource.department', track_visibility='onchange', string='部门ID', ondelete='restrict',
                                    readonly=True, states=READONLY, index=True)
    department = fields.Char(string='部门', track_visibility='onchange', related='department_id.name', store=True, readonly=True, states=READONLY, index=True)
    user_id = fields.Many2one('res.users', track_visibility='onchange', string='相关用户', ondelete='restrict', states=READONLY, index=True)
    # account_count = fields.Integer(compute='get_account_count', store=True)
    crm_c_partner_id = fields.Integer(string=u'老crm中的客户', track_visibility='onchange', readonly=True, states=READONLY)
    state = fields.Selection([('draft', '草稿'), ('approval', '待审核'), ('done', '完成')], string='状态', default='draft',
                             track_visibility='onchange', index=True)
    material_ids = fields.Many2many('code.material_codes', track_visibility='onchange', ondelete='restrict', string=u'物料', index=True)
    user_char = fields.Char(string='用户备注')
    # first_letter = fields.Char(compute='_get_first_letter', store=True, string=u'名称首字母')
    employee_id = fields.Many2one('partner.archives', string=u'制单人', default=lambda self: self.env['partner.archives'].
                                  search([('user_id', '=', self.env.user.id)], limit=1).id,
                                  track_visibility='onchange', index=True, ondelete='restrict')
    flow_company_id = fields.Many2one('partner.archives', string=u'客户公司', related='employee_id.company_id', store=True)
    #
    # @api.one
    # @api.depends('name')
    # def _get_first_letter(self):
    #     name = self.name
    #     if name:
    #         self.first_letter = git_first.get_first_letter(name)

    def change_partner_message(self):
        view_id = self.env.ref('partner_erp.change_archives_form').id
        return {'type': 'ir.actions.act_window',
                'view_type': 'form',
                'res_model': 'partner.change_archives',
                'target': 'new',
                'views': [[view_id, "form"]],
                'context': {
                    'default_archives_id': self.id,
                    'from_view_ref': 'partner_erp.change_archives_form'
                    }
                }

    @api.onchange('user_id')
    def get_ueser_phone(self):
        if self.user_id:
            if self.user_id.phone:
                self.phone = self.user_id.phone

    ###############################################################################################################
    # 增加附件上传功能
    attachment_number = fields.Integer(compute='_compute_attachment_number', string='Number of Attachments')
    @api.multi
    def _compute_attachment_number(self):
        """附件上传"""
        attachment_data = self.env['ir.attachment'].read_group([('res_model', '=', 'partner.archives'), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
        for expense in self:
            expense.attachment_number = attachment.get(expense.id, 0)

    @api.multi
    def action_get_attachment_view(self):
        """附件上传动作视图"""
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('base', 'action_attachment')
        res['domain'] = [('res_model', '=', 'partner.archives'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'partner.archives', 'default_res_id': self.id}
        return res
    #############################################################################################

    @api.model
    def create(self, vals):
        res = super(Archives, self).create(vals)
        if res.bill_type == 'partner':
            name = self.search([('name', '=', res.name)])
            if len(name) > 1:
                raise ValidationError("客户为{0}已存在，请重新填写!".format(res.name))
        return res

    @api.one
    def unlink(self):
        """在state字段不为草稿时不允许删除，"""
        if self.state != 'draft':
            raise UserError(u'完成状态下不允许删除。')
        else:
            return super(Archives, self).unlink()


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

    @api.constrains('business_licence')
    def _check_business_licence(self):
        """限制统一社会信用代码不能重复出现"""
        business_licences = self.search([('business_licence', '=', self.business_licence)])
        if len(business_licences) > 1:
            raise ValidationError("统一社会信用代码或身份证号为{0}已存在，请重新填写!" .format(self.business_licence))

    def _get_company_id(self, company_name):
        company = self.env['partner.archives']
        company_ids = company.search([['name', '=', company_name]])
        company_id = company_ids[0].id
        return company_id

    @api.one
    def _compute_datas(self):
        """生成附件"""
        attach = self.env['ir.attachment'].search([['res_field', '=', 'datas'], ['res_model', '=', 'partner.archives'], ['res_id', '=', self.id]])
        if attach:
            self.datas = attach.datas

    @api.one
    def _inverse_datas(self):
        """生成附件"""
        attach = self.env['ir.attachment'].search([['res_field', '=', 'datas'], ['res_model', '=', 'partner.archives'], ['res_id', '=', self.id]])
        if attach:
            if self.datas:
                attach.write({'name': self.datas_fname,
                              'datas_fname': self.datas_fname,
                              'res_model': 'partner.archives',
                              'res_field': 'datas',
                              'res_id': self.id,
                              'type': 'binary',
                              'datas': self.datas})
            else:
                attach.unlink()
        else:
            if self.datas:
                self.env['ir.attachment'].create({'name': self.datas_fname,
                                                  'datas_fname': self.datas_fname,
                                                  'res_model': 'partner.archives',
                                                  'res_field': 'datas',
                                                  'res_id': self.id,
                                                  'type': 'binary',
                                                  'datas': self.datas})

    def get_crm_c_company(self):
        odoo = odoorpc.ODOO('baoshunkeji.com', port=8069)
        odoo.login('tender_db', 'admin', 'OeN4Bj0^')
        if 'crm_c.partner' in odoo.env:
            Order = odoo.env['crm_c.partner']
            order_ids = Order.search([['business_licence', '!=', ''], ['is_erp', '=', False]], limit=10)
            for order in Order.browse(order_ids):
                lineval = {}
                lineval['name'] = order.name
                lineval['bill_type'] = 'partner'
                lineval['is_sale'] = order.is_sale_customer
                lineval['is_purchase'] = order.is_purchase_supplier
                lineval['phone'] = order.phone
                lineval['address'] = order.address
                lineval['mobile'] = order.mobile
                lineval['business_licence'] = order.business_licence
                lineval['main_business'] = order.main_business
                lineval['note'] = order.comment

                self.create(lineval)
                order.write({'is_erp': True})

    def get_material_partner(self):
        odoo = odoorpc.ODOO('baoshunkeji.com', port=8069)
        odoo.login('tender_db', 'admin', 'OeN4Bj0^')
        if 'tender.partner' in odoo.env:
            Order = odoo.env['tender.partner']
            order_ids = Order.search([['business_licence', '!=', ''], ['state', '=', 'done'], ['is_erp', '=', False]], limit=10)
            for order in Order.browse(order_ids):
                lineval = {}
                lineval['name'] = order.name
                lineval['bill_type'] = 'partner'
                lineval['is_material'] = True
                lineval['phone'] = order.phone
                lineval['address'] = order.address
                lineval['mobile'] = order.mobile
                lineval['zone_code'] = order.zone_code
                lineval['fax'] = order.fax
                lineval['website'] = order.website
                lineval['business_licence'] = order.business_licence
                lineval['main_business'] = order.main_business
                lineval['identity_no'] = order.identity_no
                lineval['note'] = order.comment
                self.create(lineval)
                order.write({'is_erp': True})

    def get_company(self):
        """人员"""
        odoo = odoorpc.ODOO('hr.baoshunkeji.com', port=8069)
        odoo.login('hr_db', 'admin', 'OeN4Bj0^')
        if 'human_resource.psn_coll' in odoo.env:
            Order = odoo.env['human_resource.psn_coll']
            order_ids = Order.search([['id_num', '!=', False], ['is_erp', '=', False]], limit=10)
            for order in Order.browse(order_ids):
                if order.company_id.name == '宝舜科技股份有限公司':
                    company_id = self._get_company_id(order.company_id.name)
                    lineval = {}
                    lineval['hr_company_id'] = order.id
                    lineval['name'] = order.name
                    lineval['bill_type'] = 'users'
                    lineval['business_licence'] = order.id_num
                    if order.department_id and order.department_id.name and self.env['human_resource.department'].search(
                            [['name', '=', order.department_id.name]]):
                        lineval['department_id'] = self.env['human_resource.department'].search(
                            [['name', '=', order.department_id.name]])[0].id
                    if order.post_id and order.post_id.name and self.env['partner.post'].search([['name', '=', order.post_id.name]]):
                        lineval['post_id'] = self.env['partner.post'].search([['name', '=', order.post_id.name]])[0].id
                    lineval['company_id'] = company_id
                    self.create(lineval)
                else:
                    lineval = {}
                    lineval['hr_company_id'] = order.id
                    lineval['name'] = order.name
                    lineval['bill_type'] = 'users'
                    lineval['business_licence'] = order.id_num
                    if order.department_id and order.department_id.name and self.env[
                        'human_resource.department'].search(
                            [['name', '=', order.department_id.name]]):
                        lineval['department_id'] = self.env['human_resource.department'].search(
                            [['name', '=', order.department_id.name]])[0].id
                    if order.post_id and order.post_id.name and self.env['partner.post'].search(
                            [['name', '=', order.post_id.name]]):
                        lineval['post_id'] = self.env['partner.post'].search([['name', '=', order.post_id.name]])[0].id
                    lineval['company_id'] = company_id
                    order[0].write(lineval)
                order.write({'is_erp': True})

        # server_conf = xmlrpclib.ServerProxy("http://hr.baoshunkeji.com/xmlrpc/common")
        # uid = server_conf.login('hr_db', 'admin', 'OeN4Bj0^')
        # server = xmlrpclib.ServerProxy("http://hr.baoshunkeji.com/xmlrpc/object")
        # ids = server.execute_kw('hr_db', uid, 'OeN4Bj0^',
        #                         'human_resource.psn_coll', 'search_read',
        #                         [[['id_num', '!=', False]
        #                           ]],
        #                         {'fields': ['id', 'name','id_num','department_id','company_id','post_id',
        #                                     ]})
        # for id in ids:
        #     partner_id = self.env['human_resource.department'].search([['hr_department_id', '=', id['id']]])
        #     if id['company_id'][1] == '宝舜科技股份有限公司':
        #         company_id = self._get_company_id(id['company_id'][1])
        #         if not partner_id :
        #             lineval = {}
        #             lineval['hr_company_id'] = id['id']
        #             lineval['name'] = id['name']
        #             lineval['bill_type'] = 'users'
        #             lineval['business_licence'] = id['id_num']
        #             if id['department_id'] and id['department_id'][1] and self.env['human_resource.department'].search(
        #                     [['name', '=', id['department_id'][1]]]):
        #                 lineval['department_id'] = \
        #                 self.env['human_resource.department'].search([['name', '=', id['department_id'][1]]])[0].id
        #             if id['post_id'] and id['post_id'][1] and self.env[
        #                 'partner.post'].search(
        #                     [['name', '=', id['post_id'][1]]]):
        #                 lineval['post_id'] = \
        #                     self.env['partner.post'].search([['name', '=', id['post_id'][1]]])[0].id
        #             lineval['company_id'] = company_id
        #             self.create(lineval)
        #         else:
        #             lineval = {}
        #             lineval['hr_company_id'] = id['id']
        #             lineval['name'] = id['name']
        #             lineval['bill_type'] = 'users'
        #             lineval['business_licence'] = id['id_num']
        #             if id['department_id'] and id['department_id'][1] and self.env['human_resource.department'].search(
        #                     [['name', '=', id['department_id'][1]]]):
        #                 lineval['department_id'] = \
        #                     self.env['human_resource.department'].search([['name', '=', id['department_id'][1]]])[0].id
        #             if id['post_id'] and id['post_id'][1] and self.env[
        #                 'partner.post'].search(
        #                 [['name', '=', id['post_id'][1]]]):
        #                 lineval['post_id'] = \
        #                     self.env['partner.post'].search([['name', '=', id['post_id'][1]]])[0].id
        #             lineval['company_id'] = company_id
        #             partner_id[0].write(lineval)
        #         i = id['id']
        #         server.execute_kw('hr_db', uid, 'OeN4Bj0^', 'human_resource.psn_coll', 'write', [[i], {'is_erp': True}])

    @api.constrains('bill_type')
    def check_group(self):
        if not self.env.user.has_group('partner_erp.group_all'):
            if self.is_company is True:
                if not self.env.user.has_group('partner_erp.group_group_finance'):
                    raise ValidationError('集团财务权限能操作此单据')
            # elif self.bill_type == 'partner':
            #     if not self.env.user.has_group('partner_erp.group_crm_employee') and not self.env.user.has_group('partner_erp.group_crm_secretary') and not self.env.user.has_group('partner_erp.group_crm_leader'):
            #         raise ValidationError('供销业务员,供销秘书,供销领导权限能操作此单据')
            elif self.bill_type == 'users':
                if not self.env.user.has_group('partner_erp.group_all') or not self.env.user.has_group('partner_erp.group_group_finance'):
                    raise ValidationError('管理员和集团财务权限能操作此单据')

    @api.multi
    def write(self, vals):
        """变更客户名称判断过磅是否已有客户信息"""
        if 'name' in vals:
            hn_odoo = odoorpc.ODOO('bs.baoshunkeji.com', port=8069)
            hn_odoo.login('bs_db', 'odoorpc', 'odoorpc')
            weigh_partner_id = hn_odoo.env['weigh.partner'].search_read([['name', '=', self.name]])
            if not weigh_partner_id:
                sd_odoo = odoorpc.ODOO('192.168.5.7', port=8069)
                sd_odoo.login('weigh', 'weigh', 'OeN4Bj0^')
                weigh_partner_id = sd_odoo.env['res.partner'].search_read([['name', '=', self.name]])
                if not weigh_partner_id:
                    xj_odoo = odoorpc.ODOO('xj.baoshunkeji.com', port=8069)
                    xj_odoo.login('weigh', 'weigh', 'OeN4Bj0^')
                    weigh_partner_id = xj_odoo.env['weigh.partner'].search_read([['name', '=', self.name]])
            if weigh_partner_id:
                raise ValidationError('过磅系统已经生成该客户信息，不可修改，如果必须修改请联系IT人员')
        return super(Archives, self).write(vals)

    #融资字段
    parent_id = fields.Many2one('partner.archives', ondelete='restrict', domain=[('is_parent', '=', True), ('is_company', '=', True)],
                                track_visibility='onchange', readonly=True, states=READONLY, string=u'母公司', index=True)
    is_parent = fields.Boolean(default=False, track_visibility='onchange', readonly=True, states=READONLY,
                               string=u'是否是母公司', index=True)
    is_self = fields.Boolean(default=False, track_visibility='onchange', readonly=True, states=READONLY,
                             string=u'是否是本公司', index=True)


class Account(models.Model):
    """银行账户"""
    _name = 'partner.account'
    _inherit = ['mail.thread']
    _description = "银行账户"
    READONLY = {'draft': [('readonly', False)]}

    archives_id = fields.Many2one('partner.archives', '客户名称', track_visibility='onchange', required=True,
                                  ondelete='restrict', readonly=True, states=READONLY, index=True)
    flow_company_id = fields.Many2one('partner.archives', string=u'客户公司', related='archives_id.flow_company_id', store=True)
    name = fields.Char(string=u'账户名称', compute='get_name', store=True, track_visibility='onchange',
                       readonly=True, states=READONLY, index=True)
    bank_table_id = fields.Many2one('partner.bank_table', string=u'银行', track_visibility='onchange', required=True,
                                    readonly=True, states=READONLY, ondelete='restrict', index=True)
    # other_bank_type = fields.Char(string=u'具体账户类型', track_visibility='onchange')
    bank_name = fields.Char(string=u'账户名称', track_visibility='onchange', required=True, readonly=True, states=READONLY, index=True)
    number = fields.Char(string=u'银行账号', track_visibility='onchange', required=True, readonly=True, states=READONLY, index=True)
    # name = fields.Char(string=u'客户银行账号', compute='_name_get', store=True)
    note = fields.Text(string=u'备注', readonly=True, states=READONLY)
    bill_type = fields.Selection([('partner', '客户档案'),
                                  ('users', '人员档案'),
                                  ('company', '公司档案'), ], string=u'类型',
                                 track_visibility='onchange', readonly=True, states=READONLY, index=True)
    state = fields.Selection([('draft', '草稿'), ('approval', '待审核'), ('done', '完成')], string='状态', default='draft',
                             track_visibility='onchange', index=True)
    currency_id = fields.Many2one('res.currency', string=u'币种',
                                  default=lambda self: self.env['res.currency'].search(
                                      [('code', '=', 'CNY')]), readonly=True, states=READONLY, index=True, ondelete='restrict')
    account_type = fields.Selection(
        [('current', '活期'), ('agreement', '协定'), ('margin', '保证金户'), ('notice', '通知'), ('regular', '定期')],
        string='账户类型', track_visibility='onchange', readonly=True, states=READONLY, index=True)
    account_type_id = fields.Many2one('partner.account_type', string=u'账户类别')
    account_type_detail_id = fields.Many2one('partner.account_type_detail', string=u'账户类别明细',
                                             domain="[('account_type_id', '=', account_type_id)]")
    account_nature = fields.Char(string=u'账户性质', default='单位', index=True)
    account_open_date = fields.Date(string=u'开户日期')
    account_state = fields.Selection([('current', '正常'), ('margin', '不正常'), ('sales', '销户'), ('noneed', '不用')], string='账户状态', default='current',
                                     track_visibility='onchange', index=True)
    # account_state = fields.Many2one('partner.account_state', string=u'账户状态')
    is_default = fields.Boolean(string=u'是否默认账户', default=False, index=True)
    # first_letter = fields.Char(compute='_get_first_letter', store=True, string=u'名称首字母')
    #
    # @api.one
    # @api.depends('name')
    # def _get_first_letter(self):
    #     name = self.name
    #     if name:
    #         self.first_letter = git_first.get_first_letter(name)

    @api.constrains('archives_id', 'is_default')
    def _check_name_default(self):
        """限制银行名字不能重复出现"""
        names = self.search(['&', ('archives_id', '=', self.archives_id.id), ('is_default', '=', True)])
        if len(names) > 1:
            raise ValidationError('该客户的默认账户已经存在！')

    @api.one
    @api.depends('bank_table_id', 'number')
    def get_name(self):
        self.name = self.bank_table_id.name + '' + self.number[-4: ]

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

    @api.one
    def unlink(self):
        """在state字段不为草稿时不允许删除，"""
        if self.state == 'done' or self.state == 'approval':
            raise UserError(u'该状态下的单据不可删除！')
        else:
            return super(Account, self).unlink()

    @api.constrains('bill_type')
    def check_group(self):
        if not self.env.user.has_group('partner_erp.group_all'):
            if self.bill_type == 'company':
                if self.env.user.has_group('partner_erp.group_group_finance'):
                    raise ValidationError('只有集团财务权限能操作此单据')
            # elif self.bill_type == 'partner':
            #     if not self.env.user.has_group('partner_erp.group_crm_employee') and not self.env.user.has_group(
            #             'partner_erp.group_crm_secretary') and not self.env.user.has_group('partner_erp.group_crm_leader'):
            #         raise ValidationError('只有供销业务员、供销秘书和供销领导权限能操作此单据')
            elif self.bill_type == 'users':
                if not self.env.user.has_group('partner_erp.group_all') or self.env.user.has_group('partner_erp.group_group_finance'):
                    raise ValidationError('只有管理员或集团财务能操作此单据')


class AccountState(models.Model):
    """银行账户状态"""
    _name = 'partner.account_state'
    _inherit = ['mail.thread']
    _description = "银行账户状态"
    READONLY = {'draft': [('readonly', False)]}

    name = fields.Char(string=u'名称', index=True, readonly=True, states=READONLY)
    state = fields.Selection([('draft', '草稿'),
                              ('confirm', '审批中'),
                              ('done', '完成')], string='状态', default='draft', track_visibility='onchange', index=True)

    # first_letter = fields.Char(compute='_get_first_letter', store=True, string=u'名称首字母')
    #
    # @api.one
    # @api.depends('name')
    # def _get_first_letter(self):
    #     name = self.name
    #     if name:
    #         self.first_letter = git_first.get_first_letter(name)

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
            return super(AccountState, self).unlink()


class Bank(models.Model):
    """银行"""
    _name = 'partner.bank'
    _description = "银行名称"
    READONLY = {'draft': [('readonly', False)]}

    name = fields.Char(string=u'银行名称', required=True, track_visibility='onchange', readonly=True, states=READONLY, index=True)
    state = fields.Selection([('draft', '草稿'), ('approval', '待审核'), ('done', '完成')], string='状态', default='draft',
                             track_visibility='onchange', index=True)
    mnemonic_code = fields.Char(string=u'助记码', index=True)
    active = fields.Boolean(default=True, track_visibility='onchange', states=READONLY, index=True)
    # first_letter = fields.Char(compute='_get_first_letter', store=True, string=u'名称首字母')
    bank_type_id = fields.Many2one('partner.bank_type', string=u'银行类别')

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

    @api.constrains('name')
    def _check_name(self):
        """限制银行名字不能重复出现"""
        names = self.search([('name', '=', self.name)])
        if len(names) > 1:
            raise ValidationError('银行名字已经存在！')


class BankTable(models.Model):
    """银行表"""
    _name = 'partner.bank_table'
    _inherit = ['mail.thread']
    _description = "银行表"
    READONLY = {'draft': [('readonly', False)]}

    bank_id = fields.Many2one('partner.bank', ondelete='restrict', required=True, string=u'银行类别',
                              readonly=True, states=READONLY, index=True, domain="[('state', '=', 'done')]")
    bank_address = fields.Char(required=True, track_visibility='onchange', string=u'银行所在地（市）',
                               readonly=True, states=READONLY, index=True)
    bank_name = fields.Char(required=True, track_visibility='onchange', string=u'支行名称', readonly=True,
                            states=READONLY, index=True)
    name = fields.Char(string=u'银行', store=True, readonly=True, states=READONLY, index=True, required=True)
    # create_id = fields.Many2one('res.users', '创建人', required=True, default=lambda self: self._uid,
    #                             readonly=True)
    # is_bank = fields.Boolean(default=True, track_visibility='onchange', readonly=True, states=READONLY, string=u'是否是贷款银行')
    state = fields.Selection([('draft', '草稿'), ('approval', '待审核'), ('done', '完成')], string='状态', default='draft',
                             track_visibility='onchange', index=True)
    active = fields.Boolean(default=True, track_visibility='onchange', states=READONLY, index=True)
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

    @api.one
    @api.depends('bank_id', 'bank_address', 'bank_name')
    def _name_get(self):
        """拼名字"""
        if self.bank_id and self.bank_address and self.bank_name:
            self.name = str(self.bank_id.name) + str(self.bank_address) + str(self.bank_name)

    @api.constrains('name')
    def _check_name(self):
        """限制银行名字不能重复出现"""
        names = self.search([('name', '=', self.name)])
        if len(names) > 1:
            raise ValidationError('名字已经存在！')


    #融资
    # is_bank = fields.Boolean(default=True, track_visibility='onchange',
    #                          string=u'是否是贷款银行')
    # loans_ids = fields.One2many('financing.loans', 'branch_bank_id', string=u'贷款合同')
    # credit_ids = fields.One2many('financing.credit', 'branch_bank_id', string=u'授信')
    # credit_amount = fields.Float(digits=(2, 2), compute='_get_credit', store=True, string=u'授信总额')
    # # credit_remaining = fields.Float(digits=(2, 2), compute='_get_credit', store=True, string=u'授信余额')
    # loans_remaining = fields.Float(digits=(2, 2), compute='_get_loans_remaining', store=True, string=u'贷款余额')
    # cost = fields.Float(digits=(2, 4), string=u'成本')
    # loans_count = fields.Integer(compute='_get_loans_count', string=u'贷款合同数')
    # loan_ids = fields.One2many('financing.loan', 'branch_bank_id', string=u'放款')
    # matching_ids = fields.One2many('financing.matching', 'branch_bank_id', string=u'配套业务')
    # matching_count = fields.Integer(compute='_get_matching_count', string=u'配套业务数量')
    #
    # @api.model
    # def fm_bank_cost(self):
    #     """计算银行成本"""
    #     for cost in self.search([]):
    #         cost.get_bank_cost()
    #     for cost in self.env['partner.archives'].search([]):
    #         cost.get_company_cost()
    #
    # @api.one
    # def get_bank_cost(self):
    #     value1 = value2 = value3 = 0.0
    #     for i in self.loan_ids:
    #         value2 += i.loan_amount
    #     for j in self.matching_ids:
    #         value3 += j.matching_cost * 100
    #     for k in self.loans_ids:
    #         value1 += k.year_cost
    #     if value2:
    #         self.cost = (value1 + value3) / value2
    #
    # @api.one
    # @api.depends('main_bank_id', 'main_bank_id.name', 'branch_bank_address', 'branch_bank')
    # def _name_get(self):
    #     """拼名字"""
    #     self.name = self.main_bank_id.name + self.branch_bank_address + self.branch_bank
    #
    # @api.one
    # @api.depends('credit_ids', 'credit_ids.actual_credit_amount', 'credit_ids.states')
    # def _get_credit(self):
    #     """计算授信总额 余额"""
    #     credit_ids = self.env['financing.credit'].search((['states', 'in', ('final', 'three month')],
    #                                                       ['branch_bank_id', '=', self.id]))
    #     self.credit_amount = sum(credit_ids.mapped('actual_credit_amount'))
    #
    #     # value1 = value2 = 0.0
    #     #
    #     # for i in self.credit_ids:
    #     #     value1 += i.actual_credit_amount
    #     # self.credit_amount = value1
    #
    # # @api.one
    # # @api.depends('credit_ids', 'credit_ids.states', 'credit_ids.actual_credit_amount')
    # # def _get_credit(self):
    # #     value1 = 0.0
    # #     for i in self.credit_ids:
    # #         if i.states == 'overdue' or i.states == 'renewal':
    # #             continue
    # #         else:
    # #             value1 += i.actual_credit_amount
    # #     self.credit_amount = value1
    #
    # @api.one
    # @api.depends('loans_ids', 'loans_ids.loans_state', 'loans_ids.loans_remaining')
    # def _get_loans_remaining(self):
    #     """计算贷款余额"""
    #     value1 = 0.0
    #     for i in self.loans_ids:
    #         if i.loans_state != 'over':
    #             value1 += i.loans_remaining
    #     self.loans_remaining = value1
    #
    # # @api.one
    # # @api.depends('loans_ids', 'loans_ids.loans_state', 'loans_ids.total_amount', 'loans_ids.capital')
    # # def _get_loans_remaining(self):
    # #     value = 0.0
    # #     for i in self.loans_ids:
    # #         if i.loans_state == 'repayment':
    # #             value += i.total_amount - i.capital
    # #         elif i.loans_state == 'over':
    # #             value += 0.0
    # #         else:
    # #             value += i.total_amount
    # #     self.loans_remaining = value
    #
    # @api.one
    # @api.depends('loans_ids')
    # def _get_loans_count(self):
    #     """计算合同数量"""
    #     self.loans_count = self.loans_ids.__len__()
    #
    # @api.one
    # @api.depends('matching_ids')
    # def _get_matching_count(self):
    #     """计算配套业务数量"""
    #     self.matching_count = self.matching_ids.__len__()


class Contact(models.Model):
    """ 客户联系人"""
    _name = 'partner.contact'
    _inherit = ['mail.thread']
    _description = "客户联系人"
    READONLY = {'draft': [('readonly', False)]}

    archives_id = fields.Many2one('partner.archives', ondelete='restrict', index=True,
                                  track_visibility='onchange', string=u'客户', required=True, readonly=True, states=READONLY)
    name = fields.Char(required=True, track_visibility='onchange', string=u'名称', readonly=True, states=READONLY, index=True)
    title = fields.Char(track_visibility='onchange', string=u'称谓', readonly=True, states=READONLY, index=True)
    function = fields.Char(track_visibility='onchange', string=u'职位', readonly=True, states=READONLY, index=True)
    email = fields.Char(track_visibility='onchange', string=u'邮箱', readonly=True, states=READONLY, index=True)
    phone = fields.Char(track_visibility='onchange', string=u'电话', readonly=True, states=READONLY, index=True)
    mobile = fields.Char(track_visibility='onchange', string=u'手机', readonly=True, states=READONLY, index=True)
    identity = fields.Char(track_visibility='onchange', string=u'身份证号', readonly=True, states=READONLY, index=True)
    interest = fields.Text(track_visibility='onchange', string=u'爱好', readonly=True, states=READONLY)
    experience = fields.Text(track_visibility='onchange', string=u'经历', readonly=True, states=READONLY)
    experience_ids = fields.One2many('partner.experience', 'contact_id',track_visibility='onchange',  string=u'经历',
                                     readonly=True, states=READONLY, index=True)
    country_id = fields.Char(default='Chinese',track_visibility='onchange', readonly=True, states=READONLY, index=True)
    stated_id = fields.Char(string=u'省/市',track_visibility='onchange', readonly=True, states=READONLY, index=True)
    city = fields.Char(string=u'城市',track_visibility='onchange', readonly=True, states=READONLY, index=True)
    # create_id = fields.Many2one('res.users', '创建人', required=True, default=lambda self: self._uid,
    #                             readonly=True, states=READONLY)
    state = fields.Selection([('draft', '草稿'), ('approval', '待审核'), ('done', '完成')], string='状态', default='draft',
                             track_visibility='onchange', readonly=True, states=READONLY, index=True)

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

    def get_partner_contact(self):
        odoo = odoorpc.ODOO('baoshunkeji.com', port=8069)
        odoo.login('tender_db', 'admin', 'OeN4Bj0^')
        if 'crm_c.contact' in odoo.env:
            Order = odoo.env['crm_c.contact']
            order_ids = Order.search([['is_erp', '=', False]], limit=10)
            for order in Order.browse(order_ids):
                partner_id = self.env['partner.archives'].search([['bill_type', '=', 'partner'],
                                                                  ['is_material', '=', False],
                                                                  ['name', '=', order.partner_id.name]])
                if partner_id:
                    lineval = {}
                    lineval['archives_id'] = partner_id[0].id
                    lineval['name'] = order.name
                    lineval['title'] = order.title
                    lineval['function'] = order.function
                    lineval['email'] = order.email
                    lineval['phone'] = order.phone
                    lineval['mobile'] = order.mobile
                    lineval['identity'] = order.identity
                    lineval['country_id'] = order.country_id
                    lineval['city'] = order.city
                    lineval['interest'] = order.interest
                    self.create(lineval)
                order.write({'is_erp': True})


class Experience(models.Model):
    """ 经历"""
    _name = 'partner.experience'
    _description = "经历"

    contact_id = fields.Many2one('partner.contact', ondelete='restrict', index=True)
    name = fields.Text(string=u'经历', index=True)







