'''
声明：
    此程序为那些需要看灯塔的人准备~~~
    请在引用程序时和作者沟通，否则后果自己承担
版本号:1.1
此程序适用于系统分辨率>(1920,1200)或(1600,1200)<系统分辨率<(1920,1200)
需要安装以下第三方库:pillow、pyautogui、baidu-aip
程序开始时需具备以下条件：
    浏览器只留下一个网页，且网页必须在 https://dyjy.dtdjzx.gov.cn/#/personSpace/studyCours
    程序窗口不要挡到右半部分
'''
from PIL import ImageGrab
import time
import os
import re
import pyautogui
from aip import AipOcr

# 设置百度数据及模型
""" 你的 APPID AK SK """
APP_ID = '25179696'
API_KEY = 'FVITbKv6VfF0MWSwTvb56Mem'
SECRET_KEY = 'LL4YUf9wocqCfAX0fZL3c9W5hjBMvZuC'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

# 设置OCR所需位置
a = (694, 454, 900, 711)
r = re.compile('课程时长[:：](\d+)[:：](\d+)')

def OCR(sc):
    img = ImageGrab.grab(bbox=sc)
    img.save('screenshot.jpg')
    d = open('screenshot.jpg', 'rb')
    h = d.read()
    d.close()

    # 使用百度OCR
    k = client.basicGeneral(h)
    try:
        for i in k['words_result']:
            if '课程时长' in i['words']:
                return i['words'].lstrip('课程时长：')
        d = True
    except Exception as e:
        print('报错，照片已保留')  
        print(repr(e))
        d = False
    if d:
        os.remove('screenshot.jpg')

def ctime(t):
    change = re.search(r,t)
    mine = int(change.group(1))
    sec = int(change.group(2))
    t = mine * 60 + sec
    return t


def video():
    # 计算视频时间
    time.sleep(3)
    b = OCR(a)
    c = ctime(b)
    # 开始看视频
    pyautogui.moveTo(380, 654)
    pyautogui.click()
    time.sleep(c+1)
    pyautogui.moveTo(507, 14, 0.5)
    pyautogui.click()

def scr():
    time.sleep(1)
    pyautogui.scroll(3000)
    time.sleep(1)
    pyautogui.scroll(-1025)
    time.sleep(1)

# 主程序
def main(number):
    nu1 = number // 4
    nu2 = number % 4
    time.sleep(2)

    # 每个视频的坐标
    li = [(1126, 132),(1126,325),(1126,514),(1126,700)]
    pyautogui.moveTo(1126, 132)
    # 循环观看整十数视频
    for i in range(nu1):
        pyautogui.moveTo(1126,132,0.5)
        scr()
        time.sleep(1)
        for y in li:
            time.sleep(1)
            pyautogui.moveTo(y[0], y[1], 0.4)
            pyautogui.click()
            video()
        pyautogui.moveTo(70, 47, 0.5)
        pyautogui.click()

    # 如果剩下还有视频把个位数的视频看完
    if nu2 != 0:
        pyautogui.moveTo(1126,132,0.5)
        scr()
        for i in range(nu2):
            time.sleep(1)
            pyautogui.moveTo(li[i][0], li[i][1])
            pyautogui.click()
            time.sleep(1)
            video()
