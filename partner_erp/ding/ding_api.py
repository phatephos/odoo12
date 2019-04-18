# -*- coding:utf-8 -*-

import requests
import time
import json
import datetime
from odoo.exceptions import UserError
import hashlib
import urllib
import urllib.parse

requests.packages.urllib3.disable_warnings()
DEFAULT_SERVER_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_SERVER_TIME_FORMAT = "%H:%M:%S"
DEFAULT_SERVER_DATETIME_FORMAT = "%s %s" % (
    DEFAULT_SERVER_DATE_FORMAT,
    DEFAULT_SERVER_TIME_FORMAT)


class Dingtalk(object):
    __instance = None
    __init_flag = False

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = object.__new__(cls)
            return cls.__instance
        else:
            return cls.__instance
    def __init__(self, corpid, corpsecret):
        self.__params = {
            "corpid": corpid,
            "corpsecret": corpsecret
        }
        if not self.__init_flag:
            self.token = {}
            self.token_dict = {
                "access_token": self.token.get("access_token")
            }
            # 请求头
            self.__header = {"content-type": "application/json"}
            # token url
            self.url_get_token = 'https://oapi.dingtalk.com/gettoken'
            # 部门列表
            self.url_get_dept_list = 'https://oapi.dingtalk.com/department/list'
            # 部门详情
            self.url_get_dept_detail = 'https://oapi.dingtalk.com/department/get'
            # 创建部门
            # self.url_create_dept = 'https://oapi.dingtalk.com/department/create'
            # 删除部门
            # self.url_delete_dept = 'https://oapi.dingtalk.com/department/delete'
            # 更新部门
            # self.url_update_dept = 'https://oapi.dingtalk.com/department/update'
            # 根据unionid获取成员的userid
            # self.url_get_user_id_by_unionid = 'https://oapi.dingtalk.com/user/getUseridByUnionid'
            # 成员详情
            self.url_get_user_detail = 'https://oapi.dingtalk.com/user/get'
            # 获取部门成员（详情）
            self.url_user_list = 'https://oapi.dingtalk.com/user/list'
            # 创建成员
            # self.url_create_user = 'https://oapi.dingtalk.com/user/create'
            # 更新成员
            # self.url_update_user = 'https://oapi.dingtalk.com/user/update'
            # 删除成员
            # self.url_delete_user = 'https://oapi.dingtalk.com/user/delete'
            # 获取企业员工人数
            self.url_get_user_count = 'https://oapi.dingtalk.com/user/get_org_user_count'
            # 考勤记录
            self.url_get_users_attendance = 'https://oapi.dingtalk.com/attendance/list'
            # 考勤组列表详情
            self.url_get_attend_groups = 'https://eco.taobao.com/router/rest'
            # 获取用户userid
            self.url_get_userid = 'https://oapi.dingtalk.com/user/getuserinfo'
            self._url_jsapi_ticket = 'https://oapi.dingtalk.com/get_jsapi_ticket'
            # 发送工作通知消息
            self.url_message = 'https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2'
            # 查询工作通知消息的发送结果
            self.url_meesage_result = 'https://oapi.dingtalk.com/topapi/message/corpconversation/getsendresult'

            self.__init_flag = True
    # 错误
    def __raise_error(self, res):
        raise UserError(u'错误代码: %s,详细错误信息: %s' % (res.json()['errcode'], res.json()['errmsg']))
        global senderr
        sendstatus = False
        senderr = 'error code: %s,error message: %s' % (res.json()['errcode'], res.json()['errmsg'])
    # 获取token
    def get_token(self):
        res = requests.get(self.url_get_token, headers=self.__header, params=self.__params)
        try:
            self.token = res.json()
            self.token['expires_in'] = time.time()+7200
            self.token_dict = {
                "access_token": self.token.get("access_token")
            }
            return None
        except:
            self.__raise_error(res)
    # 检查是否过期
    def token_is_expired(self):
        if not any(self.token):
            self.get_token()
        elif float(self.token["expires_in"]) <= time.time():
            self.get_token()
        else:
            self.token_dict = {
                "access_token": self.token.get("access_token")
            }

    # 部门列表
    def get_dept_list(self):
        self.token_is_expired()

        params = self.token_dict
        params["fetch_child"] = True
        params["id"] = 1
        res = requests.get(self.url_get_dept_list, headers=self.__header, params=params)
        try:
            return res.json()["department"]
        except:
            self.__raise_error(res)
    # 部门详情
    def get_dept_detail(self, dept_id):
        self.token_is_expired()

        params = self.token_dict
        params.update({"id" : dept_id})
        res = requests.get(self.url_get_dept_detail, headers=self.__header, params=params)
        try:
            return res.json()
        except:
            self.__raise_error(res)
    # 人员详情
    def get_user_detail(self, userid):
        self.token_is_expired()

        params = self.token_dict
        params.update({"userid" : userid})
        res = requests.get(self.url_get_user_detail, headers=self.__header, params=params)
        try:
            return res.json()
        except:
            self.__raise_error(res)
    # 部门人员详情
    def get_dept_user_list(self, department_id, offset=None, size=None, order=None):
        self.token_is_expired()

        params = self.token_dict
        params["department_id"] = department_id
        # params["offset"] = offset
        # params["size"] = size
        # params["order"] = order
        res = requests.get(self.url_user_list, headers=self.__header, params=params)
        try:
            return res.json()["userlist"]
        except:
            self.__raise_error(res)
    # 激活人数
    def get_user_count(self, only_active=0):
        self.token_is_expired()

        params = self.token_dict
        params.update({"onlyActive" : only_active})
        res = requests.get(self.url_get_user_count, headers=self.__header, params=params)
        try:
            return res.json()["count"]
        except:
            self.__raise_error(res)


    # 考勤
    def get_users_attendance(self, workDateFrom, workDateTo, offset, limit, userIdList=[]):
        self.token_is_expired()

        params = self.token_dict

        postData = {
            'workDateFrom': workDateFrom,
            'workDateTo': workDateTo,
            'userIdList': userIdList,
            'offset': offset,
            'limit': limit,
        }
        res = requests.post(self.url_get_users_attendance, data=json.dumps(postData), params=params)
        try:
            return res.json()
        except:
            self.__raise_error(res)

    # 注册回调
    def registerCallBack(self, token, callback_tag, aes_key, callback_url):
        self.token_is_expired()
        params = self.token_dict

        postData = {
            'token': token,
            'call_back_tag': callback_tag,
            'aes_key': aes_key,
            'url': callback_url,
        }
        url = 'https://oapi.dingtalk.com/call_back/register_call_back'
        res = requests.post(url, json=postData, params=params)
        try:
            return res.json()
        except:
            self.__raise_error(res)
    # 更新回调
    def updateCallBack(self, token, callback_tag, aes_key, callback_url):
        self.token_is_expired()
        params = self.token_dict

        postData = {
            'token': token,
            'call_back_tag': callback_tag,
            'aes_key': aes_key,
            'url': callback_url,
        }
        url = 'https://oapi.dingtalk.com/call_back/update_call_back'
        res = requests.post(url, json=postData, params=params)
        try:
            return res.json()
        except:
            self.__raise_error(res)
    # 失败回调
    def getCallBackFailedResult(self):
        self.token_is_expired()
        params = self.token_dict
        url = 'https://oapi.dingtalk.com/call_back/get_call_back_failed_result'
        res = requests.get(url, params=params)
        try:
            return res.json()
        except:
            raise UserError(u'错误代码: %s,详细错误信息: %s' % (res))
    # 考勤组
    def getAttendGroups(self, offset):
        self.token_is_expired()
        now_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        postData = {
            'method': 'dingtalk.smartwork.attends.getsimplegroups',
            'session': self.token.get("access_token"),
            'format': 'json',
            'timestamp': now_time_str,
            'v': 2.0,
            'simplify': True,
            'offset': offset,
            'size': 10
        }
        res = requests.post(self.url_get_attend_groups, data=postData, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        result = json.loads(res.content.decode(encoding='utf-8'))
        try:
            return result['result']
        except:
            raise UserError(u'错误代码: %s,详细错误信息: %s' % (res))

    # 免登录获取access_token
    def get_access_token(self):
        params = {}
        params["appkey"] = 'ding3qtrpmfokdoutfob'
        params["appsecret"] = 'UG4F2BsVNVE6_vjXmxbnFGgcLu8Q6ZmmWAxAX59L6hvy7vPZ8DlMssW6AxrqUN4I'
        res = requests.get(self.url_get_token, headers=self.__header, params=params)
        try:
            return res.json()
        except:
            self.__raise_error(res)

    # 通过authCode和access_token获取免登用户的userid
    def get_userinfo(self, access_token, code):
        params = {}
        params["access_token"] = access_token
        params["code"] = code
        res = requests.get(self.url_get_userid, headers=self.__header, params=params)
        try:
            return res.json()
        except:
            self.__raise_error(res)

    def get_js_api_ticket(self):
        """
        获取 jsapi 的访问 票据
        :return:
        """
        self.token_is_expired()

        res = requests.get(self._url_jsapi_ticket, params=self.token_dict)
        try:
            return res.json()['ticket']
        except:
            self.__raise_error(res)

    def cmp(self, val_one, val_two):
        return_val = 0
        if val_one > val_two:
            return_val = 1
        elif val_one < val_two:
            return_val = -1
        return return_val

    def get_signature(self, vals={}):
        """
        对jsapi 参数进行处理获取 对应参数的 signature
        :param vals:
        :return:
        """
        keys = sorted(vals)
        plain = ''
        for key in keys:
            plain += '{0}={1}&'.format(key, vals.get(key))
        plain = plain.strip('&')
        plain_bytes = plain.encode('utf-8')
        signature = hashlib.sha1(plain_bytes).hexdigest()
        # sorted_vals = sorted(vals.items())
        # url_vals = urllib.parse.urlencode(sorted_vals)
        # signature = hashlib.sha1(url_vals).hexdigest()  # sha 加密
        return signature

    def get_js_api_params(self, url, nonceStr):
        """
        处理 数据 去的 jsapi 需要的 各种参数
        :param url:
        :param nonceStr:
        :return: 返回各种需要的参数 在 jsapi 中
        """
        jsapi_ticket = self.get_js_api_ticket()
        timestamp = int(time.time())
        signature_vals = {
            'noncestr': nonceStr,
            'jsapi_ticket': jsapi_ticket,
            'url': url,
            'timestamp': timestamp,
        }
        signature = self.get_signature(signature_vals)
        try:
            return signature, timestamp, nonceStr
        except:
            self.__raise_error({"error": u'错误！'})

    def send_message(self, msg_obj):


        title = "ERP待审批通知"
        text = str(msg_obj.creator) + "提交的" + str(msg_obj.pending_approval_modelname) + "审批请点击查看（" + str(
            msg_obj.pending_approval_active_id) + "）"        # title = "你好!1@"
        # text = "这是一个小测试1334"
        #text = "这是一个小测试1"
        self.token_is_expired()
        # messageUrl = "http://meeting.baoshunkeji.com/#/mobile/mobile-project-detail?project_id=%s" % project_id
        # messageUrl = "http://erp.baoshunkeji.com:8069/web#view_type=list&model=crm_c.contract&menu_id=224&action=268"
        #messageUrl = "http://erp.baoshunkeji.com:8069"
        messageUrl = "http://erp.baoshunkeji.com:8069/web#id="+str(msg_obj.pending_approval_id)+"&view_type=form&model="+str(msg_obj.pending_approval_model)+"&active_id="+str(msg_obj.pending_approval_active_id)

        messageUrl = urllib.parse.quote_plus(messageUrl)
        msgDic = {
            "msgtype": "link",
            "link": {
                "messageUrl": ("dingtalk://dingtalkclient/page/link?url={0}&pc_slide=true").format(messageUrl),
                "picUrl": "@lALPBY0V5NSKr7Nubg",
                "title": title,
                "text": text
            }
        }

        postData = {
            'agent_id': '215844301',
            # 'userid_list':str(msg_obj.approver_name_id),
            'userid_list': ','.join(eval(msg_obj.approver_name_id)),
            'msg': json.dumps(msgDic),

        }
        res = requests.post(self.url_message, data=postData, params=self.token_dict)
        try:
            return res.json()
        except:
            raise UserError(u'错误代码: %s,详细错误信息: %s' % (res))

    # def send_message_new(self, msg_obj):
    #
    #
    #     title = "ERP消息通知"
    #     text = str(msg_obj.message).strip('<p></p>') + "           新的消息请点击查看（" + str(
    #         msg_obj.pending_approval_id) + "）"
    #     self.token_is_expired()
    #     messageUrl = "http://fm.baoshunkeji.com:8069/mail/view?message_id="+str(msg_obj.creator_description)
    #     messageUrl = urllib.parse.quote_plus(messageUrl)
    #     msgDic = {
    #         "msgtype": "link",
    #         "link": {
    #             "messageUrl": ("dingtalk://dingtalkclient/page/link?url={0}&pc_slide=true").format(messageUrl),
    #             "picUrl": "@lALPBY0V5NSKr7Nubg",
    #             "title": title,
    #             "text": text
    #         }
    #     }
    #
    #     postData = {
    #         'agent_id': '215844301',
    #         'userid_list': ','.join(eval(msg_obj.approver_name_id)),
    #         'msg': json.dumps(msgDic),
    #
    #     }
    #     res = requests.post(self.url_message, data=postData, params=self.token_dict)
    #     try:
    #         return res.json()
    #     except:
    #         raise UserError(u'错误代码: %s,详细错误信息: %s' % (res))

    def get_message_result(self, task_id):

        self.token_is_expired()
        postData = {
            'agent_id': '215844301',
            'task_id': task_id,
        }
        res = requests.post(self.url_meesage_result, data=postData, params=self.token_dict)
        try:
            return res.json()
        except:
            raise UserError(u'错误代码: %s,详细错误信息: %s' % (res))

