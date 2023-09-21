import distance_sensor as ds
import time

# 初始化人数为0
current_count = 0

# 定义阈值（小于1米）
threshold_distance = 100  # 假设100厘米表示1米

# 定义用于记录上一个传感器的标识符的变量
state = 0

while True:
    # 传感器1: Trig 4, Echo 17
    s1, d1, t1 = ds.detect(7, 11, "sensor 1")
    # 传感器2: Trig 5, Echo 35
    s2, d2, t2 = ds.detect(29, 35, "sensor 2")

    # 如果传感器1小于阈值，表示有人经过
    if state == 0:
            if d1 <= threshold_distance:
                state = 1
    elif state == 1:
            if d2 <= threshold_distance:
                current_count += 1
                state = 0

    # 如果传感器2小于阈值，表示有人经过
    if state == 0:
            if d2 <= threshold_distance:
                state = 2
    elif state == 2:
            if d1 <= threshold_distance:
                current_count -= 1
                state = 0
    # 打印当前人数
    print(f"当前人数：{current_count}")

    # 等待一段时间再进行下一次测量
    time.sleep(1)
