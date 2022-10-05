import numpy as np

class Vehicle:
    def __init__(self, config={}): 
        # Set default configuration
        self.set_default_config()

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)

        # Calculate properties
        self.init_properties()

    def set_default_config(self):    
        self.l = 1  # Vehicle lenght
        self.s0 = 1 # minimum desired vehicle distance (bumper to bumper)
        self.T = 1 # reaction time
        self.v_max = 20 # max desired speed
        self.a_max = 1.44 # max aceleration
        self.b_max = 4.61 # comfortable deceleration

        self.path = [] # path to follow when multiple roads are connected, empty if it only follows one road)
        self.current_road_index = 0 # index of road in path, starts at 0, increases by 1 every time it proceeds to the next road
        self.parallel_roads = [] # parallel roads with same flow direction

        self.x = 0 # position
        self.v = self.v_max # velocity (dx/dt)
        # self.v = np.random.rand()*self.v_max*1.5 # randomly generated velocity
        self.a = 0 # acceleration (dv/dt -> d²x/dt²)
        self.stopped = False

        # self.patience = np.empty_likerandom.uniform(0,1)

    def init_properties(self):
        self.sqrt_ab = 2*np.sqrt(self.a_max*self.b_max) # sqrt factor
        self._v_max = self.v_max # private variable, to avoid being overwritten

    def update(self, lead, dt): # lead = none, when vehicle is leading, else is the vehicle in front of it
        # Update position and velocity
        if self.v + self.a*dt < 0: # doesn't allow for negative velocities to exist
            self.x -= 1/2*self.v*self.v/self.a # from solving for v=0
            self.v = 0 # set velocity to 0
        else: # Normal scenario
            self.v += self.a*dt
            self.x += self.v*dt + self.a*dt*dt/2
        
        # Update acceleration
        alpha = 0
        if lead: # equivalent to "lead != None"
            delta_x = lead.x - self.x - lead.l # bumper distance (s)
            delta_v = self.v - lead.v # velocity difference

            alpha = (self.s0 + max(0, self.T*self.v + delta_v*self.v/self.sqrt_ab)) / delta_x # IDM acceleration of interaction

        self.a = self.a_max * (1-(self.v/self.v_max)**4 - alpha**2)

        if self.stopped: # when in a red light
            self.a = -self.b_max*self.v/self.v_max # damping equation ()
        
    def stop(self):
        self.stopped = True # For wehen vehicle enters stop zone

    def unstop(self):
        self.stopped = False # For when vehicle leaves stop zone

    def slow(self, v):
        self.v_max = v # when vehicle is in slow down zone

    def unslow(self):
        self.v_max = self._v_max # For when vehicle leaves slow-down zone
        

