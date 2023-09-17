import random
import create
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ReadSensor import test_sensor

#testing value: time and distance

#read data from sensor from test_sensor.py

t,p = test_sensor.readFromSensor()

# go with my testing data
vNum = []
vTime = []
Num = 50
for i in range(0,Num):
    vNum.append(random.randint(0,10))
    vTime.append("10:"+ "{:02}".format(i))

print(vNum)
print(vTime)
create.createJson(vNum,vTime,"Bus")
