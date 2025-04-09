#!/usr/bin/python3

import numpy as np
# import matplotlib.pyplot as plt
from numba_pokemon_prngs.lcrng import BWRNG
import itertools
from numba_pokemon_prngs.sha1 import SHA1
from numba_pokemon_prngs.enums import Language, Game, DSType
if __name__ == '__main__':
    from keypresses import *
    from sharedfuncs import *
else:
    from trainer_skips.keypresses import *
    from trainer_skips.sharedfuncs import * 

# from trainer_skips import Parameters

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

debug = False

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

ptable = [[50,100,100,100,100],[50,50,100,100,100],[30,50,100,100,100],[25,30,50,100,100],[20,25,33,50,100],[100,100,100,100,100]]

def getInitialFrame(seed):
    fc = 0
    for x in range (0,5):
        for y in range(0,6):
            for z in range (0,5):
                if ptable[y][z] == 100:
                    break
                fc+=1
                seed=rngAdvance(seed)
                rng = seed>>32
                rng = rng*101
                rng = rng>>32
                if rng <= ptable[y][z]:
                    break
        if x == 0:
            adv = 3
            for j in range (0,adv):
                fc+=1
                seed = rngAdvance(seed)
    fc = extra(seed,fc)
    return fc

def extra(seed,fc):
    loop = True
    limit = 0
    while loop and limit<100:
        loop = False
        tmp = [0,0,0]
        fc+=3
        for x in range (0,3):
            seed = rngAdvance(seed)
            rng = seed>>32
            rng = rng*15
            rng = rng>>32
            tmp[x] = rng
        for i in range (0,3):
            for j in range (0,3):
                if i==j:
                    continue
                if tmp[i] == tmp[j]:
                    loop = True
        limit+=1
    return fc

# below are fast tiles      #(4,213)
usable_first_skip_tiles = [(6,213)]
usable_second_skip_tiles = [ (4,26), (6,26), (5,27), (6,23), (5,24), (4,23)]


# these are tiles where a cloud should spawn for a valid skip

usable_first_cloud_tiles = [(5,214)]
usable_second_cloud_tiles = [(4,28), (5,28)]
#usable_third_cloud_tiles = [(53, 13), (53, 14)]





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

                # 170
        if state_index < frame + 180 and state_index > (frame + 155): #and ((state_index - frame) % 2 == 0 --remove parity check for now
            for first_coords in usable_first_skip_tiles: # reasonable tiles to step on to spawn cloud
                comparison_1, quadrant = cloud_location_finder(states[1], first_coords, valid_route21_tiles)
                if comparison_1 != "No dust cloud" and (comparison_1 in usable_first_cloud_tiles):
                    # print("Frame ", str(state_index), " has a first skip ", first_coords, comparison_1, quadrant)
                    first = 1
                    pair_one = (state_index, first_coords)
                    one.append(pair_one)
                    continue


        for valid_first in one:
            first_frame = valid_first[0]
                            # Need to make clouds like 120-130 from first cloud-ish
            if state_index < first_frame + 200 and state_index > (first_frame + 130):    #450 - 260
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
        if(len(two) > 1 and len(one) > 1):       # Make sure there's at least 2 phenomenon each
            return True, one, two

    return False, [], []




keypress_fake = [[0xdf290000, "custom"]]

def wholeskip(outfile):
    global sha1

    file = open(outfile, "w")

    for time in times:


        for presses in keypresses:
            if illegal_keypresses(presses[1]):
                continue
            
            
            sha1.set_button(presses[0])
            sha1.set_time(*time)
            seed = sha1.hash_seed(precompute)

            ret = multi_cloud(seed)
            cloud_states = ret[5] #[[frame, rng value of frame], ...]
            init = getInitialFrame(seed)

            valid_skip, first, second = skip_checker(cloud_states, init)

            if valid_skip is True:
                # print(time, hex(seed), init, presses[1], "first ", first, " second ", second)

                output = f"{time[0]}:{time[1]}:{time[2]} {hex(seed)}\n {init} {presses[1]} \n first {len(first)} {first} \n second {len(second)} {second}\n\n"
                file.write(output)

    file.close()

def main(parameters, outfile):
    global sha1, precompute, times

    print("initializing...")
    print("computing times...")

    times = compute_times()

    print("generating RNG...")

    sha1 = SHA1(version = parameters.Version, 
                language = parameters.Language, 
                ds_type = parameters.DSType, 
                mac = parameters.MAC, 
                soft_reset = False, 
                v_frame = 8, 
                gx_state = 6 )
    
    sha1.set_timer0(parameters.Timer0Min, parameters.VCount)
    date = (parameters.Year, parameters.Month, parameters.Day, parameters.DOW)
    sha1.set_date(*date)
    precompute = sha1.precompute()

    print("Searching...")
    wholeskip(outfile)

def test_multicloud():
    clouds = multi_cloud(0x1111111111111111)
    print(clouds)


def test():
    global test
    test = True
    seed =  0x33960b0a8db0e38f
    ret = multi_cloud(seed)
    cloud_states = ret[5]
    init = getInitialFrame(seed)
    print("Initial frame:", init)
    valid_skip, one, two = skip_checker(cloud_states, init)
    print(hex(seed), one, two)


if __name__ == '__main__':
    test()

