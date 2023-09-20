import distance_sensor as ds

s1_distance = []
s2_distance = []
s1_time = []
s2_time = []
while True:
    #sensor1: Trig 4, Echo 17
    s1,d1,t1 = ds.detect(7,11,"sensor 1")
    if (d1>0 and d1< 100):
        s1_distance.append(d1)
        s1_time.append(t1) 
    #sensor2: Trig 5, Echo 35
    s2,d2,t2 = ds.detect(29,35,"sensor 2")
    if (d2>0 and d2< 100):
        s2_distance.append(d1)
        s2_time.append(t1) 
