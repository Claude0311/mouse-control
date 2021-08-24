import autopy
import math
import time
import random
import sys
import requests
import traceback
import numpy as np
width, height = autopy.screen.size()
print(width,height)
# broad = [(width-10,height-10),(10,height-10),(10,10),(width-10,10)]
# screen  = []
screen = np.load('p.npy')
det = []
sideLen = []
baseURL = 'HTTP://192.168.0.17:5001'

def main():
    try:
        centers = requests.get(baseURL+'/centers')
        pos = centers.json()
        if len(pos) == 0:
            raise Exception("Error")
        [x,y,z] = pos[0]
        [toX,toY] = calPos(x,y)
        # print(toX,toY)
        autopy.mouse.move(toX,toY)
        return True
    except Exception as e:
        return False
        # error_class = e.__class__.__name__ #取得錯誤類型
        # detail = e.args[0] #取得詳細內容
        # cl, exc, tb = sys.exc_info() #取得Call Stack
        # lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
        # fileName = lastCallStack[0] #取得發生的檔案名稱
        # lineNum = lastCallStack[1] #取得發生的行號
        # funcName = lastCallStack[2] #取得發生的函數名稱
        # errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
        # print(errMsg)
    # time.sleep(0.005)


def init():
    global screen
    # if len(screen)==0:
    #     for x,y in broad:
    #         autopy.mouse.move(x,y)
    #         print('init')
    #         for i in range(3,0,-1):
    #             time.sleep(1)
    #             print('start in',i)
    #         x_avg = []
    #         y_avg = []
    #         for count in range(50):
    #             try:
    #                 centers = requests.get(baseURL+'/centers')
    #                 pos = centers.json()
    #                 if len(pos) == 0:
    #                     raise BaseException("Error")
    #             except:
    #                 time.sleep(0.03)
    #                 print('skip',count)
    #                 continue
    #             [x,y,z] = pos[0]
    #             x_avg.append(x)
    #             y_avg.append(y)
    #         screen.append([sum(x_avg)/len(x_avg),sum(y_avg)/len(y_avg)])
    print(screen)
    global det
    global sideLen
    det = [
        screen[0][0]*screen[1][1]-screen[0][1]*screen[1][0],
        screen[1][0]*screen[2][1]-screen[1][1]*screen[2][0],
        screen[2][0]*screen[3][1]-screen[2][1]*screen[3][0],
        screen[3][0]*screen[0][1]-screen[3][1]*screen[0][0]
    ]
    sideLen = [
        ((screen[0][0]-screen[1][0])**2+(screen[0][1]-screen[1][1])**2)**0.5,
        ((screen[1][0]-screen[2][0])**2+(screen[1][1]-screen[2][1])**2)**0.5,
        ((screen[2][0]-screen[3][0])**2+(screen[2][1]-screen[3][1])**2)**0.5,
        ((screen[3][0]-screen[0][0])**2+(screen[3][1]-screen[0][1])**2)**0.5
    ]
    # return screen

def calPos(x,y):
    area = [
         - (det[0]+y*(screen[1][0]-screen[0][0])-x*(screen[1][1]-screen[0][1])),
         - (det[1]+y*(screen[2][0]-screen[1][0])-x*(screen[2][1]-screen[1][1])),
         - (det[2]+y*(screen[3][0]-screen[2][0])-x*(screen[3][1]-screen[2][1])),
         - (det[3]+y*(screen[0][0]-screen[3][0])-x*(screen[0][1]-screen[3][1]))
    ]
    # print(area)
    # if area[0]<0 or area[1]<0 or area[2]<0 or area[3]<0:
    #     return
    innerH = [
        area[0]/sideLen[0],
        area[1]/sideLen[1],
        area[2]/sideLen[2],
        area[3]/sideLen[3]
    ]
    position = [
        width*innerH[3]/(innerH[1]+innerH[3]),
        height - height*innerH[0]/(innerH[0]+innerH[2])
    ]
    if position[0]>width-1: position[0]=width-1
    elif position[0]<0: position[0] = 0
    if position[1]>height-1: position[1]=height-1
    if position[1]<0: position[1]=0
    # print(position)
    return position



import time

if __name__=='__main__':
    init()
    count = 0
    tim = time.time()
    while True:
        isGet = main()
        if isGet:
            count += 1
        if count>60:
            iter = time.time()-tim 
            print(round(60/iter),'FPS')
            count = 0
            tim = time.time()
        
    