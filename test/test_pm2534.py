#!/usr/bin/python

from pm2534 import PM2534

if __name__ == '__main__':
    import time

    pm2534 = PM2534()

    print pm2534.id
    pm2534.function = 'VDC'
    print pm2534.function
    pm2534.speed = 2
    print pm2534.speed
    pm2534.range = 30
    print pm2534.range
    print pm2534.filter
    pm2534.filter = True
    print pm2534.filter
    pm2534.text = "HI"
    time.sleep(5)
    pm2534.display = False
    for i in xrange(0, 100):
        print pm2534.reading
    pm2534.display = True
