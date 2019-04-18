# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta
import time
from odoo.exceptions import UserError, ValidationError
# 人员信息表
import datetime
import calendar
class PsnColl(models.Model):
    _name = 'ding.psn_coll'
    _inherit = ['mail.thread']


    name = fields.Char(string=u'姓名', required=True, index=True)
    mobile = fields.Char(string=u'手机号')
    department_id = fields.Many2one('ding.ding_department', string=u'部门')
    ding_userid = fields.Char(string=u"钉钉userid", index=True)
    avatar = fields.Char(string=u'钉钉头像链接')
    idcard_img = fields.Binary(string='身份证图片')
    birth_date = fields.Date(string=u'出生日期')
    age = fields.Integer(string=u'年龄', store=True, index=True)
