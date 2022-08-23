import numpy as np
import cv2
from mss import mss
# from PIL import Image
import math
import requests
import time
import win32api

SCREEN_W = 2550
SCREEN_H = 1440

bounding_box = {'top': 0, 'left': 0, 'width': SCREEN_W, 'height': SCREEN_H}

SPLIT_W = 37
SPLIT_H = 22

ZONE_W = math.floor(SCREEN_W / SPLIT_W)
ZONE_H = math.floor(SCREEN_H / SPLIT_H)
ZONE_STEP = 5
PERCENT_LIGHT = 0.145

sct = mss()


def on_exit(signal_type):
   print('caught signal:', str(signal_type))
   requests.get('http://192.168.1.144/off');

win32api.SetConsoleCtrlHandler(on_exit, True)

if __name__ == '__main__':
    while True:
        sct_img = sct.grab(bounding_box)
        arr = np.array(sct_img)
        
        screen_sample = np.zeros((SPLIT_H, SPLIT_W, 3), dtype=np.uint8);

        screen_sample = np.zeros((SPLIT_H, SPLIT_W, 3), dtype=np.uint8);
        for i in range(0, SPLIT_W):
            for j in range(0, SPLIT_H):
                if (j == 0 or j == SPLIT_H-1 or i == 0 or i == SPLIT_W-1):
                    mean_col = [0, 0, 0]
                    for x in range(0, ZONE_W, ZONE_STEP):
                        for y in range(0, ZONE_H, ZONE_STEP):
                            mean_col[0] += arr[y + (j * ZONE_H)][x + (i * ZONE_W)][0]
                            mean_col[1] += arr[y + (j * ZONE_H)][x + (i * ZONE_W)][1]
                            mean_col[2] += arr[y + (j * ZONE_H)][x + (i * ZONE_W)][2]
                    screen_sample[j, i][2] = round(((mean_col[0] * ZONE_STEP * ZONE_STEP) / (ZONE_H * ZONE_W)) * PERCENT_LIGHT)
                    screen_sample[j, i][1] = round(((mean_col[1] * ZONE_STEP * ZONE_STEP) / (ZONE_H * ZONE_W)) * PERCENT_LIGHT)
                    screen_sample[j, i][0] = round(((mean_col[2] * ZONE_STEP * ZONE_STEP) / (ZONE_H * ZONE_W)) * PERCENT_LIGHT)
        
        ct = 1
        htmlParam = "?0=0,0,0"
        for i in range(0, SPLIT_W - 1):
            htmlParam += "&" + str(ct) + "=" + str(screen_sample[0, i][0]) + "," + str(screen_sample[0, i][1]) + "," + str(screen_sample[0, i][2])
            ct+=1
        for i in range(0, SPLIT_H - 1):
            htmlParam += "&" + str(ct) + "=" + str(screen_sample[i, SPLIT_W - 1][0]) + "," + str(screen_sample[i, SPLIT_W - 1][1]) + "," + str(screen_sample[i, SPLIT_W - 1][2])
            ct+=1
        for i in range(SPLIT_W - 1, 0, -1):
            htmlParam += "&" + str(ct) + "=" + str(screen_sample[SPLIT_H - 1, i][0]) + "," + str(screen_sample[SPLIT_H - 1, i][1]) + "," + str(screen_sample[SPLIT_H - 1, i][2])
            ct+=1
        for i in range(SPLIT_H - 1, 0, -1):
            htmlParam += "&" + str(ct) + "=" + str(screen_sample[i, 0][0]) + "," + str(screen_sample[i, 0][1]) + "," + str(screen_sample[i, 0][2])
            ct+=1
        requests.get('http://192.168.1.144/set' + htmlParam);
        time.sleep(0.05)
