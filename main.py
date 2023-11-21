from environment import Environment
from drones2 import DroneAgent, sort_drones_by_capacity, sort_packages_by_weight
from hubs import HubAgent
import spade
import random
import asyncio


async def main():
    # Creating environment
    env = Environment(width=40, height=40, tile_size=1)
    numpacks = 18
    numdrones = 9
    x = int(input("Choose the Hub's coord x:"))
    y = int(input("Choose the Hub's coord y:"))
    hubH = (x, y)
    env.add_hub(position=hubH, name="X")

    # Creating obstacles
    for _ in range(70):
        position = env.get_random_empty_position()
        env.add_obstacle(position[0], position[1])

    # Creating drones and hub agents
    # The speed of the drones can be changed if we want to run the program faster

    drones = []

    drone1 = DroneAgent("Drone1@localhost", "password", hubH, "1", 40, 3.5, 150, 60, env)
    await drone1.start()
    drones.append(drone1)

    drone2 = DroneAgent("Drone2@localhost", "password", hubH, "2", 40, 2.2, 140, 40, env)
    await drone2.start()
    drones.append(drone2)

    drone3 = DroneAgent("Drone3@localhost", "password", hubH, "3", 20, 4.7, 180, 30, env)
    await drone3.start()
    drones.append(drone3)

    drone4 = DroneAgent("Drone4@localhost", "password", hubH, "4", 40, 3.1, 150, 80, env)
    await drone4.start()
    drones.append(drone4)

    drone5 = DroneAgent("Drone5@localhost", "password", hubH, "5", 20, 3.9, 190, 50, env)
    await drone5.start()
    drones.append(drone5)

    drone6 = DroneAgent("Drone6@localhost", "password", hubH, "6", 20, 2.4, 200, 45, env)
    await drone6.start()
    drones.append(drone6)

    drone7 = DroneAgent("Drone7@localhost", "password", hubH, "7", 40, 4.8, 170, 35, env)
    await drone7.start()
    drones.append(drone7)

    drone8 = DroneAgent("Drone8@localhost", "password", hubH, "8", 40, 4.1, 140, 60, env)
    await drone8.start()
    drones.append(drone8)

    drone9 = DroneAgent("Drone9@localhost", "password", hubH, "9", 10, 2.9, 190, 60, env)
    await drone9.start()
    drones.append(drone9)

    hub = HubAgent(jid=f"HubH@localhost", password="password", hub_name="hubH",
                   position=hubH, packages=[], num_drones=numdrones)
    await hub.start()

    for drone in drones:
        await hub.assign_drone(drone)

    # Sorting drones by capacity and packages by weight

    # Creating packages

    test_package1 = {'name': 'a', 'hub_position': hubH, 'weight': 5.7, 'destination': (31, 38), 'status': 'ready'}
    env.add_destination(test_package1['name'], test_package1['destination'])
    test_package2 = {'name': 'b', 'hub_position': hubH, 'weight': 2.3, 'destination': (11, 29), 'status': 'ready'}
    env.add_destination(test_package2['name'], test_package2['destination'])
    test_package3 = {'name': 'c', 'hub_position': hubH, 'weight': 5.1, 'destination': (17, 4), 'status': 'ready'}
    env.add_destination(test_package3['name'], test_package3['destination'])
    test_package4 = {'name': 'd', 'hub_position': hubH, 'weight': 5.9, 'destination': (24, 6), 'status': 'ready'}
    env.add_destination(test_package4['name'], test_package4['destination'])
    test_package5 = {'name': 'e', 'hub_position': hubH, 'weight': 9.1, 'destination': (33, 31), 'status': 'ready'}
    env.add_destination(test_package5['name'], test_package5['destination'])
    test_package6 = {'name': 'f', 'hub_position': hubH, 'weight': 1.7, 'destination': (22, 22), 'status': 'ready'}
    env.add_destination(test_package6['name'], test_package6['destination'])
    test_package7 = {'name': 'g', 'hub_position': hubH, 'weight': 6.6, 'destination': (9, 26), 'status': 'ready'}
    env.add_destination(test_package7['name'], test_package7['destination'])
    test_package8 = {'name': 'h', 'hub_position': hubH, 'weight': 3.1, 'destination': (14, 37), 'status': 'ready'}
    env.add_destination(test_package8['name'], test_package8['destination'])
    test_package9 = {'name': 'i', 'hub_position': hubH, 'weight': 4.1, 'destination': (15, 1), 'status': 'ready'}
    env.add_destination(test_package9['name'], test_package9['destination'])
    test_package10 = {'name': 'j', 'hub_position': hubH, 'weight': 9.5, 'destination': (23, 17), 'status': 'ready'}
    env.add_destination(test_package10['name'], test_package10['destination'])
    test_package11 = {'name': 'k', 'hub_position': hubH, 'weight': 8.8, 'destination': (15, 2), 'status': 'ready'}
    env.add_destination(test_package11['name'], test_package11['destination'])
    test_package12 = {'name': 'l', 'hub_position': hubH, 'weight': 1.3, 'destination': (16, 12), 'status': 'ready'}
    env.add_destination(test_package12['name'], test_package12['destination'])
    test_package13 = {'name': 'm', 'hub_position': hubH, 'weight': 5.3, 'destination': (31, 11), 'status': 'ready'}
    env.add_destination(test_package13['name'], test_package13['destination'])
    test_package14 = {'name': 'n', 'hub_position': hubH, 'weight': 5.4, 'destination': (14, 4), 'status': 'ready'}
    env.add_destination(test_package14['name'], test_package14['destination'])
    test_package15 = {'name': 'o', 'hub_position': hubH, 'weight': 6.0, 'destination': (36, 28), 'status': 'ready'}
    env.add_destination(test_package15['name'], test_package15['destination'])
    test_package16 = {'name': 'p', 'hub_position': hubH, 'weight': 2.8, 'destination': (2, 5), 'status': 'ready'}
    env.add_destination(test_package16['name'], test_package16['destination'])
    test_package17 = {'name': 'q', 'hub_position': hubH, 'weight': 7.1, 'destination': (5, 11), 'status': 'ready'}
    env.add_destination(test_package17['name'], test_package17['destination'])
    test_package18 = {'name': 'r', 'hub_position': hubH, 'weight': 7.3, 'destination': (18, 19), 'status': 'ready'}
    env.add_destination(test_package18['name'], test_package18['destination'])

    # The drones and packages are being sorted, but we couldn't allocate
    # the packages to the respective drones

    sorteddrones = sort_drones_by_capacity(drones)
    print([drone.name for drone in sorteddrones])
    # sortedpackages = sort_packages_by_weight(env.packages)
    # print(sortedpackages)
    # goals = [package['destination'] for package in sortedpackages]
    # env.allocate_packages_to_drones(drones, env.packages, hubH, goals)

    # Assigning the packages to the drones and making
    # them do all the necessary movements

    await drone1.pick_up_package(test_package1)
    await drone1.move_to_location(hubH, test_package1['destination'])
    await drone1.deliver_package(test_package1, test_package1['destination'])
    await drone1.return_to_hub(hubH, test_package1['destination'])

    await drone2.pick_up_package(test_package2)
    await drone2.move_to_location(hubH, test_package2['destination'])
    await drone2.deliver_package(test_package2, test_package2['destination'])
    await drone2.return_to_hub(hubH, test_package2['destination'])

    await drone3.pick_up_package(test_package3)
    await drone3.move_to_location(hubH, test_package3['destination'])
    await drone3.deliver_package(test_package3, test_package3['destination'])
    await drone3.return_to_hub(hubH, test_package3['destination'])

    await drone4.pick_up_package(test_package4)
    await drone4.move_to_location(hubH, test_package4['destination'])
    await drone4.deliver_package(test_package4, test_package4['destination'])
    await drone4.return_to_hub(hubH, test_package4['destination'])

    await drone5.pick_up_package(test_package5)
    await drone5.move_to_location(hubH, test_package5['destination'])
    await drone5.deliver_package(test_package5, test_package5['destination'])
    await drone5.return_to_hub(hubH, test_package5['destination'])

    await drone6.pick_up_package(test_package6)
    await drone6.move_to_location(hubH, test_package6['destination'])
    await drone6.deliver_package(test_package6, test_package6['destination'])
    await drone6.return_to_hub(hubH, test_package6['destination'])

    await drone7.pick_up_package(test_package7)
    await drone7.move_to_location(hubH, test_package7['destination'])
    await drone7.deliver_package(test_package7, test_package7['destination'])
    await drone7.return_to_hub(hubH, test_package7['destination'])

    await drone8.pick_up_package(test_package8)
    await drone8.move_to_location(hubH, test_package8['destination'])
    await drone8.deliver_package(test_package8, test_package8['destination'])
    await drone8.return_to_hub(hubH, test_package8['destination'])

    await drone9.pick_up_package(test_package9)
    await drone9.move_to_location(hubH, test_package9['destination'])
    await drone9.deliver_package(test_package9, test_package9['destination'])
    await drone9.return_to_hub(hubH, test_package9['destination'])

    await drone1.pick_up_package(test_package10)
    await drone1.move_to_location(hubH, test_package10['destination'])
    await drone1.deliver_package(test_package10, test_package10['destination'])
    await drone1.return_to_hub(hubH, test_package10['destination'])

    await drone2.pick_up_package(test_package11)
    await drone2.move_to_location(hubH, test_package11['destination'])
    await drone2.deliver_package(test_package11, test_package11['destination'])
    await drone2.return_to_hub(hubH, test_package11['destination'])

    await drone3.pick_up_package(test_package12)
    await drone3.move_to_location(hubH, test_package12['destination'])
    await drone3.deliver_package(test_package12, test_package12['destination'])
    await drone3.return_to_hub(hubH, test_package12['destination'])

    await drone4.pick_up_package(test_package13)
    await drone4.move_to_location(hubH, test_package13['destination'])
    await drone4.deliver_package(test_package13, test_package13['destination'])
    await drone4.return_to_hub(hubH, test_package13['destination'])

    await drone5.pick_up_package(test_package14)
    await drone5.move_to_location(hubH, test_package14['destination'])
    await drone5.deliver_package(test_package14, test_package14['destination'])
    await drone5.return_to_hub(hubH, test_package14['destination'])

    await drone6.pick_up_package(test_package15)
    await drone6.move_to_location(hubH, test_package15['destination'])
    await drone6.deliver_package(test_package15, test_package15['destination'])
    await drone6.return_to_hub(hubH, test_package15['destination'])

    await drone7.pick_up_package(test_package16)
    await drone7.move_to_location(hubH, test_package16['destination'])
    await drone7.deliver_package(test_package16, test_package16['destination'])
    await drone7.return_to_hub(hubH, test_package16['destination'])

    await drone8.pick_up_package(test_package17)
    await drone8.move_to_location(hubH, test_package17['destination'])
    await drone8.deliver_package(test_package17, test_package17['destination'])
    await drone8.return_to_hub(hubH, test_package17['destination'])

    await drone9.pick_up_package(test_package18)
    await drone9.move_to_location(hubH, test_package18['destination'])
    await drone9.deliver_package(test_package18, test_package18['destination'])
    await drone9.return_to_hub(hubH, test_package18['destination'])

    # Stopping the drones

    await drone1.stop()
    await drone2.stop()
    await drone3.stop()
    await drone4.stop()
    await drone5.stop()
    await drone6.stop()
    await drone7.stop()
    await drone8.stop()
    await drone9.stop()

    # Printing the packages that are on the hub (need to be [])
    print("Remaining packages: ", env.packages)


if __name__ == "__main__":
    asyncio.run(main())
