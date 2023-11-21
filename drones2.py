from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
from environment import Environment
import json
import asyncio


class DroneAgent(Agent):

    # init function
    def __init__(self, jid, password, position, drone_name, max_weight, speed, energy_capacity, dronerange,
                 environment):
        super().__init__(jid, password)
        self.drone_name = drone_name
        self.max_weight = max_weight
        self.speed = speed
        self.energy_capacity = energy_capacity
        self.energy = energy_capacity  # tracks the current energy
        self.dronerange = dronerange
        self.position = position  # tracks the current drone position
        self.packages = []
        self.current_package = None
        self.current_path = []
        self.environment = environment

    # Starting the drones
    async def setup(self):
        msg = Message(to="HubH@localhost")
        msg.set_metadata("performative", "inform")
        drone_name = self.drone_name
        msg.body = f"Drone {drone_name} is ready"
        # await self.send(msg)
        print(f"Sent message: {msg.body}")


    # Function that makes the drones to pick the packages
    async def pick_up_package(self, package):
        await asyncio.sleep(2)
        path, total_distance = await self.calculate_path(package['destination'])
        if self.energy - 2 * total_distance < 25:
            # if energy after the delivery is below 25, recharge the drone first
            await self.recharge()
        self.current_package = package
        package['status'] = "in transit"
        self.update_energy(-5)  # Example energy cost for picking up a package

        # Spade message
        msg = Message(to="HubH@localhost")
        msg.set_metadata("performative", "inform")
        drone_id = self.jid
        package_id = self.current_package['name']
        msg.body = f"Drone {drone_id} picked package {package_id} and left the hub"
        print(f"Sent message: {msg.body}")
        await asyncio.sleep(2)

    # Function needed to make the drones move
    async def move_to_location(self, hub, destination):
        # Spade message
        msg = Message(to="HubH@localhost")
        msg.set_metadata("performative", "inform")
        drone_id = self.jid
        package_id = self.current_package['name']
        msg.body = f"Drone {drone_id} is delivering the package {package_id} to the position {destination}"
        print(f"Sent message: {msg.body}")
        await asyncio.sleep(2)

        path, total_distance = await self.calculate_path(destination)
        self.current_path = path
        previous = hub
        for step in path:
            if step == None:
                continue
            self.position = step
            self.update_energy(-1)  # Example energy cost for moving
            self.environment.add_drones(step, previous, self.drone_name)
            self.environment.print_grid()
            print("\n")
            previous = step # keeps the previous step to help make the visual drone movement
            await asyncio.sleep(1 / self.speed) # speed of each movement

    # Function responsible for the package deliveries
    async def deliver_package(self, package, destination):
        # Spade message
        await asyncio.sleep(2)
        msg = Message(to="HubH@localhost")
        msg.set_metadata("performative", "inform")
        drone_id = self.jid
        package_id = self.current_package['name']
        msg.body = f"Drone {drone_id} has successfully delivered the package {package_id}"
        print(f"Sent message: {msg.body}")
        await asyncio.sleep(2)

        # Logic to deliver a package
        path, distance = await self.calculate_path(destination)
        package['status'] = "delivered"
        newname = package['name'].upper()
        self.environment.add_destination(newname, destination)
        self.current_package = None
        self.update_energy(-5)  # Example energy cost for delivering a package
        self.update_energy(-distance)
        await asyncio.sleep(3)

    # Makes possible the drone movement from the destination back to the hub
    async def return_to_hub(self, hub, destination):
        # Spade message
        await asyncio.sleep(2)
        msg = Message(to="HubH@localhost")
        msg.set_metadata("performative", "inform")
        drone_id = self.jid
        msg.body = f"Drone {drone_id} is returning to hubH"
        # await self.send(msg)
        print(f"Sent message: {msg.body}")
        await asyncio.sleep(2)

        previous = destination
        path = self.current_path[::-1]  # Reverses the path from hub to destination
        # Move to each position in the path
        for step in path:
            if step == None:
                continue
            self.update_energy(-1)  # Energy cost example
            self.environment.add_drones(step, previous, self.drone_name)
            self.environment.print_grid()
            print("\n")
            previous = step # tracks the previous step (same as move_to_location())
            await asyncio.sleep(1 / self.speed)

        # Spade messages
        await asyncio.sleep(2)
        msg = Message(to="HubH@localhost")
        msg.set_metadata("performative", "inform")
        drone_id = self.jid
        msg.body = f"Drone {drone_id} returned to HubH"
        # await self.send(msg)
        print(f"Sent message: {msg.body}")
        await asyncio.sleep(2)

        msg = Message(to="HubH@localhost")
        msg.set_metadata("performative", "inform")
        msg.body = f"The next drone can leave the hub"
        await asyncio.sleep(2)

        # Outputting some delivery stats
        wasted = self.energy_capacity - self.energy
        time = ((self.energy_capacity - self.energy + 10) / 2) / self.speed
        print(f"Energy wasted: {wasted}")
        print(f"Drone {drone_id} energy left: ", self.energy)
        print(f"Delivery time: {round(time, 3)} seconds")

        await asyncio.sleep(2)

    # Helps the drones to stop after delivering all packages
    async def stop(self):
        msg = Message(to="HubH@localhost")
        msg.set_metadata("performative", "inform")
        drone_id = self.jid
        msg.body = f"Drone {drone_id} stopped!"
        # await self.send(msg)
        print(f"Sent message: {msg.body}")

    # Recharge the drones whose energy isn't enough (< 25 + next_path_cost) for the next delivery
    async def recharge(self):
        # Spade message
        msg = Message(to="HubH@localhost")
        msg.set_metadata("performative", "inform")
        drone_id = self.jid
        msg.body = f"Drone {drone_id} recharging..."
        print(f"Sent message: {msg.body}")
        # Recharges 5 energy each second until it is complete
        while self.energy < self.energy_capacity:
            self.energy += 5
            await asyncio.sleep(1)

    # Function that updates the energy
    def update_energy(self, amount):
        self.energy += amount

    # Helps to calculate the path and the distance of it, using the plan_path() in environment.py
    async def calculate_path(self, destination):
        result = self.environment.plan_path(self.position, destination)
        if result is None:
            print(f"Warning: No path found from {self.position} to {destination}.")
            return [], 0  # Return an empty path and zero distance

        path, total_distance = result
        return path, total_distance


# Sorts the drones by its capacity
def sort_drones_by_capacity(drones):
    return sorted(drones, key=lambda drone: drone.max_weight, reverse=True)


# Sorts the packages by its weight
def sort_packages_by_weight(packages):
    return sorted(packages, key=lambda package: package['weight'], reverse=True)
