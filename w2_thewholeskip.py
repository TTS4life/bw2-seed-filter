#!/usr/bin/python3

import numpy as np
# import matplotlib.pyplot as plt
from numba_pokemon_prngs.lcrng import BWRNG
import itertools
from numba_pokemon_prngs.sha1 import SHA1
from numba_pokemon_prngs.enums import Language, Game, DSType

from keypresses import keypresses_2, keypresses_3_4, keypresses_lite

test = False
user_year = None
user_month = None
user_day = None    
user_dow = None
user_mac = None
user_keypress = None
sha1 = None
precompute = None
times = []

def compute_times(user_hour, user_min):
    global times
    for i in range(max(user_hour - 5, 0), min(user_hour + 5, 24)):
        for j in range(max(user_min - 10, 0), min(user_min + 10, 60)):
           for k in range(5,7):
                  time1 = (i, j, k)
                  times.append(time1)

ranges = (
    (-5, 5, -5, 5), # default case
    (0, 5, -5, 5), #Right of player
    (-5, 0, -5, 5), #left of player
    (-5, 5, -5, 0), #above player
    (-5, 5, 0, 5) #below player
)

valid_route21_tiles = {                               (4,214), (4,213), (4,212), (4,211), (4,210), (4,209), (4,208), 
                           (5,217), (5,216), (5,215), (5,214), (5,213), (5,212), (5,211), (5,210), (5,209), (5,208),
                  (6,218), (6,217), (6,216), (6,215), (6,214), (6,213),(6,212),                             (6,208),
(7,220), (7,219), (7,218), (7,217),                   (7,214),
(8,220), (8,219), (8,218), (8,217),                   (8, 214),
         (9,219), (9,218),                            (9,214), (9,215),
                                                      (10,214), (10,215),
                            (11,217), (11,216), (11,215), (11,212), (11,211),(11,210),(11,209),(11,208),
(12,220),(12,219),(12,218), (12,217), (12,216), (12,215), (12,212), (12,211),(12,210),(12,209),(12,208) }

valid_seaside_tiles = {(2,28), 
                                          (2,29), (2,30), (2,31),
                                          (3,28), (3,29), (3,30), (3,31),
       (4,23), (4,24),       (4,26), (4,27), (4,28), (4,29), (4,30), (4,31),
                       (9,25), (8,25),
(5,15),(5,16), (5,17), (5,19), (5,20), (5,22), (5,23), (5,24),      (5,26), (5,27), (5,28), (5,29), (5,30), (5,31),
(6,15),(6,16,),(6,17),(6,18),(6,19),(6,20), (6,21), (6,22),  (6,23), (6,24),      (6,26), (6,27), (6,28), (6,29), (6,31), #(6,30) is hidden item, do not include
(7,15),(7,16),(7,17),(7,18),(7,19),(7,20),(7,21), (7,22), (7,29), (7,30), (7,31),
                       (8,25), (8,26), (8,27),
(9,15),(9,16),(9,17),(9,18),(9,19),(9,20), (9,21), (9,22),       (9,25), (9,26), (9,27),          (9,29), (9,30), (9,31),
(10,21), (10,22), (10,23),                        (10,27),        (10, 29), (10, 30), (10, 31),
(11, 17), (11,16), (11,15), (11, 18), (11,21), (11,22),(11,23),(11,24),(11,25), (11,26), (11,27),      (11,29), (11,30), (11,31), (11,32)
}

def rngAdvance(prev):
	next=0x5D588B656C078965 * prev + 0x0000000000269EC3
	return next%0x10000000000000000

def rngRAdvance(prev):
    next = 0xdedcedae9638806d * prev + 0x9b1ae6e9a384e6f9
    return next%0x10000000000000000

table = [[50, 100, 100, 100], [50, 50, 100, 100], [30, 50, 100, 100],[25, 30, 50, 100], [20, 25, 33, 50]]

def advance_table(prng):
    count = 0

    for i in range(5):
        for j in range(4):
            if table[i][j] == 100:
                break

            count += 1
            prng = rngAdvance(prng)
            rand = ((prng >> 32) * 101) >> 32
            if rand <= table[i][j]:
                break

    return prng, count

def initial_frame_bw(prng):
    count = 0

    for i in range(5):
        prng, num = advance_table(prng)
        count += num

    return count

def initial_frame_bw2(prng, memory = False):
    count = 1
    
    for i in range(5):
        prng, num = advance_table(prng)
        count += num

        if i == 0:
            for j in range(2 if memory else 3):
                count += 1
                prng = rngAdvance(prng)

    for i in range(100):
        count += 3

        prng = rngAdvance(prng)
        rand1 = ((prng >> 32) * 15) >> 32

        prng = rngAdvance(prng)
        rand2 = ((prng >> 32) * 15) >> 32

        prng = rngAdvance(prng)
        rand3 = ((prng >> 32) * 15) >> 32

        if rand1 != rand2 and rand1 != rand3 and rand2 != rand3:
            break

    return count - 1

#usable_first_skip_tiles = [(47, 35), (47, 36), (48,34), (48, 35), (48, 36),(49,34), (49, 35), (49, 36), (50, 35), (50, 34), (51, 35), (51, 34), (52, 35), (52, 34), (53, 35), (53, 34), (54, 35), (54, 34)]
#usable_second_skip_tiles = [(49, 22), (49, 23), (49, 24), (49, 25), (49, 26), (49, 27),(50, 22), (49, 23), (49, 24), (49, 25), (49, 26), (49, 27)]
#usable_third_skip_tiles = [(56, 15), (54, 15), (55, 12), (55, 14), (56, 13), (54, 13), (56, 17), (56, 19)]
#usable_fourth_skip_tiles = [(46, 4), (45, 5), (47, 5), (46, 6), (45, 7), (46, 7), (46, 8), (45, 9), (47, 9)]

# below are fast tiles
usable_first_skip_tiles = [(4,213), (6,213)]
usable_second_skip_tiles = [ (4,26), #(6,26), (6,24), (6,23), (5,24), (4,23), (5,27)
]
# usable_third_skip_tiles = [(54, 13), (55, 12)]
# usable_fourth_skip_tiles = [(47, 5), (45, 7), (47, 9)]


# these are tiles where a cloud should spawn for a valid skip

usable_first_cloud_tiles = [(5,214)]
usable_second_cloud_tiles = [(4,28), (5,28)]
#usable_third_cloud_tiles = [(53, 13), (53, 14)]

# below is the optimal tile

# valid_chargestone_tiles = {(49, 23), (55, 57), (50, 6), (30, 0), (52, 15), (60, 37), (52, 33), (56, 12), (33, 56), (56, 21), (44, 56), (53, 34), (25, 52), (37, 26), (46, 4), (49, 9), (55, 43), (38, 18), (55, 52), (59, 50), (47, 57), (48, 31), (52, 10), (40, 54), (60, 41), (52, 46), (53, 20), (44, 51), (56, 16), (37, 21), (32, 55), (43, 55), (49, 4), (47, 43), (55, 56), (28, 39), (52, 5), (52, 14), (52, 32), (54, 51), (56, 20), (43, 50), (35, 55), (55, 51), (47, 47), (48, 12), (59, 49), (28, 43), (36, 56), (47, 56), (48, 30), (52, 9), (54, 46), (39, 57), (31, 53), (54, 55), (51, 31), (43, 36), (32, 45), (32, 54), (43, 54), (24, 50), (59, 35), (47, 42), (48, 7), (28, 38), (48, 34), (52, 13), (44, 9), (39, 52), (54, 50), (51, 35), (24, 36), (43, 49), (55, 14), (36, 19), (47, 46), (28, 42), (58, 43), (50, 57), (42, 53), (51, 12), (31, 43), (54, 45), (39, 56), (51, 21), (31, 52), (54, 54), (35, 22), (43, 35), (32, 44), (47, 5), (43, 53), (47, 14), (48, 6), (28, 37), (61, 34), (50, 34), (61, 43), (27, 41), (42, 39), (27, 50), (54, 13), (42, 57), (51, 7), (54, 49), (43, 12), (31, 56), (51, 34), (35, 17), (24, 35), (55, 13), (24, 44), (47, 9), (46, 41), (36, 18), (46, 50), (57, 50), (49, 46), (38, 55), (50, 20), (50, 29), (27, 36), (61, 38), (58, 51), (50, 47), (50, 56), (42, 52), (54, 35), (54, 44), (51, 20), (35, 21), (53, 57), (45, 53), (56, 53), (47, 4), (49, 32), (50, 24), (50, 33), (27, 40), (61, 42), (42, 38), (54, 12), (42, 56), (54, 21), (51, 6), (43, 11), (53, 43), (45, 48), (45, 57), (56, 57), (49, 27), (46, 49), (57, 49), (50, 10), (26, 52), (50, 28), (27, 35), (61, 37), (30, 31), (27, 44), (60, 50), (41, 55), (51, 10), (56, 34), (53, 47), (56, 43), (46, 8), (53, 56), (45, 52), (56, 52), (49, 13), (37, 57), (49, 22), (46, 35), (57, 35), (49, 31), (50, 5), (50, 14), (50, 23), (50, 32), (27, 39), (60, 36), (53, 15), (33, 55), (44, 55), (25, 51), (45, 47), (49, 8), (34, 56), (45, 56), (56, 56), (49, 26), (49, 35), (50, 9), (26, 51), (42, 14), (48, 57), (40, 53), (60, 40), (60, 49), (52, 45), (41, 54), (44, 50), (56, 15), (37, 20), (53, 46), (46, 7), (45, 51), (56, 51), (49, 12), (37, 56), (49, 21), (55, 55), (49, 30), (50, 4), (42, 9), (40, 57), (60, 35), (52, 31), (44, 36), (53, 14), (44, 54), (56, 19), (25, 50), (49, 7), (55, 50), (49, 25), (36, 55), (48, 29), (48, 47), (52, 8), (48, 56), (40, 52), (60, 39), (52, 35), (52, 44), (25, 36), (44, 49), (45, 14), (56, 14), (51, 57), (37, 19), (32, 53), (46, 6), (59, 34), (59, 43), (55, 54), (48, 33), (52, 12), (44, 8), (40, 56), (52, 21), (60, 34), (44, 35), (53, 13), (45, 9), (56, 18), (43, 48), (43, 57), (55, 49), (47, 45), (48, 10), (28, 41), (48, 46), (52, 7), (39, 55), (54, 53), (25, 35), (56, 13), (51, 47), (32, 43), (51, 56), (32, 52), (43, 52), (36, 22), (55, 35), (48, 5), (55, 53), (28, 36), (48, 14), (48, 32), (52, 20), (31, 55), (54, 57), (51, 33), (43, 47), (55, 12), (47, 8), (32, 56), (55, 21), (43, 56), (24, 52), (36, 17), (48, 9), (28, 40), (58, 50), (50, 46), (52, 6), (54, 34), (54, 43), (39, 54), (54, 52), (35, 20), (51, 46), (43, 51), (35, 56), (36, 21), (55, 34), (48, 4), (28, 35), (48, 13), (28, 44), (61, 41), (40, 18), (42, 37), (42, 55), (54, 20), (51, 5), (51, 14), (54, 47), (31, 45), (43, 10), (31, 54), (54, 56), (51, 32), (47, 7), (55, 20), (24, 51), (46, 48), (46, 57), (48, 8), (50, 27), (61, 36), (58, 49), (27, 43), (42, 41), (27, 52), (54, 15), (51, 9), (39, 53), (35, 19), (55, 15), (57, 34), (57, 43), (36, 20), (50, 13), (38, 57), (50, 22), (49, 57), (58, 35), (50, 31), (27, 38), (61, 40), (42, 36), (42, 54), (51, 4), (51, 13), (31, 44), (43, 9), (34, 55), (45, 55), (56, 55), (47, 6), (49, 34), (46, 47), (50, 8), (46, 56), (26, 50), (50, 26), (50, 35), (61, 35), (27, 42), (42, 40), (27, 51), (54, 14), (41, 53), (51, 8), (43, 13), (53, 45), (35, 18), (45, 50), (56, 50), (37, 55), (49, 20), (49, 29), (26, 36), (57, 51), (49, 47), (50, 12), (42, 8), (38, 56), (50, 21), (49, 56), (58, 34), (50, 30), (42, 26), (27, 37), (61, 39), (42, 35), (60, 43), (41, 57), (52, 57), (44, 53), (49, 6), (45, 54), (56, 54), (49, 24), (49, 33), (50, 7), (50, 25), (60, 38), (52, 34), (52, 43), (41, 52), (44, 48), (25, 44), (44, 57), (53, 35), (37, 18), (53, 44), (45, 49), (46, 14), (56, 49), (49, 10), (59, 51), (49, 28), (26, 35), (26, 44), (40, 55), (30, 32), (60, 42), (60, 51), (52, 47), (53, 12), (45, 8), (41, 56), (53, 21), (52, 56), (44, 52), (56, 17), (37, 22), (45, 35), (56, 35), (46, 9), (49, 5), (49, 14)}

def cloud_location_finder(rngstate, coords, tileset):
    global test

    rng = BWRNG(np.uint64(rngstate))
    player_x = coords[0]
    player_y = coords[1]
    #player_x, player_y = 46, 6
    if rng.next_rand(1000) < 100:
        # TODO: when does default case actually happen
        quadrant = rng.next_rand(4) + 1

        if test is True:
            print("quadrant ", quadrant, ["Right", "Left", "Up", "Down"][quadrant - 1])

        x_min, x_max, y_min, y_max = ranges[quadrant]


        x_min_in_chunk = max((player_x % 32) + x_min, 0)
        x_max_in_chunk = min((player_x % 32) + x_max, 31)
        y_min_in_chunk = max((player_y % 32) + y_min, 0)
        y_max_in_chunk = min((player_y % 32) + y_max, 31)

        x_min = x_min_in_chunk + player_x - (player_x % 32)
        x_max = x_max_in_chunk + player_x - (player_x % 32)
        y_min = y_min_in_chunk + player_y - (player_y % 32)
        y_max = y_max_in_chunk + player_y - (player_y % 32)

        if test is True:
            print(x_min, y_min, x_max, y_max)

        possible = []
        possible_x = []
        possible_y = []
        for dust_y in range(y_min, y_max + 1):
            for dust_x in range(x_min, x_max + 1):
                if (dust_x, dust_y) in tileset:
                    possible.append((dust_x, dust_y))
                    possible_x.append(dust_x)
                    possible_y.append(dust_y)
                    
        rand_tile = rng.next_rand(len(possible))
        dust_cloud_x, dust_cloud_y = possible[rand_tile]
    else:
        # print("no valid clouds")
        return "No dust cloud"
    if test is True:
        print("cloud spawns at ", (dust_cloud_x, dust_cloud_y), " from coords ", coords, " rand tile ", rand_tile, " possible ", possible, len(possible)
              )
    
    return ((dust_cloud_x, dust_cloud_y), quadrant)

print()

def generate_seed(
        sha1: SHA1,
        button: np.uint32,
        timer0: np.uint32,
        vcount: np.uint32,
        date: tuple[np.uint16],
        time: tuple[np.uint8],
    ) -> int:
        # not setting button/timer0/date/time causes undefined behaviour as the data array is empty
        # and these values would always otherwise be present
        sha1.set_button(button)
        sha1.set_timer0(timer0, vcount)
        sha1.set_date(*date)
        sha1.set_time(*time)
        return sha1.hash_seed(sha1.precompute())



# Find all the good clouds on a seed up to PID Frame 500 (starts from initial frame)
def multi_cloud(seed):
    success = 0
    clouds = []
    cloud_states = []
    first_skip_indices = []
    second_skip_indices = []
    third_skip_indices = []
    fourth_skip_indices = []
    for i in range(500):
        seed = rngAdvance(seed)
        #print(hex(seed))
        temp = seed
        if (((temp >> 32) * 1000) >> 32) < 100:
            success += 1
            clouds.append(i)
            prev = rngRAdvance(temp)
            # print("found cloud at", i, prev)
            pair = [i, prev]
            cloud_states.append(pair)

            # [ [ All cloud frames ], [], [], ... [ cloud frame, frame seed ] ]
    return [clouds, first_skip_indices, second_skip_indices, third_skip_indices, fourth_skip_indices, cloud_states]

def seed_frame(seed):
    return seed, initial_frame_bw(seed)


#[[frame, rng value of frame], ..., initial frame of seed]
def skip_checker(states_array, frame):
    global test

    first= 0 #flag if we have a valid skip
    second = 0
    one = [] #clouds of valid skip
    two = []
    extra_clouds = [] # for testing, see extra clouds in a seed
    for states in states_array:
        state_index = states[0] # RNG Frame of cloud
        
        if test is True:
            print("======")
            print (state_index)
        
        
        if state_index < 235 and state_index > (frame + 160): #and ((state_index - frame) % 2 == 0 --remove parity check for now
            for first_coords in usable_first_skip_tiles: # reasonable tiles to step on to spawn cloud
                comparison_1, quadrant = cloud_location_finder(states[1], first_coords, valid_route21_tiles)
                if comparison_1 != "No dust cloud" and (comparison_1 in usable_first_cloud_tiles):
                    # print("Frame ", str(state_index), " has a first skip ", first_coords, comparison_1, quadrant)
                    first = 1
                    pair_one = (state_index, first_coords)
                    one.append(pair_one)
                    continue


        if state_index < 440 and state_index > (frame + 260):    #450 - 260
            for second_coords in usable_second_skip_tiles:
                comp_2, quadrant = cloud_location_finder(states[1], second_coords, valid_seaside_tiles)
                if(comp_2 != "No dust cloud" and (comp_2 in usable_second_cloud_tiles)):
                    # print("Frame ", str(state_index), " has a second skip ", second_coords, comp_2, quadrant)
                    second = 1
                    two.append((state_index, second_coords))
                    continue
                # else: 
                    # print("frame ", state_index, " spawn cloud ", comp_2, " from tile " , second_coords)
                

        
    comparison = [first, second]

    if comparison == [1,1]:
        if(len(one) > 1 and len(two) > 1):
            return True, one, two
    
    return False, [], []




keypress_fake = [[0xdf290000, "custom"]]

def illegal_keypresses(keypresses):
    return ( 'Up' in keypresses and 'Down' in keypresses ) or ( 'Left' in keypresses and 'Right' in keypresses )

def wholeskip():
    global sha1
 
    file = open("result.txt", "w")

    
    if user_keypress == 1:
        key_presses = keypresses_3_4
    else:
        key_presses = keypresses_2


    for presses in key_presses:

        if illegal_keypresses(presses[1]):
            continue

        for time in times:
            sha1.set_button(presses[0])
            sha1.set_time(*time)
            seed = sha1.hash_seed(precompute)

            ret = multi_cloud(seed)
            cloud_states = ret[5] #[[frame, rng value of frame], ...]
            init = initial_frame_bw(seed)

            valid_skip, first, second = skip_checker(cloud_states, init)

            if valid_skip is True:
                print(time, hex(seed), presses[1], "first ", first, " second ", second)

                output = f"{time[0]}:{time[1]}:{time[2]}, {hex(seed)} {presses[1]} first {first}, second {second}\n"
                file.write(output)

    file.close()

def main():
    global user_year, user_month, user_day, user_dow, user_mac, user_keypress, sha1, precompute
    user_year= int(input("Enter Year: "))
    user_month= int(input("Enter Month: "))
    user_day= int(input("Enter Day: "))
    user_dow = int(input("Enter day of week (Monday = 1, Tuesday = 2, etc): "))
    user_mac = int(input("Enter MAC Address in decimal (convert from hex to decimal)"), 16)
    user_keypress = int(input("Enter keypress choice. Enter 0 for 0-2 keypresses, enter 1 for 3-4 keypresses"))
    user_hour = int(input("Enter hour you are at near skip"))
    user_min = int(input("enter minute near skip"))

    print("initializing...")
    print("computing times...")
    compute_times(user_hour, user_min)

    print("generating RNG...")
    sha1 = SHA1(version = Game.WHITE2, language = Language.ENGLISH, ds_type=DSType.DS, mac = user_mac, soft_reset=False, v_frame= 8, gx_state=6)
    timer0 = 0x10F4
    sha1.set_timer0(timer0, 0x82)
    date = (user_year, user_month, user_day, user_dow)
    sha1.set_date(*date)
    precompute = sha1.precompute()

    print("Searching...")
    wholeskip()
    
def test_multicloud():
    clouds = multi_cloud(0x1111111111111111)
    print(clouds)


def test():
    global test
    test = True
    seed =  0x328a55b4d00e86b1
    ret = multi_cloud(seed)
    cloud_states = ret[5]
    init = initial_frame_bw2(seed)
    print("Initial frame:", init)
    valid_skip, one, two = skip_checker(cloud_states, init)
    print(hex(seed), one, two)


if __name__ == '__main__':
    test()

