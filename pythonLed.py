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

# SPLIT_W = 37
# SPLIT_H = 22

# ZONE_W = math.floor(SCREEN_W / SPLIT_W)
# ZONE_H = math.floor(SCREEN_H / SPLIT_H)
ZONE_STEP = 5
PERCENT_LIGHT = 1

sct = mss()


def on_exit(signal_type):
   print('caught signal:', str(signal_type))
   requests.get('http://192.168.1.144/off');

win32api.SetConsoleCtrlHandler(on_exit, True)

pixZone = [
    #Top line
    {"x1" :    0, "y1" : 0, "x2": 45  , "y2" : 70},
    {"x1" :   45, "y1" : 0, "x2": 115 , "y2" : 70},
    {"x1" :  115, "y1" : 0, "x2": 185 , "y2" : 70},
    {"x1" :  185, "y1" : 0, "x2": 255 , "y2" : 70},
    {"x1" :  255, "y1" : 0, "x2": 325 , "y2" : 70},
    {"x1" :  325, "y1" : 0, "x2": 395 , "y2" : 70},
    {"x1" :  395, "y1" : 0, "x2": 465 , "y2" : 70},
    {"x1" :  465, "y1" : 0, "x2": 535 , "y2" : 70},
    {"x1" :  535, "y1" : 0, "x2": 605 , "y2" : 70},
    {"x1" :  605, "y1" : 0, "x2": 675 , "y2" : 70},
    {"x1" :  675, "y1" : 0, "x2": 745 , "y2" : 70},
    {"x1" :  745, "y1" : 0, "x2": 815 , "y2" : 70},
    {"x1" :  815, "y1" : 0, "x2": 885 , "y2" : 70},
    {"x1" :  885, "y1" : 0, "x2": 955 , "y2" : 70},
    {"x1" :  955, "y1" : 0, "x2": 1025, "y2" : 70},
    {"x1" : 1025, "y1" : 0, "x2": 1095, "y2" : 70},
    {"x1" : 1095, "y1" : 0, "x2": 1165, "y2" : 70},
    {"x1" : 1165, "y1" : 0, "x2": 1235, "y2" : 70},
    {"x1" : 1235, "y1" : 0, "x2": 1305, "y2" : 70},
    {"x1" : 1305, "y1" : 0, "x2": 1375, "y2" : 70},
    {"x1" : 1375, "y1" : 0, "x2": 1445, "y2" : 70},
    {"x1" : 1445, "y1" : 0, "x2": 1515, "y2" : 70},
    {"x1" : 1515, "y1" : 0, "x2": 1585, "y2" : 70},
    {"x1" : 1585, "y1" : 0, "x2": 1655, "y2" : 70},
    {"x1" : 1655, "y1" : 0, "x2": 1725, "y2" : 70},
    {"x1" : 1725, "y1" : 0, "x2": 1795, "y2" : 70},
    {"x1" : 1795, "y1" : 0, "x2": 1865, "y2" : 70},
    {"x1" : 1865, "y1" : 0, "x2": 1935, "y2" : 70},
    {"x1" : 1935, "y1" : 0, "x2": 2005, "y2" : 70},
    {"x1" : 2005, "y1" : 0, "x2": 2075, "y2" : 70},
    {"x1" : 2075, "y1" : 0, "x2": 2145, "y2" : 70},
    {"x1" : 2145, "y1" : 0, "x2": 2215, "y2" : 70},
    {"x1" : 2215, "y1" : 0, "x2": 2285, "y2" : 70},
    {"x1" : 2285, "y1" : 0, "x2": 2355, "y2" : 70},
    {"x1" : 2355, "y1" : 0, "x2": 2425, "y2" : 70},
    {"x1" : 2425, "y1" : 0, "x2": 2495, "y2" : 70},

    #Right Col
    {"x1" : 2480, "y1" :    0, "x2": 2550, "y2" :   30},
    {"x1" : 2480, "y1" :   30, "x2": 2550, "y2" :  100},
    {"x1" : 2480, "y1" :  100, "x2": 2550, "y2" :  170},
    {"x1" : 2480, "y1" :  170, "x2": 2550, "y2" :  240},
    {"x1" : 2480, "y1" :  240, "x2": 2550, "y2" :  310},
    {"x1" : 2480, "y1" :  310, "x2": 2550, "y2" :  380},
    {"x1" : 2480, "y1" :  380, "x2": 2550, "y2" :  450},
    {"x1" : 2480, "y1" :  450, "x2": 2550, "y2" :  520},
    {"x1" : 2480, "y1" :  520, "x2": 2550, "y2" :  590},
    {"x1" : 2480, "y1" :  590, "x2": 2550, "y2" :  660},
    {"x1" : 2480, "y1" :  660, "x2": 2550, "y2" :  730},
    {"x1" : 2480, "y1" :  730, "x2": 2550, "y2" :  800},
    {"x1" : 2480, "y1" :  800, "x2": 2550, "y2" :  870},
    {"x1" : 2480, "y1" :  870, "x2": 2550, "y2" :  940},
    {"x1" : 2480, "y1" :  940, "x2": 2550, "y2" : 1010},
    {"x1" : 2480, "y1" : 1010, "x2": 2550, "y2" : 1080},
    {"x1" : 2480, "y1" : 1080, "x2": 2550, "y2" : 1150},
    {"x1" : 2480, "y1" : 1150, "x2": 2550, "y2" : 1220},
    {"x1" : 2480, "y1" : 1220, "x2": 2550, "y2" : 1290},
    {"x1" : 2480, "y1" : 1290, "x2": 2550, "y2" : 1360},
    {"x1" : 2480, "y1" : 1360, "x2": 2550, "y2" : 1430},
    {"x1" : 2480, "y1" : 1430, "x2": 2550, "y2" : 1440},
    
    #Bottom line
    {"x1" : 2410, "y1" : 1370, "x2": 2480, "y2" : 1440},
    {"x1" : 2340, "y1" : 1370, "x2": 2410, "y2" : 1440},
    {"x1" : 2270, "y1" : 1370, "x2": 2340, "y2" : 1440},
    {"x1" : 2200, "y1" : 1370, "x2": 2270, "y2" : 1440},
    {"x1" : 2130, "y1" : 1370, "x2": 2200, "y2" : 1440},
    {"x1" : 2060, "y1" : 1370, "x2": 2130, "y2" : 1440},
    {"x1" : 1990, "y1" : 1370, "x2": 2060, "y2" : 1440},
    {"x1" : 1920, "y1" : 1370, "x2": 1990, "y2" : 1440},
    {"x1" : 1850, "y1" : 1370, "x2": 1920, "y2" : 1440},
    {"x1" : 1780, "y1" : 1370, "x2": 1850, "y2" : 1440},
    {"x1" : 1710, "y1" : 1370, "x2": 1780, "y2" : 1440},
    {"x1" : 1640, "y1" : 1370, "x2": 1710, "y2" : 1440},
    
    {"x1" : 1595, "y1" : 1370, "x2": 1640, "y2" : 1440},

    {"x1" : 1525, "y1" : 1370, "x2": 1595, "y2" : 1440},
    {"x1" : 1455, "y1" : 1370, "x2": 1525, "y2" : 1440},
    {"x1" : 1385, "y1" : 1370, "x2": 1455, "y2" : 1440},
    {"x1" : 1315, "y1" : 1370, "x2": 1385, "y2" : 1440},
    {"x1" : 1245, "y1" : 1370, "x2": 1315, "y2" : 1440},
    {"x1" : 1175, "y1" : 1370, "x2": 1245, "y2" : 1440},
    {"x1" : 1105, "y1" : 1370, "x2": 1175, "y2" : 1440},
    {"x1" : 1035, "y1" : 1370, "x2": 1105, "y2" : 1440},
    {"x1" :  965, "y1" : 1370, "x2": 1035, "y2" : 1440},
    {"x1" :  895, "y1" : 1370, "x2":  965, "y2" : 1440},
    
    {"x1" :  850, "y1" : 1370, "x2":  895, "y2" : 1440},

    {"x1" :  780, "y1" : 1370, "x2":  850, "y2" : 1440},
    {"x1" :  710, "y1" : 1370, "x2":  780, "y2" : 1440},
    {"x1" :  640, "y1" : 1370, "x2":  710, "y2" : 1440},
    {"x1" :  570, "y1" : 1370, "x2":  640, "y2" : 1440},
    {"x1" :  500, "y1" : 1370, "x2":  570, "y2" : 1440},
    {"x1" :  430, "y1" : 1370, "x2":  500, "y2" : 1440},
    {"x1" :  360, "y1" : 1370, "x2":  430, "y2" : 1440},
    {"x1" :  290, "y1" : 1370, "x2":  360, "y2" : 1440},
    {"x1" :  220, "y1" : 1370, "x2":  290, "y2" : 1440},
    {"x1" :  150, "y1" : 1370, "x2":  220, "y2" : 1440},
    {"x1" :   80, "y1" : 1370, "x2":  150, "y2" : 1440},
    {"x1" :   10, "y1" : 1370, "x2":   80, "y2" : 1440},
    {"x1" :    0, "y1" : 1370, "x2":   30, "y2" : 1440},
    
    #Left col
    {"x1" : 0, "y1" : 1410, "x2": 70, "y2" : 1440},
    {"x1" : 0, "y1" : 1355, "x2": 70, "y2" : 1425},
    {"x1" : 0, "y1" : 1285, "x2": 70, "y2" : 1355},
    {"x1" : 0, "y1" : 1215, "x2": 70, "y2" : 1285},
    {"x1" : 0, "y1" : 1145, "x2": 70, "y2" : 1215},
    {"x1" : 0, "y1" : 1075, "x2": 70, "y2" : 1145},
    {"x1" : 0, "y1" : 1005, "x2": 70, "y2" : 1075},
    {"x1" : 0, "y1" :  935, "x2": 70, "y2" : 1005},
    {"x1" : 0, "y1" :  865, "x2": 70, "y2" :  935},
    {"x1" : 0, "y1" :  795, "x2": 70, "y2" :  865},
    {"x1" : 0, "y1" :  725, "x2": 70, "y2" :  795},
    {"x1" : 0, "y1" :  655, "x2": 70, "y2" :  725},
    {"x1" : 0, "y1" :  585, "x2": 70, "y2" :  655},
    {"x1" : 0, "y1" :  515, "x2": 70, "y2" :  585},
    {"x1" : 0, "y1" :  445, "x2": 70, "y2" :  515},
    {"x1" : 0, "y1" :  375, "x2": 70, "y2" :  445},
    {"x1" : 0, "y1" :  305, "x2": 70, "y2" :  375},
    {"x1" : 0, "y1" :  235, "x2": 70, "y2" :  305},
    {"x1" : 0, "y1" :  165, "x2": 70, "y2" :  235},
    {"x1" : 0, "y1" :   95, "x2": 70, "y2" :  165},
    {"x1" : 0, "y1" :   25, "x2": 70, "y2" :   95},
    {"x1" : 0, "y1" :    0, "x2": 70, "y2" :   30},
]


#from PIL import Image
#col = [
#    [255, 0, 0],
#    [0, 255, 0],
#    [0, 0, 255],
#    [255, 0, 255],
#    [0, 255, 255],
#    [255, 255, 0],
#]
#img = np.zeros((1440, 2550, 3), dtype=np.uint8)
#for i in range(0, len(pixZone)):
#   print(i, pixZone[i])
#   for x in range(pixZone[i]["x1"], pixZone[i]["x2"]):
#       for y in range(pixZone[i]["y1"], pixZone[i]["y2"]):
#           # print(x, y)
#           img[y, x] = col[i%len(col)]
#image = Image.fromarray(img)
#image.save("testGenerate.png")

if __name__ == '__main__':
    while True:
        sct_img = sct.grab(bounding_box)
        arr = np.array(sct_img)
        
        screen_sample = [];
        for i in range(0, len(pixZone)):
            mean_col = [0, 0, 0]
            counter = 0
            for x in range(pixZone[i]["x1"], pixZone[i]["x2"], ZONE_STEP):
                for y in range(pixZone[i]["y1"], pixZone[i]["y2"], ZONE_STEP):
                    counter += 1
                    mean_col[0] += arr[y][x][0]
                    mean_col[1] += arr[y][x][1]
                    mean_col[2] += arr[y][x][2]
            new_sample = [0, 0, 0]
            new_sample[2] = round(((mean_col[0]) / (counter)) * PERCENT_LIGHT)
            new_sample[1] = round(((mean_col[1]) / (counter)) * PERCENT_LIGHT)
            new_sample[0] = round(((mean_col[2]) / (counter)) * PERCENT_LIGHT)
            
            #For gray pixels, dimming te leds or making them brighter
            if (np.var(new_sample) < 5):
                if (np.mean(new_sample) > 192):
                    new_sample[2] = round(new_sample[2] * 1.25) if round(new_sample[2] * 1.25) < 255 else 255 
                    new_sample[1] = round(new_sample[1] * 1.25) if round(new_sample[1] * 1.25) < 255 else 255
                    new_sample[0] = round(new_sample[0] * 1.25) if round(new_sample[0] * 1.25) < 255 else 255
                    
                elif (np.mean(new_sample) < 128):
                    new_sample[2] = round(new_sample[2] * 0.05)
                    new_sample[1] = round(new_sample[1] * 0.05)
                    new_sample[0] = round(new_sample[0] * 0.05)
            screen_sample.append(new_sample)
        htmlParam = "?0=0,0,0"
        for ct in range(0, len(screen_sample)):
            htmlParam += "&" + str(ct+1) + "=" + str(screen_sample[ct][0]) + "," + str(screen_sample[ct][1]) + "," + str(screen_sample[ct][2])
        #for i in range(0, SPLIT_W):
        #    for j in range(0, SPLIT_H):
        #        if (j == 0 or j == SPLIT_H-1 or i == 0 or i == SPLIT_W-1):
        #            mean_col = [0, 0, 0]
        #            for x in range(0, ZONE_W, ZONE_STEP):
        #                for y in range(0, ZONE_H, ZONE_STEP):
        #                    mean_col[0] += arr[y + (j * ZONE_H)][x + (i * ZONE_W)][0]
        #                    mean_col[1] += arr[y + (j * ZONE_H)][x + (i * ZONE_W)][1]
        #                    mean_col[2] += arr[y + (j * ZONE_H)][x + (i * ZONE_W)][2]
        #            screen_sample[j, i][2] = round(((mean_col[0] * ZONE_STEP * ZONE_STEP) / (ZONE_H * ZONE_W)) * PERCENT_LIGHT)
        #            screen_sample[j, i][1] = round(((mean_col[1] * ZONE_STEP * ZONE_STEP) / (ZONE_H * ZONE_W)) * PERCENT_LIGHT)
        #            screen_sample[j, i][0] = round(((mean_col[2] * ZONE_STEP * ZONE_STEP) / (ZONE_H * ZONE_W)) * PERCENT_LIGHT)
        
        #ct = 1
        #htmlParam = "?0=0,0,0"
        #for i in range(0, SPLIT_W - 1):
        #    htmlParam += "&" + str(ct) + "=" + str(screen_sample[0, i][0]) + "," + str(screen_sample[0, i][1]) + "," + str(screen_sample[0, i][2])
        #    ct+=1
        #for i in range(0, SPLIT_H - 1):
        #    htmlParam += "&" + str(ct) + "=" + str(screen_sample[i, SPLIT_W - 1][0]) + "," + str(screen_sample[i, SPLIT_W - 1][1]) + "," + str(screen_sample[i, SPLIT_W - 1][2])
        #    ct+=1
        #for i in range(SPLIT_W - 1, 0, -1):
        #    htmlParam += "&" + str(ct) + "=" + str(screen_sample[SPLIT_H - 1, i][0]) + "," + str(screen_sample[SPLIT_H - 1, i][1]) + "," + str(screen_sample[SPLIT_H - 1, i][2])
        #    ct+=1
        #for i in range(SPLIT_H - 1, 0, -1):
        #    htmlParam += "&" + str(ct) + "=" + str(screen_sample[i, 0][0]) + "," + str(screen_sample[i, 0][1]) + "," + str(screen_sample[i, 0][2])
        #    ct+=1
        requests.get('http://192.168.1.144/set' + htmlParam);
        time.sleep(0.05)
