# -*- coding: cp1252 -*-
import simpy
import random

# el proceso process muestra un veh�culo que se estaciona un tiempo
# y luego se conduce otro lapso de tiempo
def Process(nombre,env,process_time,ram):
    global totalDia  # :( mala practica, pero ni modo

    # Simular que esta conduciendo un tiempo antes de llegar a la gasolinera
    yield env.timeout(process_time)
    
    # llegando a la gasolinera
    horaLlegada = env.now

    # simular que necesita un tiempo para processgar gasolina. Probablemente
    # si es processro peque�o necesita menos tiempo y si es proceso grande mas tiempo
    tiempoProceso = random.randint(1, 7)
    print ('%s llega a las %f necesita %d para hechar gasolina' % (nombre,horaLlegada,tiempoProceso))
    
    # ahora se dirige a la bomba de gasolina,
    # pero si hay otros carros, debe hacer cola
    with ram.request() as turno:
        yield turno      #ya puso la manguera de gasolina en el proceso!
        yield env.timeout(tiempoProceso) #hecha gasolina por un tiempo
        print ('%s sale de gasolinera a las %f' % (nombre, env.now))
        #aqui el proceso hace un release automatico de la bomba de gasolina
        
    tiempoTotal = env.now - horaLlegada
    print ('%s se tardo %f' % (nombre, tiempoTotal))
    totalDia = totalDia + tiempoTotal
           

# ----------------------

env = simpy.Environment() #ambiente de simulaci�n
ram = simpy.Resource(env,capacity = 1)
random.seed(10) # fijar el inicio de random

totalDia = 0
for i in range(5):
    env.process(Process('proceso %d'%i,env,random.expovariate(1.0/10),ram))

env.run(until=50)  #correr la simulaci�n hasta el tiempo = 50

print ("tiempo promedio por veh�culo es: ", totalDia/5.0)