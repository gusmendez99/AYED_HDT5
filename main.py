# Universidad del Valle de Guatemala
# Algoritmos y estructuras de datos - main.py
# HDT5 - 01-03-19
# Gustavo Mendez    18500
# Luis Urbina       18473

import simpy
import random
import statistics

#Procesadores a utilizar
procesors = int(input("> Cantidad de procesadores: "))
#Procesos a cargar
process_qty = int(input("> Cantidad de procesos (25,50,100,150 o,200): "))
# Intervalo de tiempo a usar
interval_time = int(input("> Unidades de tiempo (1, 5, 10...): "))
#RAM disponible
ram_qty = int(input("> RAM (100 o 200): "))


env = simpy.Environment()
ram = simpy.Container(env, init=100, capacity=100)
cpu = simpy.Resource(env, capacity=procesors)
cpu_capacity = 3 #can ve changed if the processor is better

random.seed(10) # fijar el inicio de random
timesList = []


class Process(object): #Every process will be an object, for better control
    def __init__ (self, env, instruction_qty, time, needed_ram, ram, cpu, state, name):
        self.env = env
        self.action = env.process(self.start(env, instruction_qty, time, needed_ram, ram, cpu, state, name)) 
        #to control when the process will#be stopped

    def start(self, env, instruction_qty, time, needed_ram, ram, cpu, state, name):
        
        while True:
            #step 0 (new) Process will ask for ram with the new() function
            
            print('Process %s requesting %s of RAM at %s' % (name, needed_ram ,env.now))
            #generator = env.process(new(env,instruction_qty,needed_ram,ram,cpu, 0, name))
            #env.run(generator)
            yield  env.process(new(env,instruction_qty,time, needed_ram,ram,cpu, 0, name))


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
                        yield env.process(waiting(env, time)) # After this time, the process will be passed to ready again
                        print('Process %s is executing I/O operationes at %s' % (name, env.now))
                        state = 1 #ready state again
                    else:
                        state = 1 #ready state again

        
def new(env, instruction_qty, time, needed_ram, ram, cpu, state, name):
    if (ram.level > needed_ram):
        yield ram.get(needed_ram)
        yield env.timeout(time)
        
def terminate(env, instruction_qty, needed_ram, ram, cpu, state, name, cpu_request):
    print(ram.level)
    cpu.release(cpu_request)
    timesList.append(env.now)
    yield ram.put(needed_ram)

def waiting(env, waiting_timeout):
    yield env.timeout(waiting_timeout)


def runNewSimulation(process_qty):
    
    for i in range(process_qty):
        
        ram_qty = random.randint(1, 10)
        instruction_qty = random.randint(1, 10)
        time = random.expovariate(1.0 / interval_time)#Generamos el intervalo

        Process(env, instruction_qty, time, ram_qty, ram, cpu, 0, "Proceso %s" %(i + 1))
        

runNewSimulation(process_qty)
env.run()



totalProcessTime = 0
for i in timesList:#Calculamos el promedio
    totalProcessTime +=  i

avg_time = (totalProcessTime / len(timesList))

desv_time = statistics.stdev(timesList) # desviacion estandar

# Resultados finales
print("Tiempo promedio: " + str(int (avg_time)) + " unidades de tiempo.\n")
print("Desvest: " + str(int (desv_time))+ "\n")

#Process(env, 3, 10, ram, cpu, 0, "myProcess")