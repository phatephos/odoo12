# -*- coding:utf-8 -*-

from odoo import models, fields, api, _, SUPERUSER_ID, tools


class DingMessage(models.Model):
    _name = 'ding.ding_message'
    _description = '钉钉消息'

    is_send = fields.Boolean(string='是否发送', default=False)
    message = fields.Char(string='发送消息内容')
    pending_approval_id = fields.Char(string='待审批单据id')
    pending_approval_model = fields.Char(string='待审批单据model')
    pending_approval_active_id = fields.Char(string='待审批单据active_id')
    pending_approval_modelname = fields.Char(string='待审批单据model名称')
    creator = fields.Char(string='创建人')
    approver_name = fields.Char(string='审批人')
    approver_name_id = fields.Char(string='审批人id')
    creator_description = fields.Char(string='描述')







