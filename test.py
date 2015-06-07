import datetime
import time
expire_time = "2013-05-21T09:50:35"
d = datetime.datetime.strptime(expire_time,"%Y-%m-%dT%H:%M:%S")
print d.date()
print d.time()

a = 1
b = 2
if a < 3 & b < 3:
    print "yes"


