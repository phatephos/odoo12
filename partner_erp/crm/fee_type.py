# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, AccessError


class TransportType(models.Model):
    """ 火车、海上运输费用类型"""
    _name = 'crm_c.fee_type'
    _description = u"运输类型"
    _inherit = ['mail.thread']

    name = fields.Char(string='类型名称', required=True, track_visibility='onchange', index=True)
    user_id = fields.Many2one('partner.archives', string=u'创建人', track_visibility='onchange',
                                  default=lambda self: self.env['partner.archives'].
                                  search([('user_id', '=', self.env.user.id)], limit=1).id,
                                  ondelete='restrict', readonly=True, index=True, store=True)

    @api.constrains('name')
    def _check_name(self):
        """限制类型名字不能重复出现"""
        names = self.search([('name', '=', self.name)])
        if len(names) > 1:
            raise ValidationError('名字已经存在')
