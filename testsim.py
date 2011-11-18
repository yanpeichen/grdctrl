#!/usr/bin/python

from dummyload import *
from simctrl import *
import heapq
import sys

def test_one(loads):
    print "Generating demands."
    demands = []
    for load in loads:
        demand = None
        while demand is None:
            demand = load.generate_demand_unit(0)
        heapq.heappush(demands, demand)
        print demand

    total_power_demanded = 0
    for demand in demands:
        total_power_demanded += demand.work[0].power

    supply = total_power_demanded * .75

    print "\n\nGenerating allocations."
    allocations = allocate(demands, supply)

    for (demand_unit, work_level) in allocations.iteritems():
        print(demand_unit, work_level)

    print "Done."

def test_two(loads):

    # make sure demand units are sorting properly and demands get unique IDs
    pq = []
    for load in loads:
        for i in range(1000):
            demand = load.generate_demand_unit(i)
            if demand is not None:
                heapq.heappush(pq, demand)

    pq.sort()
    last_priority = 1000000
    last_class = -1
    for demand_unit in pq:
        sys.stdout.write('~')
        assert(demand_unit.cls >= last_class)
        if demand_unit.cls == last_class:
            assert(demand_unit.origin.priority <= last_priority)
        last_class = demand_unit.cls
        last_priority = demand_unit.origin.priority

    seen_IDs = {}
    for demand_unit in pq:
        sys.stdout.write('*')
        assert (demand_unit.id not in seen_IDs)
        seen_IDs[demand_unit.id] = 1


if __name__ == "__main__":

    
    a = DummyLoad(0, 'interactive', 10, LoadInertia.VERYHIGH, LoadIntensity.HIGH, LoadMagnitude.LOW, levels=3)
    b = DummyLoad(1, 'interactive', 5, LoadInertia.VERYLOW, LoadIntensity.VERYHIGH, LoadMagnitude.VERYLOW) 
    c = DummyLoad(2, 'batch', 5, LoadInertia.MEDIUM, LoadIntensity.LOW, LoadMagnitude.MEDIUM, levels=3)
    d = DummyLoad(3, 'batch', 1, LoadInertia.VERYHIGH, LoadIntensity.VERYLOW, LoadMagnitude.VERYHIGH, levels=4)
    e = DummyLoad(4, 'batch', 2, LoadInertia.VERYLOW, LoadIntensity.MEDIUM, LoadMagnitude.VERYLOW)

    loads = [a, b, c, d, e]

    test_two(loads)

