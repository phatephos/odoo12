# -*- coding: utf-8 -*-
from odoo import models, fields, api


class NcType(models.Model):
    _name = 'fm.nc_type'
    _description = u"业务流程"
    _inherit = ['mail.thread']

    code = fields.Char(string=u'业务代码', index=True, required=True,)
    name = fields.Char(string=u'业务名称', index=True, required=True,)
    material_ids = fields.Many2many('code.material', string=u'存货分类')
    in_out = fields.Selection([('in','采购'), ('out', '销售')], string=u'业务类型')
    archives_id = fields.Many2one('partner.archives', string=u'业务公司', index=True, required=True)

    _sql_constraints = [('name_UNIQUE', 'unique (name)', "业务名称已存在!"), ('code_UNIQUE', 'unique (code)', "业务代码已存在!")]
