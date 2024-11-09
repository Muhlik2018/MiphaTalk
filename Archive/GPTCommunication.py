#import SupportingFunction.feature as ftDetect
#import SupportingFunction.hear as monitoring
# -*- coding: utf-8 -*-

from openai import OpenAI
from playsound import playsound
import os
import time
from datetime import datetime


def windowsPlaysound(filepath):
    os.system("start "+filepath)
    os.system("del  "+filepath)

def macPlaysound(filepath):
    playsound(filepath)
    os.remove('./'+filepath)
# ftDetect.findFeature()
# 设置OpenAI API密钥
client=OpenAI(api_key='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'#这里需要替换为你的账户API KEY
)

# 定义初始对话历史
conversation_history = [
    {'role': 'system', 'content': 'You are a helpful assistant.'}
]

# 循环交互
while True:
    # 处理用户输入
    user_input = input("User: ")

    # 将用户输入添加到对话历史中
    conversation_history.append({'role': 'user', 'content': user_input})

    # 发送聊天请求
    text_response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=conversation_history,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7
    )

    # 获取助手的回复
    assistant_reply = text_response.choices[0].message.content

    # 打印助手的回复
    print("Assistant:", assistant_reply)
    audio_response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=assistant_reply,
    )
    now = datetime.now()
    current_time = now.strftime("%H%M%S")
    audio_file_path="ANSWERED"+current_time+".mp3"

    audio_response.stream_to_file(audio_file_path)
    # windowsPlaysound(audio_file_path)
    macPlaysound(audio_file_path)

    conversation_history.append({'role': 'assistant', 'content': assistant_reply})

    # 检查用户是否选择退出循环
    if user_input.lower() == 'exit':
        break





