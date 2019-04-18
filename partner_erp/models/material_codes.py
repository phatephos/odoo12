# -*- coding:utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, AccessError
from .import git_first
try:
    from xmlrpc import client as xmlrpclib
except ImportError:
    import xmlrpclib
from .import git_first


class MaterialCodes(models.Model):
    """
    存货详情副本
    """
    _name = 'code.material_codes'
    _description = u'存货详情'
    _inherit = ['mail.thread',]
    READONLY = {'draft': [('readonly', False)]}

    name = fields.Char(string=u'存货名称', readonly=True, states=READONLY, track_visibility='onchange', index=True)
    domain = fields.Char(string='条件')
    material_id = fields.Many2one('code.material', string=u'存货分类', readonly=True, states=READONLY, track_visibility='onchange', index=True)
    label_id = fields.Many2one('code.label', string=u'标签', readonly=True, states=READONLY, track_visibility='onchange', index=True)
    main_measurement = fields.Many2one('code.metering', string=u'主计量单位', readonly=True, states=READONLY, track_visibility='onchange', index=True)
    invcode = fields.Char(string=u'物料编码', readonly=True, states=READONLY, track_visibility='onchange', index=True)
    invspec = fields.Char(string=u'规格', readonly=True, states=READONLY, track_visibility='onchange', index=True)
    state = fields.Selection([('draft', '草稿'), ('approval', '待审核'), ('done', '完成')], string='状态', default='draft',
                             track_visibility='onchange', index=True)
    tax_id = fields.Many2one('fm.account.tax', string=u'税率', ondelete='restrict', index=True, track_visibility='onchange')
    archives_ids = fields.Many2many('partner.archives', string=u'客户', index=True)
    other_name_ids = fields.Many2many('partner.other_name', string=u'物料别名', readonly=True, states=READONLY, ondelete='restrict')
    first_letter = fields.Char(compute='_get_first_letter', store=True, string=u'名称首字母')

    @api.one
    @api.depends('name')
    def _get_first_letter(self):
        name = self.name
        if name:
            self.first_letter = git_first.get_first_letter(name)

    @api.one
    @api.depends('name')
    def _get_first_letter(self):
        name = self.name
        if name:
            self.first_letter = git_first.get_first_letter(name)

    @api.model
    def create(self, vals):
        """创建主要材料、能源、产成品、辅料材料时要创建默认的别名"""
        result = super(MaterialCodes, self).create(vals)
        material_ids = self.env['code.material'].search(['|', '|', '|', ['name', '=', '主要材料'],
                                                         ['name', '=', '能源'],
                                                         ['name', '=', '产成品'],
                                                         ['name', '=', '辅料材料']]).ids
        if result.material_id.id in material_ids:
            other_name_id = self.env['partner.other_name'].create({
                'name': result.name,
                'state': 'done',
            })
            result.other_name_ids = [(6, 0, [other_name_id.id])]
        return result

    def update_other_name(self):
        material_ids = self.env['code.material'].search(['|', '|', '|', ['name', '=', '主要材料'],
                                                         ['name', '=', '能源'],
                                                         ['name', '=', '产成品'],
                                                         ['name', '=', '辅料材料']]).ids
        material_codes_ids = self.env['code.material_codes'].search([['material_id', 'in', material_ids]])
        for material_codes_id in material_codes_ids:
            other_name_id = self.env['partner.other_name'].create({
                'name': material_codes_id.name,
                'state': 'done',
            })
            material_codes_id.other_name_ids = [(6, 0, [other_name_id.id])]

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

    @api.constrains('name','invcode')
    def _check_name(self):
        """限制银行名字不能重复出现"""
        names = self.search([('invcode', '=', self.invcode)])
        if len(names) > 1:
            raise ValidationError('该存货编码已经存在！')

    @api.one
    def unlink(self):
        """在state字段不为草稿时不允许删除，"""
        if self.state == 'done' or self.state == 'approval':
            raise UserError(u'该状态下的单据不可删除！')
        else:
            return super(MaterialCodes, self).unlink()


class OtherName(models.Model):
    """物料别名"""
    _name = 'partner.other_name'
    _description = u"物料别名"
    _inherit = ['mail.thread']
    READONLY = {'draft': [('readonly', False)]}

    name = fields.Char(string=u'名称', index=True, readonly=True, states=READONLY)
    material_codes_ids = fields.Many2many('code.material_codes', string=u'物料')
    state = fields.Selection([('draft', '草稿'),
                              ('confirm', '审批中'),
                              ('done', '完成')], string='状态', default='draft', track_visibility='onchange', index=True)


class Material(models.Model):
    """
    存货分类
    """
    _name = 'code.material'
    _description = u'存货分类'
    _inherit = ['mail.thread']
    READONLY = {'draft': [('readonly', False)]}

    name = fields.Char(string=u'名称', readonly=True, states=READONLY, track_visibility='onchange', index=True)
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


class Label(models.Model):
    _name = 'code.label'
    _description = u'标签'
    _inherit = ['mail.thread']
    READONLY = {'draft': [('readonly', False)]}

    name = fields.Char(string=u"标签名", readonly=True, states=READONLY, track_visibility='onchange', index=True)
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


class Metering(models.Model):
    """
    计量单位
    """
    _name = 'code.metering'
    _description = u'计量单位'
    _inherit = ['mail.thread']
    READONLY = {'draft': [('readonly', False)]}

    # 限制名称唯一性
    _sql_constraints = [('code_metering_name', 'unique(name)', u'需保证名称唯一性，请换一个名称输入')]

    name = fields.Char(string='主计量单位', readonly=True, states=READONLY, track_visibility='onchange', index=True)
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