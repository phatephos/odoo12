# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Department(models.Model):
    _name = "ding.ding_department"
    _description = "钉钉部门"
    _rec_name = 'complete_name'

    name = fields.Char(string=u"部门名称")
    complete_name = fields.Char('Complete Name', compute='_compute_complete_name', store=True)
    dept_id = fields.Char(string="钉钉部门ID")
    dept_parent_id = fields.Char(string="钉钉上级部门ID")
    parent_id = fields.Many2one('ding.ding_department', string=u'上级部门')
    child_ids = fields.One2many('ding.ding_department', 'parent_id', string='下级部门')
    # 有上下级的部门名称
    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for department in self:
            if department.parent_id:
                department.complete_name = '%s / %s' % (department.parent_id.complete_name, department.name)
            else:
                department.complete_name = department.name