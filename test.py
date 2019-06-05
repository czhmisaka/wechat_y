#!/usr/bin/env python
# coding: utf-8
#
import time

from wxbot import *
import bot
Bot = bot.TulingWXBot()

class MyWXBot(WXBot):
    def __init__(self):
        #super(MyWXBot,self).__init__()
        WXBot.__init__(self)
        self.is_lock = False
        self.user_dict = {}
        self.gl_key = False
        print self.group_list
    def auto_reply_first(self,msg):
        local_time = time.localtime(time.time())
        time_hour = int(local_time.tm_hour)
        if  time_hour >=7 and time_hour<=8:
            self.send_msg_by_uid(u'----来自一个听话的小机器人:----\n你要找的那个人现在背单词ing！我会把消息转达给她的！\n tips:你可以发送「sys0」来关闭小机器人哦！有效时间为1h', msg['user']['id'])
        elif time_hour >8 and time_hour<11:
            self.send_msg_by_uid(u'----来自一个听话的小机器人:----\n你要找的那个人现在上课哦！我会把消息转达给她的！\n tips:你可以发送「sys0」来关闭小机器人哦！有效时间为1h', msg['user']['id'])
        elif time_hour>=11 and time_hour<13:
            self.send_msg_by_uid(u'----来自一个听话的小机器人:----\n你要找的那个人现在午休哦！我会把消息转达给她的！\n tips:你可以发送「sys0」来关闭小机器人哦！有效时间为1h', msg['user']['id'])
        elif time_hour>=13 and time_hour<18:
            self.send_msg_by_uid(u'----来自一个听话的小机器人:-----\n你要找的那个人现在学习哦！我会把消息转达给她的！\n tips:你可以发送「sys0」来关闭小机器人哦！有效时间为1h', msg['user']['id'])
        elif time_hour>=18 and time_hour<23:
            self.send_msg_by_uid(u'----来自一个听话的小机器人:-----\n你要找的那个人现在还在学习哦！我会把消息转达给她的！\n tips:你可以发送「sys0」来关闭小机器人哦！有效时间为1h', msg['user']['id'])
        elif time_hour>=23 or time_hour<=6:
            self.send_msg_by_uid(u'----来自一个听话的小机器人:----\n你要找的那个人现在睡觉哦！我会把消息转达给她的！\n tips:你可以发送「sys0」来关闭小机器人哦！有效时间为1h', msg['user']['id'])
    def auto_reply(self,msg):
        if msg['content']['type']==0:
            u_dict = self.user_dict[msg['user']['id']]
            if(u_dict['count']==0):
                self.auto_reply_first(msg)
            elif u_dict['count']==1:
                self.send_msg_by_uid(u'----来自一个听话的小机器人:----\n你要找的那个人真的不在啦，再发的话那小机器人我陪你聊天啦', msg['user']['id'])
            elif u_dict['count']>=2:
                data = Bot.tuling_auto_reply(msg['user']['id'],msg['content']['data'])
                self.send_msg_by_uid(u'[小机器人]: '+data, msg['user']['id'])
                #self.send_msg_by_uid(u'----来自一个听话的小机器人:----\n你已经发了%d条咯QVQ！\n第一次发送时间:%d\n最后一次发送时间%d' %(u_dict['count']+1,u_dict['first_time'],u_dict['last_time']), msg['user']['id'])
        else:
            self.send_msg_by_uid(u'[小机器人]: 很遗憾我现在只能看的懂中文来着【哭】', msg['user']['id'])

    def handle_msg_all(self, msg):
        if msg['msg_type_id'] == 1:
            if msg['content']['data'].strip()=="sys0":
                self.gl_key = True
                #self.send_msg_by_uid(u'----来自一个听话的小机器人:----\n 最高权限小机器人已经关闭了哦', msg['user']['id'])
            elif msg['content']['data'].strip()=="sys1":

                self.gl_key = False
                #self.send_msg_by_uid(u'----来自一个听话的小机器人:----\n 最高权限小机器人已经开启了哦', msg['user']['id'])
            return
        if msg['content']['data'].strip()=="sys0":
            self.user_dict[msg['user']['id']]['is_lock']=True
            self.send_msg_by_uid(u'----来自一个听话的小机器人:----\n 我自闭啦~', msg['user']['id'])
            return
        elif msg['content']['data'].strip()=="sys1":
            self.user_dict[msg['user']['id']]['is_lock']=False
            self.send_msg_by_uid(u'----来自一个听话的小机器人:----\n 我想开啦', msg['user']['id'])
            return
        if msg['msg_type_id'] == 4:
            cur_time = time.time()
            is_key = False
            if not self.gl_key:
                for userid in self.user_dict:
                    if userid == msg['user']['id']:
                        is_key = True
                        self.user_dict[userid]['last_time']=cur_time
                        self.user_dict[userid]['count']+=1
                if not is_key:
                        self.user_dict[msg['user']['id']]={"user_id":msg['user']['id'],"username":msg['user']['name'],"first_time":cur_time,"last_time":cur_time,"count":0,"is_lock":False}
                if(not self.user_dict[msg['user']['id']]['is_lock']):
                    self.auto_reply(msg)


            #self.send_img_msg_by_uid("img/1.png", msg['user']['id'])
            #self.send_file_msg_by_uid("img/1.png", msg['user']['id'])

    def schedule(self):
         cur_time = time.time()
         for userid in self.user_dict:
             deltaTime = int(cur_time) - int(self.user_dict[userid]['last_time'])
             name = self.user_dict[userid]['username']
             if deltaTime >180:
                self.user_dict.pop(userid)
                print u'已经清除%s的信息' %(name)
         time.sleep(3)




def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'tty'
    bot.run()


if __name__ == '__main__':
    main()
