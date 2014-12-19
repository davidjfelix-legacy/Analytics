#!/bin/env python

import json
import random
import sys

ROAD_SAMPLES = 2

def order_one(pmf, hoods, roads):
    mass = random.random()
    for i, m in enumerate(pmf):
        if mass < m:
            break
        mass -= m

    real_roads = [r for r in hoods[i]['roads'] if roads[r]]
    if not real_roads:
        raise Exception("%s ain't real." % (hoods[i]['name']))

    samples = [roads[random.choice(real_roads)]
               for i in range(ROAD_SAMPLES)]

    return tuple(float(sum(s[i] for s in samples)) / len(samples)
                 for i in (0, 1))

def main(cityfile, roadsfile, outfile):
    with open(cityfile, 'r') as f:
        hoods = json.load(f)
    with open(roadsfile, 'r') as f:
        roads = json.load(f)

    pmf = [h['population'] + h['income']
           for h in hoods]
    pmf_sum = sum(pmf)
    pmf = [float(m) / pmf_sum for m in pmf]

    random.seed(0)
    orders = [order_one(pmf, hoods, roads) for i in range(100)]

    with open(outfile, 'w') as f:
        json.dump(orders, f)

    for i, order in enumerate(orders):
        print('%s, %f, %f' % (('Order ' + str(i + 1),) + order))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: %s <city> <roads> <output>" % (sys.argv[0]))
        sys.exit(1)

    main(*sys.argv[1:])
