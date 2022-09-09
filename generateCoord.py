#right col
#step = 70
#for i in range(30, 1440, step):
#    print('    {"x1" : 2480, "y1" : '+ '{:4d}'.format(i) +', "x2": 2550, "y2" : '+ '{:4d}'.format(1440 if (i + step)>1440 else (i + step)) +'},')

#bottom line
step = 70
for i in range(1440+70-15, 0, -step):
    print('    {"x1" : 0, "y1" : '+     '{:4d}'.format(0 if (i - step)<0 else (i - step))     +', "x2": 30, "y2" : '+    '{:4d}'.format(i)    +'},')
