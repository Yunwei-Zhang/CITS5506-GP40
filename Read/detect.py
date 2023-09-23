import distance_sensor as ds
import json

s1_distance = []
s2_distance = []
s1_time = []
s2_time = []

try:
    while True:
        #sensor1: Trig 4, Echo 17
        s1,d1,t1 = ds.detect(7,11,"sensor 1")
        s1_distance.append(d1)
        s1_time.append(t1) 
        #sensor2: Trig 5, Echo 35
        s2,d2,t2 = ds.detect(29,35,"sensor 2")
        s2_distance.append(d1)
        s2_time.append(t1)
except KeyboardInterrupt:
    print("stop")

#testing data only
# s1_distance = [40,300,300,300,40,300,300,60,60,300,60,300]
# s2_distance = [300,40,300,40,300,300,300,300,60,300,300,60]
# s1_time = [1,2,3,4,5,6,7,8,9,10,11,12]
# s2_time = [1,2,3,4,5,6,7,8,9,10,11,12]

#algrithmn
come = 0
leave = 0
count = 0
dataset = []
res = {}
for i in range(0,len(s1_distance)):
    if (s1_distance[i] <= 80 and s1_distance[i] >= 0):
        if (i-1 < 0):
            if(s2_distance[i+1] <= 80 and s2_distance[i+1] >= 0):
                come = 1
                count = count + 1
                data = {
                    'Come':1,
                    'Leave':0,
                    'Time':s1_time[i],
                    'Count':count
                }
                dataset.append(data)
        else:
            if(s2_distance[i+1] <= 80 and s2_distance[i+1] >= 0 and s2_distance[i-1] > 80):
                come = 1
                count = count + 1
                data = {
                    'Come':1,
                    'Leave':0,
                    'Time':s1_time[i],
                    'Count':count
                }
                dataset.append(data)
    if (s2_distance[i] <= 80 and s2_distance[i] >= 0 and i>len(s2_distance)):
        if(s1_distance[i+1] <= 80 and s1_distance[i+1] >= 0 and s1_distance[i-1] > 80):
            leave = 1
            count -= 1
            data = {
                    'Come':0,
                    'Leave':1,
                    'Time':s2_time[i],
                    'Count':count
                }
            dataset.append(data)

res["target"] = "Bus"
res["data"] = dataset

with open('data.json', 'w') as json_file:
        json.dump(res,json_file,indent=4)