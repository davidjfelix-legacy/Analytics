#!/bin/env python

from collections import namedtuple
from datetime import date, datetime, time, timedelta
import json
import math
import random
import sys

ORDER_COUNT = 100

ROAD_SAMPLES = 2

# Peak represents a collection of orders during the day. For example, a typical
# restaurant has a lunch peak and a dinner peak, and each order is grouped into
# one of the two peaks.
#
#  start is the time object representing the start of the peak.
#  duration is the timedelta object representing the duration of the peak.
#  scale is a number representing this peak's portion of total daily orders.
#
# For example, Peak(time(hour=11), timedelta(hours=3), 30) represents a peak
# starting at 11am, lasting for 3 hours, and represents 30% of daily orders.
#
# Mathematically, a peak is modeled using a von Mises distribution. Orders
# belonging to a peak will be somewhat normally distributed around the time
# | start + duration / 2 | with deviation | duration / 2 |.

Peak = namedtuple('Peak', ('start', 'duration', 'scale'))

PEAKS = (
    Peak(time(hour=11, minute=30), timedelta(hours=2), 30),
    Peak(time(hour=17, minute=30), timedelta(hours=2), 50),
    Peak(time(hour=22, minute=30), timedelta(hours=2), 20),
)

def generate_location(pmf, hoods, roads):
    mass = random.uniform(0, sum(pmf))
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

def generate_time():
    mass = random.uniform(0, sum(p.scale for p in PEAKS))
    for i, p in enumerate(PEAKS):
        if mass < p.scale:
            break
        mass -= p.scale

    # Approximate parameters for von Mises distribution.

    day = date.today()
    start = datetime.combine(day, p.start) - datetime.combine(day, time())
    mu = ((start + p.duration / 2) / timedelta(days=1) % 1 * (2 * math.pi))

    stddev = p.duration / timedelta(days=1) * math.pi
    r = 1 - stddev * stddev / 2
    kappa = r * (2 - r * r) / (1 - r * r)

    return str((datetime.combine(day, time()) + timedelta(
            days=random.vonmisesvariate(mu, kappa) / (2 * math.pi))).time())

def main(cityfile, roadsfile, outfile):
    with open(cityfile, 'r') as f:
        hoods = json.load(f)
    with open(roadsfile, 'r') as f:
        roads = json.load(f)

    pmf = [h['population'] + h['income']
           for h in hoods]

    random.seed(0)
    orders = [{
            'time': generate_time(),
            'location': generate_location(pmf, hoods, roads),
        } for i in range(ORDER_COUNT)]

    with open(outfile, 'w') as f:
        json.dump(orders, f)

    for i, order in enumerate(orders):
        print('Order %d\t%s\t%f\t%f' %
                ((i + 1, str(order['time'])) + order['location']))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: %s <city> <roads> <output>" % (sys.argv[0]))
        sys.exit(1)

    main(*sys.argv[1:])
