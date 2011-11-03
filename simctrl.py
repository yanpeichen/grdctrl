#!/usr/bin/python

import heapq
import random
import sys

STEP = 1

class Work:
    def __init__(self, power, time):
        self.power = power
        self.time = time

    def __str__(self):
        return ''.join(["[power:", str(self.power), ", duration:",  str(self.time), "]"])

class Class():
    DO_NOT_DELAY = 0
    DELAY_LAST = 1
    DELAY_FIRST = 2
    classes = [1, 2, 3]

class Demand():
    def __init__(self, origin, work, deadline, cls):
        self.origin = origin
        self.work = work
        self.deadline = deadline
        self.cls = cls

    def __str__(self):
        return ''.join(["(origin:", str(self.origin), ", work:", str(self.work), ", deadline:", str(self.deadline), ", class:", str(self.cls), ")"])  

class DummyLoad():
   
    max_power = 1000.0          # watts
    max_duration = 3.0 * 60.0   # minutes  
    sim_end = 24.0 * 60.0       # minutes

    def __init__(self, type, priority, inertia):
        self.type = type
        self.priority = priority
        self.inertia = inertia  # [0,1]
        self.last_demand_set = False
        self.last_demand = None
        # determines how 'flat' the workload is

    def demand(self, now):

        if (self.last_demand_set):
            # same demand as last time
            flip = random.random()
            if (flip < self.inertia):
                demand = self.last_demand
                return demand
        
        # choose the work
        # (alpha = 2, beta = 5)
        # (using the beta distribution for sound scientific reasons </sarcasm>) 
        power = DummyLoad.max_power * random.betavariate(2, 5)
        duration = DummyLoad.max_duration * random.betavariate(2, 5)
        work = Work(power, duration)
        
        # choose the deadline
        deadline = now + duration
        if (self.type == 'batch'):
            slack = DummyLoad.sim_end * random.betavariate(2, 5)
            deadline = duration + slack
        
        # choose the class
        random.shuffle(Class.classes)
        cls = Class.classes[0]

        # create demand
        demand = Demand(self, work, deadline, cls)
        self.last_demand_set = True
        self.last_demand = demand
        return demand

def allocate(loads, supply):
    allocations = {}
    # allocations[time] = Allocation
    #while (supply > 0):
        # DO_NOT_DEFER loads
        
    return allocations

def simulate(loads, supplies):

    done = False
    now = 0

    preallocated = {}
    preallocated[now] = 0.0

    while (not done):

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

        # take away power that was already allocated
        current_supply = current_supply - preallocated[now]

        # get current loads
        current_load = []
        for load in loads:
            current_load.add(load.load(now))
        
        # do allocations, return (load, watts)
        allocations = allocate(current_loads, current_supply)
        
        # update preallocations for next time
        for time in allocated.iterkeys():
            if time in preallocated:
                preallocated[time] = preallocated[time] + allocated[time].watts
            else:
                preallocated[time] = allocated[time].watts
        
        # update demand
        for allocation in allocated.itervalues():
            allocation.load.update_demand(allocation)

        now = now + step

if __name__ == "__main__":

    sys.exit() 
    # check arguments
    # for now hard code loads and sources
    # later read in from configuration file
    # each supply / demand should be able to scale avg and max

    
