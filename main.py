from src.wx import wx, start_listen, send_message_to_file_helper
from src.ai import ai_response
from src.config import AUTO_REPLY_DELAY, REPLAY_LIST, SUGGEST_LIST
from src.log import init_log
import time
import pandas as pd

message_manager = {}

def onMessage(chat, message):
    type = message.type
    content = message.content
    current_time = time.time()
    chat_id = chat.who

    if type == 'friend':  # 对方发送的消息
        if chat_id not in message_manager:
            message_manager[chat_id] = pd.DataFrame({
                'who': [],
                'content': [],
                'timestamp': [],
                'replied': []
            }, dtype={'who': 'object', 'content': 'object', 'timestamp': 'float64', 'replied': 'bool'})

        # 添加新消息到DataFrame
        new_message = pd.DataFrame({
            'who': ['对方'],
            'content': [content],
            'timestamp': [current_time],
            'replied': [False],
        })
        if not new_message.empty:
            message_manager[chat_id] = pd.concat([message_manager[chat_id], new_message], ignore_index=True)

    if type == 'self':  # 自己发送的消息
        if chat_id not in message_manager:
            message_manager[chat_id] = pd.DataFrame({
                'who': [],
                'content': [],
                'timestamp': [],
                'replied': []
            }, dtype={'who': 'object', 'content': 'object', 'timestamp': 'float64', 'replied': 'bool'})

        # 添加新消息到DataFrame
        new_message = pd.DataFrame({
            'who': ['我'],
            'content': [content],
            'timestamp': [current_time],
            'replied': [True],
        })
        if not new_message.empty:
            message_manager[chat_id] = pd.concat([message_manager[chat_id], new_message], ignore_index=True)

def onOneSecond():
    current_time = time.time()
    for chat_id, df in message_manager.items():
        # 检查是否有未回复的对方消息
        un_replied = df[(df['who'] == '对方') & (df['replied'] == False)]
        
        if len(un_replied) > 0 and all(un_replied['content'].isin(['[图片]', '[语音]'])):
            # 忽略图片和语音消息
            df.loc[(df['who'] == '对方') & (df['replied'] == False), 'replied'] = True
            continue
            
        if len(un_replied) > 0:
            last_message_time = df['timestamp'].iloc[-1]
            
            if current_time - last_message_time > AUTO_REPLY_DELAY:
                # 聚合所有消息内容
                all_messages = '\n'.join([f"{row['who']}: {row['content']}" for _, row in df.iterrows()])
                
                # 获取AI回复
                response = ai_response(
                    chat_id,
                    all_messages
                )
                
                # 把所有未回复的消息标记为已回复
                df.loc[(df['who'] == '对方') & (df['replied'] == False), 'replied'] = True

                # 创建临时DataFrame列表
                dfs_to_concat = []
                
                # 保留5分钟内的消息
                recent_msgs = df[df['timestamp'] > current_time - 300]
                if not recent_msgs.empty:
                    dfs_to_concat.append(recent_msgs)
                
                # 保留对方最近的3条消息
                recent_other = df[df['who'] == '对方'].sort_values('timestamp', ascending=False).head(3)
                if not recent_other.empty:
                    dfs_to_concat.append(recent_other)
                
                # 保留自己最近的3条消息
                recent_self = df[df['who'] == '我'].sort_values('timestamp', ascending=False).head(3)
                if not recent_self.empty:
                    dfs_to_concat.append(recent_self)
                # 合并
                if dfs_to_concat:
                    df = pd.concat(dfs_to_concat).drop_duplicates().sort_values('timestamp')
                    message_manager[chat_id] = df
                
                # 发送回复
                if chat_id in SUGGEST_LIST:
                    send_message_to_file_helper(response, chat_id)
                if chat_id in REPLAY_LIST:
                    wx.SendMsg(response, chat_id)
                
def main():
    init_log()
    start_listen(onOneSecond, onMessage)


if __name__ == "__main__":
    main()
