from lidar import Lidar
from region_distribution import RegionDistribution
from obstacle_detection import ObstacleDetection
from control_unit import ControlUnit
from motor import Motor
from time import sleep
import os
from lib import constants as c
import readchar
import threading


lidar = Lidar(c.lidar["id Vendor"], c.lidar["id Product"])
lidar.connect()
regions = RegionDistribution()
obstacles = ObstacleDetection()
control_unit = ControlUnit()
motor = Motor()
motor.start()


def get_ch():
    ch = readchar.readchar()
    return ch


def control_lidar_aut_mode():
    os.system('clear')
    time_delay = lidar.scan()
    regions.generate_regions(lidar.get_distances, lidar.get_angles)

    obstacles.check_obstacles(regions.front_distances, regions.limits_right, regions.limits_left,
                              regions.blind_right, regions.blind_left)
    obstacles.check_turning_zone(regions.get_distances_right, regions.get_angles_right,
                                 regions.get_distances_left, regions.get_angles_left)

    control_unit.set_minimal_distance(obstacles.get_min_distance)

    return time_delay


def control_lidar_man_mode(stop):
    while True:
        time_delay = control_lidar_aut_mode()
        control_unit.calculate_max_manual_speed()
        motor.set_max_motor_speed(control_unit.max_speed)
        print("Max: " + str(control_unit.max_speed))
        motor.control_max_speed()
        sleep(time_delay)
        if stop():
            print("stopping")
            break


def run_autonomous_mode():
    try:
        while True:
            time_delay = control_lidar_aut_mode()
            control_unit.set_free_space(obstacles.right_free, obstacles.left_free)
            control_unit.calculate_autonomous_speed()
            motor.set_motor_speed(control_unit.speed)

            if not control_unit.turn:
                motor.drive_autonomous_forward()
            elif control_unit.turn:
                motor.stop()
                sleep(0.5)
                control_unit.calculate_autonomous_turning()
                motor.set_motor_speed(control_unit.speed)
                motor.set_turning_angle(control_unit.turning_angle)
                motor.set_turning_time(control_unit.turning_time)
                motor.turn_autonomous()

            sleep(time_delay)

    except KeyboardInterrupt:
        motor.slow_down()


def run_manual_mode():
    kill_thread = False
    lidar_thread = threading.Thread(target=control_lidar_man_mode, args=(lambda: kill_thread,))
    lidar_thread.start()

    key = ""
    while True:
        print("Manual Mode")
        # time_delay = lidar_setup()
        key = ""
        key = get_ch()
        if key != 'x':
            if key == 'w':
                motor.drive_manual_forward()
            elif key == 's':
                motor.drive_manual_reverse()
            elif key == 'a':
                motor.turn_manual_left()
            elif key == 'd':
                motor.turn_manual_right()
            else:
                print("Invalid input")
        else:
            kill_thread = True
            lidar_thread.join()
            motor.slow_down()
            print("Stopped 1")
            break
        # sleep(time_delay)




