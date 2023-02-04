import sys

import numpy as np

h, w = int(sys.argv[1]), int(sys.argv[2])
random_range = [i-128 for i in range(256)]

out = '{} {}'.format(w, h)
for row in range(h):
    line = ''
    out += '\n'
    for column in range(w):
        line += str(np.random.choice(random_range)) + ' '
    line = line[:-1]
    out += line 
print(out)


