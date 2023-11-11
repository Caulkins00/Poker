import numpy as np
import sys

#num1 = (2400*28-4)/8
#num = (52*53*53*53*53*19/2400)
num = 410305012/4800
#0, 1, 2, 4, 8, 16, 32, 64, 128 all have unique sums. The highest integer in the matrix will be 255
#the dimension will be 52*53*53*53*53 (410,305,012 entries)
#total space complexity: 11,488,540,336

#will need a flashdrive for this. It will take 1.6 GB of storage to fit the whole matrix.

#saving the data and reading it again
data = np.arange(4800).reshape((4,5,10,4,6))

print(data)
print(sys.getsizeof(num))
print(num)
#"""
with open('test.npy', 'wb') as f:
    np.save(f, data)
with open('test.npy', 'rb') as f:
    a = np.load(f)
#"""