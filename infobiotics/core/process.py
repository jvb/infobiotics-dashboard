import time
for i in range(101):
    time.sleep(0.1)
    if i != 0 and i % 20 == 0:
        exit('error')
    print i
    
