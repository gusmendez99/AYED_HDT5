# Universidad del Valle de Guatemala
# Algoritmos y estructuras de datos - main.py
# HDT5 - 01-03-19
# Gustavo Mendez    18500
# Luis Urbina       18473

import simpy
import random
import math
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

    def start(self, env, instructions_qty, time, needed_ram, ram, cpu, state, name):
        with ram.get(needed_ram) as ramQueue:
            startTime = env.now
            yield ramQueue
            print('Process %s requesting %s of RAM at %s' % (name, needed_ram ,env.now))
            state = 1
            print("state is " + str(state))

            #CPU ---------
            yield env.timeout(0.5)
            while(instructions_qty > 0):
                with cpu.request() as req:
                    yield req
                    print('Process %s is running now' % (name))
                    if((instructions_qty - 3) <= 0): ##change this if wanna change the instructions_qty per Process
                        yield env.timeout(time)
                        instructions_qty = instructions_qty - instructions_qty
                        print('Process %s is Terminated at %s' %(name, env.now))
                        timesList.append(env.now - startTime)
                        ram.put(needed_ram) 
                    else:
                        yield env.timeout(1)
                        instructions_qty = instructions_qty - cpu_capacity
                        print('Process %s leaves the CPU at %s' % (name, env.now))
                        
                        random_integer = random.randint(1,2)
                        if (random_integer == 1):
                            yield env.timeout(1) # After this time, the process will be passed to ready again
                            print('Process %s is executing I/O operationes at %s' % (name, env.now))
                            state = 1 #ready state again
                        else:
                            state = 1 #ready state again
                        

def runNewSimulation(process_qty):
    
    for i in range(process_qty):
        
        ram_qty = random.randint(1, 10)
        instruction_qty = random.randint(1, 10)
        #time = random.expovariate(1.0 / interval_time)#Generamos el intervalo
        time = math.exp(1.0/interval_time)
        Process(env, instruction_qty, time, ram_qty, ram, cpu, 0, "Proceso %s" %(i + 1))
        

runNewSimulation(process_qty)
env.run()



totalProcessTime = 0
for i in timesList:#Calculamos el promedio
    totalProcessTime +=  i

avg_time = float(totalProcessTime / len(timesList))

desv_time = statistics.stdev(timesList) # desviacion estandar

# Resultados finales
print("\n\nTiempo promedio: " + str(int (avg_time)) + " unidades de tiempo.")
print("Desvest: " + str(int (desv_time))+ "\n")

#Process(env, 3, 10, ram, cpu, 0, "myProcess")