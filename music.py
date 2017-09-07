#!/usr/bin/python3
# -*- coding:utf8 -*-

import os
from aip import AipSpeech
import RPi.GPIO as GPIO
import threading
import time

APP_ID = 'your APP_ID'
API_KEY = 'your API_KEY'
SECRET_KEY = 'your SECRET_KEY'
aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)

# 用到的语音消息
if not os.path.exists('./wel.mp3'):
    wel = aipSpeech.synthesis('你好，我是小羽，下面我来为你播放音乐。', 'zh', 1, {'vol':5,'per':4})
    if not isinstance(wel, dict):
        with open('wel.mp3', 'wb') as f:
            f.write(wel)

if not os.path.exists('./up.mp3'):
    up = aipSpeech.synthesis('我在，什么事', 'zh', 1, {'vol':5,'per':4})
    if not isinstance(up, dict):
        with open('up.mp3', 'wb') as f:
            f.write(up)

if not os.path.exists('./errs.mp3'):
    errs = aipSpeech.synthesis('未检测到存储设备', 'zh', 1, {'vol':5,'per':4})
    if not isinstance(errs, dict):
        with open('errs.mp3', 'wb') as f:
            f.write(errs)

if not os.path.exists('./errsn.mp3'):
    errsn = aipSpeech.synthesis('未检测到MP3文件', 'zh', 1, {'vol':5,'per':4})
    if not isinstance(errsn, dict):
        with open('errsn.mp3', 'wb') as f:
            f.write(errsn)

if not os.path.exists('./exitend.mp3'):
    exitend = aipSpeech.synthesis('这首歌结束后，将退出播放，谢谢使用', 'zh', 1, {'vol':5,'per':4})
    if not isinstance(exitend, dict):
        with open('exitend.mp3', 'wb') as f:
            f.write(exitend)

if not os.path.exists('./end.mp3'):
    end = aipSpeech.synthesis('全部音乐播放完毕,我的工作做完了，拜拜', 'zh', 1, {'vol':5,'per':4})
    if not isinstance(end, dict):
        with open('end.mp3', 'wb') as f:
            f.write(end)

class musicThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print ('播放')
        os.system('mplayer ' + path + '/' + f)
        print ('--------------------')

os.system('mplayer ./wel.mp3')

file_num = 0
file_list = []
dir_list = []
path = r'/media/pi'
files = os.listdir(path)

if not files:
    print('未检测到存储设备')
    os.system('mplayer ./errs.mp3')
    exit()

path = path + '/' + files[0]
files = os.listdir(path)

# 这里可以用递归法逐级搜索，可以改进
# 搜索一级菜单
for f in files:
    if os.path.isfile(path + '/' + f):
        if f[-4:] == '.mp3':
            file_list.append(f)
            file_num += 1
    if os.path.isdir(path + '/' + f):
        dir_list.append(f)
# 搜索二级菜单
for dir in dir_list:
    files = os.listdir(path + '/' + dir)
    for f in files:
        if os.path.isfile(path + '/' + dir + '/' + f):
            if f[-4:] == '.mp3':
                file_list.append(dir + '/' + f)
                file_num += 1

if file_num == 0:
    print('没有检测到mp3文件')
    os.system('mplayer ./errsn.mp3')
    exit()    

print(str(file_num) + '个文件：')

num = aipSpeech.synthesis('一共检测到' + str(file_num) + '首音乐', 'zh', 1, {'vol':5,'per':4})
if not isinstance(num, dict):
    with open('num.mp3', 'wb') as f:
        f.write(num)
os.system('mplayer ./num.mp3')
n = 1
for f in file_list:
    cf = f[0:-4]
    song = aipSpeech.synthesis('第' + str(n) + '首音乐' + str(cf) + '送给你', 'zh', 1, {'vol':5,'per':4})
    if not isinstance(song, dict):
        with open('song.mp3', 'wb') as s:
            s.write(song)
    f = f.replace(' ', '\ ')
    print(f)
    thread = musicThread()
    thread.start()
    os.system('mplayer ./song.mp3')
    while thread.isAlive():
        if GPIO.input(21):
            os.system('mplayer ./exitend.mp3')
            exit()
    n += 1

os.system('mplayer ./end.mp3')


