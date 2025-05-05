from src.wx import wx, start_listen, send_message_to_file_helper
from src.ai import ai_response
from src.config import AUTO_REPLY_DELAY, REPLAY_LIST, SUGGEST_LIST
from src.log import init_log
import time

message_manager = {}
def onMessage(chat, message):
    type = message.type
    content = message.content
    current_time = time.time()
    chat_id = chat.who

    if type == 'friend':  # 对方发送的消息
        if chat_id not in message_manager:
            message_manager[chat_id] = []

        message_manager[chat_id].append({
            'who': '对方',
            'content': content,
            'timestamp': current_time,
            'replied': False,
        })

    if type == 'self':  # 自己发送的消息
        if chat_id not in message_manager:
            message_manager[chat_id] = []

        message_manager[chat_id].append({
            'who': '自己',
            'content': content,
            'timestamp': current_time,
        })

def onOneSecond():
    current_time = time.time()
    for chat_id, messages in message_manager.items():
        # 检查是否有未回复的对方消息
        unreplied_messages = [message for message in messages if message['who'] == '对方' and message.get('replied', False) == False]
        
        if unreplied_messages:
            last_message_time = messages[-1]['timestamp']
            
            if current_time - last_message_time > AUTO_REPLY_DELAY:
                # 聚合所有消息内容
                all_messages = '\n'.join([f"{message['who']}: {message['content']}" for message in messages])
                
                # 获取AI回复
                response1 = ai_response(
                    chat_id,
                    all_messages
                )
                if chat_id in SUGGEST_LIST:
                    response2 = ai_response(
                        chat_id,
                        all_messages
                    )
                
                # 把所有未回复的消息标记为已回复
                for message in unreplied_messages:
                    message['replied'] = True
                    
                # 发送回复
                if chat_id in SUGGEST_LIST:
                    send_message_to_file_helper([response1, response2], chat_id)
                if chat_id in REPLAY_LIST:
                    wx.SendMsg(response1, chat_id)
                
def main():
    init_log()
    start_listen(onOneSecond, onMessage)


if __name__ == "__main__":
    main()
