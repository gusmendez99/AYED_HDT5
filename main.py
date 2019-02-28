# -*- coding: cp1252 -*-
import simpy
import random



env = simpy.Environment()
ram = simpy.Container(env, init=100, capacity=100)
cpu = simpy.Resource(env, capacity=1)
random.seed(10) # fijar el inicio de random

def Process(name, env , instruction_qty , needed_ram, ram, cpu):
    state = 0
    print(ram.level)
    while True:
        if (state == 0):
            print(state) #todo
            print('Process %s requesting %s of RAM at %s' % (name, needed_ram ,env.now))
            if (ram.level > needed_ram):
                yield ram.get(needed_ram)
                yield env.timeout(1)
                state = 1
            else:
                print("insuficient RAM in the system")
        elif(state != 0 ):
            print(state) #
            #Changed State, initialize ready process
            print('Process %s requesting CPU access at %s' % (name, env.now))
            with cpu.request() as cpu_request:
                yield cpu_request
                print('Process %s got CPU access at %s' % (name, env.now))
                state = 2
                if (instruction_qty <= 3):
                    instruction_qty = 0
                    yield env.timeout(1)
                    cpu.release(cpu_request)
                    state = 4 #terminated
                    print("Process ended")
                else:
                    instruction_qty -= 3
                    cpu.release(cpu_request)
                    #In case the process needs to wait for I/O operations
                    random_integer = random.randint(1,2)
                    if (random_integer == 1):
                        waiting_timeout = 1 #can be any number
                        state = 3
                        yield env.timeout(waiting_timeout) # After this time, the process will be passed to ready again
                           
myProcess = env.process(Process("A",env,10,10,ram,cpu))

env.run(until=5)
#With a for loop, not with until
