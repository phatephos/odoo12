# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResUsers(models.Model):
    """继承官方uses"""
    _inherit = 'res.users'

    partner_company_ids = fields.Many2many('partner.archives', domain="[('bill_type', '=', 'company')]", string=u'相关公司', index=True)