import random
import create

#testing value: time and distance
vNum = []
vTime = []
Num = 50
for i in range(0,Num):
    vNum.append(random.randint(0,10))
    vTime.append("10:"+ "{:02}".format(i))

print(vNum)
print(vTime)
create.createJson(vNum,vTime,"Bus")
