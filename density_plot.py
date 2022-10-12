from trafSim import *
import matplotlib.pyplot as plt
from random import sample


N = list(range(0,301,4))
flows = []
densities = []
for n in N:
    sim = Simulation()
    sim.create_roads([((0,50),(300,50))])

    # print([road.length for road in sim.roads])
    # sim.create_gen({
    #     'vehicle_rate' : 40,
    #     'vehicles':[
    #         [1,{'path':[0]}]
    #     ]
    # })
    positions = sample(N,n//4+1)
    for pos in positions:
        car = Vehicle(config={'x':pos,'path':[0,0,0,0,0,0,0,0,0,0,0]})
        sim.roads[0].vehicles.append(car)

    sim.run(1200)

    flows.append(np.mean(sim.roads[0].flow_array))
    # densities.append(np.mean(sim.roads[0].density))
    densities.append((n//4+1)/300)

# road.flow_array : array with flows (cars/time)
# road.density : array with densities (no. of cars in road divided by road length)
# road.time_array : array with times at which the flows/densities are calculated

# flows = [road.flow_array for road in sim.roads]
# densities = [road.density for road in sim.roads]
# times = [road.flow_time for road in sim.roads]

# n = 0
# plt.plot(times[n],flows[n],label='flow')
# plt.plot(times[n],densities[n],label='density')
plt.plot(densities,flows)
plt.savefig('rho_vs_flow.pdf')
plt.show()