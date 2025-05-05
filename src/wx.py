import time
from wxauto import WeChat
from src.config import REPLAY_LIST, SUGGEST_LIST
from src.log import log

wx = WeChat()

for i in REPLAY_LIST:
    wx.AddListenChat(who=i, savepic=False)
for i in SUGGEST_LIST:
    wx.AddListenChat(who=i, savepic=False)

def send_message_to_file_helper(message, chat_id):
    who = '文件传输助手'
    wx.SendMsg(f'AI建议回复{chat_id}', who)
    wx.SendMsg(message, who)

def start_listen(emitOneSecond, emitMessage):
    while True:
        allChats = wx.GetListenMessage()
        for chat in allChats: # 对于每个人
            who = chat.who
            messages = allChats.get(chat)

            for message in messages: # 对于每条消息
                logJson = {
                    'type': message.type,
                    'content': message.content,
                }
                log(who, logJson)
                emitMessage(chat, message)
        emitOneSecond()
        time.sleep(1)
