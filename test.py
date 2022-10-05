from trafSim import *
import matplotlib.pyplot as plt

sim = Simulation() 
step = 30
sim.create_roads([((st,50),(st+step,50)) for st in range(0,300,step)])
# print([road.length for road in sim.roads])
sim.create_gen({
    'vehicle_rate' : 200,
    'vehicles':[
        [1,{'path':list(range(300//step))}]
    ]
})

sim.run(10000)

# road.flow_array : array with flows (cars/time)
# road.density : array with densities (no. of cars in road divided by road length)
# road.time_array : array with times at which the flows/densities are calculated

flows = [road.flow_array for road in sim.roads]
densities = [road.density for road in sim.roads]
times = [road.flow_time for road in sim.roads]

n = 0

plt.plot(times[n],flows[n],label='flow')
plt.plot(times[n],densities[n],label='density')
plt.legend()
# plt.plot(densities[0],flows[0])
plt.show()