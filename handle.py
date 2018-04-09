# filename: handle.py
# -*- coding: utf-8 -*-

import hashlib
import web
import receive
import reply
import requests
import json


class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr             
            token = "hellobqlq" #Please specify this value in accordance with the information given in the public platform official site / basic configuration             list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument
        
    def POST(self):
        try:
            webData = web.data()
            print "Handle Post webdata is ", webData
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if recMsg.MsgType == 'text' and recMsg.Content == 'bitcoin':
                    requestText =  "https://api.coinmarketcap.com/v1/ticker/" + recMsg.Content + "/?convert=CNY"
                    response = requests.get("https://api.coinmarketcap.com/v1/ticker/bitcoin/?convert=CNY")
                    jsonResponse = json.loads(response.content)
                    content = '加密货币名称：比特币 交易代码：BTC 交易排名：'  + str(jsonResponse[0]['rank']) \
                    + ' 美元价格：' + str(jsonResponse[0]['price_usd'])  + '美元' + ' 人民币价格：' \
                    + str(jsonResponse[0]['price_cny'])  + '人民币' + ' 比特币价格：' \
                    + str(jsonResponse[0]['price_btc']) + '比特币\n' + ' 全部市值:' + str(jsonResponse[0]['market_cap_usd']) \
                    + '美元' + ' 24小时交易量：' + str(jsonResponse[0]['24h_volume_usd']) + '美元' + ' 市场流通量：' \
                    + str(jsonResponse[0]['available_supply']) + ' 全部流通量：' + str(jsonResponse[0]['total_supply']) \
                    + '\n' + ' 1小时价格变动：' + str(jsonResponse[0]['percent_change_1h']) + '%' + ' 24小时价格变动：' \
                    + str(jsonResponse[0]['percent_change_24h']) + '%' + ' 7天价格变动：' + str(jsonResponse[0]['percent_change_7d']) + '%'
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()
                if recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    return replyMsg.send()
                else:
                    return 'Please type in the correct code'
            else:
                print "Processing Temporarily Suspended"
                return "Please type in the correct code"
        except Exception, Argment:
            return Argment