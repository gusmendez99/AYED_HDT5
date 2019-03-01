# -*- coding: cp1252 -*-
import simpy
import random



env = simpy.Environment()
ram = simpy.Container(env, init=100, capacity=100)
cpu = simpy.Resource(env, capacity=1)
cpu_capacity = 3 #can ve changed if the processor is better
random.seed(10) # fijar el inicio de random

class Process(object): #Every process will be an object, for better control
    def __init__ (self, env, instruction_qty, needed_ram, ram, cpu, state, name):
        self.env = env
        self.action = env.process(self.start(env, instruction_qty, needed_ram, ram, cpu, state, name)) 
        #to control when the process will#be stopped

    def start(self, env, instruction_qty, needed_ram, ram, cpu, state, name):
        while True:
            #step 0 (new) Process will ask for ram with the new() function
            print('Process %s requesting %s of RAM at %s' % (name, needed_ram ,env.now))
            yield env.process(new(env,instruction_qty,needed_ram,ram,cpu, 0, name))
            state = 1
            print("state is " + str(state))
            print('Process %s requesting CPU access at %s' % (name, env.now))

            
            #step 1 (ready) Process will ask for the CPU resource for attendance
            with cpu.request() as cpu_request:                       
                yield cpu_request
                
                #step 2(running) Process now will be executed and sended to Waiting in case there are
                #instructions left
                instruction_qty = instruction_qty - cpu_capacity
                state = 2
                print("state is " + str(state))
                print('Process %s got CPU access at %s' % (name, env.now))
                if (instruction_qty <= 0): #If instructions are all done
                    env.process(terminate(env,instruction_qty,needed_ram,ram,cpu,state,name, cpu_request))
                    #Step 4 (terminated) Process will be done (no more instructions left)
                    print('Process %s got terminated at %s' % (name, env.now))
                    state = 4
                    print("state is " + str(state))
                    
                else:
                    yield env.timeout(1)
                    cpu.release(cpu_request)
                    print('Process %s released cpu_resourse at %s' % (name, env.now))
                    print('Theres still %s instructions in %s' %(instruction_qty, name))

                    #generate random integer to decidethe next step to the process
                    random_integer = random.randint(1,2)
                    if (random_integer == 1):
                        yield env.process(waiting(env, 1)) # After this time, the process will be passed to ready again
                        print('Process %s is executing I/O operationes at %s' % (name, env.now))
                        state = 1 #ready state again
                    else:
                        state = 1 #ready state again

        
def new(env, instruction_qty, needed_ram, ram, cpu, state, name):
    if (ram.level > needed_ram):
        yield ram.get(needed_ram)
        yield env.timeout(1)
        
def terminate(env, instruction_qty, needed_ram, ram, cpu, state, name, cpu_request):
    print(ram.level)
    cpu.release(cpu_request)
    yield ram.put(needed_ram)
def waiting(env, waiting_timeout):
    yield env.timeout(waiting_timeout)


myProcess = Process(env, 3, 10, ram, cpu, 0, "myProcess")
otheProcess = Process(env, 10, 10,  ram, cpu, 0, "oTherProcess")

env.run(until=5)
#With a for loop, not with until
