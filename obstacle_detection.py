from lib import constants as c
from math import cos, radians


class ObstacleDetection(object):
    def __init__(self):
        self.__minimal_distance = c.lidar_distances["maximum distance"]
        self.__free_space_right = False
        self.__free_space_left = False

    def __check_blind_sides(self, bsd, limit_distances):
        cb_distances = []
        if bsd is not None:
            for i in range(len(limit_distances)):
                if bsd[i] <= limit_distances[i]:
                    cb_distances.append(bsd[i])
                else:
                    pass

        return cb_distances

    def check_obstacles(self, front_distances, limit_distances_right, limit_distances_left, bsd_right, bsd_left):
        cbd_left = self.__check_blind_sides(bsd_left, limit_distances_left)
        cbd_right = self.__check_blind_sides(bsd_right, limit_distances_right)

        # print("CBD Left: " + str(cbd_left))
        # print("BSD Left: " + str(bsd_left))
        # print("Limit Left: " + str(limit_distances_left))

        compare_values = []
        compare_values.extend(front_distances)
        compare_values.extend(cbd_left)
        compare_values.extend(cbd_right)

        self.__minimal_distance = min(filter(lambda x: x is not None, compare_values))

    @property
    def get_min_distance(self):
        return self.__minimal_distance

    # Turning Zone
    def __calculate_turning_zone_limits(self, angles, index_start, index_mid, index_stop):
        safety_gap = c.picar["safety gap"]
        half_width = (c.picar["tire-tire width"]+c.picar["offset"])/2
        turning_radius = self.__minimal_distance - safety_gap - half_width
        bw2front = 272
        turning_length = turning_radius + bw2front
        limit_distances_top = []
        limit_distances_bottom = []

        # Right Turning Side
        if angles[0] == 90:
            for i in range(index_start, index_mid):
                limit_distances_bottom.append(turning_length/cos(radians(90-angles[i])))
            for i in range(index_mid, index_stop):
                limit_distances_top.append(self.__minimal_distance/cos(radians(abs(angles[i]))))

            if limit_distances_top and limit_distances_bottom is not None:
                return limit_distances_top, limit_distances_bottom

        # Left Turning Side
        elif angles[0] == -0:
            for i in range(index_start, index_mid):
                limit_distances_top.append(self.__minimal_distance / cos(radians(abs(angles[i]))))

            for i in range(index_mid, index_stop):
                limit_distances_bottom.append(turning_length / cos(radians(90 - abs(angles[i]))))

            if limit_distances_top and limit_distances_bottom is not None:
                return limit_distances_top, limit_distances_bottom

    def __calculate_safety_distances(self, angles_right, angles_left):
        safety_distances_right = []
        safety_distances_left = []

        ldr_top, ldr_bottom = self.__calculate_turning_zone_limits(angles=angles_right, index_start=10, index_mid=30, index_stop=90)
        ldl_top, ldl_bottom = self.__calculate_turning_zone_limits(angles=angles_left, index_start=1, index_mid=60, index_stop=81)

        safety_distances_right.extend(ldr_bottom)
        safety_distances_right.extend(ldr_top)

        safety_distances_left.extend(ldl_top)
        safety_distances_left.extend(ldl_bottom)

        if safety_distances_right and safety_distances_left is not None:
            return safety_distances_right, safety_distances_left

    def __check_free_turning_space(self, distances, safety_distances):
        turning_zone_distances = []

        for i in range(len(safety_distances)):
            if distances[i] <= safety_distances[i]:
                turning_zone_distances.append(distances[i])
                # print("Turning: " + str(turning_zone_distances))

        if turning_zone_distances:
            free_space = False
            return free_space
        elif not turning_zone_distances:
            free_space = True
            return free_space

    def __check_closest_object(self, distances_right, distances_left):
        close_right = []
        close_left = []

        for i in range(10, 30):
            close_right.append(distances_right)
        closest_distance_right = min(x for x in close_right)

        for i in range(60, 80):
            close_left.append(distances_left)
        closest_distance_left = min(x for x in close_left)

        if closest_distance_right < closest_distance_left:
            free_space_right = False
            free_space_left = True
        elif closest_distance_right > closest_distance_left:
            free_space_right = True
            free_space_left = False
        else:
            free_space_right = True
            free_space_left = True

        return free_space_right, free_space_left

    def check_turning_zone(self, distances_right, angles_right, distances_left, angles_left):
        print("Minimal Distances: " + str(self.__minimal_distance))
        if c.lidar_distances["turning min"] <= self.__minimal_distance < c.lidar_distances["turning max"]:
            safety_distances_right, safety_distances_left = self.__calculate_safety_distances(angles_right, angles_left)
            free_space_right = self.__check_free_turning_space(distances_right, safety_distances_right)
            free_space_left = self.__check_free_turning_space(distances_left, safety_distances_left)

            print("Free Space Right 1: " + str(free_space_right))
            print("Free Space Left 1: " + str(free_space_left))

            if free_space_right and free_space_left is True:
                free_space_right, free_space_left = self.__check_closest_object(distances_right, distances_left)

            '''
            print("Safety Right: " + str(safety_distances_right))
            print("Safety Left: " + str(safety_distances_left))

            print("Distance Right: " + str(distances_right))
            print("Distance Left: " + str(distances_left))
            '''
            print("Free Space Right 2: " + str(free_space_right))
            print("Free Space Left 2: " + str(free_space_left))

            self.__free_space_right = free_space_right
            self.__free_space_left = free_space_left

    @property
    def right_free(self):
        return self.__free_space_right

    @property
    def left_free(self):
        return self.__free_space_left

