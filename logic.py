# Sets threshold for distance that determines if someone is passing by
THRESHOLD = 8


def logic(sensor1, sensor2, currentCount, enterFlag, leaveFlag):
    """
    Implements logic of passerby counting system to determine if someone
    is entering or leaving the location of deployment.
    """
    input1 = sensor1 < THRESHOLD
    input2 = sensor2 < THRESHOLD
    
    new_current_count = currentCount
    new_enter_flag = enterFlag
    new_leave_flag = leaveFlag
    
    # Designed to only take one flag if one is True,
    # and not check both at the same time.
    if input1:
        if leaveFlag:
            # Confirmed leave case
            new_current_count -= 1
            new_leave_flag = False
        elif not enterFlag:
            # Enter case
            new_enter_flag = True
    elif input2:
        if enterFlag:
            # Confirmed enter case
            new_enter_flag = False
            new_current_count += 1
        elif not leaveFlag:
            # Leave case
            new_leave_flag = True
    elif not input1 and not input2:
        if enterFlag:
            # Changed my mind, not going in case
            new_enter_flag = False
        elif leaveFlag:
            # Changed my mind, I'm staying case
            new_leave_flag = False
    
    return new_current_count, new_enter_flag, new_leave_flag

if __name__ == "__main__":
    samples = [
        [10, 10],
        [5, 10],
        [10, 7],
        [10, 10],
        [10, 10],
        [6, 10,],
        [10, 7],
        [10, 10],
        [4, 10],
        [10, 10]
    ]
    
    total_count = 0
    enter = False
    leave = False
    for sample in samples:
        total_count, enter, leave = logic(sample[0], sample[1], total_count, enter, leave)
    
    try:
        assert total_count == 2
    except:
        print(f"Expected: 1, Got: {total_count}")
    else:
        print("Success!")