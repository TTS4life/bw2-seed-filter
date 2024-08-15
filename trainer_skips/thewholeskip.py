#!/usr/bin/python3

# print("4 Trainer Plasma Skipper: Pokemon Black Version")
# print("Version only supports English Pokemon Black for DS Original/Lite")


# print("\n")

# print("How to interpret result: ")
# print("\n")
# print("[[(96, (48, 34))], [(156, (49, 23)), (170, (49, 23))], [(242, (54, 13))], [(320, (47, 5)), (320, (45, 7)), (356, (45, 7)), (358, (45, 7))]] \n (19, 40, 6) 0x2d87c473533530c2 ['R', 'L', 'X']")

# print("\n")

# print("First four lists state the frame of dust cloud, followed by the map coordinate you need to step on to spawn a plasma skip")

# print("\n")

# print("Below is time in Hour, Minute, Second. Then its the seed, followed by Keypresses. Tool is filtered for 5-7 second only. ")

import numpy as np
import matplotlib.pyplot as plt
from numba_pokemon_prngs.lcrng import BWRNG
import itertools
from numba_pokemon_prngs.sha1 import SHA1
from numba_pokemon_prngs.enums import Language, Game, DSType

from keypresses import *

user_year= None
user_month= None
user_day= None
user_dow = None 
user_mac = None
user_keypress = None
sha1 = None
precompute = None

ranges = (
    (-5, 5, -5, 5), # default case
    (0, 5, -5, 5),  # 
    (-5, 0, -5, 5),
    (-5, 5, -5, 0),
    (-5, 5, 0, 5)
)

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


#for buttons_pressed in itertools.product(*((False, True) for _ in range(4))):
#    for button_pressed in buttons_pressed:
#        if button_pressed:
#            keypress_value = base - value_array
#    print(buttons_pressed)


    


#usable_first_skip_tiles = [(47, 35), (47, 36), (48,34), (48, 35), (48, 36),(49,34), (49, 35), (49, 36), (50, 35), (50, 34), (51, 35), (51, 34), (52, 35), (52, 34), (53, 35), (53, 34), (54, 35), (54, 34)]
#usable_second_skip_tiles = [(49, 22), (49, 23), (49, 24), (49, 25), (49, 26), (49, 27),(50, 22), (49, 23), (49, 24), (49, 25), (49, 26), (49, 27)]
#usable_third_skip_tiles = [(56, 15), (54, 15), (55, 12), (55, 14), (56, 13), (54, 13), (56, 17), (56, 19)]
#usable_fourth_skip_tiles = [(46, 4), (45, 5), (47, 5), (46, 6), (45, 7), (46, 7), (46, 8), (45, 9), (47, 9)]

# below are fast tiles
usable_first_skip_tiles = [(48, 34)]
# usable_first_skip_tiles = [(55, 52), (55,53), (55,51), (54,51), (54,52), (54,53), (56,52),(56,51), (56,53),
                        #    (56,49),
                        #    (56, 50), (55,50), (54,50)]

usable_second_skip_tiles = [(49, 23)]
usable_third_skip_tiles = [(54, 13), (55, 14)]
usable_fifth_skip_tiles = [(45,8), (47,8), (47,6), (47,4), (45,4)]
usable_fourth_skip_tiles = [(43,11), (43,13), (44,14)]


# these are tiles where a cloud should spawn for a valid skip

usable_first_cloud_tiles = [(49, 33), (50, 33), (51, 33)]

usable_second_cloud_tiles = [(50, 21), (51, 21), (52, 21)]
# usable_third_cloud_tiles = [(53, 13), (53, 14)]
usable_third_cloud_tiles = [(53, 14)]
usable_fourth_cloud_tiles = [(44,9)]
usable_fifth_cloud_tiles = [(48, 5), (48, 6), (48, 7), (48, 8)]

# below is the optimal tile



def chargestone_clouds(rngstate, coords):
    valid_tiles = {(49, 23), (55, 57), (50, 6), (30, 0), (52, 15), (60, 37), (52, 33), (56, 12), (33, 56), (56, 21), (44, 56), (53, 34), (25, 52), (37, 26), (46, 4), (49, 9), (55, 43), (38, 18), (55, 52), (59, 50), (47, 57), (48, 31), (52, 10), (40, 54), (60, 41), (52, 46), (53, 20), (44, 51), (56, 16), (37, 21), (32, 55), (43, 55), (49, 4), (47, 43), (55, 56), (28, 39), (52, 5), (52, 14), (52, 32), (54, 51), (56, 20), (43, 50), (35, 55), (55, 51), (47, 47), (48, 12), (59, 49), (28, 43), (36, 56), (47, 56), (48, 30), (52, 9), (54, 46), (39, 57), (31, 53), (54, 55), (51, 31), (43, 36), (32, 45), (32, 54), (43, 54), (24, 50), (59, 35), (47, 42), (48, 7), (28, 38), (48, 34), (52, 13), (44, 9), (39, 52), (54, 50), (51, 35), (24, 36), (43, 49), (55, 14), (36, 19), (47, 46), (28, 42), (58, 43), (50, 57), (42, 53), (51, 12), (31, 43), (54, 45), (39, 56), (51, 21), (31, 52), (54, 54), (35, 22), (43, 35), (32, 44), (47, 5), (43, 53), (47, 14), (48, 6), (28, 37), (61, 34), (50, 34), (61, 43), (27, 41), (42, 39), (27, 50), (54, 13), (42, 57), (51, 7), (54, 49), (43, 12), (31, 56), (51, 34), (35, 17), (24, 35), (55, 13), (24, 44), (47, 9), (46, 41), (36, 18), (46, 50), (57, 50), (49, 46), (38, 55), (50, 20), (50, 29), (27, 36), (61, 38), (58, 51), (50, 47), (50, 56), (42, 52), (54, 35), (54, 44), (51, 20), (35, 21), (53, 57), (45, 53), (56, 53), (47, 4), (49, 32), (50, 24), (50, 33), (27, 40), (61, 42), (42, 38), (54, 12), (42, 56), (54, 21), (51, 6), (43, 11), (53, 43), (45, 48), (45, 57), (56, 57), (49, 27), (46, 49), (57, 49), (50, 10), (26, 52), (50, 28), (27, 35), (61, 37), (30, 31), (27, 44), (60, 50), (41, 55), (51, 10), (56, 34), (53, 47), (56, 43), (46, 8), (53, 56), (45, 52), (56, 52), (49, 13), (37, 57), (49, 22), (46, 35), (57, 35), (49, 31), (50, 5), (50, 14), (50, 23), (50, 32), (27, 39), (60, 36), (53, 15), (33, 55), (44, 55), (25, 51), (45, 47), (49, 8), (34, 56), (45, 56), (56, 56), (49, 26), (49, 35), (50, 9), (26, 51), (42, 14), (48, 57), (40, 53), (60, 40), (60, 49), (52, 45), (41, 54), (44, 50), (56, 15), (37, 20), (53, 46), (46, 7), (45, 51), (56, 51), (49, 12), (37, 56), (49, 21), (55, 55), (49, 30), (50, 4), (42, 9), (40, 57), (60, 35), (52, 31), (44, 36), (53, 14), (44, 54), (56, 19), (25, 50), (49, 7), (55, 50), (49, 25), (36, 55), (48, 29), (48, 47), (52, 8), (48, 56), (40, 52), (60, 39), (52, 35), (52, 44), (25, 36), (44, 49), (45, 14), (56, 14), (51, 57), (37, 19), (32, 53), (46, 6), (59, 34), (59, 43), (55, 54), (48, 33), (52, 12), (44, 8), (40, 56), (52, 21), (60, 34), (44, 35), (53, 13), (45, 9), (56, 18), (43, 48), (43, 57), (55, 49), (47, 45), (48, 10), (28, 41), (48, 46), (52, 7), (39, 55), (54, 53), (25, 35), (56, 13), (51, 47), (32, 43), (51, 56), (32, 52), (43, 52), (36, 22), (55, 35), (48, 5), (55, 53), (28, 36), (48, 14), (48, 32), (52, 20), (31, 55), (54, 57), (51, 33), (43, 47), (55, 12), (47, 8), (32, 56), (55, 21), (43, 56), (24, 52), (36, 17), (48, 9), (28, 40), (58, 50), (50, 46), (52, 6), (54, 34), (54, 43), (39, 54), (54, 52), (35, 20), (51, 46), (43, 51), (35, 56), (36, 21), (55, 34), (48, 4), (28, 35), (48, 13), (28, 44), (61, 41), (40, 18), (42, 37), (42, 55), (54, 20), (51, 5), (51, 14), (54, 47), (31, 45), (43, 10), (31, 54), (54, 56), (51, 32), (47, 7), (55, 20), (24, 51), (46, 48), (46, 57), (48, 8), (50, 27), (61, 36), (58, 49), (27, 43), (42, 41), (27, 52), (54, 15), (51, 9), (39, 53), (35, 19), (55, 15), (57, 34), (57, 43), (36, 20), (50, 13), (38, 57), (50, 22), (49, 57), (58, 35), (50, 31), (27, 38), (61, 40), (42, 36), (42, 54), (51, 4), (51, 13), (31, 44), (43, 9), (34, 55), (45, 55), (56, 55), (47, 6), (49, 34), (46, 47), (50, 8), (46, 56), (26, 50), (50, 26), (50, 35), (61, 35), (27, 42), (42, 40), (27, 51), (54, 14), (41, 53), (51, 8), (43, 13), (53, 45), (35, 18), (45, 50), (56, 50), (37, 55), (49, 20), (49, 29), (26, 36), (57, 51), (49, 47), (50, 12), (42, 8), (38, 56), (50, 21), (49, 56), (58, 34), (50, 30), (42, 26), (27, 37), (61, 39), (42, 35), (60, 43), (41, 57), (52, 57), (44, 53), (49, 6), (45, 54), (56, 54), (49, 24), (49, 33), (50, 7), (50, 25), (60, 38), (52, 34), (52, 43), (41, 52), (44, 48), (25, 44), (44, 57), (53, 35), (37, 18), (53, 44), (45, 49), (46, 14), (56, 49), (49, 10), (59, 51), (49, 28), (26, 35), (26, 44), (40, 55), (30, 32), (60, 42), (60, 51), (52, 47), (53, 12), (45, 8), (41, 56), (53, 21), (52, 56), (44, 52), (56, 17), (37, 22), (45, 35), (56, 35), (46, 9), (49, 5), (49, 14)}
    rng = BWRNG(np.uint64(rngstate))
    player_x = coords[0]
    player_y = coords[1]
    #player_x, player_y = 46, 6
    if rng.next_rand(1000) < 100:
        # TODO: when does default case actually happen
        x_min, x_max, y_min, y_max = ranges[rng.next_rand(4) + 1]

        x_min_in_chunk = max((player_x % 32) + x_min, 0)
        x_max_in_chunk = min((player_x % 32) + x_max, 31)
        y_min_in_chunk = max((player_y % 32) + y_min, 0)
        y_max_in_chunk = min((player_y % 32) + y_max, 31)


        x_min = x_min_in_chunk + player_x - (player_x % 32)
        x_max = x_max_in_chunk + player_x - (player_x % 32)
        y_min = y_min_in_chunk + player_y - (player_y % 32)
        y_max = y_max_in_chunk + player_y - (player_y % 32)


        possible = []
        possible_x = []
        possible_y = []
        for dust_y in range(y_min, y_max + 1):
            for dust_x in range(x_min, x_max + 1):
                if (dust_x, dust_y) in valid_tiles:
                    possible.append((dust_x, dust_y))
                    possible_x.append(dust_x)
                    possible_y.append(dust_y)
        dust_cloud_x, dust_cloud_y = possible[rng.next_rand(len(possible))]
        # print("cloud spawns at ", dust_cloud_x, dust_cloud_y , " from coords ", coords)
    else:
        return "No dust cloud"
    return (dust_cloud_x, dust_cloud_y)

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
            pair = [i, prev]
            cloud_states.append(pair)


    return [clouds, first_skip_indices, second_skip_indices, third_skip_indices, fourth_skip_indices, cloud_states]

def seed_frame(seed):
    return seed, initial_frame_bw(seed)


def skip_checker(states_array, initial_frame):
    first, second, third, fourth, fifth = 0, 0, 0, 0, 0
    one, two, three, four, five = [], [], [], [], []
    for states in states_array:
        state_index = states[0] #RNG frame of cloud

        if state_index < initial_frame + 60 and state_index > initial_frame + 36 and ((state_index - initial_frame ) % 2 == 0):
            for first_coords in usable_first_skip_tiles:
                comparison_1 = chargestone_clouds(states[1], first_coords)
                if comparison_1 != "No dust cloud" and (comparison_1 in usable_first_cloud_tiles):
                    first = 1
                    pair_one = (state_index, first_coords)
                    one.append(pair_one)
                    
        for valid_first in one:
            first_frame = valid_first[0]
            if state_index < first_frame + 80 and  state_index > first_frame + 60 and ((state_index - initial_frame) % 2 == 0):
                for second_coords in usable_second_skip_tiles:
                    comparison_2 = chargestone_clouds(states[1], second_coords)
                    if comparison_2 != "No dust cloud" and (comparison_2 in usable_second_cloud_tiles):
                        second = 1
                        pair_two = (state_index, second_coords)
                        two.append(pair_two)
                        
        for valid_second in two:
            second_frame = valid_second[0]
            if state_index < second_frame + 90 and state_index > second_frame + 70 and ((second_frame - state_index) % 2 == 0):
                for third_coords in usable_third_skip_tiles:
                    comparison_3 = chargestone_clouds(states[1], third_coords)
                    if(comparison_3 != "No dust cloud" and (comparison_3 in usable_third_cloud_tiles)):
                        third = 1
                        three.append((state_index, third_coords))

        for valid_third in three:
            third_frame = valid_third[0]
            if state_index < third_frame + 90 and state_index > third_frame + 55 and ((third_frame - state_index) % 2 == 1):
                for fourth_coords in usable_fourth_skip_tiles:
                    comparison_4 = chargestone_clouds(states[1], fourth_coords)
                    if comparison_4 != "No dust cloud" and (comparison_4 in usable_fourth_cloud_tiles):
                        fourth = 1
                        four.append((state_index, fourth_coords))

        for valid_fourth in four:
            fourth_frame = valid_fourth[0]
            if state_index < fourth_frame + 75 and state_index > fourth_frame + 45 and ((state_index - fourth_frame) % 2 == 1):
                for fifth_coords in usable_fifth_skip_tiles:
                    comparison_5 = chargestone_clouds(states[1], fifth_coords)
                    if comparison_5 != "No dust cloud" and (comparison_5 in usable_fifth_cloud_tiles):
                        fifth = 1 
                        five.append((state_index, fifth_coords))



    comparison = [first, second, third, fourth, fifth]
    skips = [initial_frame, set(one), set(two), set(three), set(four), set(five)]


    # print(comparison)
    if comparison == [1,1,1,1,1]:
        #print("this seed fucking works")
            print(skips)
            return True

    

times = []
for i in range(0,23):
    for j in range(0,60):
           for k in range(5,7):
                  time1 = (i, j, k)
                  times.append(time1)




def wholeskip():
    seeds_searched = 0
    seeds_found = 0
    for time in times:

        for presses in keypresses:
            sha1.set_button(presses[0])
            sha1.set_time(*time)
            seed = sha1.hash_seed(precompute)
            seeds_searched = seeds_searched + 1
            ret = multi_cloud(seed)
            cloud_states = ret[5]
            init = initial_frame_bw(seed)
            if skip_checker(cloud_states, init):
                seeds_found = seeds_found + 1
                print(time, hex(seed), presses[1])

    print(f"Found {seeds_found} seeds out of {seeds_searched}")

# wholeskip()

# t = input("Press enter to quit: ")
# t

def main():
    global sha1, precompute
    user_year= int(input("Enter Year: "))
    user_month= int(input("Enter Month: "))
    user_day= int(input("Enter Day: "))
    user_dow = int(input("Enter day of week (Monday = 1, Tuesday = 2, etc): "))
    user_mac = int(input("Enter MAC Address in decimal (convert from hex to decimal)"), 16)


    sha1 = SHA1(version = Game.WHITE, language = Language.ENGLISH, ds_type=DSType.DS, mac = user_mac, soft_reset=False, v_frame= 8, gx_state=6)
    timer0 = 0xc80
    sha1.set_timer0(timer0, 0x60)
    date = (user_year, user_month, user_day, user_dow)
    sha1.set_date(*date)
    precompute = sha1.precompute()
    print("Start!")
    wholeskip()

def test():
    seed = 0x6fef814e65d4da49 
    ret = multi_cloud(seed)
    cloud_states = ret[5]
    init = initial_frame_bw(seed)
    print("Initial frame:", init)
    if skip_checker(cloud_states, init):
        print(hex(seed))

if __name__ == '__main__':
    main()