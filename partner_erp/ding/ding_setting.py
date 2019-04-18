# coding: utf-8
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

from .ding_api import Dingtalk
import base64, csv, os,datetime


# xlrd,
from datetime import timedelta
import time

class DingSetting(models.Model):
    _name = "ding.setting"
    _description = "钉钉账户信息配置"

    corpid = fields.Char(string=u"钉钉corpid", required=True, default='dingd951b7448023172c35c2f4657eb6378f')
    corpsecret = fields.Char(string=u"钉钉corpsecret", required=True, default='IX98WcG0nQ_Exf-nLZ8HuULau4z9WFgi37yNZuc_P-F-CxlIQA-XNGVgm0J6rOU2')

    bs_file = fields.Binary(string=u'上传文件')

    def update_partner_users(self):
        """根据钉钉人员更新partner人员"""
        for user in self.env['ding.psn_coll'].search([]):
            if not self.env['partner.archives'].search([['name', '=', user.name]]):
                self.env['partner.archives'].create({
                    "name" : user.name,
                    "business_licence": user.name,
                    "phone" : user.mobile,
                    "bill_type" : "users",
                    "user_char" : user.department_id.complete_name
                })
                self._cr.commit()

    # bs_file_name = fields.Char(string='工资考勤文件')

    # @api.model
    # def create(self, vals):
    #     for obj in self.search([]):
    #         obj.unlink()
    #     result = super(DingSetting, self).create(vals)
    #     return result
    def get_ding_common_message(self, agent_id=False):

        return ('dingd951b7448023172c35c2f4657eb6378f',
                'IX98WcG0nQ_Exf-nLZ8HuULau4z9WFgi37yNZuc_P-F-CxlIQA-XNGVgm0J6rOU2',
                '203970362',
                )


    # 部门
    def getDingDepartment(self):
        # 钉钉设置表对象
        # ding_obj = self.env["ding.setting"]
        ding_list = self.search_read()
        if not ding_list:
            raise UserError(u'corpid或corpsecret不能为空')
            return False
        ding_setting_obj = ding_list[-1]
        corpid = ding_setting_obj.get("corpid")
        corpsecret = ding_setting_obj.get("corpsecret")

        ding_talk_obj = Dingtalk(corpid, corpsecret)
        department_list = ding_talk_obj.get_dept_list()

        if not department_list:
            raise UserError(u'企业号中还没创建部门')

        department_obj = self.env["ding.ding_department"]


        for department in department_list:
            if department.get("id") and department.get("name"):
                is_have_record = department_obj.search([("dept_id", "=", department.get("id"))])
                tempDept = {"dept_id": department.get('id'),
                            "name": department.get('name'),
                            "dept_parent_id": department.get('parentid')}
                if not is_have_record:
                    department_obj.create(tempDept)
                else:
                    is_have_record.write(tempDept)
        for department in department_obj.search([]):
            records = department_obj.search([("dept_id", "=", department['dept_parent_id'])])
            if records:
                department.write({'parent_id': records[0]['id']})
            else:
                department.write({'parent_id': False})

        return True
    # 部门人员
    def getDingUser(self):

        ding_list = self.search_read()
        if not ding_list:
            raise UserError(u'corpid或corpsecret不能为空')
            return False

        ding_setting_obj = ding_list[-1]
        corpid = ding_setting_obj.get("corpid")
        corpsecret = ding_setting_obj.get("corpsecret")

        ding_talk_obj = Dingtalk(corpid, corpsecret)
        # 人员表对象
        person_obj = self.env["ding.psn_coll"]

        department_obj = self.env["ding.ding_department"]
        department_obj_list = department_obj.search_read([],['dept_id'])
        if not department_obj_list:
            raise UserError(u"还没有部门数据")
        flag_index = 0
        for dept_dic in department_obj_list:
            dept_id = dept_dic.get("dept_id")
            flag_index = flag_index + 1
            if flag_index > 100:
                time.sleep(2)
                flag_index = 0
            self.getDeptUser(ding_talk_obj, dept_id, person_obj, department_obj)

        return True
    # 创建部门人员
    @api.one
    def getDeptUser(self, ding_talk_obj, dept_id, person_obj, department_obj):
        department_user_list = ding_talk_obj.get_dept_user_list(dept_id)
        if department_user_list:
            for user in department_user_list:
                user_department_id = user.get('department')[-1]
                department_record = department_obj.search([('dept_id', '=', user_department_id)])
                # temp_dept_ids = []
                # for temp_dept_id in user.get('department'):
                #     temp_department_record = department_obj.search([('dept_id', '=', temp_dept_id)])
                #     temp_dept_ids.append(temp_department_record.id)
                mobile = user.get('mobile')
                if mobile is None:
                    mobile = ''
                user_obj = {"name": user.get("name"),
                            "mobile": user.get("mobile"),
                            # "psn_code": psn_code,
                            "ding_userid": user.get("userid"),
                            "department_id": department_record.id,
                            "avatar": user.get("avatar"),
                            }
                if len(mobile) == 0:
                    user_obj = {"name": user.get("name"),
                                "mobile": user.get("mobile"),
                                # "post": user.get("position"),
                                "ding_userid": user.get("userid"),
                                "department_id": department_record.id,
                                "avatar": user.get("avatar"),
                                }

                if len(mobile) > 2:
                    is_have_record = person_obj.search([("mobile", "=", mobile)])
                    if not is_have_record:
                        # pass
                        person_obj.create(user_obj)
                        self._cr.commit()
                    else:
                        for psn_obj in is_have_record:
                            psn_obj.write(user_obj)
                else:
                    pass
                    # is_have_record = person_obj.search([("ding_userid", "=", user.get("userid"))])
                    # if not is_have_record:
                    #     person_obj.create(user_obj)
                    # else:
                    #     is_have_record.write(user_obj)


                # is_have_record.department_ids = [6, 0, temp_dept_ids]



    # 班次
    def getDingAttendGroups(self):
        ding_list = self.search_read()
        if not ding_list:
            raise UserError(u'corpid或corpsecret不能为空')
            return False
        ding_setting_obj = ding_list[-1]
        corpid = ding_setting_obj.get("corpid")
        corpsecret = ding_setting_obj.get("corpsecret")

        class_obj = self.env['ding.class']

        ding_talk_obj = Dingtalk(corpid, corpsecret)

        self.getDingAttendGroupsMore(ding_talk_obj, class_obj, 0)

    # 创建班次
    def getDingAttendGroupsMore(self, ding_talk_obj, class_obj, offset):
        res = ding_talk_obj.getAttendGroups(offset)
        res = res['result']
        group_list = res['groups']
        is_have_more = res['has_more']
        if is_have_more:
            offset = offset + 10
            self.getDingAttendGroupsMore(ding_talk_obj, class_obj, offset)

        for group in group_list:
            # if group['type'] == 'FIXED':
            #     class_id = group['default_class_id']
            for selected_class in group['selected_class']:
                class_id = selected_class['class_id']

                class_name = selected_class['class_name']
                attend_time = ''
                for section in selected_class['sections']:

                    temp_time = ''
                    for s_time in section['times']:
                        across = s_time['across']
                        check_time = s_time['check_time']
                        check_time = check_time[-8:-3]
                        if across == 1:
                            check_time = ('次日%s' % (check_time))
                        temp_time = temp_time + '-' + check_time
                    temp_time = temp_time[1:]
                    attend_time = attend_time + ' ' + temp_time

                class_instance_obj = {
                    'class_id': class_id,
                    'name': class_name,
                    'attend_time': attend_time,
                }

                is_have_record = class_obj.search([('class_id', '=', class_id)])
                if not is_have_record:
                    class_obj.create(class_instance_obj)
                else:
                    is_have_record.write(class_instance_obj)
    # 注册通讯录回调
    @api.one
    def registerCallBack(self):

        ding_talk_obj = Dingtalk(self.corpid, self.corpsecret)
        token = '123456'
        callback_tag = ['user_add_org', 'user_modify_org', 'user_leave_org', 'org_dept_create', 'org_dept_modify',
                        'org_dept_remove']
        aes_key = '11111111lvdhntotr3x9qhlbytb18zyz5z111111111'
        callback_url = 'http://hr.baoshunkeji.com/callbackreceive'
        res = ding_talk_obj.registerCallBack(token, callback_tag, aes_key, callback_url)
        if res['errcode']:
            self.update_callback(token, callback_tag, aes_key, callback_url)
        print(res)
    # 更新通讯录回调
    def update_callback(self, token, callback_tag, aes_key, callback_url):
        """
        更新钉钉回调
        :param access_token:
        :param token:
        :param callback_tag:
        :param aes_key:
        :param callback_url:
        :return:
        """
        ding_talk_obj = Dingtalk(self.corpid, self.corpsecret)
        res = ding_talk_obj.updateCallBack(token, callback_tag, aes_key, callback_url)
        print('update = ', res)
        if res['errcode']:
            raise UserError('更新失败')

    # 获取回调失败的结果
    def getCallBackFailedResult(self):
        ding_talk_obj = Dingtalk(self.corpid, self.corpsecret)
        res = ding_talk_obj.getCallBackFailedResult()

        ding_setting_obj = self.env['ding.setting']
        ding_list = ding_setting_obj.sudo().search_read([], ['id'])
        ding_record_dic = ding_list[-1]
        ding_obj = ding_setting_obj.sudo().browse(ding_record_dic['id'])
        try:
            is_have_more = res['has_more']
        except:
            is_have_more = res['hasMore']

        if is_have_more:
            self.getCallBackFailedResult()

        failed_list = res['failed_list']
        print(failed_list)
        for event in failed_list:

            eventType = event['call_back_tag']
            if eventType == 'check_url':
                pass
            elif eventType == 'user_add_org':
                user_add_org = event['user_add_org']
                userids = user_add_org['userid']
                ding_obj.createUpdateLocalPerson(userids)
            elif eventType == 'user_modify_org':
                user_modify_org = event['user_modify_org']
                userids = user_modify_org['userid']
                ding_obj.createUpdateLocalPerson(userids)
            elif eventType == 'user_leave_org':
                user_leave_org = event['user_leave_org']
                userids = user_leave_org['userid']
                ding_obj.leaveLocalPerson(userids)
            elif eventType == 'org_dept_create':
                org_dept_create = event['org_dept_create']
                deptids = org_dept_create['deptid']
                ding_obj.createUpdateDept(deptids)
            elif eventType == 'org_dept_modify':
                org_dept_modify = event['org_dept_modify']
                deptids = org_dept_modify['deptid']
                ding_obj.createUpdateDept(deptids)
            elif eventType == 'org_dept_remove':
                org_dept_remove = event['org_dept_remove']
                deptids = org_dept_remove['deptid']
                ding_obj.deleteDept(deptids)

    # 创建更新钉钉人员
    def createUpdateLocalPerson(self, ding_userids):

        person_obj = self.env["ding.psn_coll"]
        ding_list = self.search_read()
        if not ding_list:
            raise UserError(u'corpid或corpsecret不能为空')
        ding_setting_obj = ding_list[-1]
        corpid = ding_setting_obj.get("corpid")
        corpsecret = ding_setting_obj.get("corpsecret")

        ding_talk_obj = Dingtalk(corpid, corpsecret)

        for userid in ding_userids:
            user = ding_talk_obj.get_user_detail(userid)
            user_department_id = user.get('department')[-1]
            department_obj = self.env["ding.ding_department"]
            department_record = department_obj.search([('dept_id', '=', user_department_id)])
            mobile = user.get('mobile')
            if mobile is None:
                mobile = ''
            user_obj = {"name": user.get("name"),
                        "mobile": user.get("mobile"),
                        # "post": user.get("position"),
                        # "psn_code": psn_code,
                        "ding_userid": user.get("userid"),
                        # "department_id": department_record.id,
                        "avatar": user.get("avatar"),
                        }
            if len(mobile) == 0:
                user_obj = {"name": user.get("name"),
                            "mobile": user.get("mobile"),
                            # "post": user.get("position"),
                            "ding_userid": user.get("userid"),
                            # "department_id": department_record.id,
                            "avatar": user.get("avatar"),
                            }
            if len(mobile) > 2:
                is_have_record = person_obj.search([("mobile", "=", mobile)])
                if not is_have_record:
                    # pass
                    person_obj.create(user_obj)
                    self._cr.commit()
                else:
                    for psn_obj in is_have_record:
                        psn_obj.write(user_obj)



    #钉钉离职，更新本地人员在职状态
    def leaveLocalPerson(self, ding_userids):
        person_obj = self.env["ding.psn_coll"]
        ding_list = self.search_read()
        if not ding_list:
            raise UserError(u'corpid或corpsecret不能为空')
        ding_setting_obj = ding_list[-1]
        corpid = ding_setting_obj.get("corpid")
        corpsecret = ding_setting_obj.get("corpsecret")

        ding_talk_obj = Dingtalk(corpid, corpsecret)
        for userid in ding_userids:
            # user = ding_talk_obj.get_user_detail(userid)
            is_have_record = person_obj.search([("ding_userid", "=", userid)])
            if is_have_record:
                pass
                # is_have_record.write({"psn_type": 'step_back'})

    #创建/更新部门
    def createUpdateDept(self, ding_deptids):

        ding_list = self.search_read()
        if not ding_list:
            raise UserError(u'corpid或corpsecret不能为空')
        ding_setting_obj = ding_list[-1]
        corpid = ding_setting_obj.get("corpid")
        corpsecret = ding_setting_obj.get("corpsecret")

        ding_talk_obj = Dingtalk(corpid, corpsecret)
        for deptid in ding_deptids:
            dept = ding_talk_obj.get_dept_detail(deptid)

            department_obj = self.env["ding.ding_department"]

            department_record = department_obj.search([('dept_id', '=', deptid)])
            if not department_record:
                department_obj.create({
                    'name': dept["name"],
                    'dept_id': dept['id'],
                    'dept_parent_id': dept['parentid'],
                })
            else:
                department_record.write({
                    'name': dept["name"],
                    'dept_id': dept['id'],
                    'dept_parent_id': dept['parentid'],
                })

        # 更新上级部门id
        for department in department_obj.search([]):
            records = department_obj.search([("dept_id", "=", department['dept_parent_id'])])
            if records:
                department.write({'parent_id': records[0]['id']})
            else:
                department.write({'parent_id': False})

    # 钉钉删除部门
    @api.one
    def deleteDept(self, ding_deptids):
        department_obj = self.env["ding.ding_department"]

        for deptid in ding_deptids:
            record_list = department_obj.search([('dept_id', '=', deptid)])
            for record in record_list:
                record.unlink()

            record_sub_list = department_obj.search([('dept_parent_id', '=', deptid)])
            for sub in record_sub_list:
                sub.unlink()


    def sendMessage(self):
        corpid, corpsecret, agent_id = self.env['ding.setting'].sudo().get_ding_common_message()
        ding_obj = Dingtalk(corpid=corpid, corpsecret=corpsecret)
        msg_obj_list = self.env['ding.ding_message'].search([('is_send', '=', False)])
        for msg_obj in msg_obj_list:
            result = ding_obj.send_message(msg_obj)
            if result and result['errcode'] == 0:
                msg_obj.is_send = True
                # msg_obj.project_id.task_id = result['task_id']
            elif result['errcode'] == 201:
                msg_obj.unlink()

    # def sendMessage_new(self):
    #     corpid, corpsecret, agent_id = self.env['ding.setting'].sudo().get_ding_common_message()
    #     ding_obj = Dingtalk(corpid=corpid, corpsecret=corpsecret)
    #     msg_obj_list = self.env['ding.ding_message'].search([('is_send', '=', False)])
    #     for msg_obj in msg_obj_list:
    #         result = ding_obj.send_message_new(msg_obj)
    #         if result and result['errcode'] == 0:
    #             msg_obj.is_send = True
    #             # msg_obj.project_id.task_id = result['task_id']
    #         elif result['errcode'] == 201:
    #             msg_obj.unlink()

    def delete_message(self):
        AdjustementLines = self.env['ding.ding_message']
        AdjustementLines.search([('is_send', '=', True)]).unlink()



