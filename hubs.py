from spade.agent import Agent
from spade.behaviour import OneShotBehaviour

class HubAgent(Agent):
    # init function
    # initial plan: create 3 hubs and distribute the drones among them
    def __init__(self, jid, hub_name, password, position, packages, num_drones):
        super().__init__(jid, password)
        self.hub_name = hub_name
        self.position = position
        self.packages = packages
        self.num_drones = num_drones
        self.drones = []  # drones allocated to the hub

    async def setup(self):
        # Starting the hub
        print(f"Hub {self.jid} is ready.")
        print(f"Hub {self.jid} is located at {self.position}")
        self.add_behaviour(CreatingEnvironmentBehaviour())
        self.add_behaviour(ManageDronesBehavior())
        self.add_behaviour(ManagePackagesBehavior())

    # Assigns the drones to the hubs
    async def assign_drone(self, drone):
        self.drones.append(drone)
        print(f"Assigned Drone {drone.drone_name} to {self.hub_name}")


# Spade code for starting the environment
class CreatingEnvironmentBehaviour(OneShotBehaviour):
    async def run(self):
        print("Creating the environment.")


# Spade code for the drones management
class ManageDronesBehavior(OneShotBehaviour):
    async def run(self):
        # Implement logic for managing drones at the hub
        hub = self.agent
        print(f"{hub.hub_name}: Managing drones at {hub.position}.")


# Spade code for the packages management
class ManagePackagesBehavior(OneShotBehaviour):
    async def run(self):
        # Implement logic for managing packages at the hub
        hub = self.agent
        print(f"{hub.hub_name}: Managing packages at {hub.position}.")
