# -*- coding: utf-8 -*-
# filename: handle.py
import hashlib
import reply
import receive
import web

class Handle(object):
    def POST(self):
        try:
            webData = web.data()
            print ("Handle Post webdata is ", webData)   #后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = "test"
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            else:
                print ("Processing Temporarily Suspended")
                return "success"
        except Exception:
            return "Exception occurred"