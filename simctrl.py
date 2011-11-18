#!/usr/bin/python

import heapq
import random
import sys

from dummyload import *

OUTPUT = False
STEP = 1

def allocate(demands, supply):
    # sort by class, deadline, type_priority
    total_allocated = 0.0
    supply_left = True
    allocations = {}
    while (supply > total_allocated and len(demands) > 0):
        print "Supply available: ", supply
        demands_left = []
        demands.sort()
        for demand_unit in demands: 
            print "Checking ", demand_unit.id
            
            if demand_unit.id not in allocations:
                allocations[demand_unit.id] = (demand_unit, -1)
            (demand_unit, prev_allocation_level) = allocations[demand_unit.id]
            print "Previous allocation level: ", prev_allocation_level
            new_allocation_level = prev_allocation_level + 1
            new_allocation_power = demand_unit.work[new_allocation_level].power

            must_allocate = (demand_unit.cls == DemandClass.DO_NOT_DELAY and \
                                prev_allocation_level == -1)
            can_allocate = (supply >= new_allocation_power)
            
            if (must_allocate):
                supply -= new_allocation_power
                total_allocated += new_allocation_power 
                allocations[demand_unit.id] = (demand_unit, new_allocation_level) 
                if (new_allocation_level + 1 < len(demand_unit.work)):
                    print "Placing back on demand queue: ", demand_unit
                    heapq.heappush(demands_left, demand_unit)
                print "Must allocate: ", demand_unit, " at level ", new_allocation_level
            else:
                if (can_allocate):
                    supply -= new_allocation_power
                    total_allocated += new_allocation_power 
                    allocations[demand_unit.id] = (demand_unit, new_allocation_level)
                    if (new_allocation_level + 1 < len(demand_unit.work)):
                        print "Placing back on demand queue: ", demand_unit
                        heapq.heappush(demands_left, demand_unit)
                    print "Can allocate: ", demand_unit, " at level ", new_allocation_level
        demands = demands_left
    print "Done allocating."
    return allocations, total_allocated

def update_preallocated(preallocated, allocations, now):
    for (demand_unit, work_level) in allocations.itervalues():
        work_unit = demand_unit.work[work_level]
        preallocated_power = work_unit.power
        preallocated_time = work_unit.time
        for t in range(now, now + preallocated_time + 2):
            if t not in preallocated:
                preallocated[t] = 0.0
            preallocated[t] = preallocated[t] + work_unit.power
        
def update_loads(allocations, now):
    for (demand_unit, work_level) in allocations.itervalues():
        demand_unit.origin.update_demand_curve(demand_unit, work_level, now)

def output(*strings):
    if OUTPUT:
        print(''.join(''.join([str(s), ', ']) for s in strings))

def simulate(loads, supplies, end):
    done = False
    now = 0

    preallocated = {}
    preallocated[now] = 0.0

    while (now <= end):

        # don't need to store allocations for times that have already passed
        tmp = {}
        for time in preallocated.iterkeys():
            if time < now:
                continue
            else:
                tmp[time] = preallocated[time]
        preallocated = tmp
        
        # get current available supply
        current_supply = 0.0
        for supply in supplies:
            current_supply = current_supply + supply.supply(now)
        output("supply", now, current_supply)
        current_supply = current_supply - preallocated[now]
        output("preallocated", now, preallocated[now])

        # get current loads
        current_demand = []
        for load in loads:
            demands = load.demand(now)
            for demand in demands:
                heapq.heappush(current_demand, demand)

        # allocated and update
        allocations, total_allocated = allocate(current_demand, current_supply)
        #print allocations
        output("allocated", now, total_allocated)
        update_preallocated(preallocated, allocations, now)
        update_loads(allocations, now)

        now = now + STEP

if __name__ == "__main__":

    # check arguments
    # for now hard code loads and sources
    # later read in from configuration file
    # each supply / demand should be able to scale avg and max

    a = DummyLoad(0, 'interactive', 10, LoadInertia.VERYHIGH, LoadIntensity.HIGH, LoadMagnitude.LOW, levels=3)
    b = DummyLoad(1, 'interactive', 5, LoadInertia.VERYLOW, LoadIntensity.VERYHIGH, LoadMagnitude.VERYLOW) 
    c = DummyLoad(2, 'batch', 5, LoadInertia.MEDIUM, LoadIntensity.LOW, LoadMagnitude.MEDIUM, levels=3)
    d = DummyLoad(3, 'batch', 1, LoadInertia.VERYHIGH, LoadIntensity.VERYLOW, LoadMagnitude.VERYHIGH, levels=4)
    e = DummyLoad(4, 'batch', 2, LoadInertia.VERYLOW, LoadIntensity.MEDIUM, LoadMagnitude.VERYLOW)

    z = DummySupply()

    loads = [a, b, c, d, e]
    supplies = [z]
    
    simulate(loads, supplies, 24*60.0)
