#!/usr/bin/python

import random

STEP = 1 # TODO: FIXME: This is defined in two places.

class Work:
    def __init__(self, id, power, time):
        self.id = id
        self.power = power
        self.time = time

    def __str__(self):
        return ''.join(["[id:", str(self.id), ", power:", str(self.power), ", duration:",  str(self.time), "],"])

    def __lt__(self, other):
        if (self.power < other.power):
            return True
        if (self.power > other.power):
            return False
        if (self.duration < other.duration):
            return True
        if (self.duration < other.duration):
            return False
        if (self.id < other.id):
            return True
        if (self.id > other.id):
            return False
        return False

    def __eq__(self, other):
        return (self.power == other.power and self.duration == other.duration and self.id == other.id)

class DemandClass():
    DO_NOT_DELAY = 0
    DELAY_LAST = 1
    DELAY_FIRST = 2
    classes = [0, 1, 2]

class DemandUnit():
    def __init__(self, id, origin, work, arrival, deadline, cls):
        self.id = (origin.id, id)
        self.origin = origin
        self.work = work
        self.arrival = arrival
        self.deadline = deadline
        self.cls = cls

    def __str__(self):
        work_string = ''.join([str(w) for w in self.work])
        return ''.join(["(id:", str(self.id), ", origin:", str(self.origin), ", work:{", work_string, "}, deadline:", str(self.deadline), ", class:", str(self.cls), ")"])   

    def __lt__(self, other):
        if (self.cls < other.cls):
            return True
        if (self.cls > other.cls):
            return False
        if (self.origin.priority < other.origin.priority):
            return False
        if (self.origin.priority > other.origin.priority):
            return True
        if (self.deadline < other.deadline):
            return True
        if (self.deadline > other.deadline):
            return False
        if (self.work[0].power < other.work[0].power):
            return True
        if (self.work[0].power > other.work[0].power):
            return False
        return False

    def __eq__(self, other):
        if (self.cls == other.cls and \
            self.origin.priority == other.origin.priority and \
            self.deadline == other.deadline and \
            self.work[0].power == other.work[0].power):
            return True
        return False

class DummySupply():

    def supply(self, now):
        return random.random() * 1000.0

class LoadIntensity():
    VERYLOW = .1
    LOW = .25
    MEDIUM = .5
    HIGH = .75
    VERYHIGH = .9

class LoadMagnitude():
    VERYLOW = .1
    LOW = .25
    MEDIUM = .5
    HIGH = .75
    VERYHIGH = .9

class LoadInertia():
    VERYLOW = .1
    LOW = .25
    MEDIUM = .5
    HIGH = .75
    VERYHIGH = .9

class DummyLoad():
    
    max_power = 1000.0          # watts
    max_duration = 3.0 * 60.0   # minutes  
    sim_end = 24 * 60           # minutes
   
    def __init__(self, id, type, priority, inertia, intensity, magnitude, levels=1):
        self.id = id
        self.type = type
        self.priority = priority
        self.inertia = inertia  # in [0,1]
        self.intensity = intensity # in [0,1]
        self.magnitude = magnitude
        self.levels = levels
        self.last_demand = None
        self.demand_count = 0
        self.demand_curve_offered = {}
        self.demand_curve_realized = {}
        self.create_demand_curve()
        # determines how 'flat' the workload is

    def demand(self, now):
        return self.demand_curve_offered[now]

    def create_demand_curve(self):
        for t in range(DummyLoad.sim_end + 1):
            self.demand_curve_offered[t] = []
            self.demand_curve_realized[t] = []
            demand_unit = self.generate_demand_unit(t)
            if demand_unit is not None:
                self.demand_curve_offered[t].append(demand_unit)

    def update_demand_curve(self, demand_unit, work_level, now):
        if (work_level == -1):
            self.demand_curve_offered[now].remove(demand_unit)
            self.demand_curve_offered[now + STEP].append(demand_unit)
        else:
            tup = (demand_unit, work_level)
            self.demand_curve_realized[now].append(tup)
                
    def generate_demand_unit(self, now):
 
        # there may be no demand
        flip = random.random()
        if (flip > self.intensity):
            self.last_demand = None
            return None

        # the demand may be the same as before
        flip = random.random()
        if (flip < self.inertia):
            demand = self.last_demand
            if demand is not None:
                demand.arrival = now
                demand.deadline += STEP 

                demand.id = (self.id, self.demand_count)
                
                self.demand_count = self.demand_count + 1
                self.last_demand = demand
            return demand
        
        # else choose the work and the deadline with betavariate(alpha = 2, beta = 5)
        # assume interactive at first
        high_power = DummyLoad.max_power * self.magnitude * random.betavariate(2, 5)
        duration = STEP
        deadline = now + duration
        works = {}
        for level in range(1, self.levels + 1):
            pinc = high_power / self.levels
            power = pinc*level
            works[power] = duration
        if (self.type == 'batch'): 
            high_duration = int(DummyLoad.max_duration * random.betavariate(2, 5))
            total_energy = high_power * high_duration
            for power in works.iterkeys():
                duration = int(total_energy / power)
                works[power] = duration
            slack = DummyLoad.sim_end * random.betavariate(2, 5)
            powers = works.keys()
            powers.sort()
            longest_duration = works[powers[0]]
            deadline = longest_duration + slack
        work = []
        count = 0
        for (power, duration) in works.iteritems():
            work.append(Work(count, power, duration))
            count = count + 1
        work.sort()
        last_w = None
        for w in work:
            if last_w is not None:
                assert last_w.power < w.power
            last_w = w

        # choose the class
        random.shuffle(DemandClass.classes)
        cls = DemandClass.classes[0]

        # return the demand
        demand = DemandUnit(self.demand_count, self, work, now, deadline, cls)
        self.demant_count = self.demand_count + 1
        self.last_demand = demand
        return demand
