from scipy.spatial import distance
from collections import deque

class Road: 
    def __init__(self, start, end):
        self.start = start
        self.end = end

        self.vehicles = deque()

        self.init_properties()
        self.flow = 0 # Total flow of cars
        self.flow_array = [] # Flow array, appends every time a car passes the road
        self.flow_time = [] # Time array, "                                      "
        self.density = [] # Density array, "                                     "

    def init_properties(self):
        self.length = distance.euclidean(self.start, self.end)
        self.angle_sin = (self.end[1]-self.start[1]) / self.length
        self.angle_cos = (self.end[0]-self.start[0]) / self.length
        # self.angle = np.arctan2(self.end[1]-self.start[1], self.end[0]-self.start[0])
        self.has_traffic_signal = False

    def set_traffic_signal(self, signal, group):
        self.traffic_signal = signal
        self.traffic_signal_group = group
        self.has_traffic_signal = True

    @property
    def traffic_signal_state(self):
        if self.has_traffic_signal:
            i = self.traffic_signal_group
            return self.traffic_signal.current_cycle[i]
        return True

    def update(self, dt,SIM):
        n = len(self.vehicles) # number of vehicles

        if n > 0:
            # Update first vehicle
            # sum_index = 1
            # while len(SIM.roads[self.vehicles[0].path[self.vehicles[0].current_road_index+1]].vehicles)==0:
            #     sum_index+=1
            try:
                lead0 = SIM.roads[self.vehicles[0].path[self.vehicles[0].current_road_index+1]].vehicles[-1]
            except:
                lead0 = None
            self.vehicles[0].update(lead0, dt)
            # Update other vehicles
            for i in range(1, n):
                lead = self.vehicles[i-1]
                self.vehicles[i].update(lead, dt)

             # Check for traffic signal
            if self.traffic_signal_state:
                # If traffic signal is green or doesn't exist
                # Then let vehicles pass
                self.vehicles[0].unstop()
                for vehicle in self.vehicles:
                    vehicle.unslow()
            else:
                # If traffic signal is red
                if self.vehicles[0].x >= self.length - self.traffic_signal.slow_distance:
                    # Slow vehicles in slowing zone
                    self.vehicles[0].slow(self.traffic_signal.slow_factor*self.vehicles[0]._v_max)
                if self.vehicles[0].x >= self.length - self.traffic_signal.stop_distance and\
                   self.vehicles[0].x <= self.length - self.traffic_signal.stop_distance / 2:
                    # Stop vehicles in the stop zone
                    self.vehicles[0].stop()

    def init_vehicles(self,vehicle_count):
        for count in vehicle_count:

            self.vehicles.append()
